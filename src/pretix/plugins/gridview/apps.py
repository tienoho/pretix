from django.apps import AppConfig
from django.utils.translation import gettext_lazy as _
from pretix import __version__ as version


class GridViewApp(AppConfig):
    name = 'pretix.plugins.gridview'
    label = 'pretix_gridview'
    verbose_name = _("Grid View")

    class PretixPluginMeta:
        name = _("Grid View for Events")
        author = "TCG Team"
        version = version
        category = 'FEATURE'
        description = _("Display events in a modern grid layout.")
