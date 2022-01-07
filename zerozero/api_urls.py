from django.urls import include, path
from rest_framework.routers import DefaultRouter

from zerozero.api_views import ZeroZeroViewSet

from zerozero.registry import REGISTERED_MODELS

router = DefaultRouter()
for model_path, info in REGISTERED_MODELS.items():
    model = info["model"]
    options = info["options"]
    CurrentViewSet = ZeroZeroViewSet(model=model)
    router.register(
        f"{model._meta.app_label}/{model._meta.model_name}",
        CurrentViewSet,
        basename=f"{model._meta.app_label}_{model._meta.model_name}",
    )

urlpatterns = router.urls
