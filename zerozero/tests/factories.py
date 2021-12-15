import factory


class Example(factory.django.DjangoModelFactory):
    char = factory.Sequence(lambda n: "char %03d" % n)

    class Meta:
        model = "test_app.example"


class User(factory.django.DjangoModelFactory):
    class Meta:
        model = "auth.User"

    first_name = factory.Sequence(lambda n: "Agent %03d" % n)
