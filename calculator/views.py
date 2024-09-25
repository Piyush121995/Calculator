from django.contrib.auth.decorators import login_required
from django.contrib.auth.hashers import make_password
from django.shortcuts import render,redirect
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django import forms
from .import forms
from calculator.forms import SignupForm

import re
import logging
logger = logging.getLogger(__name__)


# Your existing calculator functions
import re


# Safely evaluate the expression using eval after cleaning input
def calculate_expression(expression):
    try:
        # Clean the expression (e.g., remove invalid characters)
        expression = re.sub(r'[^0-9+\-*/().%]', '', expression)

        # Evaluate the expression
        result = eval(expression)

        return result
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except Exception as e:
        return f"Error: Invalid expression. {str(e)}"


# View to render the HTML form and handle the calculation
@csrf_exempt
@login_required(login_url='login')
def calculate(request):
    if request.method == 'POST':
        expression = request.POST.get('expression', '')
        result = calculate_expression(expression)
        return render(request, 'design.html', {'result': result, 'expression': expression})

    return render(request, 'design.html')


#login Functionality
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('calculator')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request,'login.html')

def sign_up(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Account created successfully! You can now log in.')
            return render(request, 'signup_success.html')
    else:
        form = SignupForm()

    return render(request, 'sign-up.html', {'form': form})

def signup_success(request):
    return render(request, 'signup_success.html')



