# -*- encoding=utf-8 -*-
from django.shortcuts import render, redirect
from django.views.generic import View
from django.http import HttpResponse as HTTPr
from ..models import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from deadline import number_deadlines_from_user

class CategoryView(LoginRequiredMixin, View):
    def get(self, req):
        viewitems = {
            'title': 'Categories',
            'username': req.user.username,
            'number_deadlines': number_deadlines_from_user(req.user),
            'categories': req.user.category_set.all()
        }
        return render(req, 'gst/category.html', viewitems)

class CategoryCreateView(LoginRequiredMixin, View):
    def post(self, req):
        name = req.POST['name']
        try:
            req.user.category_set.get(name=name)
            viewitems = {
                'title': 'Categories',
                'username': req.user.username,
                'number_deadlines': number_deadlines_from_user(req.user),
                'categories': req.user.category_set.all(),
                'error': 'La categoría ya existe. No pueden haber duplicados.'
            }
            return render(req, 'gst/category.html', viewitems)
        except Category.DoesNotExist:
            req.user.category_set.create(name=name)
            return redirect('task', category=req.user.category_set.get(name=name).id)

class CategoryEditView(LoginRequiredMixin, View):
    def get(self, req, category):
        viewitems = {
            'title': 'Category Edit',
            'username': req.user.username,
            'number_deadlines': number_deadlines_from_user(req.user),
            'category': req.user.category_set.get(id=category)
        }
        return render(req, 'gst/category_edit.html', viewitems)

    def post(self, req, category):

        category = req.user.category_set.get(id=category)
        if category.name == 'Goals':
            return HTTPr('You can not edit the main category.')
        if req.POST.get('new_name', False):
            category.name = req.POST.get('new_name')
        category.save()
        return redirect('category')

class CategoryDeleteView(LoginRequiredMixin, View):
    def post(self, req, category):
        # Never delete default category.
        if req.user.category_set.get(id=category).name != 'Goals':
            req.user.category_set.get(id=category).delete()
        return redirect('category')
