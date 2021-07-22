from webusers.models import User

user = User.objects.get(pk=1)
user.set_password("1afiado2")
user.save()
