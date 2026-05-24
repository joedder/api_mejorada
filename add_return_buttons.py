import os
import glob
import re

mapping = {
    'doctor': ['crear_doctor.html', 'doctor_show.html'],
    'patient': ['crear_patient.html', 'patient_show.html'],
    'patientrecord': ['crear_patientrecord.html', 'patientrecord_show.html'],
    'medicalappointment': ['crear_medicalappointment.html', 'medicalappointment_show.html'],
    'medicalrecord': ['crear_medicalrecord.html', 'medicalrecord_show.html'],
    'categorymedicalrecord': ['crear_categorymedicalrecord.html', 'categorymedicalrecord_show.html'],
    'typeappointment': ['crear_typeappointment.html', 'typeappointment_show.html'],
    'priorityappointment': ['crear_priorityappointment.html', 'priorityappointment_show.html'],
}

def process_file(filepath, return_url):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Pattern for list files with a primary button
    # <section class="page-heading">
    #     <h1>Title</h1>
    #     <a class="button button-primary" href="...">...</a>
    # </section>
    pattern_list = re.compile(r'(<section class="page-heading">\s*)<h1>(.*?)</h1>(\s*<a .*?>.*?</a>\s*</section>)', re.DOTALL)
    
    # Pattern for show/create files without a primary button
    # <section class="page-heading">
    #     <h1>Title</h1>
    # </section>
    pattern_show = re.compile(r'(<section class="page-heading">\s*)<h1>(.*?)</h1>(\s*</section>)', re.DOTALL)
    
    # Check if we already replaced it to avoid double replacements
    if '⬅ Volver' in content:
        print(f"Skipping {filepath}, already has Volver button")
        return

    replacement = r'\1<div style="display: flex; align-items: center; gap: 15px;">\n        <a href="{% url \'' + return_url + r'\' %}" class="button button-secondary" title="Volver">⬅ Volver</a>\n        <h1 style="margin: 0;">\2</h1>\n    </div>\3'
    
    new_content = pattern_list.sub(replacement, content)
    if new_content == content:
        new_content = pattern_show.sub(replacement, content)

    if new_content != content:
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filepath} with return_url={return_url}")
    else:
        print(f"Could not match pattern in {filepath}")

def main():
    path = r'd:\laragon\www\api_mejorada\citas\templates\citas\*.html'
    for filepath in glob.glob(path):
        filename = os.path.basename(filepath)
        
        # Determine return_url
        if filename.endswith('_list.html'):
            process_file(filepath, 'dashboard')
        else:
            for module, files in mapping.items():
                if filename in files:
                    process_file(filepath, module)
                    break

if __name__ == '__main__':
    main()
