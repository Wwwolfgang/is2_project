from django.db.models import fields
from django.test import TestCase
from sso import models
from django.utils import timezone
from django.urls import reverse
from sso.forms import UpdateRolSistemaForm,UserAssignRolForm
from django.contrib.auth.models import Group,Permission

class User(TestCase):

    def create_user(self, username="wolfgang", first_name="Wolfgang", last_name="Wiens Wohlgemuth",email="wwwolfgang469@gmail.com"):
        return models.User.objects.create(username=username, first_name=first_name,last_name=last_name,email=email)

    def test_user_creation(self):
        user = self.create_user()
        self.assertTrue(isinstance(user, models.User))
        self.assertEqual(user.__str__(), user.username)

    def test_user_edit(self):
        user = self.create_user()
        form_data = {
            "is_administrator": False,
            "first_name": "Test",
            "last_name": "Usuario"
        }
        edit_user_form = UpdateRolSistemaForm(data = form_data, instance = user)
        self.assertTrue(edit_user_form.is_valid())
        edit_user_form.save()
        user.refresh_from_db()
        self.assertEqual(user.first_name, "Test")

class RolSistema(TestCase):

    def create_rol(self, name="Scrum Master"):
        return Group.objects.create(name=name)

    def test_rol_creation(self):
        group = self.create_rol()
        self.assertTrue(isinstance(group, Group))
        self.assertEqual(group.__str__(), group.name)

    def test_rol_edit_through_form(self):
        rol = self.create_rol()
        permisos = Permission.objects.filter(codename__startswith='pg_')

        print('Antes de actualizar el groupo:',rol.permissions.all())
        form_data = {
            "permissions": [permisos.first().pk]
        }
        add_rol_form = UpdateRolSistemaForm(data = form_data, instance = rol)
        add_rol_form.save()
        rol.refresh_from_db()
        print('Después de usar el form tiene el permiso:',rol.permissions.all())
        self.assertTrue(not rol.permissions.all())