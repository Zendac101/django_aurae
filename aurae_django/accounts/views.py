from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.messages import get_messages
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm
# Import your specific database schema models here
from .models import ActivityHistory, UserProfile


@ensure_csrf_cookie
def LogRes(request):
    # get message
    storage = get_messages(request)
    for _ in storage:
        pass

    if request.method == 'POST':
        # Registration
        if 'register_submit' in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                try:
                    # Execute all table writes together; if one fails, none are saved
                    with transaction.atomic():
                        # Save base Django auth User object
                        user = form.save()

                        # userprofile
                        UserProfile.objects.create(
                            user=user, is_verified=True
                        )

                        # Activity History Table
                        ActivityHistory.objects.create(
                            user=user, activity_log="Account initialized via registration.")

                        messages.success(
                            request, "Account created successfully! Please log in.")
                    return redirect('registerUser')

                except Exception as e:
                    # catch errors
                    messages.error(request, f"Database saving error: {str(e)}")
                    return render(request, 'index.html', {'form': form, 'active_form': 'signUp_form'})
            else:

                return render(request, 'index.html', {'form': form, 'active_form': 'signUp_form'})

        # login
        elif 'login_submit' in request.POST:
            login_identifier = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')

            # Find matching user
            user_obj = User.objects.filter(email__iexact=login_identifier).first() or \
                User.objects.filter(username__iexact=login_identifier).first()

            if user_obj:
                user = authenticate(
                    request, username=user_obj.username, password=password)
            else:
                user = None

            if user is not None:
                login(request, user)
                if user.is_superuser == True or user.is_staff == True:
                    return redirect('/admin_dashboard/home')
                else:
                    return redirect('/client_dashboard/home')
            else:

                messages.error(request, "Invalid username/email or password.")
                return render(request, 'index.html', {'form': RegisterForm(), 'active_form': 'logIn_form'})

    # GET request
    form = RegisterForm()
    return render(request, 'index.html', {'form': form, 'active_form': 'logIn_form'})
