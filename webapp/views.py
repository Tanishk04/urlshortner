from django.shortcuts import render
from django.http import HttpResponseRedirect
from .forms import URLForm
import requests
from django.contrib.auth import authenticate
from django.contrib.auth.decorators import login_required
import requests
from requests.auth import HTTPBasicAuth  # Import HTTPBasicAuth for Basic Authentication
from django.shortcuts import render, redirect
from django.contrib import messages
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken

@login_required
def url_list(request):
    api_endpoint = 'http://127.0.0.1:8000/api/ShortURLList'

    try:

        token = request.session.get('token')

        headers = {'Authorization': f'Bearer {token}'}

        # Make API call to fetch registered URLs with JWT token
        response = requests.get(api_endpoint, headers=headers)
        response.raise_for_status()  # Raise an exception for any HTTP error status codes
        urls = response.json()
    except requests.RequestException as e:
        # Handle network errors or API call failures
        error_message = f"Failed to fetch registered URLs: {str(e)}"
        return render(request, 'webapp/error.html', {'error_message': error_message})
    
    return render(request, 'webapp/url_list.html', {'urls': urls})

@login_required
def shorten_url(request):
    if request.method == 'POST':
        form = URLForm(request.POST)
        if form.is_valid():
            # Extract data from the form
            original_url = form.cleaned_data['long']
            custom_alias = form.cleaned_data.get('alias', '')
            
            # Construct the payload
            payload = {'long': original_url, 'alias': custom_alias}

            # Example: API endpoint to shorten the URL
            api_endpoint = 'http://127.0.0.1:8000/api/shortenURL'

            try:
                # Get JWT token from user's session
                jwt_token = request.session.get('token')

                # Include JWT token in the request headers
                headers = {'Authorization': f'Bearer {jwt_token}'}

                # Make the API call to shorten the URL with JWT token
                response = requests.post(api_endpoint, json=payload, headers=headers)
                if response.status_code == 201:
                    # Fetch updated URL list
                    return redirect('url_list')
                else:
                    # Handle API call failure
                    error_message = "Failed to shorten the URL. Please try again later."
                    return render(request, 'webapp/error.html', {'error_message': error_message})
            except requests.RequestException as e:
                # Handle network errors
                error_message = f"An error occurred: {str(e)}"
                return render(request, 'webapp/error.html', {'error_message': error_message})
    else:
        # If it's a GET request, simply render the form
        form = URLForm()
    
    return render(request, 'webapp/url_form.html', {'form': form})

def home(request):
    return render(request, template_name='webapp/home.html')

@login_required
def update_url(request, alias):
    if request.method == 'POST':
        # Extract data from the form
        original_url = request.POST.get('long')
        custom_alias = request.POST.get('alias', '')
        
        # Construct the payload
        payload = {'long': original_url, 'alias': custom_alias}

        # Construct the URL for the API endpoint
        api_url = reverse('url-update-delete', kwargs={'pk': alias})

        try:
            # Obtain JWT token from the user's session
            token = request.session.get('token')

            # Include the token in the headers
            headers = {'Authorization': f'Bearer {token}'}

            # Make the API call to update the URL with JWT token
            response = requests.put(f"http://127.0.0.1:8000{api_url}", json=payload, headers=headers)
            if response.status_code == 200:
                return redirect('url_list')  # Redirect to a success page
            else:
                # Handle API call failure
                error_message = "Failed to update the URL. Please try again later."
                return render(request, 'webapp/error.html', {'error_message': error_message})
        except requests.RequestException as e:
            # Handle network errors
            error_message = f"An error occurred: {str(e)}"
            return render(request, 'webapp/error.html', {'error_message': error_message})
    else:
        try:
            # Obtain JWT token from the user's session
            token = request.session.get('token')

            # Include the token in the headers
            headers = {'Authorization': f'Bearer {token}'}

            # Fetch data from the API endpoint
            api_url = reverse('url-update-delete', kwargs={'pk': alias})
            response = requests.get(f'http://127.0.0.1:8000{api_url}', headers=headers)
            data = response.json()
            
            # Populate form with retrieved data
            fm = URLForm(data=data)
            return render(request, 'webapp/url_form.html', {"form": fm})
        except requests.RequestException as e:
            # Handle network errors
            error_message = f"An error occurred: {str(e)}"
            return render(request, 'webapp/error.html', {'error_message': error_message})
        
@login_required
def delete_url(request, alias):
    # Construct the URL for the API endpoint
    api_url = reverse('url-update-delete', kwargs={'pk': alias})

    try:
        # Obtain JWT token
        refresh = RefreshToken.for_user(request.user)
        access_token = str(refresh.access_token)

        # Make the API call to delete the URL with JWT token authentication
        headers = {'Authorization': f'Bearer {access_token}'}
        response = requests.delete(f"http://127.0.0.1:8000{api_url}", headers=headers)
        
        if response.status_code == 204:
            messages.success(request, 'URL deleted successfully.')
            return redirect('url_list')  
        else:
            # Handle API call failure
            error_message = "Failed to delete the URL. Please try again later."
            return render(request, 'webapp/error.html', {'error_message': error_message})
    except requests.RequestException as e:
        # Handle network errors
        error_message = f"An error occurred: {str(e)}"
        return render(request, 'webapp/error.html', {'error_message': error_message})
    
def my_redirect(request, alias):
    url = f"{alias}"
    return redirect(url)


