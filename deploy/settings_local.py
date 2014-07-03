DEBUG = False

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': '%(db_name)s',
        'USER': '%(db_user)s',
        'PASSWORD': '%(db_password)s',
        'HOST': '',
        'PORT': ''
    }
}

EMAIL_HOST = 'localhost'
EMAIL_HOST_USER = '%(email_user)s'
EMAIL_HOST_PASSWORD = '%(email_password)s'
DEFAULT_FROM_EMAIL='%(email_from)s'

SECRET_KEY = '%(secret_key)s'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'formatters': {
        'verbose': {
            'format': '%%(levelname)s %%(asctime)s %%(module)s %%(process)d %%(thread)d %%(message)s'
        },
        'simple': {
            'format': '%%(levelname)s %%(message)s'
        },
        },
    'handlers': {
        'file': {
            'level':'DEBUG',
            'class':'logging.handlers.RotatingFileHandler',
            'filename': '%(remote_project_dir)s/logs/project.log',
            'maxBytes': 1024*1024*5, # 5 MB
            'backupCount': 5,
            'formatter': 'verbose'

        },
        'console':{
            'level':'DEBUG',
            'class':'logging.StreamHandler',
            'formatter': 'verbose'
        },
        'mail_admins': {
            'level': 'ERROR',
            'class': 'django.utils.log.AdminEmailHandler'
        }

    },
    'loggers': {
        '': {
            'handlers':['file','console'],
            'propagate': True,
            'level':'DEBUG',
            },

        'django': {
            'handlers':['file','console'],
            'propagate': True,
            'level':'INFO',
            },
        'django.request': {
            'handlers': ['file','console','mail_admins'],
            'level': 'ERROR',
            'propagate': False,
            },
        'django.db.backends': {
            'handlers': ['file','console','mail_admins'],
            'level': 'ERROR',
            'propagate': False,
            },
        'project': {
            'handlers': ['file','console'],
            'level': 'DEBUG',
            },
        }
}

COMPRESS_PRECOMPILERS = (
       ('text/x-sass', '%(remote_project_dir)s/env/bin/pyscss {infile} > {outfile}'),
)

#CACHES = {
#    'default': {
#        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
#        'LOCATION': '127.0.0.1:11211',
#        }
#}
