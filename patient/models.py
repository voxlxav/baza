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


class Response(models.Model):
  class RECIST_criteria(models.TextChoices):
    CR = "CR", "CR - complete response"
    PR = "PR", "PR - partial response"
    SD = "SD", "SD - stable disease"
    PD = "PD", "PD - progressive disease"

  response_cycle_id = models.ForeignKey(
    TherapyCycle,
    on_delete=models.CASCADE,
    null=True,
    related_name='response_ci',
    verbose_name="Terapia"
  )
  assessment_date = models.DateField(verbose_name='Data oceny reakcji')

  recist_result = models.CharField(
    choices=RECIST_criteria.choices,
    default=RECIST_criteria.SD,
    verbose_name='Kryterium RECIST'
  )

  notes = models.TextField(
    max_length=1000,
    null=True,
    blank=True,
    verbose_name='Notatki'
  )

  def __str__(self):
    return f'{self.cycle_id} - {self.assessment_date}'

class AdverseEvent(models.Model):
  class severity_grades(models.TextChoices):
    g1 = "Grade 1"
    g2 = "Grade 2"
    g3 = "Grade 3"
    g4 = "Grade 4"
    g5 = "Grade 5"

  adverse_event_cycle_id = models.ForeignKey(
    TherapyCycle,
    on_delete=models.CASCADE,
    related_name='adverse_event_response',
    null=True,
    verbose_name="Terapia"
  )

  event_date = models.DateField(verbose_name='Data zdarzenia')
  description = models.TextField(
    max_length=1500,
    verbose_name= "Opis zdarzenia"
  )

  severity = models.CharField(
    choices=severity_grades.choices,
    default=severity_grades.g1,
    verbose_name= "Severity"
  )

  action_taken = models.TextField(
    max_length=1500,
    verbose_name= "Podjęte działanie"
  )
  def __str__(self):
    return f'{self.cycle_id} - {self.event_date}'