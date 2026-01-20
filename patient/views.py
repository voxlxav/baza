from django.shortcuts import render, redirect

from patient.models import Patient


# Create your views here.
def home(request):
  if request.user.is_authenticated:
      user = request.user
      return render(request, 'home_page/home.html', {'username': user.username})
  else:
    return redirect('login/')