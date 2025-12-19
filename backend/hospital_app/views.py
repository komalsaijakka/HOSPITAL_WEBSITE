from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib import messages
from .forms import SignUpForm, LoginForm, AppointmentForm 
from .models import Staff, Appointment, Service, Facility, Achievement, Speciality, Therapy, Doctor 
from django.db.models import Q
from django.core.paginator import Paginator
from django.utils import timezone

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
        else:
           return render(request, 'registration/signup.html', {'form': form})
    else:
        form = SignUpForm()
    return render(request, 'registration/signup.html', {'form': form})
def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main')  
    else:
        form = LoginForm()
    return render(request, 'registration/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('main') 

def main_view(request):
    specialities = Speciality.objects.all()
    therapies = Therapy.objects.all()
    doctors = Staff.objects.filter(staff_type='doctor')[:3]
    return render(request, 'main.html', {'specialities': specialities, 'therapies': therapies, 'doctors': doctors})

def search_view(request):
    query = request.GET.get('q')
    results = []
    if query:
        results_staff = Staff.objects.filter(
            Q(name__icontains=query) | Q(specialization__icontains=query) | Q(bio__icontains=query)
        )
        results_specialities = Speciality.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )
        results_therapies = Therapy.objects.filter(
            Q(name__icontains=query) | Q(description__icontains=query)
        )

        results = list(results_staff) + list(results_specialities) + list(results_therapies)
        for result in results_staff:
            result.search_type = 'Doctor'
        for result in results_specialities:
            result.search_type = 'Speciality'
        for result in results_therapies:
            result.search_type = 'Therapy'

        results.sort(key=lambda x: getattr(x, 'name', str(x)))
    return render(request, 'main.html', {'search_results': results, 'query': query})

def services_view(request):
    services_list = Service.objects.all()
    return render(request, 'services.html', {'services': services_list})

def facilities_view(request):
    facilities_list = Facility.objects.all()
    return render(request, 'facilities.html', {'facilities': facilities_list})

def about_us_view(request):
    about_content = "Welcome to MediCare...."
    achievements = Achievement.objects.all()
    return render(request, 'about_us.html', {'about_content': about_content, 'achievements': achievements})

def consultants_view(request):
    doctors = Staff.objects.filter(staff_type='doctor')
    residents = Staff.objects.filter(staff_type='resident')
    nurses = Staff.objects.filter(staff_type='nurse')
    return render(request, 'consultants.html', {'doctors': doctors, 'residents': residents, 'nurses': nurses})

@login_required
def appointment_history_view(request):
    appointments = Appointment.objects.filter(user=request.user).select_related('doctor')
    return render(request, 'appointment.html', {'appointments': appointments})

def speciality_detail_view(request, speciality_id):
    speciality = get_object_or_404(Speciality, pk=speciality_id)
    doctors = Staff.objects.filter(staff_type='doctor', department__name=speciality.name)
    return render(request, 'speciality_detail.html', {'speciality': speciality, 'doctors': doctors})

def staff_detail_view(request, staff_id):
    staff_member = get_object_or_404(Staff, pk=staff_id)
    return render(request, 'staff_detail.html', {'staff_member': staff_member})

def service_detail_view(request, service_id):
    service = get_object_or_404(Service, pk=service_id)
    return render(request, 'service_detail.html', {'service': service})

def facility_detail_view(request, facility_id):
    facility = get_object_or_404(Facility, pk=facility_id)
    return render(request, 'facility_detail.html', {'facility': facility})
@login_required
def create_appointment(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user

            print("Form data:", form.cleaned_data)

            try:
                appointment.doctor = form.cleaned_data['selected_doctor'] 
            except KeyError:
                messages.error(request, "Doctor selection is missing. Please select a doctor.")
                return render(request, 'appointment.html', {'form': form})  

            appointment.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect('appointment_history')
        else:
            messages.error(request, "Error booking appointment. Please check the form.")
            return render(request, 'appointment.html', {'form': form})  
    else:
        form = AppointmentForm()
    return render(request, 'appointment.html', {'form': form})

def check_appointment_clash(doctor_id, appointment_time):
    if timezone.is_naive(appointment_time):
        appointment_time = timezone.make_aware(appointment_time, timezone.get_current_timezone())

    overlapping_appointments = Appointment.objects.filter(
        doctor_id=doctor_id, 
        appointment_date__range=(
            appointment_time - timezone.timedelta(minutes=59),
            appointment_time + timezone.timedelta(minutes=59),
        ),
    )
    if overlapping_appointments.exists():
        return True, "An appointment already exists for this doctor within the selected time."
    else:
        return False, "No clash found."



@login_required
def appointment_view(request):
    if request.method == 'POST':
        form = AppointmentForm(request.POST)
        if form.is_valid():
            appointment = form.save(commit=False)
            appointment.user = request.user
            doctor = form.cleaned_data['doctor'] 
            appointment.doctor = doctor
            appointment_date_str = form.cleaned_data['appointment_date']
            clash, message = check_appointment_clash(doctor.id, appointment_date_str)  
            if clash:
                messages.error(request, message)
                return render(request, 'appointment.html', {'form': form})

            appointment.save()
            messages.success(request, "Appointment booked successfully!")
            return redirect('appointment_history')
        else:
            messages.error(request, "Error booking appointment. Please check the form.")
            return render(request, 'appointment.html', {'form': form})
    else:
        form = AppointmentForm()
    return render(request, 'appointment.html', {'form': form})