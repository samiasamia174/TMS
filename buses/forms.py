
from django import forms
from .models import Bus

class BusRegistrationForm(forms.ModelForm):
    class Meta:
        model = Bus
        fields = ['bus_number', 'bus_name', 'capacity']
        
    def clean_bus_number(self):
        bus_number = self.cleaned_data.get('bus_number')
        if Bus.objects.filter(bus_number=bus_number).exists():
            raise forms.ValidationError('A bus with this number already exists.')
        return bus_number

class BusEditForm(BusRegistrationForm):
    class Meta(BusRegistrationForm.Meta):
        pass
