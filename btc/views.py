from django.shortcuts import render,redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from django.contrib import  messages
from panel.models import Investors,Deposite,Withdraw,Transaction,RefferalProfile,Packages,Investment,Notification,Message
from .forms import InvestorAuthenticationForm,RegistrationForm,DepositeForm,AccountsetupForm
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string  
from django.core.mail import EmailMessage
from .tokens import TokenGenerator
import uuid
import random
import string
from datetime import datetime, timedelta,date
from django.contrib.auth.decorators import login_required

def dashboard(request,*args, **kwargs):
	code = str(kwargs.get('ref_code'))
	try:
		profile = Investors.objects.get(ref_code=code)
		request.session['ref_profile'] = profile.id
		print(profile.ref_code)
	except:
		pass
	print(request.session.get_expiry_date())
	if request.method == 'POST':
		email = request.POST['email']
		subject = request.POST['subject']
		body = request.POST['body']
		Message.objects.create(email=email,subject=subject,body=body)
		messages.success(request, f'your message has been sent we wil get back to you as soon as possible ')
		return redirect("user-dashboard")
	return render(request, 'user-dashboard.html')




	

@login_required
def account(request):
	user = request.user
	context ={}
	try:
		context['investment']=Investment.objects.get(user=user)
	except:
		context['investment']= None
	return render(request, 'userstemplate/index.html',context)

@login_required
def notification(request):
	user = request.user
	context ={}
	try:
		context['notifications']=Notification.objects.filter(user=user)
	except:
		context['notifications']= None
	return render(request, 'userstemplate/notification.html',context)


def rand_code():
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))

@login_required
def deposite(request):
	if request.method == 'POST':
		user =request.user
		form = DepositeForm(request.POST)
		if form.is_valid:
			dp = form.save(commit=False)
			dp.status = "pending"
			dp.Investor = user
			dp.save()
			bal = form.cleaned_data["amount"]
			Transaction.objects.create(
			user=user,
			amount=bal,
			status = "pending",
			service = "deposite"
			)
			messages.success(request, f'your deposite of {bal} is been processed you will be credited once it has been approved')
			return redirect("deposite")
	else:
		form = DepositeForm()
	return render(request, 'userstemplate/deposite.html',{"form":form})


@login_required
def withdraw(request):
	if request.method == "POST":
		user = request.user
		try:
			invest = Investment.objects.get(user=user)
		except:
			invest = None
		amount = float(request.POST['amount'])
		if invest is not None :
			ba = invest.total_earnings()
			if invest.is_past_due == False:
				messages.success(request, f'You have not reach your withdraw limit')
				return redirect("withdraw")
			if amount > ba :
				messages.success(request, f'you dont have enough balance to withdraw')
				return redirect("withdraw")
			Withdraw.objects.create(
				user = user,
				status = "pending",
				amount= amount
			)
			invest.withdraw = True
			invest.save()
			invest.delete()
			Transaction.objects.create(
				user=user,
				amount=amount,
				status = "pending",
				service = "withdraw"
			)
			messages.success(request, f'your withdraw of ${amount} is been processed you will be credited once it has been approved Note: Your package Has Ended ')
			return redirect("withdraw")
		messages.success(request, f'you did not purchase any package  or it has ended')
		return redirect("withdraw")
	return render(request, 'userstemplate/withdraw.html')




@login_required
def tranfer_log(request):
	user = request.user
	context = {
		'withdraws':Withdraw.objects.filter(user=user),
		'deposites':Deposite.objects.filter(Investor=user),
	}
	return render(request, 'userstemplate/tranferlog.html',context)










@login_required
def account_refferal(request):
	user = request.user
	ref = RefferalProfile.objects.get(user=user)
	my_recs = ref.recom_profies()
	return render(request, 'userstemplate/refferal.html',{"my_recs":my_recs})



def get_deadline():
	return datetime.today() + timedelta(days=7)

"""def get_withdraw():
	return datetime.today() + timedelta(days=7)"""


@login_required
def package(request):
	if request.method == 'POST':
		user =request.user
		amount = float(request.POST['amount'])
		name = request.POST['name']
		pack = Packages.objects.get(name=name,amount=amount)
		try:
			invest = Investment.objects.get(user=user)
		except:
			invest = None
		if invest is not None:
			if invest.is_past_due == True:
				messages.success(request, f'you packag is completed you can now request a withdraw before you purchase another package')
				return redirect("packages")
		elif amount > user.balance:
			messages.success(request, f'Insuufficent funds to purchase package')
			return redirect("packages")
		elif invest is not None:
			messages.success(request, f'you are already runing this package purchase package')
			return redirect("packages")
		elif invest is None:
			Investment.objects.create(user=user,pack=pack,end_date=get_deadline(), status='Active')
			user.balance -= amount
			user.save()
			messages.success(request, f'Your purchase is succesful  thanks ')
			return redirect("packages")
		messages.success(request, f'Your currently running an active package  ')
		return redirect("packages")
	context = {
		"packages": Packages.objects.all(),
	}
	return render(request, 'userstemplate/package.html',context)







@login_required
def my_package(request):
	user = request.user
	context ={}
	try:
		context['investment']=Investment.objects.get(user=user)
	except:
		context['investment']= None
	return render(request, 'userstemplate/mypack.html',context)



def account_setup(request):
	if request.method == 'POST':
		form = AccountsetupForm(request.POST,
                                   request.FILES,
                                   instance=request.user)
		if form.is_valid():
			form.save()
			messages.success(request, f'Account updated ')
			return redirect("account-setup")
	else:
		form = AccountsetupForm(instance=request.user)
	return render(request, 'userstemplate/accsetup.html',{"form":form})
























def registration_view(request):
	user = request.user
	if user.is_authenticated: 
		return redirect("user-dashboard")
	profile_id = request.session.get('ref_profile')
	if request.POST:
		form = RegistrationForm(request.POST)
		if form.is_valid():
			if profile_id is not None:
				recom_by_profile = Investors.objects.get(id=profile_id)
				instance=form.save()
				recom_by_profile.refferal += 1
				recom_by_profile.save()
				registered_user = Investors.objects.get(id=instance.id)
				registered_ref_by = RefferalProfile.objects.get(user =registered_user )
				registered_ref_by.recommended_by = recom_by_profile
				registered_ref_by.save()
				messages.success(request, f'Account created !')
				return redirect('login')
			else:
				form.save()
				messages.success(request, f'Account created')
				return redirect("login") 
	else:
		form = RegistrationForm()
	return render(request, 'register.html', {"form":form})



def activate(request, uidb64, token):  
	try:  
		uid = force_text(urlsafe_base64_decode(uidb64))  
		user = Investors.objects.get(id=uid)  
	except(TypeError, ValueError, OverflowError, Investors.DoesNotExist):  
		user = None  
	if user is not None and account_activation_token.check_token(user, token):  
		user.is_active = True  
		user.save()
		messages.success(request, f'Thank you for your email confirmation. Now you can login your account')
		return redirect("login") 
	else:  
		messages.success(request, f'Thank you for your email confirmation. Now you can login your account')


def email_temp(request):
	return render(request, 'activate.html')

def user_logout_view(request):
	logout(request)
	return redirect('user-dashboard')




def login_view(request):
	user = request.user
	if user.is_authenticated:
		return redirect("user-dashboard")

	if request.POST:
		form = InvestorAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				login(request, user)
				if user.is_admin:
					return redirect("dashboard")
				return redirect("account")

	else:
		form = InvestorAuthenticationForm()
	return render(request, "login.html", {"form":form})
