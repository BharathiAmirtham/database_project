from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Person
import csv
from .forms import UploadCSVForm
import io


def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
        else:
            user = User.objects.create_user(username=username, password=password)
            user.save()
            messages.success(request, 'Account created successfully')
            return redirect('login')
    return render(request, 'register.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_staff == True:
                return redirect('home')
            else:
                return redirect('home')
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def user_logout(request):
    logout(request)
    return redirect('login')

def home(request):
    if request.method == 'POST':
        form = UploadCSVForm(request.POST, request.FILES)
        if form.is_valid():
            csv_file = request.FILES['csv_file']
            if not csv_file.name.endswith('.csv'):
                messages.error(request, 'This is not a CSV file')
                return redirect('home.html')

            decoded_file = csv_file.read().decode('utf-8')
            io_string = io.StringIO(decoded_file)
            reader = csv.reader(io_string, delimiter=',')
            next(reader)  

            added_count = 0
            skipped_count = 0

            for row in reader:
                name=row[0]
                email=row[1]
                department=row[2]

                if Person.objects.filter(name=name).exists():
                    skipped_count += 1
                    continue    
                
                Person.objects.create(
                    name=name,
                    email=email,
                    department=department,
                )
                added_count += 1
            
            messages.success(request, f'Successfully added {added_count} entries.')
            return redirect('home')
                
    else:
        form = UploadCSVForm()
        data=Person.objects.all()
        print(data,"data")
        return render(request, 'home.html', {'form': form,'data':data})

def delete_person(request, person_id):
    person = get_object_or_404(Person, id=person_id)
    person.delete()
    messages.success(request, f"Deleted {person.name}'s Details.")
    return redirect('home')

