REGISTERED_MODELS = []


def register(model, options=None):
    REGISTERED_MODELS.append({"model": model, "options": options or {}})
