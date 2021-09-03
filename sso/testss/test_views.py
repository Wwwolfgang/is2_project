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

class AdministrationViewTest(TestCase):

    def create_rol(self, name="Scrum Master"):
        return Group.objects.create(name=name)

    def create_user(self, username="wolfgang", first_name="Wolfgang", last_name="Wiens Wohlgemuth",email="wwwolfgang469@gmail.com"):
        return models.User.objects.create(username=username, first_name=first_name,last_name=last_name,email=email)

    def test_view_administration_url_existe_en_la_ubicacion_deseada(self):
        response = self.client.get('/administration/', follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_administration_url_es_accesible_por_nombre(self):
        response = self.client.get(reverse('sso:roles-sistema-listado'), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_update_rol_sistema_url_es_accesible_por_nombre(self):
        rol = self.create_rol()
        response = self.client.get(reverse('sso:rol-sistema-update',kwargs={'pk':rol.pk}), follow=True)
        self.assertEqual(response.status_code, 200)
    
    def test_view_asignar_rol_sistema_url_es_accesible_por_nombre(self):
        rol = self.create_rol()
        response = self.client.get(reverse('sso:rol-sistema-asignar',kwargs={'pk':rol.pk}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_update_user_url_es_accesible_por_nombre(self):
        user = self.create_user()
        response = self.client.get(reverse('sso:user-update',kwargs={'pk':user.pk}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_view_delete_user_url_es_accesible_por_nombre(self):
        user = self.create_user()
        response = self.client.get(reverse('sso:user-delete',kwargs={'pk':user.pk}), follow=True)
        self.assertEqual(response.status_code, 200)

    def test_user_delete_view(self):
        user = self.create_user()
        user_pk = user.pk
        resp = self.client.delete(reverse('sso:user-delete',kwargs={'pk': user.pk}), follow=True)
        user.refresh_from_db()
        print(resp.status_code,user)
        print(models.User.objects.all())
        self.assertFalse(models.User.objects.filter(pk=user_pk).exists())