from django.shortcuts import render, redirect, get_object_or_404
from django.http import JsonResponse
from .forms import UserInputForm
from backend_script import process_input_data
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect
from django.conf import settings
from django.core.files.storage import FileSystemStorage
import os
from django.contrib import messages
from .forms import EmailCredentialsForm, SearchCredentialsForm
from .models import EmailCredentials
from django.http import HttpResponse
from django.urls import reverse

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('submit_form')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')  # Redirect to the login page after logout

@login_required
def add_credentials(request):
    if request.method == 'POST':
        form = EmailCredentialsForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('submit_form')  # Redirect to a success page or another view
    else:
        form = EmailCredentialsForm()

    return render(request, 'add_credentials.html', {'form': form})

@login_required
def search_credentials(request):
    form = SearchCredentialsForm(request.POST or None)
    credentials = []

    if request.method == 'POST':
        form = SearchCredentialsForm(request.POST)
        if form.is_valid():
            tenant_query = form.cleaned_data['tenant']
            credentials = EmailCredentials.objects.filter(tenant__icontains=tenant_query)

    return render(request, 'myapp/search_credentials.html', {'form': form, 'credentials': credentials})

@login_required
def update_credential(request, credential_id):
    credential = get_object_or_404(EmailCredentials, id=credential_id)
    
    if request.method == 'POST':
        form = EmailCredentialsForm(request.POST, instance=credential)
        if form.is_valid():
            form.save()
            return JsonResponse({'message': 'Update successful'})
        else:
            return JsonResponse({'status': 'error', 'errors': form.errors})
    else:
        # Use the existing form instance
        form = EmailCredentialsForm(instance=credential)

    return render(request, 'myapp/update_credential.html', {'form': form})


@login_required
def delete_credential(request, credential_id):
    credential = get_object_or_404(EmailCredentials, id=credential_id)

    if request.method == 'POST':
        credential.delete()
        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'error'})


@login_required
def submit_form(request):
    if request.method == 'POST':
        form = UserInputForm(request.POST, request.FILES)
        if form.is_valid():
            # Extracted form data
            advisory_type = form.cleaned_data['advisory_type']
            advisory_number = form.cleaned_data['advisory_number']
            advisory_name = form.cleaned_data['advisory_name']
            advisory_file = form.cleaned_data['advisory_file']

            # Save the uploaded HTML file to the project directory
            project_directory = settings.BASE_DIR
            file_directory = os.path.join(project_directory, 'Html_Uploaded_Files')
            file_path = os.path.join(file_directory, advisory_file.name)

            # Create the "uploaded_files" directory if it doesn't exist
            if not os.path.exists(file_directory):
                os.makedirs(file_directory)

            # Write the content of the uploaded file to the specified path
            with open(file_path, 'wb') as destination:
                for chunk in advisory_file.chunks():
                    destination.write(chunk)

            # Process the input data using the backend script
          
            try:
                captured_output = process_input_data(advisory_type, advisory_number, advisory_name, file_path)
            except Exception as e:
                captured_output = f"Error: {str(e)}"

            success_url = reverse('success_template.html')
            success_url += f'?output={captured_output}&advisory_type={advisory_type}&advisory_number={advisory_number}&advisory_name={advisory_name}'
            return redirect(success_url)
    else:
        form = UserInputForm()

    return render(request, 'myapp/submit_form.html', {'form': form})

