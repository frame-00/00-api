from collections import OrderedDict, namedtuple

from django.urls import include, path
from django.urls import NoReverseMatch, re_path

from rest_framework.routers import DefaultRouter, APIRootView
from rest_framework.reverse import reverse
from rest_framework.response import Response

from zerozero.api_views import ZeroZeroViewSet
from zerozero.registry import REGISTERED_MODELS


class ZeroZeroRootView(APIRootView):
    def get(self, request, *args, **kwargs):
        # Return a plain {"name": "hyperlink"} response.
        ret = OrderedDict()
        namespace = request.resolver_match.namespace
        for key, url_name in self.api_root_dict.items():
            if namespace:
                url_name = namespace + ":" + url_name
            try:
                ret[key] = reverse(
                    url_name,
                    args=args,
                    kwargs=kwargs,
                    request=request,
                    format=kwargs.get("format"),
                )
            except NoReverseMatch:
                # Don't bail out if eg. no list routes exist, only detail routes.
                continue

        return Response(ret)


class ZeroZeroRouter(DefaultRouter):
    APIRootView = ZeroZeroRootView


router = ZeroZeroRouter()
for model_path, info in REGISTERED_MODELS.items():
    model = info["model"]
    options = info["options"]
    CurrentViewSet = ZeroZeroViewSet(model=model)
    router.register(
        f"{model._meta.app_label}.{model.__name__}",
        CurrentViewSet,
        basename=f"{model._meta.app_label}.{model.__name__}",
    )

urlpatterns = router.urls
