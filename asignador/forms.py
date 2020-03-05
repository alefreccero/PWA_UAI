from django import forms

TURNOS= [
    ('manana', 'Manana'),
    ('tarde', 'Tarde'),
    ('noche', 'Noche'),
    ]

COMISIONES= [
    ('a', 'A'),
    ('b', 'B'),
    ('c', 'C'),
        ]

class cursadasForm(forms.Form):
    carrera = forms.CharField(label='Nombre de Carrera', max_length=100)
    # nombremat = forms.CharField(label='Nombre de Materia', max_length=100)
    # turno = forms.CharField(label='Turno', max_length=100, widget=forms.Select(choices=TURNOS))
    # horario = forms.CharField(label='Horario', max_length=100)
    # comision = forms.CharField(label='Comision', max_length=100, widget=forms.Select(choices=COMISIONES))
    # CantAlumnos = forms.IntegerField(label='Cantidad de Aulmnos')