from django.shortcuts import render, redirect
from django.views.generic import View
from ..models import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.dateparse import parse_datetime
from django.utils import timezone

class CommentCreateView(LoginRequiredMixin, View):
    def post(self, req, category, task):
        req.user.category_set.get(id=category).task_set.get(id=task).comment_set.create(text=req.POST['text'])
        return redirect('subtask', category=category, task=task)

class CommentDeleteView(LoginRequiredMixin, View):
    def post(self, req, category, task, comment):
        req.user.category_set.get(id=category).task_set.get(id=task).comment_set.get(id=comment).delete()
        return redirect('subtask', category=category, task=task)


class CommentEditView(LoginRequiredMixin, View):
    def get(self, req, category, task, comment):
        viewitems = {
            'title': 'Editar Comentario',
            'username': req.user.username,
            'category': req.user.category_set.get(id=category),
            'task': req.user.category_set.get(id=category).task_set.get(id=task),
            'comment': req.user.category_set.get(id=category).task_set.get(id=task).comment_set.get(id=comment)
        }
        return render(req, 'gst/comment_edit.html', viewitems)

    def post(self, req, category, task, comment):
        comment = req.user.category_set.get(id=category).task_set.get(id=task).comment_set.get(id=comment)

        comment.text = req.POST.get('new_name', comment.text)
        comment.save()

        return redirect('subtask', category=category, task=task)
