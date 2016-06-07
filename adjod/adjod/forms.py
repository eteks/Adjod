from django import forms
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.utils.translation import ugettext_lazy, ugettext as _
from adjod.models import UserProfile

class UserProfileForm(forms.ModelForm):
    
    username = forms.RegexField(
        max_length=75, 
        regex=r'^[\w.@+-]+$',
        help_text='Required. 75 characters or fewer. Letters, digits and @/./+/-/_ only.',
    )
    
    password = forms.CharField(widget=forms.PasswordInput())
    
    class Meta:
        model = UserProfile

UserProfile._meta.get_field('username').max_length = 75
UserProfile._meta.get_field('username').validators[0].limit_value = 75
UserProfile._meta.get_field('email')._unique = True
