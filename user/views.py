from django.shortcuts import render
from django.shortcuts import render, redirect
from django.http import HttpResponse
from pymongo import MongoClient
from datetime import datetime, timedelta
import secrets
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from M68.response import responce



# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['intelliAi']
collection = db['accounts']


def generate_session_token():
    token = secrets.token_urlsafe(16)
    return token


def is_valid_session_token(session_token):
    if session_token:
        user_data = collection.find_one({'session_token': session_token})
        if user_data:
            expiry_date = user_data.get('expiry_date')
            if expiry_date and expiry_date > datetime.now():
                return True
    return False


# Create your views here.

def index(request):
    session_token = request.COOKIES.get('session_token')

    if is_valid_session_token(session_token):
        return render(request, 'intelliAi.html')
    else:
        return render(request, 'landingPage.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if collection.find_one({'email': email}):
            return render(request, 'signup.html', {'error_message': 'User already exists. Please log in.'})
        else:
            session_token = generate_session_token()
            expiry_date = datetime.now() + timedelta(days=1)
            user_data = {'name': name, 'email': email, 'password': password, 'session_token': session_token, 'expiry_date': expiry_date}
            collection.insert_one(user_data)
            response = redirect('intelliAi')
            response.set_cookie('session_token', session_token, expires=expiry_date)

            return response

    else:
        return render(request, 'signup.html')


def login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = collection.find_one({'email': email, 'password': password})
        
        if user:
            session_token = generate_session_token()
            expiry_date = datetime.now() + timedelta(days=1)
            collection.update_one({'email': email}, {'$set': {'session_token': session_token, 'expiry_date': expiry_date}})
            response = redirect('intelliAi')
            response.set_cookie('session_token', session_token, expires=expiry_date)
            
            return response
        else:
            return render(request, 'login.html', {'error_message': 'Invalid email or password.'})

    else:
        return render(request, 'login.html')

def intelliAi(request):
    return render(request, 'intelliAi.html')

@csrf_exempt
def ai_response(request):
    print(request)
    if request.method == 'POST':
        data = json.loads(request.body)
        prompt = data.get('prompt', '')
        ai_response = responce(prompt)
        return JsonResponse({'message': ai_response})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def logout(request):
    if request.method == 'POST':
        try:
            response = JsonResponse({'message': 'success'})
            response.delete_cookie('session_token')
            return response
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def deleteAccount(request):
    if request.method == 'POST':
        try:
            response = JsonResponse({'message': 'success'})
            response.delete_cookie('session_token')
            return response
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def clearChat():
    pass