from django import forms

class AulasForm(forms.Form):
    aula = forms.CharField(label='Nombre de Aula', max_length=100)
    capacidad = forms.IntegerField(label='Capacidad de Aula');


# class materiasForm(forms.Form):
    
#      nombremat = forms.CharField(label='Nombre de Materia', max_length=100)
# 	 carrera = forms.CharField(label='Nombre de Carrera', max_length=100)
# 	 turno = forms.CharField(label='Turno', max_length=100)
# 	 horario = forms.CharField(label='Horario', max_length=100)
# 	 comision = forms.CharField(label='Comision', max_length=100)
# 	 CantAlumnos = forms.IntegerField(label='Cantidad de Aulmnos')