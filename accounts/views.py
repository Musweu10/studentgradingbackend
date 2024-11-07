from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages  # Import messages
from .forms import TeacherRegistrationForm, LoginForm

# Define a mapping of user roles to dashboard URLs
ROLE_DASHBOARD_MAP = {
    'teacher': 'teacher:teacher_dashboard',
    'admin': 'admin:index',  # Assuming Django's admin dashboard
}


def teacher_register(request):
    if request.method == 'POST':
        form = TeacherRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.role = 'teacher'
            user.set_password(form.cleaned_data['password'])
            user.save()
            messages.success(
                request, 'Teacher registered successfully! Please Login')
            return redirect('accounts:login')
        else:
            messages.error(
                request, 'Registration failed. Please correct the errors below.')
    else:
        form = TeacherRegistrationForm()
    return render(request, 'accounts/teacher_register.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user = authenticate(request, email=email, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome {
                                 user.first_name} {user.last_name}!')

                if user.role == 'student':
                    return redirect('core:index')
                else:

                    # Get the dashboard URL based on the user's role
                    dashboard_url = ROLE_DASHBOARD_MAP.get(
                        user.role, 'student:student_dashboard')

                    # Redirect to the appropriate dashboard
                    return redirect(dashboard_url)
            else:
                messages.error(request, 'Invalid email or password.')
        else:
            messages.error(request, 'Please correct the errors below.')
    else:
        form = LoginForm()

    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    logout(request)
    messages.success(request, 'You have been logged out successfully.')
    return redirect('accounts:login')
