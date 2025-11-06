from django.db import models

# Create your models here.
class Patient(models.Model):
  class Gender(models.TextChoices):
    MALE = 'Mężczyzna'
    FEMALE = 'Kobieta'
    OTHER = 'Inna'

  first_name = models.CharField(max_length=100, verbose_name='Imię')
  last_name = models.CharField(max_length=100,verbose_name='Nazwisko')
  date_of_birth = models.DateField(verbose_name='Data urodzenia')
  gender= models.CharField(
    max_length=9,
    choices=Gender.choices,
    default=Gender.MALE,
    verbose_name="Płeć"
  )
  initial_diagnosis= models.CharField(max_length=250,verbose_name='Wstępna diagnoza')
  diagnosis_date = models.DateField(verbose_name='Data diagnozy')

  def add_patient(self):
    self.save()

  def __str__(self):
    return self.first_name + ' ' + self.last_name