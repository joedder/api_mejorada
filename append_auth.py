
auth_views = """

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
"""

filepath = r'd:\laragon\www\api_mejorada\citas\views.py'
with open(filepath, 'a', encoding='utf-8') as f:
    f.write(auth_views)
