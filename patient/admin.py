from django.contrib import admin
from .models import Patient, Response, TherapyCycle

# Register your models here.
admin.site.register(Patient)
admin.site.register(TherapyCycle)
admin.site.register(Response)