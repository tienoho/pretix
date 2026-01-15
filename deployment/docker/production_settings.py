from pretix.settings import *

LOGGING['handlers']['mail_admins']['include_html'] = True
STORAGES["staticfiles"]["BACKEND"] = 'django.core.files.storage.FileSystemStorage'

COMPRESS_ENABLED = True
COMPRESS_OFFLINE = False

ALLOWED_HOSTS = ['*']

# Allow any host to be treated as a system domain (bypassing checking against SITE_URL)
class AllHosts:
    def __contains__(self, item):
        return True

getLocalHostNames = AllHosts()
# We can't easily override the imported constant LOCAL_HOST_NAMES from settings directly if it's not re-read.
# Wait, middlewares import 'from django.conf import settings'. 
# settings object values come from this file.
LOCAL_HOST_NAMES = AllHosts()
