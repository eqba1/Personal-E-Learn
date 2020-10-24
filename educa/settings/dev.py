from ._base import *

CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.memcached.MemcachedCache',
        # install memcached and put ip address and port to here
        'LOCATION': 'cache_server_ip_address:cache_server_port_address', # 127.0.0.1:11211
    }
}

CACHE_MIDDLEWARE_ALIAS = 'default'
CACHE_MIDDLEWARE_SECONDS = 60 * 15 # 15 minutes
CACHE_MIDDLEWARE_KEY_PREFIX = 'educa'