REGISTERED_MODELS = {}


def get_model_path(model):
    model_path = "%s.%s" % (
        model._meta.app_label,
        model._meta.model_name.lower(),
    )
    return model_path


def register(model, options=None):
    model_path = get_model_path(model)
    REGISTERED_MODELS[model_path] = {"model": model, "options": options or {}}
