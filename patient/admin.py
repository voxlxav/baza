from django.contrib import admin
from .models import Patient, Response, TherapyCycle, AdverseEvent

# Register your models here.
admin.site.register(Patient)
admin.site.register(TherapyCycle)
admin.site.register(Response)
admin.site.register(AdverseEvent)