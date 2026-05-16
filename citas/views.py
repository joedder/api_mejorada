from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse
from .models import Doctor

# Create your views here.

def create_doctor(request):
    if request.method == 'POST':
        doctor = Doctor.objects.create(
            first_name=request.POST.get('first_name'),
            second_name=request.POST.get('second_name'),
            first_lastname=request.POST.get('first_lastname'),
            second_lastname=request.POST.get('second_lastname'),
            identity_id=request.POST.get('identity_id'),
            gender=request.POST.get('gender'),
            phone_number=request.POST.get('phone_number'),
            specialty=request.POST.get('specialty'),
        )
        messages.success(request, f'Doctor "{doctor.first_name} {doctor.first_lastname}" creado')
        return redirect('doctors_create')

    return render(request, 'citas/crear_doctor.html')


def doctor_list(request):
    doctors_list = Doctor.objects.all().order_by('id')
    paginator = Paginator(doctors_list, 10)
    page_number = request.GET.get('page')
    doctors = paginator.get_page(page_number)

    return render(request, 'citas/doctor_list.html', {
        'doctors': doctors,
    })


def show_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'citas/doctor_show.html', {
        'doctor': doctor,
        'editing': False,
    })


def doctors_update(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    if request.method == 'POST':
        doctor.first_name = request.POST.get('first_name')
        doctor.second_name = request.POST.get('second_name')
        doctor.first_lastname = request.POST.get('first_lastname')
        doctor.second_lastname = request.POST.get('second_lastname')
        doctor.identity_id = request.POST.get('identity_id')
        doctor.gender = request.POST.get('gender')
        doctor.phone_number = request.POST.get('phone_number')
        doctor.specialty = request.POST.get('specialty')
        doctor.save()
        messages.success(request, f'Doctor "{doctor.first_name} {doctor.first_lastname}" actualizado')
        return redirect('doctor')

    return render(request, 'citas/doctor_show.html', {
        'doctor': doctor,
        'editing': True,
    })


def doctors_disable(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.soft_delete()
    messages.success(request, f'Doctor "{doctor.first_name} {doctor.first_lastname}" desactivado')
    return redirect('doctor')


def doctors_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.hard_delete()
    messages.success(request, f'Doctor "{doctor.first_name} {doctor.first_lastname}" borrado')
    return redirect('doctor')


def hello_world(request):
    return HttpResponse("<h1>Hola Mundo<h1>")