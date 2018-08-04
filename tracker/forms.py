from django import forms
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Field, ButtonHolder, Submit
from django.forms import ModelForm
from .models import Expense

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


class DateInput(forms.DateInput):
    input_type = 'date'


class AddExpenseForm(ModelForm):
    class Meta:
        model = Expense
        fields = [
            'date',
            'description',
            'type',
            'payment',
            'amount'
        ]
        widgets = {
            'date': DateInput(),
        }