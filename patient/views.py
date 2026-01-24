from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Q

from .forms import PatientForm

from patient.models import Patient, Doctor


@login_required(login_url='login')
def home(request):
  user = request.user

  if user.is_superuser:
    patients = Patient.objects.all().order_by('-id')

  else:
    try:

      doctor_profile = user.doctor_profile

      patients = Patient.objects.filter(
        Q(attending_doctor=doctor_profile) |
        Q(consulting_doctors=doctor_profile)
      ).distinct().order_by('-id')

    except Doctor.DoesNotExist:
      patients = Patient.objects.none()

  #Wyszukiwanie
  search_query = request.GET.get('q')
  if search_query:
    patients = patients.filter(
      Q(first_name__icontains=search_query) |
      Q(last_name__icontains=search_query) |
      Q(pesel__startswith=search_query)
    )

  paginator = Paginator(patients, 15)

  page_number = request.GET.get('page')
  page_obj = paginator.get_page(page_number)

  #Paginacja
  context = {
    'user': user,
    'patients': page_obj,
    'search_query': search_query or ""
  }


  return render(request, 'home_page/home.html', context)

@login_required(login_url='login')
def patient_detail(request, pk):
  patient = get_object_or_404(Patient, pk=pk)
  context = {
    'patient': patient
  }
  return render(request,'home_page/patient_detail.html',context)

@login_required(login_url='login')
def add_patient(request):
  if request.method == 'POST':
    form = PatientForm(request.POST)
    if form.is_valid():
      patient = form.save(commit=False)

      try:
        patient.attending_doctor = request.user.doctor_profile
      except Doctor.DoesNotExist:
        pass

      patient.save()

      return redirect('home')
  else:
    form = PatientForm()

  return render(request, 'home_page/add_patient.html', {'form': form})