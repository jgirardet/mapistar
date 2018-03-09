# Third Party Libraries
import factory

fk = factory.Faker


class FacUser(factory.django.DjangoModelFactory):
    class Meta:
        model = "users.User"

    username = fk('user_name')
    email = fk('email')
