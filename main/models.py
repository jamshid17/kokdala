from tabnanny import verbose
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField


class Sector(models.Model):
    name = models.CharField(max_length=200)
    number = models.IntegerField()

    class Meta:
        verbose_name = "Sektor"
        verbose_name_plural = "Sektorlar"

    def __str__(self):
        return f"{self.name} (number: {self.number})"


class Mahalla(models.Model):
    name = models.CharField(max_length=1000)
    households_count = models.IntegerField()
    population = models.IntegerField()
    sector = models.ForeignKey(Sector, related_name="mahalla", on_delete=models.CASCADE)

    class Meta:
        verbose_name = "Mahalla"
        verbose_name_plural = "Mahallalar"
    
    def __str__(self):
        return f"Mahalla {self.pk}: {self.name}"


class Xonadon(models.Model):
    mahalla = models.ForeignKey(Mahalla, related_name='xonadon', on_delete=models.CASCADE)
    address = models.TextField()

    class Meta:
        verbose_name = "Xonadon"
        verbose_name_plural = "Xonadonlar"
    
    def __str__(self):
        return f"Xonadon: {self.address}"


class Person(models.Model):
    class GenderChoices(models.TextChoices):
        MALE = 'male', 'male'
        FEMALE = 'female', 'female'
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    birth_date = models.DateField()
    gender = models.CharField(choices=GenderChoices.choices, default=GenderChoices.MALE, max_length=200)
    phone_number = PhoneNumberField(region='UZ')
    household = models.ForeignKey(Xonadon, on_delete=models.CASCADE, related_name='person')
    is_egasi = models.BooleanField(default=False)

    class Meta:
        verbose_name = "Aholi"
        verbose_name_plural = "Aholilar"
     
    def __str__(self):
        return f"Aholi {self.pk}: {self.first_name} {self.last_name}"


class Rais(models.Model):
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200)
    phone_number = PhoneNumberField(region="UZ")
    email = models.EmailField()
    mahalla = models.OneToOneField(Mahalla, related_name='rais', on_delete=models.CASCADE)
    image = models.ImageField(upload_to='rais_images/')

    class Meta:
        verbose_name = "Rais"
        verbose_name_plural = "Raislar"
     
    def __str__(self):
        return f"Rais {self.pk}: {self.first_name} {self.last_name}"


class Problem(models.Model):
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.text


class SubProblem(models.Model):
    problem = models.ForeignKey(Problem, on_delete=models.CASCADE, related_name="subproblem")
    text = models.CharField(max_length=1000)
    
    def __str__(self):
        return self.text


class SubSubProblem(models.Model):
    subproblem = models.ForeignKey(SubProblem, on_delete=models.CASCADE, related_name="subsubproblem")
    text = models.CharField(max_length=1000)

    def __str__(self):
        return self.text

