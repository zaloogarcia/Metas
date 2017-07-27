from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse as HTTPr
from ..models import *
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from deadline import number_deadlines_from_user

# Create your views here.
@login_required
def home(req):
    viewitems = {
        'title': 'Home',
        'username': req.user.username,
        'number_deadlines': number_deadlines_from_user(req.user),
    }
    return redirect('category')

class LoginView(View):
    def get(self, req):
        viewitems = {
            'title': 'Login',
        }
        return render(req, 'gst/login.html', viewitems)

    def post(self, req):
        username = req.POST['username']
        password = req.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            login(req, user)
            return redirect('category')
        else:
            return redirect('login')

class LogoutView(LoginRequiredMixin, View):
    def get(self, req):
        logout(req)
        viewitems = {
            'title': 'Logout',
        }
        return render(req, 'gst/login.html', viewitems)

class RegisterView(View):
    def get(self, req):
        viewitems = {
            'title': 'Register',
        }
        return render(req, 'gst/register.html', viewitems)

    def post(self, req):
        first_name = req.POST['first_name']
        last_name = req.POST['last_name']
        username = req.POST['username']
        email = req.POST['email']
        password = req.POST['password']
        new_user = User.objects.create_user(username, email, password)
        new_user.first_name = first_name
        new_user.last_name = last_name
        new_user.save()

        # New users always have a default 'Goals' category.
        new_user.category_set.create(name='Goals')

        login(req, new_user)
        return redirect('category')

class AboutView(View):
    def get(self, req):
        viewitems = {
            'title': 'About',
            'username': req.user.username if req.user.username else None,
            'number_deadlines': number_deadlines_from_user(req.user) if req.user.username else None,
        }
        return render(req, 'gst/about.html', viewitems)


class UserView(LoginRequiredMixin, View):
    def get(self, req):
        viewitems = {
            'title': 'Profile Information',
            'username': req.user.username,
            'number_deadlines': number_deadlines_from_user(req.user),
            'user': req.user
        }
        return render(req, 'gst/user.html', viewitems)

class UserEditView(LoginRequiredMixin, View):
    def get(self, req):
        viewitems = {
            'title': 'Edit Profile Information',
            'username': req.user.username,
            'number_deadlines': number_deadlines_from_user(req.user),
            'user': req.user
        }
        return render(req, 'gst/user_edit.html', viewitems)

    def post(self, req):
        if req.POST.get('first_name'):
            req.user.first_name = req.POST.get('first_name')
        if req.POST.get('last_name'):
            req.user.last_name = req.POST.get('last_name')
        if req.POST.get('password'):
            req.user.set_password(req.POST['password'])
        req.user.save()
        return redirect('user')
