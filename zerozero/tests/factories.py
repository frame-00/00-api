import factory


class Example(factory.django.DjangoModelFactory):
    class Meta:
        model = (
            "test_app.example"  # Equivalent to ``model = myapp.models.User``
        )
