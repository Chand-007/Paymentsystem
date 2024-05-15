# Create your views here.

from django.shortcuts import render, redirect
from .models import Receipt 
from django.http import HttpResponse, JsonResponse, HttpResponseRedirect
from django.contrib import messages
from django.contrib.auth import login, authenticate,logout
from django.contrib.auth.decorators import login_required 
from django.contrib.auth.models import User


@login_required
def receipts(request):
	if request.method == 'POST': 
		data = request.POST
		name = data.get('name')
		price = data.get('price')
		quantity = data.get('quantity')
		total = float(price) * int(quantity)

		Receipt.objects.create(
			name = name,
			price=price,
			quantity=quantity,
			total=total
		)
		return redirect('http://127.0.0.1:8000/print/receipt/')

	queryset = Receipt.objects.all()
	if request.GET.get('search'):
		queryset = queryset.filter(
			name__icontains=request.GET.get('search'))
		
	# Calculate the total sum
	total_sum = sum(receipt.total for receipt in queryset)
	context = {'receipts': queryset, 'total_sum': total_sum}
	return render(request, 'PrintReceipt/receipt.html', context)
@login_required
def update_receipt(request, id):
	queryset = Receipt.objects.get(id=id)

	if request.method == 'POST':
		data = request.POST 
		name = data.get('name')
		price = data.get('price')
		quantity = data.get('quantity')
		total = float(price) * int(quantity)
		
		queryset.name = name
		queryset.price = price
		queryset.quantity = quantity
		queryset.total = total
		queryset.save()
		return redirect('http://127.0.0.1:8000/print/receipt/')

	context = {'receipt': queryset}
	return render(request, 'PrintReceipt/update_receipt.html', context)

@login_required
def delete_receipt(request, id):
	queryset = Receipt.objects.get(id=id)
	queryset.delete()
	return redirect('http://127.0.0.1:8000/print/receipt/')

def login_page(request):
	if request.method == "POST":
		try:
			username = request.POST.get('username')
			password = request.POST.get('password')
			user_obj = User.objects.filter(username=username)
			if not user_obj.exists():
				messages.error(request, "Username not found")
				return redirect('http://127.0.0.1:8000/print/login/')
			user_obj = authenticate(username=username, password=password)
			if user_obj:
				login(request, user_obj)
				return redirect('http://127.0.0.1:8000/print/receipt/')
			messages.error(request, "Wrong Password")
			return redirect('http://127.0.0.1:8000/print/login/')
		except Exception as e:
			messages.error(request, "Something went wrong")
			return redirect('http://127.0.0.1:8000/print/register/')
	return render(request, "PrintReceipt/login.html")

def register_page(request):
	if request.method == "POST":
		try:
			username = request.POST.get('username')
			password = request.POST.get('password')
			user_obj = User.objects.filter(username=username)
			if user_obj.exists():
				messages.error(request, "Username is taken")
				return redirect('http://127.0.0.1:8000/print/register/')
			user_obj = User.objects.create(username=username)
			user_obj.set_password(password)
			user_obj.save()
			messages.success(request, "Account created")
			return redirect('login')
		except Exception as e:
			messages.error(request, "Something went wrong")
			return redirect('http://127.0.0.1:8000/print/register/')
	return render(request, "PrintReceipt/register.html")

def custom_logout(request):
	logout(request)
	return redirect('http://127.0.0.1:8000/print/login/') 

@login_required
def pdf(request):
	if request.method == 'POST':
		print(data)
		data = request.POST 
		name = data.get('name')
		price = data.get('price')
		quantity = data.get('quantity')
		total = float(price) * int(quantity)

		Receipt.objects.create(
			name = name,
			price=price,
			quantity=quantity,
			total=total
		)
		return redirect('pdf')

	queryset = Receipt.objects.all()
	
	if request.GET.get('search'):
		queryset = queryset.filter(
			name__icontains=request.GET.get('search'))
		
	
	total_sum = sum(receipt.total for receipt in queryset)

	context = {'receipts': queryset, 'total_sum': total_sum}
	return render(request, 'PrintReceipt/pdf.html', context)
