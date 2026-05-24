import os
import glob

replacements = {
    ">Create Doctor<": ">Crear Doctor<",
    ">Create Patient<": ">Crear Paciente<",
    ">Create Patient Record<": ">Crear Expediente<",
    ">Create Medical Appointment<": ">Crear Cita Médica<",
    ">Create Medical Record<": ">Crear Registro Médico<",
    ">Create Type Appointment<": ">Crear Tipo de Cita<",
    ">Create Priority Appointment<": ">Crear Prioridad de Cita<",
    ">Create Category Medical Record<": ">Crear Categoría de Registro<",
    
    ">Update<": ">Actualizar<",
    ">Disable<": ">Desactivar<",
    ">Delete<": ">Eliminar<",
    ">Show<": ">Mostrar<",
    ">Edit<": ">Editar<",
    ">Back<": ">Volver<",
    ">Save<": ">Guardar<",
    ">Cancel<": ">Cancelar<",
    ">First<": ">Primera<",
    ">Previous<": ">Anterior<",
    ">Next<": ">Siguiente<",
    ">Last<": ">Última<",
    
    ">Doctors<": ">Doctores<",
    ">Patients<": ">Pacientes<",
    ">Patient Records<": ">Expedientes de Pacientes<",
    ">Medical Appointments<": ">Citas Médicas<",
    ">Medical Records<": ">Registros Médicos<",
    ">Type Appointments<": ">Tipos de Citas<",
    ">Priority Appointments<": ">Prioridades de Citas<",
    ">Category Medical Records<": ">Categorías de Registros<",

    "Doctor Index": "Índice de Doctores",
    "Patient Index": "Índice de Pacientes",
    "Patient Record Detail": "Detalle de Expediente",
    "Medical Appointment Detail": "Detalle de Cita Médica",
    "Medical Record Detail": "Detalle de Registro Médico",
    "Type Appointment Detail": "Detalle de Tipo de Cita",
    "Priority Appointment Detail": "Detalle de Prioridad de Cita",
    "Category Medical Record Detail": "Detalle de Categoría de Registro",
    
    "No doctors registered": "No hay doctores registrados",
    "No patients registered": "No hay pacientes registrados",
    "No patient records registered": "No hay expedientes registrados",
    "No medical appointments registered": "No hay citas médicas registradas",
    "No medical records registered": "No hay registros médicos registrados",
    "No type appointments registered": "No hay tipos de citas registrados",
    "No priority appointments registered": "No hay prioridades de citas registradas",
    "No category medical records registered": "No hay categorías registradas",

    "Second Name:": "Segundo Nombre:",
    "Second Last Name:": "Segundo Apellido:",
    "First Name:": "Primer Nombre:",
    "First Last Name:": "Primer Apellido:",
    ">Second Name</label>": ">Segundo Nombre</label>",
    ">Second Last Name</label>": ">Segundo Apellido</label>",
    ">First Name</label>": ">Primer Nombre</label>",
    ">First Last Name</label>": ">Primer Apellido</label>",
    
    "Identity ID:": "Cédula/ID:",
    ">Identity ID</label>": ">Cédula/ID</label>",
    "Gender:": "Género:",
    ">Gender</label>": ">Género</label>",
    "Phone Number:": "Número de Teléfono:",
    ">Phone Number</label>": ">Número de Teléfono</label>",
    "Mobile Number:": "Número Celular:",
    ">Mobile Number</label>": ">Número Celular</label>",
    "Specialty:": "Especialidad:",
    ">Specialty</label>": ">Especialidad</label>",
    "Birth Date:": "Fecha de Nacimiento:",
    ">Birth Date</label>": ">Fecha de Nacimiento</label>",
    "Address:": "Dirección:",
    ">Address</label>": ">Dirección</label>",
    "Blood Group:": "Grupo Sanguíneo:",
    ">Blood Group</label>": ">Grupo Sanguíneo</label>",
    "Name Emergency Contact:": "Nombre Contacto Emergencia:",
    ">Name Emergency Contact</label>": ">Nombre Contacto Emergencia</label>",
    "Last Name Emergency Contact:": "Apellido Contacto Emergencia:",
    ">Last Name Emergency Contact</label>": ">Apellido Contacto Emergencia</label>",
    "Phone Number Emergency Contact:": "Teléfono Contacto Emergencia:",
    ">Phone Number Emergency Contact</label>": ">Teléfono Contacto Emergencia</label>",
    
    "yesno:\"Male,Female\"": "yesno:\"Masculino,Femenino\"",
    ">Male<": ">Masculino<",
    ">Female<": ">Femenino<",
    
    "Entry Date:": "Fecha de Ingreso:",
    ">Entry Date</label>": ">Fecha de Ingreso</label>",
    "Patient:": "Paciente:",
    ">Patient</label>": ">Paciente</label>",
    
    "Appointment Time:": "Hora de Cita:",
    ">Appointment Time</label>": ">Hora de Cita</label>",
    "Reason Appointment:": "Motivo de Cita:",
    ">Reason Appointment</label>": ">Motivo de Cita</label>",
    "Type ID:": "Tipo:",
    ">Type ID</label>": ">Tipo</label>",
    "Priority ID:": "Prioridad:",
    ">Priority ID</label>": ">Prioridad</label>",
    "Cancellation Date:": "Fecha de Cancelación:",
    ">Cancellation Date</label>": ">Fecha de Cancelación</label>",
    "Reason For Cancellation:": "Motivo de Cancelación:",
    ">Reason For Cancellation</label>": ">Motivo de Cancelación</label>",
    "Rescheduled Date:": "Fecha Reprogramada:",
    ">Rescheduled Date</label>": ">Fecha Reprogramada</label>",
    "Patient Comments:": "Comentarios del Paciente:",
    ">Patient Comments</label>": ">Comentarios del Paciente</label>",
    "Active:": "Activo:",
    ">Active</label>": ">Activo</label>",
    
    "Category:": "Categoría:",
    ">Category</label>": ">Categoría</label>",
    "Name:": "Nombre:",
    ">Name</label>": ">Nombre</label>",
    "Description:": "Descripción:",
    ">Description</label>": ">Descripción</label>",
    "ID Patient Record:": "ID Expediente de Paciente:",
    ">ID Patient Record</label>": ">ID Expediente de Paciente</label>",

    "Doctor App": "Aplicación de Doctores",
    
    "General Information": "Información General",
    "No medical records associated.": "No hay registros médicos asociados.",
    "No medical appointments associated.": "No hay citas médicas asociadas.",
    "Cancelled": "Cancelada",
    "Priority:": "Prioridad:",
    "Reason:": "Motivo:",

    "<span>Page ": "<span>Página ",
    " of ": " de "
}

def translate():
    path = r'd:\laragon\www\api_mejorada\citas\templates\citas\*.html'
    for filepath in glob.glob(path):
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        for k, v in replacements.items():
            content = content.replace(k, v)
            
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)

if __name__ == '__main__':
    translate()
