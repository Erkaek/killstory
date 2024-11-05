from django.utils.translation import gettext_lazy as _

from allianceauth import hooks
from allianceauth.services.hooks import MenuItemHook, UrlHook

from . import urls


class KillstoryMenuItem(MenuItemHook):
    """This class ensures only authorized users will see the menu entry"""

    def __init__(self):
        # setup menu entry for sidebar with an updated icon
        MenuItemHook.__init__(
            self,
            _("killstory"),
            "fas fa-skull-crossbones fa-fw",  # Updated to a skull icon for a kill-related theme
            "killstory:index",
            navactive=["killstory:"],
        )

    def render(self, request):
        if request.user.has_perm("killstory.basic_access"):
            return MenuItemHook.render(self, request)
        return ""


@hooks.register("menu_item_hook")
def register_menu():
    return KillstoryMenuItem()


@hooks.register("url_hook")
def register_urls():
    return UrlHook(urls, "killstory", r"^killstory/")
