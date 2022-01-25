from rest_framework.permissions import BasePermission

ACTION_TO_PERMISSION = {
    "create": "add",
    "retrieve": "view",
    "list": "view",
    "update": "change",
    "partial_update": "change",
    "destroy": "delete",
    "metadata": "view",
}


class APIDefaultPermission(BasePermission):
    def __init__(self, *args, **kwargs):
        self.action = kwargs.pop("action")
        self.permission = ACTION_TO_PERMISSION.get(self.action)
        super().__init__(*args, **kwargs)

    def has_permission(self, request, view):
        app_label = view.app_label
        model_name = view.model_name
        permission_name = f"{self.permission}_{model_name}"
        perm_str = "{}.{}".format(app_label, permission_name)
        return request.user.has_perm(perm_str)
