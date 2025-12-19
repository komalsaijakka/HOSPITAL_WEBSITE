from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'), 
    path('logout/', views.logout_view, name='logout'),
    path('', views.main_view, name='main'),
    path('search/', views.search_view, name='search'),
    path('services/', views.services_view, name='services'),
    path('services/<int:service_id>/', views.service_detail_view, name='service_detail'),
    path('facilities/', views.facilities_view, name='facilities'),
    path('facilities/<int:facility_id>/', views.facility_detail_view, name='facility_detail'),
    path('about-us/', views.about_us_view, name='about_us'),
    path('consultants/', views.consultants_view, name='consultants'),
    path('staff/<int:staff_id>/', views.staff_detail_view, name='staff_detail'),
    path('appointment/', views.appointment_view, name='appointment'),
    path('appointment/history/', views.appointment_history_view, name='appointment_history'),
    path('specialities/<int:speciality_id>/', views.speciality_detail_view, name='speciality_detail'),
]