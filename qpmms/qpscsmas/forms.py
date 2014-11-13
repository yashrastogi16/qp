from .models import *
from django import forms
from django.core.validators import validate_email

class associative_companyForm(forms.ModelForm):
	class Meta:
		model = associative_company
		fields = '__all__'
class QpadminForm(forms.ModelForm):
	class Meta:
		model = Qpadmin
		fields = '__all__'
class employee_detailsForm(forms.ModelForm):
	class Meta:
		model = employee_details
		fields = '__all__'
class meal_timingForm(forms.ModelForm):
	class Meta:
		model = meal_timing
		fields = '__all__'
class device_infoForm(forms.ModelForm):
	class Meta:
		model = device_info
		fields = '__all__'
		