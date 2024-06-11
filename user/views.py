from django.shortcuts import render
from django.shortcuts import render, redirect
from pymongo import MongoClient
from datetime import datetime, timedelta
import secrets
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from M68.response import get_response
import hashlib


# Connect to MongoDB
client = MongoClient('mongodb://localhost:27017/')
db = client['intelliAi']
collection = db['accounts']
chat_history_collection = db['conv_history']

def hash_password(password):
    # SHA-256 algorithm
    hashed_password = hashlib.sha256(password.encode()).hexdigest()
    return hashed_password


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

def custom_404(request, exception):
    return render(request, '404.html', status=404)


def index(request):
    session_token = request.COOKIES.get('session_token')

    if is_valid_session_token(session_token):
        return render(request, 'intelliAi.html')
    else:
        return render(request, 'landingPage.html')

def intelliAi(request):
    if 'session_token' in request.COOKIES:
        session_token = request.COOKIES['session_token']
        user = collection.find_one({'session_token': session_token})
    return render(request, 'intelliAi.html')

def guest(request):
    if 'session_token' in request.COOKIES:
        session_token = request.COOKIES['session_token']
        user = collection.find_one({'session_token': session_token})
        if(user):
            return render(request, 'intelliAi.html')
        else:
            return render(request, 'guest.html')
    else:
        return render(request, 'guest.html')

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        password = request.POST.get('password')

        if collection.find_one({'email': email}):
            return render(request, 'signup.html', {'error_message': 'User already exists. Please log in.'})
        else:
            hashed_password = hash_password(password)
            session_token = generate_session_token()
            expiry_date = datetime.now() + timedelta(days=1)
            user_data = {'name': name, 'email': email, 'password': hashed_password, 'session_token': session_token, 'expiry_date': expiry_date}
            collection.insert_one(user_data)
            response = redirect('intelliAi')
            response.set_cookie('session_token', session_token, expires=expiry_date)
            response.set_cookie('usenmae', name)

            return response

    else:
        return render(request, 'signup.html')

# login
def user_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        hashed_password = hash_password(password)
        user = collection.find_one({'email': email, 'password': hashed_password})

        if user:
            session_token = generate_session_token()
            expiry_date = datetime.now() + timedelta(days=1)
            collection.update_one({'email': email}, {'$set': {'session_token': session_token, 'expiry_date': expiry_date}})
            response = redirect('intelliAi')
            response.set_cookie('session_token', session_token, expires=expiry_date)
            response.set_cookie('username', user['name'])
            
            return response
        else:
            return render(request, 'login.html', {'error_message': 'Invalid email or password.'})
    else:
        return render(request, 'login.html')
    
@csrf_exempt
def get_conve_history(request):
    if request.method == 'POST':
        session_token = request.COOKIES.get('session_token')
        user = collection.find_one({'session_token': session_token})
        
        if user:
            user_id = str(user['_id'])
            chat_history = chat_history_collection.find({'ref': user_id})
            
            chat_history_list = [
                {
                    '_id': str(chat['_id']),
                    'ref': chat['ref'],
                    'prompt': chat['prompt'],
                    'response': chat['response'],
                    'timestamp': chat['timestamp']
                }
                for chat in chat_history
            ]
            return JsonResponse(chat_history_list, safe=False)
        else:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def ai_response(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        image = request.FILES.get('image', None)

        ai_response = get_response(prompt, image)
        
        if not image:
            session_token = request.COOKIES.get('session_token')
            user = collection.find_one({'session_token': session_token})
        
            if user:
                timestamp = datetime.now()
                user_id = str(user['_id'])
            
                chat_history = {'ref': user_id, 'prompt': prompt, 'response': ai_response, 'timestamp': timestamp}
                chat_history_collection.insert_one(chat_history)
        
        return JsonResponse({'message': ai_response})
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
@csrf_exempt
def guest_ai_response(request):
    if request.method == 'POST':
        prompt = request.POST.get('prompt', '')
        ai_response = get_response(prompt)
        
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
        session_token = request.COOKIES.get('session_token')
        user = collection.find_one({'session_token': session_token})
        if user:
            email = user['email']
            collection.delete_one({'email': email})
            response = JsonResponse({'message': 'success'})
            response.delete_cookie('session_token')
            return response
        else:
            return JsonResponse({'error': 'user not found!'}, status=400)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def clear_data(request):
    if request.method == 'POST':
        session_token = request.COOKIES.get('session_token')
        user = collection.find_one({'session_token': session_token})
        if user:
            user_id = str(user['_id'])
            chat_history_collection.delete_many({'ref': user_id})
            return JsonResponse({'message': 'Data cleared successfully'})
        else:
            return JsonResponse({'error': 'User not found'}, status=404)
    else:
        return JsonResponse({'error': 'Method not allowed'}, status=405)