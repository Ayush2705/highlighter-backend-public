from django.shortcuts import render, redirect
from .models import User
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponse
from myapp.models import HighlightedText
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.views.decorators.csrf import csrf_exempt
import json
# user = User()
# user.username = 'abc'
# user.password = '123'
# user.save()

@csrf_exempt
def login2(request):
    if request.method=='POST':
        print(request.POST)
        try:

            username=request.POST['username']
            password=request.POST['password']

            user=User.objects.get(username=username,password=password)
            print(user)
            if user is not None:
                print(27)
                return HttpResponse('success')
            else:
                print(30)
                return HttpResponse('error')
        except KeyError as e:
            print(32,e)
            return HttpResponse(f'Missing key{e}')
        except User.DoesNotExist:
            print(35)
            return HttpResponse('invalid')
    else:
        return HttpResponse('invalid request response')
        # print(username,password,21)
        # print(user)
        # print(request.body,23)              

		
    


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        print(username,"11")
        print(password)
        try:
        #if username=="abc" and password=="123":
            user = User.objects.get(username=username, password=password)
            print(username,"14")
            print(password)
            # Login successful
            # You can implement session management here, e.g., setting session variables
            request.session['username'] = username
            return redirect('home')  # Redirect to home page after successful login
        except User.DoesNotExist:
        #else:
            # Login failed
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    else:
        return render(request, 'login.html')
# @login_required
def home(request):
    print(request)
    print(request.session)
    if request.method == 'POST':
        if 'logout' in request.POST:
            #logout(request)
            return redirect('login')
        elif 'view_highlighted_text' in request.POST:
            user1 = User.objects.get(username=request.session.get('username'))
            highlighted_texts = HighlightedText.objects.filter(user=user1)
            return render(request, 'home.html', {'username': request.session.get('username'), 'highlighted_texts': highlighted_texts})
    return render(request, 'home.html', {'username': request.session.get('username')})
# @login_required
@csrf_exempt
def store_highlighted_text(request):
    print(50,request.method, request.POST,request.body)
    if request.method == 'POST' :
        print(400000000000000)
        data = json.loads(request.body)
        text = data['text']
        user=data['user']
        print(text,user)
        user1 = User.objects.get(username=user)
        print(user1)
        # Store the highlighted text in the database
        highlighted_text = HighlightedText(text=text,user=user1)
        highlighted_text.save()
        response = JsonResponse({'success': True})
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Methods'] = 'POST'
        response['Access-Control-Allow-Headers'] = 'Content-Type'
        return response
    else:
        # Return 405 Method Not Allowed if not POST request
        response = HttpResponseNotAllowed(['POST'])
        response['Allow'] = 'POST'
        return response

def view_highlighted_text(request):
    highlighted_texts = HighlightedText.objects.all()
    return render(request, 'view_highlighted.html', {'highlighted_texts': highlighted_texts})

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = User(username=username, password=password)
            user.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})