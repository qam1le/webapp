from django.contrib.auth.forms import PasswordResetForm, SetPasswordForm
from django.contrib.auth import get_user_model

#class PasswordResetForm(PasswordResetForm):
#    def __init__(self, *args, **kwargs):
#        super(PasswordResetForm, self).__init__(*args, **kwargs)

class SetPasswordForm(SetPasswordForm):
    class Meta:
        model = get_user_model()
        fields = ['new_password1', 'new_password2']