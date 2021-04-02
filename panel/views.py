from django.shortcuts import render, redirect,get_object_or_404
from django.contrib.auth import login, authenticate, logout
from panel.forms import  AccountAuthenticationForm,PackagesForm,NotifyForm
from django.template import RequestContext
from django.contrib import messages
#from .decorators import
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
	ListView,
	DetailView,
	CreateView,
	UpdateView,
	DeleteView
)
from .decorators import manager_required
from .models import Investors,Deposite,Transaction,Packages,Withdraw,Message,Notification
from django.http import JsonResponse
import json
import random
import json
import uuid
# Create your views here.

@manager_required
def dashboard(request):
	context = {
	"deposite":  Deposite.objects.all().count(),
	"investor":  Investors.objects.all().count(),
	"transaction":  Transaction.objects.all().count(),
	"withdraw":  Withdraw.objects.all().count()
	}
	return render(request, "admin/dashboard.html", context)


@manager_required
def users(request):
	context = {

	"investor":  Investors.objects.all()
	
	}
	return render(request, "admin/users.html", context)


def message(request):
	context = {

	"messages":  Message.objects.all()
	
	}
	return render(request, "admin/message.html", context)


def notify_user(request):
	if request.method == 'POST':
		form = NotifyForm(request.POST)
		if form.is_valid:
			form.save()
			return redirect('message')
			messages.danger(request, "Notification has been sent")
	else:
		form = NotifyForm()
	return render(request, "admin/notify.html", {"form":form})



@manager_required
def users_detail(request, ref_code):
	account = Investors.objects.get(ref_code=ref_code)
	withdraw = Withdraw.objects.filter(user=account)
	deposites = Deposite.objects.filter(Investor=account)
	context = {
		"account":account,
	"withdraws": withdraw,
	"deposites": deposites
	}
	return render(request, "admin/user-detail.html",context)




def disable_profile(request):
	data =  json.loads(request.body)
	context = {}
	ref_code =  data['form']['ref_code']
	account = get_object_or_404(Investors, ref_code=ref_code)
	if account.is_active == True:
		account.is_active = False
		account.save()
		context["user"] = ' Account been deactivated'
	else:
		context['user'] = "Account was already Deactivated"
	return JsonResponse(context)

	


def enable_profile(request):
	data =  json.loads(request.body)
	context = {}
	ref_code_e =  data['form']['ref_code_e']
	account = get_object_or_404(Investors, ref_code=ref_code_e)
	if account.is_active == False:
		account.is_active = True
		account.save()
		context["user"] = 'Account is activated'
	else:
		context['user'] = "User is active"
	return JsonResponse(context)




def add_funds(request):
	context = {}
	ref_code_e = request.POST['ref']
	bal = float(request.POST['amount'])
	account = get_object_or_404(Investors, ref_code=ref_code_e)
	account.balance += bal
	account.save()
	body = f"You have been credited with ${bal}"
	Notification.objects.create(user=account, subject='credited',body=body)
	context["user"] = f"{account.username} has been credited with ${bal}"
	return JsonResponse(context)




def deduct_funds(request):
	context = {}
	ref_code_e = request.POST['reffer']
	bal = float(request.POST['amountbal'])
	account = get_object_or_404(Investors, ref_code=ref_code_e)
	if account.balance <= bal:
		context["user"] = f" {account.username} don't have enough funds to deduct from"
	else:
		account.balance -= bal
		account.save()
		body = f"${bal} has been deducted from your balance"
		Notification.objects.create(user=account, subject='Debited',body=body)
		context["user"] = f" ${bal} has been deducted from {account.username}"
	return JsonResponse(context)





@manager_required
def withdrws(request):
	withdraw = Withdraw.objects.all()
	return render(request, "admin/withdraw.html",{"withdraw":withdraw})



@manager_required
def withdrws_deteail(request, pk):
	withdraw = get_object_or_404(Withdraw, pk=pk)
	return render(request, "admin/withdraw-detail.html",{"withdraw":withdraw})




@manager_required
def transaction(request):
	transactions = Transaction.objects.all()
	return render(request, "admin/transactions.html",{"transactions":transactions})



@manager_required
def deposite_deteail(request, pk):
	deposite = get_object_or_404(Deposite, pk=pk)
	return render(request, "admin/transaction-detail.html",{"obj":deposite})

@manager_required
def deposite(request):
	investments = Deposite.objects.all()
	return render(request, "admin/investment.html",{"investments":investments})



@manager_required
def package(request):
	packages = Packages.objects.all()
	return render(request, "admin/packages.html",{"packages":packages})






def pay_users(request):
	context = {}
	ref_code_e = request.POST['ref_code_with']
	date = request.POST['date']
	#bal = float(request.POST['amountbalance'])
	account = get_object_or_404(Investors, ref_code=ref_code_e,)
	wi  = get_object_or_404(Withdraw, user=account,pk=date)
	wi.status = "sucessfull"
	bal = wi.amount
	wi.save()
	body = f"withdrawal of ${bal} has been completed"
	Notification.objects.create(user=account, subject='credited',body=body)
	context["user"] = f" {account.username} withdrawal of ${bal} has been completed"
	return JsonResponse(context)




def decline_pay_users(request):
	context = {}
	ref_code_dd = request.POST['ref_code_dd']
	pk = request.POST['pk']
	#bal = float(request.POST['amountbalance'])
	account = get_object_or_404(Investors, ref_code=ref_code_dd,)
	wi  = get_object_or_404(Withdraw, user=account,pk=pk)
	wi.status = "declined"
	wi.save()
	bal = wi.amount
	account.balance += bal
	account.save()
	body = f"Your withdraw of ${bal} has been declined"
	Notification.objects.create(user=account, subject='credited',body=body)
	context["user"] = f" {account.username} withdrawal of ${bal} has been declined"
	return JsonResponse(context)






def accept_deposite(request):
	context = {}
	ref_code_depo = request.POST['ref_code_depo']
	pk = request.POST['pkdepo']
	account = get_object_or_404(Investors, ref_code=ref_code_depo)
	dp  = get_object_or_404(Deposite, Investor=account,pk=pk)
	dp.status = "completed"
	bal = dp.amount
	dp.save()
	account.balance += bal
	account.save()
	body = f"You Deposit of ${bal} has been accepted"
	Notification.objects.create(user=account, subject='credited',body=body)
	context["user"] = f" {account.username} deposite of ${bal} has been completed"
	return JsonResponse(context)



def decline_deposite(request):
	context = {}
	ref_code_depo = request.POST['ref_code_depo']
	pk = request.POST['pkdepo']
	account = get_object_or_404(Investors, ref_code=ref_code_depo)
	dp  = get_object_or_404(Deposite, Investor=account,pk=pk)
	dp.status = "decline"
	bal = dp.amount
	dp.save()
	body = f"deposite of ${bal} has been declined"
	Notification.objects.create(user=account, subject='credited',body=body)
	context["user"] = f" {account.username} deposite of ${bal} has been declined"
	return JsonResponse(context)





@manager_required
def new_package(request):
	if request.method == 'POST':
		form = PackagesForm(request.POST)
		if form.is_valid:
			form.save()
			return redirect('admin-package')
			messages.danger(request, "Package added")
	else:
		form = PackagesForm()
	return render(request, 'admin/new-package.html',{"form": form})

	





class PackageUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
	model = Packages
	fields = ['name', 'amount','percent']
	template_name = 'admin/packages_form.html'

	'''def form_valid(self, form):
		form.instance.author = self.request.user
		return super().form_valid(form)'''

	def test_func(self):
		post = self.get_object()
		if self.request.user.is_admin == True:
			return True
		return False


class PackagesDeleteView(LoginRequiredMixin, UserPassesTestMixin, DeleteView):
	model = Packages
	success_url = '/'
	template_name = 'admin/packages_confirm_delete.html'

	def test_func(self):
		post = self.get_object()
		if self.request.user.is_admin == True:
			return True
		return False






























def logout_view(request):
	logout(request)
	return redirect('dashboard-login')




def login_view(request):
	user = request.user
	if user.is_authenticated: 
		return redirect("dashboard")
	if request.method == "POST":
		form = AccountAuthenticationForm(request.POST)
		if form.is_valid():
			email = request.POST['email']
			password = request.POST['password']
			user = authenticate(email=email, password=password)

			if user:
				if user.is_staff == False:
					messages.info(request, f'only staffs are allowed to access this page')
					return redirect("dashboard-login")
				login(request, user)
				return redirect("dashboard")


	else:
		form = AccountAuthenticationForm()
	return render(request, "admin/login.html", {"form":form})








def error_404(request, *args, **argv):
    response = render_to_response('userstemplate/page-404.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 404
    return response


def error_500(request, *args, **argv):
    response = render_to_response('userstemplate/page-500.html', {},
                                  context_instance=RequestContext(request))
    response.status_code = 500
    return response