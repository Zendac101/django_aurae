from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.messages import get_messages
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth import get_user_model
from django.db import transaction
from django.contrib.auth.hashers import make_password
from django.urls import reverse
from django.views.decorators.csrf import ensure_csrf_cookie
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm

from .tokens import account_activation_token
# Import your specific database schema models here
from .models import ActivityHistory, UserProfile


@ensure_csrf_cookie
def LogRes(request):
    storage = get_messages(request)
    for _ in storage:
        pass

    if request.method == 'POST':
        # 1. Registration Branch
        if 'register_submit' in request.POST:
            form = RegisterForm(request.POST)
            if form.is_valid():
                try:
                    with transaction.atomic():
                        user = form.save(commit=False)
                        user.is_active = False
                        user.save()

                        UserProfile.objects.create(
                            user=user, is_verified=False)
                        ActivityHistory.objects.create(
                            user=user, activity_log="Account initialized via registration."
                        )

                        uid = urlsafe_base64_encode(force_bytes(user.pk))
                        token = account_activation_token.make_token(user)
                        activation_url = request.build_absolute_uri(
                            reverse('activate', kwargs={
                                    'uidb64': uid, 'token': token})
                        )

                        send_mail(
                            subject="Activate Your Account",
                            message=f"Hello {user.username},\n\nPlease click the link to verify your account:\n{activation_url}",
                            from_email=None,
                            recipient_list=[user.email],
                            fail_silently=False,
                        )

                    messages.success(
                        request, "Account created! Please check your email to verify.")
                    return render(request, 'index.html', {'form': form, 'active_form': 'login_form'})

                except Exception as e:
                    messages.error(request, f"Database saving error: {str(e)}")
                    return render(request, 'index.html', {'form': form, 'active_form': 'signUp_form'})
            else:
                return render(request, 'index.html', {'form': form, 'active_form': 'signUp_form'})

        # 2. Login Branch
        elif 'login_submit' in request.POST:
            login_identifier = request.POST.get('email', '').strip()
            password = request.POST.get('password', '')

            user_obj = User.objects.filter(email__iexact=login_identifier).first() or \
                User.objects.filter(username__iexact=login_identifier).first()

            if user_obj:
                if not user_obj.is_active:
                    messages.error(
                        request, "Your account is not verified yet. Please check your email.")
                    return render(request, 'index.html', {'form': RegisterForm(), 'active_form': 'login_form'})

                user = authenticate(
                    request, username=user_obj.username, password=password)
            else:
                user = None

            if user is not None:
                login(request, user)
                if user.is_superuser or user.is_staff:
                    return redirect('/admin_dashboard/home')
                return redirect('/client_dashboard/home')
            else:
                messages.error(request, "Invalid username/email or password.")
                return render(request, 'index.html', {'form': RegisterForm(), 'active_form': 'login_form'})

    form = RegisterForm()
    return render(request, 'index.html', {'form': form, 'active_form': 'logIn_form'})


def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        # Update profile verification flag using the correct related_name
        if hasattr(user, 'profile'):
            user.profile.is_verified = True
            user.profile.save()

        messages.success(
            request, "Your email has been verified! You can now log in."
        )
        return redirect('registerUser')
    else:
        messages.error(
            request, "The activation link is invalid or has expired."
        )
        return redirect('registerUser')
