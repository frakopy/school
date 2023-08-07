from .base import *

LOGS_DIR = os.environ.get('LOGS_DIR')

REST_FRAMEWORK['DEFAULT_RENDERER_CLASSES'] = (
    'rest_framework.renderers.JSONRenderer',
    'rest_framework.renderers.BrowsableAPIRenderer',
)

LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        # you can add specific formats here
        'default': {
            # you can add specific format for aws here
            'format': u"%(asctime)s [%(levelname)-8s] %(message)s",
            'datefmt': "%Y-%m-%d %H:%M:%S"
        },
    },
    'handlers': {
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'default',
        },
    },
    'loggers': {
        # services logger
        'web': {
            'level': 'INFO',
            'handlers': ['console'],
        },
    },
}