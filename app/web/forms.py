from django import forms
from core.models import User, Rule


class RuleForm(forms.Form):

    url = forms.CharField(
        max_length=2048,
        min_length=1,
        label='Ссылка',
        )

    short_url = forms.CharField(
        max_length=32,
        min_length=1,
        label='Сокращение',
        required=False,
        )
