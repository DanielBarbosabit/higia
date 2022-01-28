from django.db import models
from django import forms
from django.forms import ModelForm
from web.models import Ident_dispenser
from django.contrib.auth.models import User

# class Cadastro_dispenser(ModelForm):
#     class Meta:
#         model = Ident_dispenser
#         fields = '__all__'
#     choices_dispenser = list(Ident_dispenser.objects.all().values_list())
#     choices_user = list(User.objects.all().values_list())
#
#     topico_dispenser = forms.ChoiceField(choices=choices_dispenser, required=True)
#     localizacao = forms.CharField(max_length=200, required=True)
#     usuario = forms.ChoiceField(choices=choices_user, required=True)



