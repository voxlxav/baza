from django.shortcuts import render, redirect

from patient.models import Patient


# Create your views here.
def home(request):
  if request.user.is_authenticated:
      user = request.user
      patient = Patient.objects.all()
      return render(request, 'home_page/home.html', {'username': user.username, 'patient': patient})
  else:
    return redirect('login/')