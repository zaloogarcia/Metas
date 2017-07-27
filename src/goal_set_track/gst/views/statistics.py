from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import View
from django.utils import timezone

def lenght(list):
    try:
        return len(list)
    except Exception as e:
        return False

def is_deadline(date):
    if date is None:
        return False
    if date < timezone.now():
        return True
    else:
        return False

def created_tasks_from_user(user):
    created_tasks = []
    for category in user.category_set.all():
        for task in category.task_set.all():
            if (task.created_at.month == timezone.now().month and
                task.created_at.year == timezone.now().year):
                created_tasks.append(task)
    return created_tasks

def completed_tasks_from_user(user):
    completed_tasks = []
    for category in user.category_set.all():
        for task in category.task_set.all():
            if (task.complete and
                task.created_at.month == timezone.now().month and
                task.created_at.year == timezone.now().year):
                completed_tasks.append(task)
    return completed_tasks

def failed_tasks_from_user(user):
    failed_tasks = []
    for category in user.category_set.all():
        for task in category.task_set.all():
            if (not task.complete and
                is_deadline(task.deadline) and
                task.created_at.month == timezone.now().month and
                task.created_at.year == timezone.now().year):
                failed_tasks.append(task)
    return failed_tasks

class StatisticsView(LoginRequiredMixin, View):
    def get(self, req):
        created_tasks = created_tasks_from_user(user=req.user)
        completed_tasks = completed_tasks_from_user(req.user)
        failed_tasks = failed_tasks_from_user(req.user)
        viewitems = {
            'title': 'Statistics',
            'username': req.user.username,
            'created_tasks':
                created_tasks if lenght(created_tasks) > 0 else False,
            'completed_tasks':
                completed_tasks if lenght(completed_tasks) > 0 else False,
            'failed_tasks':
                failed_tasks if lenght(failed_tasks) > 0 else False
        }
        return render(req, 'gst/statistics.html', viewitems)
