from django.db.models import fields
from django.http import response
from django.test import TestCase
from sso import models
from django.utils import timezone
from django.urls import reverse
from sso.forms import UpdateRolSistemaForm,UserAssignRolForm
from django.contrib.auth.models import Group,Permission, User
from django.test.client import Client, RequestFactory
from allauth.utils import get_user_model
import pytest
from pytest_django.asserts import assertTemplateUsed

class AdministrationFormTest(TestCase):

    def create_rol(self, name="Scrum Master"):
        return Group.objects.create(name=name)

    def create_user(self, username="wolfgang", first_name="Wolfgang", last_name="Wiens Wohlgemuth",email="wwwolfgang469@gmail.com"):
        return models.User.objects.create(username=username, first_name=first_name,last_name=last_name,email=email)

    def test_user_has_permission_after_group_asign(self):
        user = self.create_user()
        rol = self.create_rol()
        nombre = rol.name
        permisos = Permission.objects.filter(codename__startswith='pg_')
        for permiso in permisos:
            rol.permissions.add(permiso.pk)
        rol.save()
        print(rol.name)
        form_data = {
            "groups": [rol.pk]
        }
        asign_rol_form = UserAssignRolForm(data=form_data, instance=user)
        asign_rol_form.save()
        user.refresh_from_db()
        assert user.groups.filter(name=nombre)
        assert user.has_perm('sso.pg_is_user')