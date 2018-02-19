from django import forms
from .models import Expense
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, ButtonHolder, Submit


class ExpenseTableHelper(FormHelper):
    form_method = 'GET'
    layout = Layout(
        'currency',
        'description',
        'type',
        'payment',
        'amount',
        'date',
        Submit('submit', 'Filtrar'),
    )