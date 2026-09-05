from django.contrib.auth.tokens import PasswordResetTokenGenerator


class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
    """
    Token generator for account activation, based on the built-in
    PasswordResetTokenGenerator class.
    """

    def _make_hash_value(self, user, timestamp):
        """
        Include email_confirmed so the token is invalid after activation.
        """
        email_confirmed = getattr(getattr(user, "profile", None), "email_confirmed", False)
        return f"{user.pk}{timestamp}{user.is_active}{email_confirmed}"


account_activation_token = AccountActivationTokenGenerator()
