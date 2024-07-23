# Import necessary libraries 
from django.shortcuts import render, redirect 
from django.contrib.auth.decorators import login_required 
from django.contrib.auth import authenticate, login, logout 
from django.contrib import messages 
from django.http import HttpResponse
from django.contrib.auth.models import User # Import User model 
from .models import Expense 
from .models import ADD_OP_CHOICES
import datetime
import csv

# Create Expense page 

@login_required(login_url='/login/') 
def home(request): 
	if request.method == 'POST': 
		data = request.POST 
		name = data.get('name') 
		qty = int(data.get('qty', 0))
		category = data.get('category')
		type = data.get('type') 
		date = data.get('date')

		Expense.objects.create( 
			name=name, 
			qty=qty,
			category=category,
			type=type,
			date=date if date else now(),

		) 
		return redirect('/') 
	

	EXPENSE_TYPES = [type[0] for type in ADD_OP_CHOICES]  # Extract type values
	queryset = Expense.objects.all() 
	if request.GET.get('search'): 
		queryset = queryset.filter( 
			name__icontains=request.GET.get('search'))
	

	# Calculate the total sum 
	type_totals = {
		type: sum(expense.qty for expense in queryset if expense.type == type)
		 for type in EXPENSE_TYPES
	}
		 
	total_sum = sum(type_totals.values())
	context = {'expenses': queryset, 'type_totals': type_totals, 'total_sum': total_sum,}  # Include Category model
	return render(request, 'base.html', context) 

@login_required(login_url='/login/') 
def profile(request): 
		return render(request,'profile.html') 

@login_required(login_url='/login/') 
def expenses(request): 
	if request.method == 'POST': 
		data = request.POST 
		name = data.get('name') 
		qty = int(data.get('qty', 0))
		category = data.get('category')
		type = data.get('type') 
		date = data.get('date')

		Expense.objects.create( 
			name=name, 
			qty=qty,
			category=category,
			type=type,
			date=date if date else now(),

		) 
		return redirect('/') 

	queryset = Expense.objects.all() 
	if request.GET.get('search'): 
		queryset = queryset.filter( 
			name__icontains=request.GET.get('search')) 
		
	EXPENSE_TYPES = [type[0] for type in ADD_OP_CHOICES]  # Extract type values
	# Calculate the total sum 
	type_totals = {
		type: sum(expense.qty for expense in queryset if expense.type == type)
		 for type in EXPENSE_TYPES
	}
	
	total_sum = sum(type_totals.values())
	context = {'expenses': queryset, 'type_totals': type_totals, 'total_sum': total_sum}
	return render(request, 'expenses.html', context) 

# Update the Expenses data 
@login_required(login_url='/login/') 
def update_expense(request, id): 
	queryset = Expense.objects.get(id=id) 

	if request.method == 'POST': 
		data = request.POST 
		name = data.get('name') 
		qty = int(data.get('qty', 0)) 

		queryset.name = name 
		queryset.qty = qty 
		queryset.save() 
		return redirect('/') 

	context = {'expense': queryset} 
	return render(request, 'update_expense.html', context) 

# Delete the Expenses data 
@login_required(login_url='/login/') 
def delete_expense(request, id): 
	queryset = Expense.objects.get(id=id) 
	queryset.delete() 
	return redirect('/') 

# Login page for user 
def login_page(request): 
	if request.method == "POST": 
		try: 
			username = request.POST.get('username') 
			password = request.POST.get('password') 
			user_obj = User.objects.filter(username=username).first() 
			if not user_obj: 
				messages.error(request, "No se encontro el nombre de usuario") 
				return redirect('/login/') 
			user_auth = authenticate(username=username, password=password) 
			if user_auth: 
				login(request, user_auth) 
				return redirect('home') 
			messages.error(request, "Contraseña y/o Nombre de usuario invalido") 
			return redirect('/login/') 
		except Exception as e: 
			messages.error(request, "Algo salio mal") 
			return redirect('/register/') 
	return render(request, "login.html") 

# Register page for user 
def register_page(request): 
	if request.method == "POST": 
		try: 
			username = request.POST.get('username') 
			password = request.POST.get('password') 
			user_obj = User.objects.filter(username=username) 
			if user_obj.exists(): 
				messages.error(request, "El nombre de usuario ya existe") 
				return redirect('/register/') 
			user_obj = User.objects.create(username=username) 
			user_obj.set_password(password) 
			user_obj.save() 
			messages.success(request, "Cuenta Creada exitosamente") 
			return redirect('/login') 
		except Exception as e: 
			messages.error(request, "Algo salio mal") 
			return redirect('/register') 
	return render(request, "register.html") 

# Logout function 
def custom_logout(request): 
	logout(request) 
	return redirect('login') 

# Generate the Bill 
@login_required(login_url='/login/') 
def pdf(request): 
	if request.method == 'POST': 
		data = request.POST 
		name = data.get('name') 
		qty = int(data.get('qty', 0))
		category = data.get('category')
		type = data.get('type') 
		date = data.get('date')

		Expense.objects.create( 
			name=name, 
			qty=qty,
			category=category,
			type=type,
			date=date if date else now(),

		) 
		return redirect('pdf') 
	
	EXPENSE_TYPES = [type[0] for type in ADD_OP_CHOICES]  # Extract type values
	queryset = Expense.objects.all() 
	if request.GET.get('search'): 
		queryset = queryset.filter( 
			name__icontains=request.GET.get('search'))
	

	# Calculate the total sum 
	type_totals = {
		type: sum(expense.qty for expense in queryset if expense.type == type)
		 for type in EXPENSE_TYPES
	}
		 
	total_sum = sum(type_totals.values())
	context = {'expenses': queryset, 'type_totals': type_totals, 'total_sum': total_sum}
	return render(request, 'pdf.html', context) 


@login_required(login_url='/login/') 
def export_csv(request):

	response=HttpResponse(content_type='text/csv')
	response['Content-Dispossition'] ='attachment ; filename=MyFile' + str(datetime.datetime.now()) + '.csv'

	writer=csv.writer(response)
	writer.writerow(['Titulo', 'Monto', 'Fecha', 'Tipo', 'Categoria'])

	expenses=Expense.objects.all()

	for expense in expenses:
		writer.writerow([expense.name, expense.qty, expense.date, expense.type, expense.category])

	return response