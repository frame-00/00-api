import factory


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


class QueryReport(factory.django.DjangoModelFactory):
    name = factory.Sequence(lambda n: "test %03d" % n)
    slug = name
    model = "test_app.example"
    where = "{'char': 'a'}"
    fields = "char,excluded_field"
    order = "-char"
    interval = 60

    class Meta:
        model = "zerozero.queryreport"
