from tabnanny import verbose
from django.db import models
from main.models import Mahalla, Xonadon, Person, Problem, SubProblem, SubSubProblem
from django.contrib.auth import get_user_model

User = get_user_model()
# Create your models here.

class Organish(models.Model):
    class HalQilishHolati(models.TextChoices):
        IN_PROCESS = 'Davom etayapti', 'Davom etayapti'
        FINISHED = 'Yakunlangan', 'Yakunlangan'


    xonadon = models.ForeignKey(Xonadon, on_delete=models.CASCADE, related_name='organish')
    azosi = models.ForeignKey(Person, on_delete=models.SET_NULL, related_name='organish', null=True, blank=True)
    problem_context = models.CharField(max_length=100)
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name='organish')
    subproblem = models.ForeignKey(SubProblem, on_delete=models.CASCADE, related_name='organish')
    subsubproblem = models.ForeignKey(
        SubSubProblem, on_delete=models.CASCADE, related_name='organish', null=True, blank=True
    )
    organildi = models.BooleanField(default=False)
    hal_qilish_holati = models.CharField(choices=HalQilishHolati.choices, max_length=100)
    suhbat_date = models.DateField(auto_now_add=True)
    finish_date = models.DateField(verbose_name='Hal qilish vaqti')
    ishchi = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organish')
    masul_tashkilot = models.ForeignKey("Tashkilot", on_delete=models.CASCADE, related_name='organish', null=True, blank=True)
    qiymat = models.CharField(max_length=100, null=True, blank=True) 

    class Meta:
        verbose_name = "Organish"
        verbose_name_plural = "Organishlar"

    def __str__(self):
        return f"Organish: {self.pk}"

class OrganishGuruh(models.Model):
    name = models.CharField(max_length=1000)

    class Meta:
        verbose_name = "Organish guruh"
        verbose_name_plural = "Organish guruhlar" 

    def __str__(self):
        return f"Guruh: {self.name}"

class Tashkilot(models.Model):
    name = models.CharField(max_length=1000)

    def __str__(self):
        return f"Tashkilot: {self.name}"