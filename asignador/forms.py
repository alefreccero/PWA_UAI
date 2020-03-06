from django import forms


class cursadasForm(forms.Form):
    carrera = forms.CharField(label='Nombre de Carrera', max_length=100)
