from ._base import *


CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        # install memcached and put ip address and port to here
        #'LOCATION': 'cache_server_ip_address:cache_server_port_address', # 127.0.0.1:11211
        'LOCATION': '192.168.1.124:11211'
    }
}

REST_FRAMEWORK = { 
    'Default_PERMISSION_CLASSES': [
        'rest_framework.permissions.jangoModelPermissionsOrAnonReadOnly'
    ]
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60 * 15 # 15 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'educa'
ASGI_APPLICATION = 'educa.settings.routing.application'