from django.contrib import admin
from .models import (
    Sector,
    Mahalla,
    Xonadon, 
    Person, 
    Rais, 
    Problem, 
    SubProblem, 
    SubSubProblem)
# Register your models here.

admin.site.register(Sector)
admin.site.register(Mahalla)
admin.site.register(Xonadon)
admin.site.register(Person)
admin.site.register(Rais)
admin.site.register(Problem)
admin.site.register(SubProblem)
admin.site.register(SubSubProblem)



