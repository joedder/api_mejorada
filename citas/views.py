from django.shortcuts import render, redirect, get_object_or_404
from django.core.paginator import Paginator
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from .models import User
from .models import (
    Doctor,
    TypeAppointment,
    PriorityAppointment,
    CategoryMedicalRecord,
    Patient,
    PatientRecord,
    MedicalAppointment,
    MedicalRecord,
)

# Create your views here.

@login_required(login_url='login')
def create_doctor(request):
    if request.method == 'POST':
        identity_id = request.POST.get('identity_id')
        if Doctor.all_objects.filter(identity_id=identity_id).exists():
            messages.error(request, f'El doctor con la cédula "{identity_id}" ya se encuentra registrado.')
            return redirect('doctors_create')

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


@login_required(login_url='login')
def doctor_list(request):
    doctors_list = Doctor.objects.all().order_by('id')
    paginator = Paginator(doctors_list, 10)
    page_number = request.GET.get('page')
    doctors = paginator.get_page(page_number)

    return render(request, 'citas/doctor_list.html', {
        'doctors': doctors,
    })


@login_required(login_url='login')
def show_doctor(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    return render(request, 'citas/doctor_show.html', {
        'doctor': doctor,
        'editing': False,
    })


@login_required(login_url='login')
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


@login_required(login_url='login')
def doctors_disable(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.soft_delete()
    messages.success(request, f'Doctor "{doctor.first_name} {doctor.first_lastname}" desactivado')
    return redirect('doctor')


@login_required(login_url='login')
def doctors_delete(request, pk):
    doctor = get_object_or_404(Doctor, pk=pk)
    doctor.hard_delete()
    messages.success(request, f'Doctor "{doctor.first_name} {doctor.first_lastname}" borrado')
    return redirect('doctor')


@login_required(login_url='login')
def create_typeappointment(request):
    if request.method == 'POST':
        typeappointment = TypeAppointment.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        messages.success(request, f'Type appointment "{typeappointment.name}" creado')
        return redirect('typeappointments_create')

    return render(request, 'citas/crear_typeappointment.html')


@login_required(login_url='login')
def typeappointment_list(request):
    typeappointments_list = TypeAppointment.objects.all().order_by('id')
    paginator = Paginator(typeappointments_list, 10)
    page_number = request.GET.get('page')
    typeappointments = paginator.get_page(page_number)

    return render(request, 'citas/typeappointment_list.html', {
        'typeappointments': typeappointments,
    })


@login_required(login_url='login')
def typeappointment_show(request, pk):
    typeappointment = get_object_or_404(TypeAppointment, pk=pk)
    return render(request, 'citas/typeappointment_show.html', {
        'typeappointment': typeappointment,
        'editing': False,
    })


@login_required(login_url='login')
def typeappointments_update(request, pk):
    typeappointment = get_object_or_404(TypeAppointment, pk=pk)
    if request.method == 'POST':
        typeappointment.name = request.POST.get('name')
        typeappointment.description = request.POST.get('description')
        typeappointment.save()
        messages.success(request, f'Type appointment "{typeappointment.name}" actualizado')
        return redirect('typeappointment')

    return render(request, 'citas/typeappointment_show.html', {
        'typeappointment': typeappointment,
        'editing': True,
    })


@login_required(login_url='login')
def typeappointments_disable(request, pk):
    typeappointment = get_object_or_404(TypeAppointment, pk=pk)
    typeappointment.soft_delete()
    messages.success(request, f'Type appointment "{typeappointment.name}" desactivado')
    return redirect('typeappointment')


@login_required(login_url='login')
def typeappointments_delete(request, pk):
    typeappointment = get_object_or_404(TypeAppointment, pk=pk)
    typeappointment.hard_delete()
    messages.success(request, f'Type appointment "{typeappointment.name}" borrado')
    return redirect('typeappointment')


@login_required(login_url='login')
def create_priorityappointment(request):
    if request.method == 'POST':
        priorityappointment = PriorityAppointment.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        messages.success(request, f'Priority appointment "{priorityappointment.name}" creado')
        return redirect('priorityappointments_create')

    return render(request, 'citas/crear_priorityappointment.html')


@login_required(login_url='login')
def priorityappointment_list(request):
    priorityappointments_list = PriorityAppointment.objects.all().order_by('id')
    paginator = Paginator(priorityappointments_list, 10)
    page_number = request.GET.get('page')
    priorityappointments = paginator.get_page(page_number)

    return render(request, 'citas/priorityappointment_list.html', {
        'priorityappointments': priorityappointments,
    })


@login_required(login_url='login')
def priorityappointment_show(request, pk):
    priorityappointment = get_object_or_404(PriorityAppointment, pk=pk)
    return render(request, 'citas/priorityappointment_show.html', {
        'priorityappointment': priorityappointment,
        'editing': False,
    })


@login_required(login_url='login')
def priorityappointments_update(request, pk):
    priorityappointment = get_object_or_404(PriorityAppointment, pk=pk)
    if request.method == 'POST':
        priorityappointment.name = request.POST.get('name')
        priorityappointment.description = request.POST.get('description')
        priorityappointment.save()
        messages.success(request, f'Priority appointment "{priorityappointment.name}" actualizado')
        return redirect('priorityappointment')

    return render(request, 'citas/priorityappointment_show.html', {
        'priorityappointment': priorityappointment,
        'editing': True,
    })


@login_required(login_url='login')
def priorityappointments_disable(request, pk):
    priorityappointment = get_object_or_404(PriorityAppointment, pk=pk)
    priorityappointment.soft_delete()
    messages.success(request, f'Priority appointment "{priorityappointment.name}" desactivado')
    return redirect('priorityappointment')


@login_required(login_url='login')
def priorityappointments_delete(request, pk):
    priorityappointment = get_object_or_404(PriorityAppointment, pk=pk)
    priorityappointment.hard_delete()
    messages.success(request, f'Priority appointment "{priorityappointment.name}" borrado')
    return redirect('priorityappointment')


@login_required(login_url='login')
def create_categorymedicalrecord(request):
    if request.method == 'POST':
        categorymedicalrecord = CategoryMedicalRecord.objects.create(
            name=request.POST.get('name'),
            description=request.POST.get('description')
        )
        messages.success(request, f'Category medical record "{categorymedicalrecord.name}" creado')
        return redirect('categorymedicalrecords_create')

    return render(request, 'citas/crear_categorymedicalrecord.html')


@login_required(login_url='login')
def categorymedicalrecord_list(request):
    categorymedicalrecords_list = CategoryMedicalRecord.objects.all().order_by('id')
    paginator = Paginator(categorymedicalrecords_list, 10)
    page_number = request.GET.get('page')
    categorymedicalrecords = paginator.get_page(page_number)

    return render(request, 'citas/categorymedicalrecord_list.html', {
        'categorymedicalrecords': categorymedicalrecords,
    })


@login_required(login_url='login')
def categorymedicalrecord_show(request, pk):
    categorymedicalrecord = get_object_or_404(CategoryMedicalRecord, pk=pk)
    return render(request, 'citas/categorymedicalrecord_show.html', {
        'categorymedicalrecord': categorymedicalrecord,
        'editing': False,
    })


@login_required(login_url='login')
def categorymedicalrecords_update(request, pk):
    categorymedicalrecord = get_object_or_404(CategoryMedicalRecord, pk=pk)
    if request.method == 'POST':
        categorymedicalrecord.name = request.POST.get('name')
        categorymedicalrecord.description = request.POST.get('description')
        categorymedicalrecord.save()
        messages.success(request, f'Category medical record "{categorymedicalrecord.name}" actualizado')
        return redirect('categorymedicalrecord')

    return render(request, 'citas/categorymedicalrecord_show.html', {
        'categorymedicalrecord': categorymedicalrecord,
        'editing': True,
    })


@login_required(login_url='login')
def categorymedicalrecords_disable(request, pk):
    categorymedicalrecord = get_object_or_404(CategoryMedicalRecord, pk=pk)
    categorymedicalrecord.soft_delete()
    messages.success(request, f'Category medical record "{categorymedicalrecord.name}" desactivado')
    return redirect('categorymedicalrecord')


@login_required(login_url='login')
def categorymedicalrecords_delete(request, pk):
    categorymedicalrecord = get_object_or_404(CategoryMedicalRecord, pk=pk)
    categorymedicalrecord.hard_delete()
    messages.success(request, f'Category medical record "{categorymedicalrecord.name}" borrado')
    return redirect('categorymedicalrecord')


@login_required(login_url='login')
def create_patient(request):
    if request.method == 'POST':
        patient = Patient.objects.create(
            first_name=request.POST.get('first_name'),
            second_name=request.POST.get('second_name'),
            first_lastname=request.POST.get('first_lastname'),
            second_lastname=request.POST.get('second_lastname'),
            identity_id=request.POST.get('identity_id'),
            birth_date=request.POST.get('birth_date'),
            gender=request.POST.get('gender'),
            phone_number=request.POST.get('phone_number'),
            mobile_number=request.POST.get('mobile_number'),
            address=request.POST.get('address'),
            blood_group=request.POST.get('blood_group'),
            name_emergency_contact=request.POST.get('name_emergency_contact'),
            last_name_emergency_contact=request.POST.get('last_name_emergency_contact'),
            phone_number_emergency_contact=request.POST.get('phone_number_emergency_contact'),
            id_patient_record_id=request.POST.get('id_patient_record') or None,
        )
        messages.success(request, f'Patient "{patient.first_name} {patient.first_lastname}" creado')
        return redirect('patients_create')

    patientrecords = PatientRecord.objects.all()
    return render(request, 'citas/crear_patient.html', {
        'patientrecords': patientrecords,
    })


@login_required(login_url='login')
def patient_list(request):
    patients_list = Patient.objects.all().order_by('id')
    paginator = Paginator(patients_list, 10)
    page_number = request.GET.get('page')
    patients = paginator.get_page(page_number)

    return render(request, 'citas/patient_list.html', {
        'patients': patients,
    })


@login_required(login_url='login')
def patient_show(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    return render(request, 'citas/patient_show.html', {
        'patient': patient,
        'editing': False,
    })


@login_required(login_url='login')
def patients_update(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    if request.method == 'POST':
        patient.first_name = request.POST.get('first_name')
        patient.second_name = request.POST.get('second_name')
        patient.first_lastname = request.POST.get('first_lastname')
        patient.second_lastname = request.POST.get('second_lastname')
        patient.identity_id = request.POST.get('identity_id')
        patient.birth_date = request.POST.get('birth_date')
        patient.gender = request.POST.get('gender')
        patient.phone_number = request.POST.get('phone_number')
        patient.mobile_number = request.POST.get('mobile_number')
        patient.address = request.POST.get('address')
        patient.blood_group = request.POST.get('blood_group')
        patient.name_emergency_contact = request.POST.get('name_emergency_contact')
        patient.last_name_emergency_contact = request.POST.get('last_name_emergency_contact')
        patient.phone_number_emergency_contact = request.POST.get('phone_number_emergency_contact')
        patient.id_patient_record_id = request.POST.get('id_patient_record') or None
        patient.save()
        messages.success(request, f'Patient "{patient.first_name} {patient.first_lastname}" actualizado')
        return redirect('patient')

    patientrecords = PatientRecord.objects.all()
    return render(request, 'citas/patient_show.html', {
        'patient': patient,
        'patientrecords': patientrecords,
        'editing': True,
    })


@login_required(login_url='login')
def patients_disable(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.soft_delete()
    messages.success(request, f'Patient "{patient.first_name} {patient.first_lastname}" desactivado')
    return redirect('patient')


@login_required(login_url='login')
def patients_delete(request, pk):
    patient = get_object_or_404(Patient, pk=pk)
    patient.hard_delete()
    messages.success(request, f'Patient "{patient.first_name} {patient.first_lastname}" borrado')
    return redirect('patient')


@login_required(login_url='login')
def create_patientrecord(request):
    if request.method == 'POST':
        patientrecord = PatientRecord.objects.create(
            entry_date=request.POST.get('entry_date'),
            id_patient_id=request.POST.get('id_patient'),
        )
        messages.success(request, f'Patient record "{patientrecord.id}" creado')
        return redirect('patientrecords_create')

    patients = Patient.objects.all()
    return render(request, 'citas/crear_patientrecord.html', {
        'patients': patients,
    })


@login_required(login_url='login')
def patientrecord_list(request):
    patientrecords_list = PatientRecord.objects.all().order_by('id')
    paginator = Paginator(patientrecords_list, 10)
    page_number = request.GET.get('page')
    patientrecords = paginator.get_page(page_number)

    return render(request, 'citas/patientrecord_list.html', {
        'patientrecords': patientrecords,
    })


@login_required(login_url='login')
def patientrecord_show(request, pk):
    patientrecord = get_object_or_404(PatientRecord, pk=pk)
    return render(request, 'citas/patientrecord_show.html', {
        'patientrecord': patientrecord,
        'editing': False,
    })


@login_required(login_url='login')
def patientrecords_update(request, pk):
    patientrecord = get_object_or_404(PatientRecord, pk=pk)
    if request.method == 'POST':
        patientrecord.entry_date = request.POST.get('entry_date')
        patientrecord.id_patient_id = request.POST.get('id_patient')
        patientrecord.save()
        messages.success(request, f'Patient record "{patientrecord.id}" actualizado')
        return redirect('patientrecord')

    patients = Patient.objects.all()
    return render(request, 'citas/patientrecord_show.html', {
        'patientrecord': patientrecord,
        'patients': patients,
        'editing': True,
    })


@login_required(login_url='login')
def patientrecords_disable(request, pk):
    patientrecord = get_object_or_404(PatientRecord, pk=pk)
    patientrecord.soft_delete()
    messages.success(request, f'Patient record "{patientrecord.id}" desactivado')
    return redirect('patientrecord')


@login_required(login_url='login')
def patientrecords_delete(request, pk):
    patientrecord = get_object_or_404(PatientRecord, pk=pk)
    patientrecord.hard_delete()
    messages.success(request, f'Patient record "{patientrecord.id}" borrado')
    return redirect('patientrecord')


@login_required(login_url='login')
def create_medicalappointment(request):
    if request.method == 'POST':
        cancellation_date = request.POST.get('cancellation_date') or None
        active_val = request.POST.get('active')
        
        is_active = True
        if cancellation_date:
            is_active = False
        elif active_val == 'False':
            is_active = False
            
        medicalappointment = MedicalAppointment.objects.create(
            id_doctor_id=request.POST.get('id_doctor'),
            appointment_time=request.POST.get('appointment_time') or None,
            reason_appointment=request.POST.get('reason_appointment'),
            type_id_id=request.POST.get('type_id'),
            priority_id_id=request.POST.get('priority_id'),
            cancellation_date=cancellation_date,
            reason_for_cancellation=request.POST.get('reason_for_cancellation'),
            rescheduled_date=request.POST.get('rescheduled_date') or None,
            patient_record_id=request.POST.get('patient_record'),
            patient_comments=request.POST.get('patient_comments'),
            active=is_active,
        )
        messages.success(request, f'Medical appointment "{medicalappointment.id}" creado')
        return redirect('medicalappointments_create')

    doctors = Doctor.objects.all()
    typeappointments = TypeAppointment.objects.all()
    priorities = PriorityAppointment.objects.all()
    patientrecords = PatientRecord.objects.all()
    return render(request, 'citas/crear_medicalappointment.html', {
        'doctors': doctors,
        'typeappointments': typeappointments,
        'priorities': priorities,
        'patientrecords': patientrecords,
    })


@login_required(login_url='login')
def medicalappointment_list(request):
    medicalappointments_list = MedicalAppointment.objects.all().order_by('id')
    paginator = Paginator(medicalappointments_list, 10)
    page_number = request.GET.get('page')
    medicalappointments = paginator.get_page(page_number)

    return render(request, 'citas/medicalappointment_list.html', {
        'medicalappointments': medicalappointments,
    })


@login_required(login_url='login')
def medicalappointment_show(request, pk):
    medicalappointment = get_object_or_404(MedicalAppointment, pk=pk)
    return render(request, 'citas/medicalappointment_show.html', {
        'medicalappointment': medicalappointment,
        'editing': False,
    })


@login_required(login_url='login')
def medicalappointments_update(request, pk):
    medicalappointment = get_object_or_404(MedicalAppointment, pk=pk)
    if request.method == 'POST':
        medicalappointment.id_doctor_id = request.POST.get('id_doctor')
        medicalappointment.appointment_time = request.POST.get('appointment_time') or None
        medicalappointment.reason_appointment = request.POST.get('reason_appointment')
        medicalappointment.type_id_id = request.POST.get('type_id')
        medicalappointment.priority_id_id = request.POST.get('priority_id')
        medicalappointment.cancellation_date = request.POST.get('cancellation_date') or None
        medicalappointment.reason_for_cancellation = request.POST.get('reason_for_cancellation')
        medicalappointment.rescheduled_date = request.POST.get('rescheduled_date') or None
        medicalappointment.patient_record_id = request.POST.get('patient_record')
        medicalappointment.patient_comments = request.POST.get('patient_comments')
        
        if medicalappointment.rescheduled_date:
            medicalappointment.appointment_time = medicalappointment.rescheduled_date
            medicalappointment.cancellation_date = None
            medicalappointment.reason_for_cancellation = None
            medicalappointment.rescheduled_date = None
            medicalappointment.active = True
        elif medicalappointment.cancellation_date:
            medicalappointment.active = False
        else:
            active_val = request.POST.get('active')
            if active_val == 'False':
                medicalappointment.active = False
            else:
                medicalappointment.active = True
                
        medicalappointment.save()
        messages.success(request, f'Medical appointment "{medicalappointment.id}" actualizado')
        return redirect('medicalappointment')

    doctors = Doctor.objects.all()
    typeappointments = TypeAppointment.objects.all()
    priorities = PriorityAppointment.objects.all()
    patientrecords = PatientRecord.objects.all()
    return render(request, 'citas/medicalappointment_show.html', {
        'medicalappointment': medicalappointment,
        'doctors': doctors,
        'typeappointments': typeappointments,
        'priorities': priorities,
        'patientrecords': patientrecords,
        'editing': True,
    })


@login_required(login_url='login')
def medicalappointments_disable(request, pk):
    medicalappointment = get_object_or_404(MedicalAppointment, pk=pk)
    medicalappointment.soft_delete()
    messages.success(request, f'Medical appointment "{medicalappointment.id}" desactivado')
    return redirect('medicalappointment')


@login_required(login_url='login')
def medicalappointments_delete(request, pk):
    medicalappointment = get_object_or_404(MedicalAppointment, pk=pk)
    medicalappointment.hard_delete()
    messages.success(request, f'Medical appointment "{medicalappointment.id}" borrado')
    return redirect('medicalappointment')


@login_required(login_url='login')
def create_medicalrecord(request):
    if request.method == 'POST':
        medicalrecord = MedicalRecord.objects.create(
            category_id=request.POST.get('category'),
            name=request.POST.get('name'),
            description=request.POST.get('description'),
            id_patient_record_id=request.POST.get('id_patient_record'),
        )
        messages.success(request, f'Medical record "{medicalrecord.name}" creado')
        return redirect('medicalrecords_create')

    categories = CategoryMedicalRecord.objects.all()
    patientrecords = PatientRecord.objects.all()
    return render(request, 'citas/crear_medicalrecord.html', {
        'categories': categories,
        'patientrecords': patientrecords,
    })


@login_required(login_url='login')
def medicalrecord_list(request):
    medicalrecords_list = MedicalRecord.objects.all().order_by('id')
    paginator = Paginator(medicalrecords_list, 10)
    page_number = request.GET.get('page')
    medicalrecords = paginator.get_page(page_number)

    return render(request, 'citas/medicalrecord_list.html', {
        'medicalrecords': medicalrecords,
    })


@login_required(login_url='login')
def medicalrecord_show(request, pk):
    medicalrecord = get_object_or_404(MedicalRecord, pk=pk)
    return render(request, 'citas/medicalrecord_show.html', {
        'medicalrecord': medicalrecord,
        'editing': False,
    })


@login_required(login_url='login')
def medicalrecords_update(request, pk):
    medicalrecord = get_object_or_404(MedicalRecord, pk=pk)
    if request.method == 'POST':
        medicalrecord.category_id = request.POST.get('category')
        medicalrecord.name = request.POST.get('name')
        medicalrecord.description = request.POST.get('description')
        medicalrecord.id_patient_record_id = request.POST.get('id_patient_record')
        medicalrecord.save()
        messages.success(request, f'Medical record "{medicalrecord.name}" actualizado')
        return redirect('medicalrecord')

    categories = CategoryMedicalRecord.objects.all()
    patientrecords = PatientRecord.objects.all()
    return render(request, 'citas/medicalrecord_show.html', {
        'medicalrecord': medicalrecord,
        'categories': categories,
        'patientrecords': patientrecords,
        'editing': True,
    })


@login_required(login_url='login')
def medicalrecords_disable(request, pk):
    medicalrecord = get_object_or_404(MedicalRecord, pk=pk)
    medicalrecord.soft_delete()
    messages.success(request, f'Medical record "{medicalrecord.name}" desactivado')
    return redirect('medicalrecord')


@login_required(login_url='login')
def medicalrecords_delete(request, pk):
    medicalrecord = get_object_or_404(MedicalRecord, pk=pk)
    medicalrecord.hard_delete()
    messages.success(request, f'Medical record "{medicalrecord.name}" borrado')
    return redirect('medicalrecord')


@login_required(login_url='login')
def hello_world(request):
    return HttpResponse("<h1>Hola Mundo<h1>")

@login_required(login_url='login')
def dashboard(request):
    modules = [
        {
            'name': 'Doctores',
            'url': 'doctor',
            'icon': '👨‍⚕️',
            'description': 'Gestión de personal médico'
        },
        {
            'name': 'Pacientes',
            'url': 'patient',
            'icon': '🤒',
            'description': 'Gestión de pacientes'
        },
        {
            'name': 'Citas Médicas',
            'url': 'medicalappointment',
            'icon': '📅',
            'description': 'Control de citas'
        },
        {
            'name': 'Expedientes de Pacientes',
            'url': 'patientrecord',
            'icon': '📂',
            'description': 'Historial clínico por paciente'
        },
        {
            'name': 'Registros Médicos',
            'url': 'medicalrecord',
            'icon': '🩺',
            'description': 'Registros y detalles médicos'
        },
        {
            'name': 'Categorías de Registro',
            'url': 'categorymedicalrecord',
            'icon': '📑',
            'description': 'Categorías para registros'
        },
        {
            'name': 'Tipos de Cita',
            'url': 'typeappointment',
            'icon': '🏷️',
            'description': 'Clasificación de citas'
        },
        {
            'name': 'Prioridades de Cita',
            'url': 'priorityappointment',
            'icon': '⭐',
            'description': 'Niveles de prioridad'
        },
    ]
    return render(request, 'citas/dashboard.html', {'modules': modules})


# ==========================================
# AUTH VIEWS
# ==========================================

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password  = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.error(request, 'Usuario o contraseña incorrectos.')
    return render(request, 'citas/login.html')

def register_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone_number = request.POST.get('phone_number')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')

        if password != password_confirm:
            messages.error(request, 'Las contraseñas no coinciden.')
            return redirect('register')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'El nombre de usuario ya está en uso.')
            return redirect('register')
            
        if User.objects.filter(email=email).exists():
            messages.error(request, 'El correo electrónico ya está en uso.')
            return redirect('register')

        try:
            # Our custom UserManager uses create_user
            user = User.objects.create_user(
                username=username,
                email=email,
                password=password,
                name=name,
                last_name=last_name,
                phone_number=phone_number
            )
            messages.success(request, 'Cuenta creada exitosamente. Inicia sesión para continuar.')
            return redirect('login')
        except Exception as e:
            messages.error(request, f'Ocurrió un error al registrarse: {str(e)}')
            return redirect('register')

    return render(request, 'citas/register.html')

def logout_view(request):
    logout(request)
    return redirect('login')
