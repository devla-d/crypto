from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.forms.widgets import NumberInput
from django.contrib.auth import authenticate
from panel.models import Investors,Packages,Notification






class AccountAuthenticationForm(forms.ModelForm):
  
	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Investors
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login make sure your are using a staff account and note both fields are case sensitive")




class PackagesForm(forms.ModelForm):
	

	class Meta:
		model = Packages
		fields = ('name', 'amount','percent')




class NotifyForm(forms.ModelForm):
	

	class Meta:
		model = Notification
		fields = ('user', 'subject','body')
