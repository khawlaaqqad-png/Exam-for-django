from django.shortcuts import render, redirect
from . import models
from django.contrib import messages
import bcrypt

# Create your views here.
def index(request):
    return render(request, 'index.html')

def create_user(request):
    if request.method == "POST":
        errors = models.User.objects.validator(request.POST)

        if errors:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect("/")
        models.add_user(request.POST)
    return redirect("/")

def login(request):
    if request.method == "POST":
        user = models.User.objects.filter(email=request.POST['email'])
        if user:
            user = user[0]
            if bcrypt.checkpw(request.POST['password'].encode(),user.password.encode()):
                request.session['user_id'] = user.id
                request.session['first_name'] = user.first_name
                return redirect("/shows")
        messages.error(request, "Invalid email or password")
    return redirect("/")

def shows(request):
    if 'user_id' not in request.session:
        return redirect('/')
    context = {
        'Users' : models.get_user(),
        'Shows': models.get_show(),
    }
    return render(request, 'shows.html', context)

def logout(request):
    request.session.flush()
    return redirect('/')

def show_creat(request):
    if 'user_id' not in request.session:
            return redirect('/')
    
    return render(request, 'show_creat.html')

def create_show(request):
    if 'user_id' not in request.session:
        return redirect('/')

    if request.method == "POST":
            errors = models.Tv_show.objects.validator(request.POST)

            if errors:
                for key, value in errors.items():
                    messages.error(request, value)
                return redirect("/show_creat")
            models.add_show(request.POST, request.session['user_id'])

            return redirect('/shows')
    return redirect('/show_creat')

def delete_show(request, show_id):
    if 'user_id' not in request.session:
        return redirect('/')

    models.delete_show_by_id(show_id)
    return redirect('/shows')

def edit_show(request, show_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    show = models.edit_show_by_id(show_id)

    if show.user.id != request.session['user_id']:
        return redirect('/shows')
    
    if request.method == "POST":
        errors = models.Tv_show.objects.validator(request.POST)

        if errors:
            for key, value in errors.items():
                messages.error(request, value)

            return redirect("/edit_show" + str(show_id))
        
        models.update_show(show_id, request.POST)
        return redirect('/shows')

    context = {
        'show' : show
    }

    return render(request, 'edit_show.html', context)

def show_details(request, show_id):
    if 'user_id' not in request.session:
        return redirect('/')
    
    show = models.get_show_by_id(show_id)

    context = {
        'show' : show
    }

    return render(request, 'show_details.html', context)