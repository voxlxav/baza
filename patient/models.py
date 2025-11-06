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

class TherapyCycle(models.Model):
  patient = models.ForeignKey(
    Patient,
    on_delete=models.CASCADE,
    related_name='therapy_cycles',
    verbose_name='Pacjent'
  )
  start_date = models.DateField(verbose_name='Data rozpoczęcia')
  end_date = models.DateField(verbose_name='Data zakończenia', null=True, blank=True)

  class Therapy(models.TextChoices):
    CHEMO = 'Chemoterapia'
    HORMON = 'Terapia hormonalna'
    IMMUNO = 'Immunoterapia'
    PHOTO = 'Terapia fotodynamiczna'
    TARGET = 'Terapia celowana'

  protocol_name = models.CharField(
    max_length=200,
    choices=Therapy.choices,
    verbose_name='Rodzaj terapii'
  )
  class Status(models.TextChoices):
    ONGOING = 'W trakcie'
    COMPLETED = 'Zakończona'
    PAUSED = 'Wstrzymana'
    PLANNED = 'Zaplanowana'
  
  status = models.CharField(
    max_length=200,
    choices=Status.choices,
    verbose_name='Status terapii'
  )

  def __str__(self):
    return f'{self.patient.first_name} {self.patient.last_name} - {self.protocol_name} - {self.status}'

