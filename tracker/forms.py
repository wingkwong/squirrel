from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit


class ExpenseTableHelper(FormHelper):
    date = forms.DateField(
        widget=forms.TextInput(
            attrs={'type': 'date'}
        )
    )
    form_method = 'GET'
    layout = Layout(
        Field('date', placeholder='YYYY-MM-DD'),
        Field('description'),
        Field('type'),
        Field('payment'),
        Field('amount'),
        Submit('submit', 'Filter'),
    )