const modalBtn = Array.from(document.getElementsByClassName('show-modal'))
const modalLabel = document.getElementById('modalProgressLabel')
const progressBtn = document.getElementById('progressBtn')
const modalTbody = document.querySelector('#progressTable > tbody')
const closeBtns = Array.from(document.querySelectorAll('.close-modal'))

// -------------- Retrieving data from the backend ------------------------------

// Setting the URL to be used for get json data from the backend
const urlToGetData = document.getElementById('urlToGetData') 

const current_url = window.location.href
const urlToSet  = current_url.replace('/attendance/', '/attendance/get_json_progress/')
urlToGetData.setAttribute('data-url', urlToSet )


// Function to send Get request to the backend
const getJsonData = async () => {

    //As we can not use template tags inside js we put the url data inside  input with type=hidden
    const url = urlToGetData.dataset.url 
    try{
        const request = await fetch(url)
        const result = await request.json()
        return result
    }catch(error){
        return error
    }
}


// Creating <tr></tr> childs for the Table of modal window
modalBtn.map((element) => { 
    element.addEventListener('click', () => {
        getJsonData().then(result => {
            if(result){
                modalLabel.textContent = `Goal progress for student > ${element.dataset.studentName}`
                const studentId = Number(element.dataset.studentId)
                const progressData = result.json_progress.filter((el) => el.student_id === studentId )
                let goalRow = ''
                for(goal of goals){
                    const goalFiltered = progressData.find((e) => e.goals_id === goal.id)
                    if(progressData.length > 0 && goalFiltered){    
                        goalRow += 
                            `
                            <tr class="row-goal">
                                <td class="goalName">${goalFiltered.goals__name}</td>
                                <td class="progressNum"><input type="number" class="form-control" min="0" max="100" value="${goalFiltered.progress}"></td>
                                <td class="comments"><input type="text" class="form-control" value="${goalFiltered.comments}"></td>
                                <td class="goalId" style="display: none;">${goalFiltered.goals_id}</td>
                                <td class="studentId" style="display: none;">${goalFiltered.student_id}</td>
                            </tr>
                            `
                    }else{
                        goalRow += 
                            `
                            <tr class="row-goal">
                                <td class="goalName">${goal.name}</td>
                                <td class="progressNum"><input type="number" class="form-control" min="0" max="100" value="0"></td>
                                <td class="comments"><input type="text" class="form-control"></td>
                                <td class="goalId" style="display: none;">${goal.id}</td>
                                <td class="studentId" style="display: none;">${studentId}</td>
                            </tr>
                            `
                    }
                }
                modalTbody.innerHTML = goalRow
            }
        })  

    })
})


//------------------- Sending data to the backend ---------------------------------

// Get csrftoken, the code of this function is provided by django documentation
// in the link https://docs.djangoproject.com/en/4.0/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}


// Function to send json list to the backend
const sendData = async (dataToSend) => {
    //Get the CSRF token using the function code provided by django documentation
    const csrftoken = getCookie('csrftoken'); 

    //As we can not use template tags inside js we put the url data inside  input with type=hidden
    const inputUrl = document.getElementById('urlTosendData') 
    const url = inputUrl.dataset.url

    const fetchSettings = {
        method : 'POST',
        credentials: 'same-origin',
        body: JSON.stringify(dataToSend),
        headers: {'X-CSRFToken': csrftoken},
    }

    try{
        const request = await fetch(url, fetchSettings)
        const result = await request.json()
        closeBtns[0].click() //Closingd modal window (DatagoalList is set to empty list after closing modal)
        return result
    }catch(error){
        return error
    }
}


// Adding click event to the Butoom of modal window
let DatagoalList = []
progressBtn.addEventListener('click', () => {
    const rowGoal = Array.from(document.querySelectorAll('.row-goal'))
    for (let row of rowGoal) {
        const inputProgress = row.querySelector('.progressNum > input')
        const inputComments = row.querySelector('.comments > input')
        const tdGoalId = row.querySelector('.goalId')
        const tdstudentId = row.querySelector('.studentId')

        // appending object to the list which will be sent to the backend
        DatagoalList.push(
            {
                'progress': inputProgress.value === "" ? 0 : inputProgress.value, 
                'comments': inputComments.value, 
                'goalId': tdGoalId.textContent, 
                'studentId': tdstudentId.textContent
            }
        )

    }
    
    sendData(DatagoalList).then(result => {
        // If result from the backend is 'ok', execute the code inside
        if(result.result === 'ok'){
            const Toast = Swal.mixin({
                    toast: true,
                    position: 'top-end',
                    showConfirmButton: false,
                    timer: 3000,
                    timerProgressBar: true,
                    didOpen: (toast) => {
                        toast.addEventListener('mouseenter', Swal.stopTimer)
                        toast.addEventListener('mouseleave', Swal.resumeTimer)
                    }
                })
                
            Toast.fire({
                icon: 'success',
                title: 'Goal progress successfully saved'
            })
        }
    })  
})

// Adding click event to close buttoms of modal window in order to 
// clear json array ---> DatagoalList after closing modal window
closeBtns.forEach((element) => { 
    element.addEventListener('click', () => { 
        DatagoalList = []    
    })
})
