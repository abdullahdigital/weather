from django import forms

class WeatherAlertForm(forms.Form):
    city = forms.CharField(label='Enter city name', max_length=100)
