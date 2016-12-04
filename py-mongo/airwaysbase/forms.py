from django import forms
from datetimewidget.widgets import DateTimeWidget
from .custom_models import Aircraft, Airport


class NewFlightForm(forms.Form):
    source = forms.ChoiceField(label='Source', choices=Airport.get_choices())
    destination = forms.ChoiceField(label='Destination', choices=Airport.get_choices())
    aircraft = forms.ChoiceField(label='Airplane', choices=Aircraft.get_choices())
    start_date = forms.DateTimeField(widget=DateTimeWidget(
        attrs={'id':'start_date'}, usel10n=True, bootstrap_version=3))
    end_date = forms.DateTimeField(widget=DateTimeWidget(
        attrs={'id': 'end_date'}, usel10n=True, bootstrap_version=3))
    cancelled = forms.BooleanField(required=False, label='Cancelled?')
