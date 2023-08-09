// Getting the button that will send data to the backend
const btnSend = document.getElementById("btn-send");

// Getting the student id and courses availables
const studentId = json_data.student_id;
const courses = json_data.courses;
const json_list = json_data.json_list;

// Getting schedule day list
const mondayList = json_data.schedules.filter((obj) => obj.day === "Lunes");
const tuesdayList = json_data.schedules.filter((obj) => obj.day === "Martes");
const wednesdayList = json_data.schedules.filter((obj) => obj.day === "Miércoles");
const thursdayList = json_data.schedules.filter((obj) => obj.day === "Jueves");
const fridayList = json_data.schedules.filter((obj) => obj.day === "Viernes");

//Define array to be sent by Post method to the backend
let arrayObjcts = [];

const addSchedules = (dayList, idDay) => {
    const divDayContainer = document.getElementById(idDay);
    let blockHour;
    let divBlockHour;
    for (let i = 0; i < dayList.length; i++) {
        hour = dayList[i].hour;
        blockHour = dayList[i].hour_block;
        divBlockHour = divDayContainer.querySelector(
        `[data-blocknum="${blockHour}"]`
        );
        divBlockHour.innerHTML = divBlockHour.innerHTML + "&nbsp;" + hour;
        divBlockHour.classList.add("enabled");
        divBlockHour.setAttribute("data-day", idDay);
        divBlockHour.setAttribute("data-hour", dayList[i].hour);
        divBlockHour.setAttribute("data-classroom", dayList[i].classroom_id);
    }
};

// Populating div childs inside days container
addSchedules(mondayList, "Lunes");
addSchedules(tuesdayList, "Martes");
addSchedules(wednesdayList, "Miércoles");
addSchedules(thursdayList, "Jueves");
addSchedules(fridayList, "Viernes");

//Displaying schedules for next week
const showScheduled = (jsonList) => { 
    for (let json of jsonList) {
        const dayContainer = document.getElementById(json.day);
        const hourContainer = dayContainer.querySelector(
            `[data-blocknum="${json.hour_block}"]`
        );
        hourContainer.innerHTML =
            `${json.hour_block}-` +
            "&nbsp;" +
            `${json.hour}`+
            "&nbsp;" +
            json.course +
            "&nbsp;" +
            `<i class="delete-db bi bi-trash" style=font-size:1.3em; data-record-id=${json.record_id}></i>`;
        hourContainer.classList.remove("enabled");
        hourContainer.classList.add("selected");
    }
} 

showScheduled(json_list)

// Creating objects courses for use it in sweetAlert popup
let options = {};
for (let i = 0; i < courses.length; i++) {
    const course_name = courses[i].name
    const course_availability = courses[i].availability
    options[course_name] = course_availability > 0 ? `${course_name} (${course_availability} space available)`: `${course_name} (0 space available, can not be selected)`;
}


// Setting the json array to sent to the backend
const setObject = (e) => {
  // Those variables will be used only if the studen confirm our popup
    const day = e.target.getAttribute("data-day");
    const hour = e.target.getAttribute("data-hour");
    const classroom_id = e.target.getAttribute("data-classroom");
    const objId = e.target.getAttribute("id");

    Swal.fire({
        title: "Select a course",
        input: "select",
        allowOutsideClick: false,
        inputOptions: options,
        inputPlaceholder: "Select an option",
        showCancelButton: true,
        confirmButtonText: "Confirm",
        confirmButtonColor: "#2C74B3",
        cancelButtonText: "Cancel",
        didOpen: () => {
            const selectInput = Swal.getInput();
            const selectOptions = selectInput.getElementsByTagName("option");
            for (let i = 0; i < selectOptions.length; i++) {
                const option = selectOptions[i];
                const courseObj = courses.find((obj) =>  obj.name === option.value )
                if (courseObj) {
                    if (courseObj.availability <= 0) option.disabled = true;
                }
            }
        },
    }).then((result) => {
        if (result.value) {
        const course = result.value;
        const scheduleObject = {
            studentId: studentId,
            day: day,
            hour: hour,
            course: course,
            classroom_id: classroom_id,
            objId: objId,
        };

        //Add object to our list objects to be send to the backend
        arrayObjcts.push(scheduleObject);
        e.target.classList.remove("enabled");
        e.target.classList.add("selected");
        e.target.innerHTML =
            e.target.innerHTML +
            "&nbsp;" +
            `${course}` +
            "&nbsp;" +
            '<i class="delete bi bi-trash" style=font-size:1.3em;></i>';
        }
    });
};


// Remove selection from the front end
const removeObject = (e) => {
    const parentIcon = e.target.parentNode;
    const objId = parentIcon.getAttribute("id");
    let index = arrayObjcts.findIndex((obj) => {
        return obj.objId === objId;
    });
    arrayObjcts.splice(index, 1);
    parentIcon.classList.remove("selected");
    parentIcon.classList.add("enabled");
    const blockNum = parentIcon.dataset.blocknum;
    const hour = parentIcon.dataset.hour;
    parentIcon.innerHTML = `${blockNum}-&nbsp;(${hour})`;
};


// Delete record from DB

// Get csrftoken, the code of this function is provided by django documentation
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

const deleteFromDb = (e) => { 
    removeObject(e)
    const recordId = e.target.dataset.recordId
    const inpuUrl = document.getElementById('urlDelete')
    const urlSplited = inpuUrl.dataset.url.split('/')
    urlSplited.splice(-1, 1)
    const urlDelete = urlSplited.join('/') + "/" + `${recordId}`

    // Function to send Get request to the backend
    const deleteRecord = async () => {
        //Getting the url to be sent to the backend
        try{
            const csrftoken = getCookie('csrftoken');
            const response = await fetch(urlDelete, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': csrftoken
                }
            });
            const result = await response.json()
            return result
        }catch(error){
            return error
        }
    }
    
    deleteRecord().then(result => {
            // If result from the backend is 'ok', execute the code inside
            if(result.result === 'record_deleted'){
                Swal.fire({
                    position: 'top-end',
                    icon: 'success',
                    title: 'Record successfully deleted from DB!',
                    showConfirmButton: false,
                    background: "#383838",
                    color: "white",
                    timer: 1500,
                })
            }
        })
}

// Add event to the parent container for days
const dayParentCont = document.getElementById("DayparentContainer");

dayParentCont.addEventListener("click", (e) => {
    if (e.target.classList.contains("enabled")) {
        setObject(e);
    } else if (e.target.classList.contains("delete")) {
        removeObject(e);
    }else if(e.target.classList.contains("delete-db")){
        deleteFromDb(e)
    }
});

// Send data to the backend in order to create new records in DB

// Get csrftoken, the code of this function is provided by django documentation
// in the link https://docs.djangoproject.com/en/4.0/ref/csrf/
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
        const cookie = cookies[i].trim();
        // Does this cookie string begin with the name we want?
        if (cookie.substring(0, name.length + 1) === name + "=") {
            cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
            break;
        }
        }
    }
    return cookieValue;
}

// Function to send the form to the backend
const sendData = async (jsonData) => {
    //Get the CSRF token using the function code provided by django documentation
    const csrftoken = getCookie("csrftoken");

    //As we can not use template tags inside js we put the url data inside  input with type=hidden
    const inputUrl = document.getElementById("urlToSendForm");
    const url = inputUrl.dataset.url;

    const fetchSettings = {
        method: "POST",
        credentials: "same-origin",
        body: JSON.stringify({ jsonData: arrayObjcts }),
        headers: { "Content-Type": "application/json", "X-CSRFToken": csrftoken },
    };
    try {
        const request = await fetch(url, fetchSettings);
        const result = await request.json();
        return result;
    } catch (error) {
        return error;
    }
};

// Getting our loading spinner (using bootstrap)
const spinner = document.getElementById("spinner");

btnSend.addEventListener("click", () => {
  // Remove 'hide' class for show spinner
    spinner.classList.remove("hide");

    sendData(arrayObjcts).then((result) => {
        // If result from the backend is 'ok', execute the code inside
        if (result.result === "ok") {
            // Add 'hide' class for hide again spinner
            spinner.classList.add("hide");
            const jsonList = JSON.parse(result.records_created)
            showScheduled(jsonList)

            // Using sweetalert js library (through CDN)
            Swal.fire({
                title: "Schedule successfully saved",
                color: "white",
                icon: "success",
                allowOutsideClick: false,
                confirmButtonColor: "#03C988",
                background: "#383838",
                confirmButtonText: "OK",
            }).then((result) => {
                // Resete value of arrayObjcts to empty list
                if (result.isConfirmed) {
                    arrayObjcts = []
                }
            });
        } else if (result.result === "empty_list") {
            // Add 'hide' class for hide again spinner
            spinner.classList.add("hide");
            Swal.fire({
                title: "Should do at least one schedule",
                color: "white",
                icon: "warning",
                allowOutsideClick: false,
                confirmButtonColor: "#DC0000",
                background: "#383838",
                confirmButtonText: "OK",
            });
        }  else if (result.result === "no_availability") {
            // Add 'hide' class for hide again spinner
            spinner.classList.add("hide");
            Swal.fire({
                title: `No space available`,
                text: `
                there is ${result.num_available} space available for the course "${result.course_name}"
                but you sent ${result.num_records_sent}
                `,
                color: "white",
                icon: "warning",
                allowOutsideClick: false,
                confirmButtonColor: "#DC0000",
                background: "#383838",
                confirmButtonText: "OK",
            });
        } else {
            // Add 'hide' class for hide again spinner
            spinner.classList.add("hide");
            Swal.fire({
                icon: "error",
                title: "Oops...",
                color: "white",
                text: result.result,
                allowOutsideClick: false,
                confirmButtonColor: "#DC0000",
                background: "#383838",
            });
        }
    });
});
