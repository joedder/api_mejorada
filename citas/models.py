from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.utils import timezone


# =============================================================================
# ABSTRACT: SOFT DELETE
# =============================================================================

class SoftDeleteManager(models.Manager):
    """Manager por defecto: retorna solo registros no eliminados."""

    def get_queryset(self):
        return super().get_queryset().filter(deleted_at__isnull=True)


class SoftDeleteModel(models.Model):
    """
    Clase abstracta que provee funcionalidad de soft delete.
    Todos los modelos que hereden de esta clase soportarán
    eliminación lógica (soft delete) y física (hard delete).
    """
    deleted_at = models.DateTimeField(null=True, blank=True, default=None)

    # Manager por defecto (solo registros activos)
    objects = SoftDeleteManager()
    # Manager que incluye registros eliminados
    all_objects = models.Manager()

    class Meta:
        abstract = True

    def soft_delete(self):
        """Marca el registro como eliminado sin borrarlo de la base de datos."""
        self.deleted_at = timezone.now()
        self.save(update_fields=['deleted_at'])

    def hard_delete(self):
        """Elimina el registro de forma permanente de la base de datos."""
        super().delete()

    def restore(self):
        """Restaura un registro eliminado lógicamente."""
        self.deleted_at = None
        self.save(update_fields=['deleted_at'])

    @property
    def is_deleted(self):
        return self.deleted_at is not None


# =============================================================================
# CUSTOM USER MODEL
# =============================================================================

class UserManager(BaseUserManager):
    """Manager personalizado para el modelo User."""

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError('El campo username es obligatorio.')
        if not email:
            raise ValueError('El campo email es obligatorio.')
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractBaseUser, PermissionsMixin):
    """
    Modelo de usuario personalizado para autenticación del sistema.
    Reemplaza el modelo User por defecto de Django.
    """
    name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=50)
    username = models.CharField(max_length=50, unique=True)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField(max_length=200, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', 'name', 'last_name']

    objects = UserManager()

    class Meta:
        db_table = 'users'
        verbose_name = 'Usuario'
        verbose_name_plural = 'Usuarios'

    def __str__(self):
        return f'{self.name} {self.last_name} (@{self.username})'


# =============================================================================
# CATÁLOGOS
# =============================================================================

class TypeAppointment(SoftDeleteModel):
    """Tipos de cita médica (ej: consulta, seguimiento, urgencia)."""
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'type_appointments'
        verbose_name = 'Tipo de Cita'
        verbose_name_plural = 'Tipos de Cita'

    def __str__(self):
        return self.name


class PriorityAppointment(SoftDeleteModel):
    """Niveles de prioridad para citas médicas (ej: urgente, normal, baja)."""
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'priority_appointments'
        verbose_name = 'Prioridad de Cita'
        verbose_name_plural = 'Prioridades de Cita'

    def __str__(self):
        return self.name


class CategoryMedicalRecord(SoftDeleteModel):
    """Categorías para registros médicos (ej: laboratorio, imágenes, diagnóstico)."""
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)

    class Meta:
        db_table = 'category_medical_records'
        verbose_name = 'Categoría de Expediente'
        verbose_name_plural = 'Categorías de Expediente'

    def __str__(self):
        return self.name


# =============================================================================
# MODELOS PRINCIPALES
# =============================================================================

class Doctor(SoftDeleteModel):
    """Doctor médico registrado en el sistema."""
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50, null=True, blank=True)
    first_lastname = models.CharField(max_length=100)
    second_lastname = models.CharField(max_length=100, null=True, blank=True)
    identity_id = models.CharField(max_length=15, unique=True)
    gender = models.BooleanField()
    phone_number = models.CharField(max_length=15)
    specialty = models.TextField()

    class Meta:
        db_table = 'doctors'
        verbose_name = 'Doctor'
        verbose_name_plural = 'Doctores'

    def __str__(self):
        return f'Dr. {self.first_name} {self.first_lastname}'


class PatientRecord(SoftDeleteModel):
    """
    Expediente clínico del paciente.
    Se crea al registrar al paciente por primera vez.
    Referencia al paciente mediante FK.
    """
    entry_date = models.DateField()
    id_patient = models.ForeignKey(
        'Patient',
        on_delete=models.PROTECT,
        related_name='records',
        db_column='id_patient'
    )

    class Meta:
        db_table = 'patient_records'
        verbose_name = 'Expediente de Paciente'
        verbose_name_plural = 'Expedientes de Paciente'

    def __str__(self):
        return f'Expediente #{self.pk} — Paciente: {self.id_patient}'


class Patient(SoftDeleteModel):
    """
    Paciente registrado en el sistema.

    Nota: id_patient_record es una referencia circular intencional hacia
    PatientRecord. Se define como nullable para permitir la creación del
    paciente antes de su expediente. El flujo correcto es:
      1. Crear Patient (sin id_patient_record)
      2. Crear PatientRecord con FK al Patient
      3. Actualizar Patient.id_patient_record con el registro creado
    """
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50, null=True, blank=True)
    first_lastname = models.CharField(max_length=100)
    second_lastname = models.CharField(max_length=100, null=True, blank=True)
    identity_id = models.CharField(max_length=15, unique=True)
    birth_date = models.DateField()
    gender = models.BooleanField()
    phone_number = models.CharField(max_length=15)
    mobile_number = models.CharField(max_length=15)
    address = models.TextField()
    blood_group = models.CharField(max_length=8)
    name_emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    last_name_emergency_contact = models.CharField(max_length=100, null=True, blank=True)
    phone_number_emergency_contact = models.CharField(max_length=15, null=True, blank=True)
    # Referencia circular intencional — ver docstring
    id_patient_record = models.ForeignKey(
        PatientRecord,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='main_patient',
        db_column='id_patient_record'
    )

    class Meta:
        db_table = 'patients'
        verbose_name = 'Paciente'
        verbose_name_plural = 'Pacientes'

    def __str__(self):
        return f'{self.first_name} {self.first_lastname}'


class MedicalAppointment(SoftDeleteModel):
    """Cita médica programada entre un doctor y un paciente."""
    id_doctor = models.ForeignKey(
        Doctor,
        on_delete=models.PROTECT,
        related_name='appointments',
        db_column='id_doctor'
    )
    appointment_time = models.DateTimeField()
    reason_appointment = models.TextField()
    type_id = models.ForeignKey(
        TypeAppointment,
        on_delete=models.PROTECT,
        related_name='appointments',
        db_column='type_id'
    )
    priority_id = models.ForeignKey(
        PriorityAppointment,
        on_delete=models.PROTECT,
        related_name='appointments',
        db_column='priority_id'
    )
    cancellation_date = models.DateTimeField(null=True, blank=True)
    reason_for_cancellation = models.TextField(null=True, blank=True)
    rescheduled_date = models.DateTimeField(null=True, blank=True)
    patient_record = models.ForeignKey(
        PatientRecord,
        on_delete=models.PROTECT,
        related_name='appointments',
        db_column='patient_record_id'
    )
    patient_comments = models.TextField(null=True, blank=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = 'medical_appointments'
        verbose_name = 'Cita Médica'
        verbose_name_plural = 'Citas Médicas'

    def __str__(self):
        return f'Cita #{self.pk} — Dr. {self.id_doctor} | {self.appointment_time}'


class MedicalRecord(SoftDeleteModel):
    """Registro médico individual vinculado al expediente de un paciente."""
    category = models.ForeignKey(
        CategoryMedicalRecord,
        on_delete=models.PROTECT,
        related_name='medical_records',
        db_column='category_id'
    )
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    id_patient_record = models.ForeignKey(
        PatientRecord,
        on_delete=models.PROTECT,
        related_name='medical_records',
        db_column='id_patient_record'
    )

    class Meta:
        db_table = 'medical_records'
        verbose_name = 'Registro Médico'
        verbose_name_plural = 'Registros Médicos'

    def __str__(self):
        return f'{self.name} — Expediente #{self.id_patient_record_id}'
