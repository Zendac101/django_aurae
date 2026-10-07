from django.contrib.auth.signals import user_logged_in
from django.dispatch import receiver
from django.contrib.sessions.models import Session
from .models import UserSession


@receiver(user_logged_in)
def remove_other_sessions(sender, user, request, **kwargs):

    # generate session key
    if not request.session.session_key:
        request.session.create()

    current_session_key = request.session.session_key

    try:
        #  check if it has saved session
        user_session = UserSession.objects.get(user=user)

        # deklete old session key
        if user_session.session_key != current_session_key:
            Session.objects.filter(
                session_key=user_session.session_key).delete()

        # update the session tot he new one
        user_session.session_key = current_session_key
        user_session.save()

    except UserSession.DoesNotExist:
        # create new session
        UserSession.objects.create(user=user, session_key=current_session_key)
