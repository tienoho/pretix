from pretix.settings import *

LOGGING['handlers']['mail_admins']['include_html'] = True
# Disabled: manifest file not available when code is mounted from host
# STORAGES["staticfiles"]["BACKEND"] = 'django.contrib.staticfiles.storage.ManifestStaticFilesStorage'
