from django.contrib import admin
from .models import Doctor, Patient, Response, TherapyCycle, AdverseEvent, Mutation, Diagnosis, MedicalDocument, \
  Appointment

# Register your models here.
admin.site.register(Doctor)
admin.site.register(Patient)
admin.site.register(Diagnosis)
admin.site.register(MedicalDocument),
admin.site.register(Appointment)
admin.site.register(TherapyCycle)
admin.site.register(Response)
admin.site.register(AdverseEvent)
admin.site.register(Mutation)