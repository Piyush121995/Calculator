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
from rest_framework import generics

from .models import UserCalculationHistory
from .serializers import UserSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .import models

import re
import logging
logger = logging.getLogger(__name__)

from .forms import UploadForm
import os

from django.utils.encoding import smart_str
# Your existing calculator functions
import re

def calculate_expression(expression):
    try:
        # Clean the expression (e.g., remove invalid characters)
        expression = re.sub(r'[^0-9+\-*/().%^]', '', expression)
        expression = expression.replace('^', '**')

        # Evaluate the expression using sympy
        result = eval(expression)

        return result
    except ZeroDivisionError:
        return "Error: Division by zero is not allowed."
    except SyntaxError:
        return "Error: Invalid expression."
    except Exception as e:
        return f"Error: {str(e)}"

# View to render the HTML form and handle the calculation
@csrf_exempt
@login_required(login_url='login')
def calculate(request):
    user=request.user
    history = UserCalculationHistory.objects.filter(user=request.user).order_by('-Created_at')[:10]
    result = None
    expression=''
    if request.method == 'POST':
        expression = request.POST.get('expression', '')
        try:
            result = calculate_expression(expression)
            UserCalculationHistory.objects.create(
                user=user,
                expression=expression,
                result=result
            )
            history = UserCalculationHistory.objects.filter(user=user).order_by('-Created_at')[:10]
        except Exception as e:
            # Handle errors in expression calculation
            result = f"Error calculating {expression}: {str(e)}"

    return render(request, 'design.html', {'result': result, 'expression': expression,'history': history,'username':user.username})



def logout_view(request):
    logout(request)
    return redirect('login')

@csrf_exempt
@api_view(['POST'])
def api_calculate(request):
    expression = request.data.get('expression', '')
    result = calculate_expression(expression)
    return Response({"expression": expression, "result": result})

class UserListCreateApiView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        serializer.save(password=make_password(serializer.validated_data['password']))

class UserRetrieveUpdateDestroyApiView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    # lookup_field = 'id'
    # permission_classes = []

    # def get_object(self):
    #     id = self.kwargs.get('id')  # get 'username' from the URL
    #     return User.objects.get(id=id)


#login Functionality
def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # history = UserCalculationHistory.objects.filter(user=user).order_by('-Created_at')[:10]
            return redirect('calculator')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request,'login.html'  )

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

def upload_file_check(file):
    result_line=[]
    for line in file:
        expression=line.decode('utf-8').strip()
        try:
            result = eval(expression)
            result_line.append (f"{expression}={result}\n")
        except Exception as e:
            result_line.append(f"{expression}= 'Invalid data'\n")
    result_file_path = 'output/results.txt'
    os.makedirs(os.path.dirname(result_file_path), exist_ok=True)
    with open(result_file_path, 'w') as result_file:
        result_file.writelines(result_line)

    return result_file_path


def upload_file_view(request):
    if request.method == 'POST':
        # Initialize the form with POST data and uploaded files
        form = UploadForm(request.POST, request.FILES)

        # Debugging: Log form data and files
        print("POST Data:", request.POST)  # Check what is being submitted
        print("FILES Data:", request.FILES)  # Check the uploaded file

        if form.is_valid():
            uploaded_file = request.FILES['file']  # Access the file from the form
            file_name, file_extension = os.path.splitext(uploaded_file.name)

            # Check if the uploaded file is a .txt file
            if file_extension.lower() == '.txt':
                uploaded_file.seek(0)  # Ensure you're at the beginning of the file
                result_file_path = upload_file_check(uploaded_file)  # Your function to process the file

                with open(result_file_path, 'r') as result_file:
                    response = HttpResponse(result_file.read(), content_type='text/plain')
                    response['Content-Disposition'] = 'attachment; filename="results.txt"'
                    return response
            else:
                return HttpResponse("Invalid file format. Only .txt files are supported.")
        else:
            print("Form errors:", form.errors)  # Print any form validation errors
            return HttpResponse("Invalid form submission. Please check your input.")
    else:
        form = UploadForm()  # Create a new instance of the form for GET requests

    return render(request, 'design.html', {'form': form})