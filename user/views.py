from django.http import JsonResponse
from django.shortcuts import  render, redirect
from .forms import NewUserForm
from django.contrib.auth import login,authenticate,logout
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect
from rest_framework.decorators import api_view
from django.contrib.auth.decorators import login_required
import requests


def register_request(request):
    # Check if the user is already authenticated, redirect if true
    if request.user.is_authenticated:
        return JsonResponse({'message':'User is already authenticated','user':request.user.username})

    # Process registration form when the request method is "POST"
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            # Save the new user, log them in, and redirect to the homepage
            user = form.save()
            messages.success(request, "Registration successful.")
            return redirect("login")
        else:
            # Display error message if the form is invalid
            messages.error(request, "Unsuccessful registration. Invalid information.")

    # Render the registration form when the request method is not "POST"
    form = NewUserForm()
    return render(
        request=request,
        template_name="register.html",
        context={"register_form": form, "form_errors": form.errors}
    )


# The `urlAPI` class is an API view that handles POST requests to create a URL object with
# authentication and permission checks.
import requests

def login_request(request):
    if request.user.is_authenticated:
        return JsonResponse({'message': 'User already logged in','user':request.user.username})

    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                print(f'LOGGED IN as {username}')
                messages.info(request, f"You are now logged in as {username}.")

                # Assuming you need to obtain a token from an external API
                # Make a request to the API to obtain the token
                token_api_endpoint = 'http://127.0.0.1:8000/api/token'
                response = requests.post(token_api_endpoint, data={'username': username, 'password': password})
                if response.status_code == 200:
                    token = response.json().get('access')
                    # Do something with the token, such as storing it in session or cookies
                    request.session['token'] = token
                    return redirect('home')
                else:
                    messages.error(request, "Failed to obtain token from the API.")
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    else:
        form = AuthenticationForm()

    return render(request=request, template_name="login.html", context={"login_form": form})


@login_required(login_url='/')
def logout_request(request):
    username = request.user.username
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect("home")

def test(request):
    if request.user.is_authenticated:
        return JsonResponse({'message':f'{request.user.username} is authenticated'})
    else:
        return JsonResponse({'message':'User not authenticated'})
        