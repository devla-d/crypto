from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from panel.models import Investors,Deposite



class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=254)

    class Meta:
        model = Investors
        fields = ("full_name",'username','email',"phone" ,'password1', 'password2', )




class InvestorAuthenticationForm(forms.ModelForm):

	password = forms.CharField(label='Password', widget=forms.PasswordInput)

	class Meta:
		model = Investors
		fields = ('email', 'password')

	def clean(self):
		if self.is_valid():
			email = self.cleaned_data['email']
			password = self.cleaned_data['password']
			if not authenticate(email=email, password=password):
				raise forms.ValidationError("Invalid login")



class DepositeForm(forms.ModelForm):
	trans_id = forms.CharField(label="Transaction id",
                    widget=forms.TextInput(attrs={'placeholder': 'paste the transfered bitcoin transaction id '}))

	class Meta:
		model = Deposite
		fields = ["amount","trans_id"]


class AccountsetupForm(forms.ModelForm):
	
	class Meta:
		model = Investors
		fields =  ("full_name",'username','email',"phone" ,'wallet_id',"profile_image" )


