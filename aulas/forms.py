from django import forms

class AulasForm(forms.Form):
    aula = forms.CharField(label='Nombre de Aula', max_length=100)
    piso = forms.IntegerField(label='Piso')
    capacidad = forms.IntegerField(label='Capacidad de Aula')

