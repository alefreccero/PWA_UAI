from django import forms


COMISIONES= [
    ('A', 'A'),
    ('B', 'B'),
        ]


class reporteForm(forms.Form):
    carrera = forms.CharField(label='Nombre de Carrera', max_length=100)
    # nombremat = forms.CharField(label='Nombre de Materia', max_length=100)
    # turno = forms.CharField(label='Turno', max_length=100, widget=forms.Select(choices=TURNOS))
    # dia = forms.CharField(label='Dia', max_length=100, widget=forms.Select(choices=DIAS))
    comision = forms.CharField(label='Comision', max_length=100, widget=forms.Select(choices=COMISIONES))
    # Aula = forms.CharField(label='Aula')
    # piso = forms.IntegerField(label='piso')