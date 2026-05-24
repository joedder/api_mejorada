import re
import os

filepath = r'd:\laragon\www\api_mejorada\citas\views.py'
with open(filepath, 'r', encoding='utf-8') as f:
    content = f.read()

# Make sure imports are there
if 'from django.contrib.auth.decorators import login_required' not in content:
    content = content.replace('from django.http import HttpResponse', 'from django.http import HttpResponse\nfrom django.contrib.auth.decorators import login_required\nfrom django.contrib.auth import authenticate, login, logout\nfrom .models import User')

# Regex to find all def functions and add @login_required above them
# But not if it already has it.
def add_decorator(match):
    full_match = match.group(0)
    if '@login_required' in full_match:
        return full_match
    # Check the lines right before def
    lines = content[:match.start()].split('\n')
    if lines and '@login_required' in lines[-1] or (len(lines) > 1 and '@login_required' in lines[-2]):
        return full_match
    
    return f'@login_required(login_url=\'login\')\n{full_match}'

# Be careful not to decorate auth views if they already existed, but they don't yet.
new_content = re.sub(r'^def [a-zA-Z0-9_]+\(', add_decorator, content, flags=re.MULTILINE)

with open(filepath, 'w', encoding='utf-8') as f:
    f.write(new_content)
