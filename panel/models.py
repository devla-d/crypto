from django.db import models
from django.utils import timezone
from django.urls import reverse
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
import uuid
from django.utils.text import slugify
import random
import string
from datetime import datetime, timedelta,date
from django.urls import reverse
from django.utils import timezone



class Packages(models.Model):
	name = models.CharField(max_length=50)
	amount = models.IntegerField()
	date = models.DateTimeField(auto_now_add=True,blank=True,null=True)
	percent = models.IntegerField(blank=True,null=True)

	class Meta:
			ordering = ['-date']
	

	def get_absolute_url(self):
		return reverse('admin-package')

class Message(models.Model):
	email = models.EmailField(max_length=50)
	subject = models.CharField(max_length=100)
	body = models.TextField()
	date = models.DateTimeField(auto_now_add=True,blank=True,null=True)

	class Meta:
			ordering = ['-date']


class Notification(models.Model):
	user = models.ForeignKey('Investors', on_delete  = models.CASCADE)
	subject = models.CharField(max_length=100)
	body = models.TextField()
	date = models.DateTimeField(auto_now_add=True,blank=True,null=True)

	class Meta:
			ordering = ['-date']



class Deposite(models.Model):
	STATUS = (
		("pending","pending"),
		("completed","completed"),
		("decline","decline"),
	)
	Investor = models.ForeignKey('Investors', on_delete  = models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	amount = models.IntegerField()
	trans_id = models.CharField(max_length=100,blank=True,null=True)
	status = models.CharField(max_length=15, choices=STATUS)

	class Meta:
			ordering = ['-date']
  



class Transaction(models.Model):
	STATUS = (
		("pending","pending"),
		("sucessfull","sucessfull"),
	)
	SERVICES = (
		("withdraw","withdraw"),
		("deposite","deposite"),
	)
	user = models.ForeignKey('Investors', on_delete  = models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	amount = models.IntegerField()
	status = models.CharField(max_length=15, choices=STATUS)
	service = models.CharField(max_length=15, choices=SERVICES)

	class Meta:
			ordering = ['-date']





class Withdraw(models.Model):
	STATUS = (
		("pending","pending"),
		("sucessfull","sucessfull"),
		("declined","declined"),
	)
	user = models.ForeignKey('Investors', on_delete  = models.CASCADE)
	date = models.DateTimeField(auto_now_add=True)
	amount = models.IntegerField()
	status = models.CharField(max_length=15, choices=STATUS)

	class Meta:
			ordering = ['-date']
	







class MyAccountManager(BaseUserManager):
	def create_user(self,username, email, password=None):
		if not email:
			raise ValueError('email is required')
		if not username:
			raise ValueError('username is required')
		
		user = self.model(
			email= self.normalize_email(email),
			username= username
		)
		user.set_password(password)
		user.save(using=self._db)
		return user

	def create_superuser(self, username,email,password):
		user = self.create_user(
			 email= self.normalize_email(email),
			username= username,
			password= password,
		
		)
		user.is_admin=True
		user.is_superuser=True
		user.is_staff= True
		user.save(using=self._db)
		return user





def rand_slug():
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(6))


class Investors(AbstractBaseUser):
	email       = models.EmailField(verbose_name='email', max_length=60, unique=True )
	username    = models.CharField(max_length=30, unique=True)
	full_name    = models.CharField(max_length=30 ,blank=True, null= True)
	date_joined = models.DateTimeField(verbose_name='date joined', auto_now_add=True)
	last_login  = models.DateTimeField(verbose_name='last login', auto_now=True)
	is_admin    = models.BooleanField(default=False)
	is_staff    = models.BooleanField(default=False)
	is_active   = models.BooleanField(default=True)
	is_superuser = models.BooleanField(default=False)
	profile_image = models.ImageField(blank=True, null=True, default='logo-small.png', upload_to='profile')
	phone = models.CharField(max_length=60, blank=True, null=True)
	wallet_id = models.CharField(max_length=60, blank=True, null=True)
	ref_code = models.CharField(max_length=60, blank=True, null=True, unique=True)
	refferal = models.IntegerField(default=0)
	balance = models.IntegerField(default=0)
	package = models.ForeignKey('Packages', on_delete  = models.CASCADE,blank=True,null=True)
	
	
	USERNAME_FIELD = 'email'
	REQUIRED_FIELDS = ['username']

	objects = MyAccountManager()

	class Meta:
			ordering = ['-date_joined']

	def __str__(self):
		return self.email

	# For checking permissions. to keep it simple all admin have ALL permissons
	def has_perm(self, perm, obj=None):
		return self.is_admin

	# Does this user have permission to view this app? (ALWAYS YES FOR SIMPLICITY)
	def has_module_perms(self, app_label):
		return True


	def save(self, *args, **kwargs):
		if not self.ref_code:
			self.ref_code = slugify( rand_slug() + "-" + self.username)
		super(Investors, self).save(*args, **kwargs)



class RefferalProfile(models.Model):
	user = models.OneToOneField(Investors, on_delete = models.CASCADE)
	recommended_by = models.ForeignKey(Investors,related_name='recom_user', on_delete=models.CASCADE,null=True, blank=True)
	date = models.DateTimeField(auto_now_add=True)

	def recom_profies(self):
		qs = RefferalProfile.objects.all()
		my_rec = []
		for profile in qs:
			if profile.recommended_by == self.user:
				my_rec.append(profile)
		return my_rec



	def __str__(self):
		return self.user.username


	
	
class Investment(models.Model):
	STATUS = (
		("Active","active"),
		("complete","complete"),
	)
	user = models.ForeignKey('Investors', on_delete=models.CASCADE)
	pack = models.ForeignKey('Packages', on_delete=models.CASCADE)
	start_date = models.DateTimeField(auto_now_add=True)
	end_date = models.DateTimeField()
	status = models.CharField(max_length=40, choices=STATUS)
	total_prof = models.IntegerField(default=0, blank=True,null=True)
	withdraw = models.BooleanField(default=False)

	def total_earnings(self):
		price = self.pack.amount
		percent = self.pack.percent
		perc = percent/100 * price
		total = perc * 7
		entire = total + price
		return entire

	@property
	def is_past_due(self):
		time = timezone.now()
		if time >= self.end_date:
			return True
		return False

	def total_perc(self):
		price = self.pack.amount
		percent = self.pack.percent
		perc = percent/100 * price
		return perc
		
	
        
		 

	def __str__(self):
		return self.user.username
