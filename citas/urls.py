from django.urls import path
from . import views

urlpatterns = [
    path('doctors/', views.doctor_list, name='doctor'),
    path('doctors/create/', views.create_doctor, name='doctors_create'),
    path('doctors/<int:pk>/', views.show_doctor, name='doctors_show'),
    path('doctors/update/<int:pk>/', views.doctors_update, name='doctors_update'),
    path('doctors/disable/<int:pk>/', views.doctors_disable, name='doctors_disable'),
    path('doctors/delete/<int:pk>/', views.doctors_delete, name='doctors_delete'),
    path('hello_world/', views.hello_world),
]
