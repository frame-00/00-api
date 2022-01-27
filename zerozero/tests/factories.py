import factory
from rest_framework.authtoken.models import Token


class Example(factory.django.DjangoModelFactory):
    char = factory.Sequence(lambda n: "char %03d" % n)

    class Meta:
        model = "test_app.example"


class ExamplesChild(factory.django.DjangoModelFactory):
    parent = factory.SubFactory(Example)

    class Meta:
        model = "test_app.exampleschild"


class User(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"
