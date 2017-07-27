from django.shortcuts import render, redirect
from django.views.generic import View
from ..models import *
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.dateparse import parse_datetime
from django.utils import timezone
from django.http import JsonResponse

def is_deadline_near(date):
    if date is None:
        return False
    if date > timezone.now():
        delta = date - timezone.now()
        return delta.days == 0

def number_deadlines_from_user(user):
    task_deadlines, subtask_deadlines = deadlines_from_user(user)
    return len(task_deadlines) + len(subtask_deadlines)

def deadlines_from_user(user):
    task_deadlines = []
    subtask_deadlines = []
    for category in user.category_set.all():
        for task in category.task_set.all():
            if (not task.complete and
                task.notify_user and
                is_deadline_near(task.deadline)):
                task_deadlines.append(task)
            for subtask in task.subtask_set.all():
                if (not subtask.complete and
                    subtask.notify_user and
                    is_deadline_near(subtask.deadline)):
                    subtask_deadlines.append(subtask)

    return task_deadlines, subtask_deadlines

class DeadlinesView(LoginRequiredMixin, View):
    def get(self, req):
        task_deadlines, subtask_deadlines = deadlines_from_user(req.user)
        viewitems = {
            'title': 'Notificaciones',
            'username': req.user.username,
            'number_deadlines': number_deadlines_from_user(req.user),
            'task_deadlines': task_deadlines if len(task_deadlines) > 0 else False,
            'subtask_deadlines': subtask_deadlines if len(subtask_deadlines) > 0 else False,
        }
        return render(req, 'gst/deadlines.html', viewitems)

class DeadlinesAmmountView(LoginRequiredMixin, View):
    def get(self, req):
        if req.user:
            number_deadlines = number_deadlines_from_user(req.user)
            return JsonResponse({"number_deadlines": number_deadlines})
