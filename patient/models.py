from django.db import models
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator

def validate_pesel(value):
  if len(value) != 11:
    raise ValidationError('PESEL musi mieć 11 znaków.')
  if not value.isdigit():
    raise ValidationError('PESEL musi składać się wyłącznie z cyfr.')

  wages = [1, 3, 7, 9, 1, 3, 7, 9, 1, 3]
  control_sum = sum(int(value[i]) * wages[i] for i in range(10))
  control_value = (10 - (control_sum % 10)) % 10
  if int(value[-1]) != control_value:
    raise ValidationError('Nieprawidłowa suma kontrolna numeru PESEL.')

class Doctor(models.Model):
  class Specialization(models.TextChoices):
    ONCOLOGIST = 'ONKOLOG','Onkolog kliniczny'
    ONKOGENETICIST = 'ONKOGENETYK', 'Onkogenetyk'
    RADIOLOGIST = 'RADIOLOG', 'Radiolog'
    PATHOMORPHOLOGIST = 'PATOMORFOLOG', 'Patomorfolog'
    SURGEON = 'CHIRURG', 'Chirurg onkologiczny'
    OTHER = 'INNY', 'Inna specjalizacja'

  first_name = models.CharField(max_length=100,verbose_name='Imię')
  last_name = models.CharField(max_length=100,verbose_name='Nazwisko')
  pwz_number = models.CharField(
    max_length = 7,
    unique = True,
    verbose_name = 'Numer PWZ',
    help_text = '7-cyfrowy numepr prawa wykonywania zawodu'
  )
  specialization = models.CharField(
    max_length = 50,
    choices = Specialization.choices,
    default = Specialization.ONCOLOGIST,
    verbose_name='Specializacja'
  )
  email = models.EmailField(verbose_name='Email służbowy',blank=True,null = True)
  phone = models.CharField(max_length=15,verbose_name='Telefon kontaktowy',blank=True, null=True)

  def __str__(self):
    return f'lek. {self.first_name} {self.last_name} ({self.specialization})'

  class Meta:
    verbose_name = 'Lekarz'
    verbose_name_plural = 'Lekarze'

class Patient(models.Model): 
  class Gender(models.TextChoices):
    MALE = 'Mężczyzna','Mężczyzna'
    FEMALE = 'Kobieta','Kobieta'
    OTHER = 'Inna','Inna'

  first_name = models.CharField(max_length=100, verbose_name='Imię')
  last_name = models.CharField(max_length=100,verbose_name='Nazwisko')
  pesel = models.CharField(
    max_length = 11,
    unique = True,
    null = True,
    blank = True,
    validators=[validate_pesel],
    verbose_name = 'PESEL',
    help_text = '11-cyfrowy numer identyfikacyjny'
  )
  date_of_birth = models.DateField(verbose_name='Data urodzenia')
  gender= models.CharField(
    max_length=15,
    choices=Gender.choices,
    default=Gender.MALE,
    verbose_name='Płeć'
  )
  #Adres zamieszkania
  address_street = models.CharField(max_length=200, verbose_name='Ulica i nr domu', blank=True, null=True)
  address_zip_code = models.CharField(
    max_length=6,
    verbose_name='Kod pocztowy',
    blank=True,
    null=True,
    validators=[RegexValidator(r'^\d{2}-\d{3}$', 'Format kodu: XX-XXX')]
  )
  address_city = models.CharField(max_length=100, verbose_name='Miejscowość', blank=True, null=True)

  #Dane kontaktowe
  phone_number = models.CharField(max_length= 15, verbose_name='Numer telefonu',blank=True, null= True)
  email = models.EmailField(verbose_name= 'Email', blank= True, null= True)

  #Relacja z lekarzami
  attending_doctor = models.ForeignKey(
    Doctor,
    on_delete=models.SET_NULL,
    null = True,
    blank = True,
    related_name= 'primary_patients',
    verbose_name= 'Lekarz Prowadzący',
  )
  consulting_doctors = models.ManyToManyField(
    Doctor,
    blank= True,
    related_name= 'consultation_patients',
    verbose_name= 'Lekarze konsultujący'
  )

  # Dane Medyczne (POLA ARCHIWALNE)
  initial_diagnosis= models.CharField(max_length=250,verbose_name='Wstępna diagnoza (ARCHIWALNE)',blank=True, null=True)
  diagnosis_date = models.DateField(verbose_name='Data diagnozy (ARCHIWALNE)', blank = True, null= True)

  def __str__(self):
    identifier = self.pesel if self.pesel else self.date_of_birth
    return f'{self.first_name} {self.last_name} ({identifier})'

  class Meta:
    verbose_name = 'Pacjent'
    verbose_name_plural = 'Pacjenci'

class Diagnosis(models.Model):
  class Status(models.TextChoices):
    SUSPECTED = 'PODEJRZENIE', 'Podejrzenie'
    CONFIRMED = 'POTWIERDZONA', 'Potwierdzona histopatologicznie'
    RECURRENCE = 'WZNOWA', 'Wznowa'
    REMISSION = 'REMISJA', 'Remisja (Wyleczona)'
    PALLIATIVE = 'PALIATYWNA', 'Opieka paliatywna'

  patient = models.ForeignKey(
    Patient,
    on_delete=models.CASCADE,
    related_name='diagnoses',
    verbose_name='Pacjenci'
  )
  icd_code =models.CharField(
    max_length= 10,
    verbose_name= 'Kod ICD-10',
    help_text= 'np. C34.1',
    blank= True,
    null= True
  )

  name = models.CharField(max_length=250, verbose_name='Rozpoznanie opisowe (np. Rak płuca)')
  diagnosis_date = models.DateField(verbose_name='Data postawienia diagnozy')

  # Klasyfikacja TNM
  tumor_stage = models.CharField(
    max_length=10,
    verbose_name='Cecha T (Guz)',
    help_text='Wielkość guza pierwotnego (np. T1, T2)',
    blank=True, null=True
  )
  node_stage = models.CharField(
    max_length=10,
    verbose_name='Cecha N (Węzły)',
    help_text='Stan regionalnych węzłów chłonnych (np. N0, N1)',
    blank=True, null=True
  )
  metastasis_stage = models.CharField(
    max_length=10,
    verbose_name='Cecha M (Przerzuty)',
    help_text='Obecność przerzutów odległych (np. M0, M1)',
    blank=True, null=True
  )

  description = models.TextField(verbose_name='Opis szczegółowy / Wynik hist-pat', blank=True, null=True)

  status = models.CharField(
    max_length=20,
    choices=Status.choices,
    default=Status.CONFIRMED,
    verbose_name='Status diagnozy'
  )

  def __str__(self):
    return f"{self.icd_code} - {self.name} ({self.diagnosis_date})"

  class Meta:
    verbose_name = "Diagnoza"
    verbose_name_plural = "Historia Chorób (Diagnozy)"
    ordering = ['-diagnosis_date']

class MedicalDocument(models.Model):
  patient = models.ForeignKey(
    Patient,
    on_delete=models.CASCADE,
    related_name='medical_documents',
    verbose_name='Pacjent'
  )
  name = models.CharField(max_length=250, verbose_name='Nazwa dokumentu (np. Wynik TK)')
  file = models.FileField(upload_to='medical_documents/', blank=True, null=True)
  upload_date = models.DateField(verbose_name='Data dodania dokumentu', blank=True, null=True)
  description = models.TextField(verbose_name= 'Komentarz',blank=True, null=True)

  def __str__(self):
    return f"{self.name} {self.upload_date}- {self.patient.last_name}"

  class Meta:
    verbose_name = "Dokument medyczny"
    verbose_name_plural = "Dokumentacja medyczna"
    ordering = ['-upload_date']

class Appointment(models.Model):
  class Status(models.TextChoices):
    SCHEDULED = 'ZAPLANOWANA', 'Zaplanowana'
    COMPLETED = 'ODBYTA', 'Odbyta'
    CANCELLED = 'ANULOWANA', 'Anulowana'
    NO_SHOW = 'NIESTAWIENNICTWO', 'Pacjent nie przyszedł'

  class AppointmentType(models.TextChoices):
    CONSULTATION = 'KONSULTACJA', 'Konsultacja lekarska'
    CHECKUP = 'KONTROLA', 'Badanie kontrolne'
    PROCEDURE = 'ZABIEG', 'Drobny zabieg'
    QUALIFICATION = 'KWALIFIKACJA', 'Kwalifikacja do leczenia'

  patient = models.ForeignKey(
    Patient,
    on_delete=models.CASCADE,
    related_name='appointments',
    verbose_name='Pacjent'
  )

  doctor = models.ForeignKey(
    Doctor,
    on_delete=models.CASCADE,
    related_name='appointments',
    verbose_name='Pacjent'
  )

  date_time= models.DateTimeField(verbose_name='Data i godzina wizyty')
  appointment_type = models.CharField(
    max_length=50,
    choices=AppointmentType.choices,
    default=AppointmentType.CONSULTATION,
    verbose_name='Rodzaj wizyty'
  )
  status = models.CharField(
    max_length=20,
    choices=Status.choices,
    default=Status.SCHEDULED,
    verbose_name='Status'
  )
  notes = models.TextField(verbose_name='Notatki z wizyty',blank=True, null=True)

  def __str__(self):
    return f'{self.date_time.strftime("%Y-%m-%d %H:%M")} - {self.patient.last_name}'

  class Meta:
    verbose_name = "Wizyta"
    verbose_name_plural = "Wizyty"

class TherapyCycle(models.Model):
  #Stara relacja zostawiona w celu kompatybilności starszych danych
  patient = models.ForeignKey(
    Patient,
    on_delete=models.CASCADE,
    related_name='therapy_cycles',
    verbose_name='Pacjent'
  )
  diagnosis = models.ForeignKey(
    Diagnosis,
    on_delete=models.CASCADE,
    related_name='therapy_cycles',
    verbose_name='Leczona choroba',
    null=True,
    blank=True,
  )
  start_date = models.DateField(verbose_name='Data rozpoczęcia')
  end_date = models.DateField(verbose_name='Data zakończenia', null=True, blank=True)


  class Therapy(models.TextChoices):
    CHEMO = 'Chemoterapia', 'Chemioterapia'
    HORMON = 'Terapia hormonalna', 'Terapia hormonalna'
    IMMUNO = 'Immunoterapia', 'Immunoterapia'
    PHOTO = 'Terapia fotodynamiczna', 'Terapia fotodynamiczna'
    TARGET = 'Terapia celowana', 'Terapia celowana'
    RADIO = 'Radioterapia', 'Radioterapia'

  protocol_name = models.CharField(
    max_length=200,
    choices=Therapy.choices,
    verbose_name='Rodzaj terapii'
  )
  class Status(models.TextChoices):
    ONGOING = 'W trakcie', 'W trakcie'
    COMPLETED = 'Zakończona', 'Zakończona'
    PAUSED = 'Wstrzymana', 'Wstrzymana'
    PLANNED = 'Zaplanowana', 'Zaplanowana'
  
  status = models.CharField(
    max_length=200,
    choices=Status.choices,
    verbose_name='Status terapii'
  )

  def clean(self):
    if self.diagnosis and self.patient:
      if self.diagnosis.patient != self.patient:
        raise ValidationError('Wybrana diagnoza nie należy do przypisanego pacjenta!')


  def __str__(self):
    if self.diagnosis:
      return f'{self.patient.last_name} - {self.protocol_name} (Leczenie: {self.diagnosis.name})'
    return f'{self.patient.last_name} - {self.protocol_name}'


  class Meta:
    verbose_name = "Cykl Terapii"
    verbose_name_plural = "Cykle Terapii"


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
    return f'{self.therapy_cycle} - {self.assessment_date}'


class Meta:
  verbose_name = "Odpowiedź na leczenie"
  verbose_name_plural = "Odpowiedzi na leczenie"

class AdverseEvent(models.Model):
  class severity_grades(models.TextChoices):
    G1 = "Grade 1", "Grade 1 - Łagodne"
    G2 = "Grade 2", "Grade 2 - Umiarkowane"
    G3 = "Grade 3", "Grade 3 - Ciężkie"
    G4 = "Grade 4", "Grade 4 - Zagrażające życiu"
    G5 = "Grade 5", "Grade 5 - Zgon"

  therapy_cycle = models.ForeignKey(
    TherapyCycle,
    on_delete=models.CASCADE,
    related_name='adverse_events',
    verbose_name="Cykl terapii",
    null=True
  )

  event_date = models.DateField(verbose_name='Data zdarzenia')
  description = models.TextField(
    max_length=1500,
    verbose_name= "Opis zdarzenia"
  )

  severity = models.CharField(
    choices=severity_grades.choices,
    default=severity_grades.G1,
    verbose_name= "Severity"
  )

  action_taken = models.TextField(
    max_length=1500,
    verbose_name= "Podjęte działanie"
  )

  def __str__(self):
    return f'{self.therapy_cycle} - {self.severity}'

  class Meta:
    verbose_name = "Zdarzenie niepożądane"
    verbose_name_plural = "Zdarzenia niepożądane"

class Mutation(models.Model):
  class MutationTypeChoices(models.TextChoices):
    MISSENSE = 'MISSENSE', 'Missense'
    NONSENSE = 'NONSENSE', 'Nonsense'
    FRAMESHIFT = 'FRAMESHIFT', 'Frameshift'
    SILENT = 'SILENT', 'Silent'
    SPLICE_SITE = 'SPLICE_SITE', 'Splice site'
    INDEL = 'INDEL', 'Indel'
    OTHER = 'OTHER', 'Inna'

  patient = models.ForeignKey(
    Patient,
    on_delete=models.CASCADE,
    related_name='mutations',
    verbose_name="Pacjent"
  )

  gene = models.CharField(
        max_length=15,
        verbose_name='ENSEMBL Gene ID',
        help_text='The 15-character ENSEMBL stable ID (e.g., ENSG00000139618)',
  )

  chromosome_location = models.CharField(
      max_length=100,
      help_text="Format: chr:start-end (e.g., chr17:41196312-41277500)",
      verbose_name="Lokalizacja w genomie"
  ),

  mutation_type = models.CharField(
        max_length=20,
        choices=MutationTypeChoices.choices,
        default=MutationTypeChoices.OTHER,)

  vaf = models.FloatField(
    verbose_name="VAF"
  )

  def __str__(self):
    return f'{self.gene} ({self.patient.last_name})'

  class Meta:
    verbose_name = "Mutacja"
    verbose_name_plural = "Mutacje"