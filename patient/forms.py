from django import forms
from patient.models import Patient

class PatientForm(forms.ModelForm):
  class Meta:
        model = Patient
        fields = [
          "first_name", "last_name", "pesel", "date_of_birth",
          "gender","address_street","address_zip_code","address_city",
          "phone_number","email"
        ]
        widgets = {
          'date_of_birth': forms.DateInput(attrs={'type':'date','class':'form-control'}),
        }