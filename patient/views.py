from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from patient.models import Patient, Doctor


@login_required(login_url='login')
def home(request):
  user = request.user

  if user.is_superuser:
    patients = Patient.objects.all()

  else:
    try:

      doctor_profile = user.doctor_profile

      patients = Patient.objects.filter(
        Q(attending_doctor=doctor_profile) |
        Q(consulting_doctors=doctor_profile)
      ).distinct()

    except Doctor.DoesNotExist:

      patients = []

  context = {
    'user': user,
    'patients': patients
  }

  return render(request, 'home_page/home.html', context)