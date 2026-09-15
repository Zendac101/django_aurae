from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        return (
            str(user.pk) + str(timestamp) + str(user.is_active)
        )


class AuraePasswordResetTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, user, timestamp):
        # Invalidates token immediately once the password or last_login changes
        login_timestamp = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        return (
            str(user.pk)
            + user.password
            + str(login_timestamp)
            + str(timestamp)
        )


class SafePasswordResetTokenGenerator(PasswordResetTokenGenerator):

    def _make_hash_value(self, user, timestamp):
        # Base the token strictly on ID, current password, and timestamp
        login_ts = (
            ""
            if user.last_login is None
            else user.last_login.replace(microsecond=0, tzinfo=None)
        )
        return str(user.pk) + user.password + str(login_ts) + str(timestamp)


account_activation_token = AccountActivationTokenGenerator()
password_reset_token = SafePasswordResetTokenGenerator()
