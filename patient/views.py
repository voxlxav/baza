from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q

from .forms import PatientForm

from patient.models import Patient, Doctor, Appointment

from django.shortcuts import render, get_object_or_404, redirect
from .models import Patient
from .forms import PatientForm


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
def add_patient(request):
    if request.method == 'POST':
        form = PatientForm(request.POST)
        if form.is_valid():
            patient = form.save(commit=False)

            try:
                patient.attending_doctor = request.user.doctor_profile
                patient.save()
            except Doctor.DoesNotExist:
                messages.error(request, "Błąd: Twoje konto nie jest powiązane z profilem lekarza.")
        else:
            for field, errors in form.errors.items():
                for error in errors:
                  messages.error(request, f"Błąd w polu {field}: {error}")

            return redirect('home')

    return redirect('home')

@login_required(login_url='login')
<<<<<<< Updated upstream
def appointments(request):
  user = request.user
  context = {
    'user': user
  }
  return render(request,"appointments/appointments.html",context)
=======
def patient_detail(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    editing = request.GET.get("edit") == "1"

    if request.method == "POST":
        form = PatientForm(request.POST, instance=patient)
        if form.is_valid():
            form.save()
            return redirect("patient_detail", pk=pk)
    else:
        form = PatientForm(instance=patient)

    return render(request, "home_page/patient_detail.html", {
        "patient": patient,
        "form": form,
        "editing": editing,
    })

@login_required(login_url='login')
def delete_patient(request, pk):
    patient = get_object_or_404(Patient, pk=pk)

    if request.method == "POST":
        patient.delete()
        return redirect("home")

    return redirect("patient_detail", pk=pk)
>>>>>>> Stashed changes
