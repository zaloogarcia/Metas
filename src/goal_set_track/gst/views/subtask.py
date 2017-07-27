from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from django.views.generic import View

from deadline import number_deadlines_from_user


class SubTaskView(LoginRequiredMixin, View):
    def get(self, req, category, task):
        viewitems = {
            'title': 'Sub Tareas',
            'username': req.user.username,
            'number_deadlines': number_deadlines_from_user(req.user),
            'category': req.user.category_set.get(id=category),
            'task': req.user.category_set.get(id=category).task_set.get(id=task),
            'subtasks': req.user.category_set.get(id=category)
                            .task_set.get(id=task).subtask_set.all(),
            'comments': req.user.category_set.get(id=category)
                            .task_set.get(id=task).comment_set.all(),
        }
        return render(req, 'gst/subtask.html', viewitems)

class SubTaskCreateView(LoginRequiredMixin, View):
    def post(self, req, category, task):
        t = req.user.category_set.get(id=category).task_set.get(id=task)
        data = _subtask_data_from_POST(req.POST)
        data = _validate_subtask_deadline(t, data)

        print data
        t.subtask_set.create(name=data['name'],
                             description=data['description'],
                             deadline=data['deadline'],
                             notify_user=data['notify_user'],
                             complete=False)

        _update_progress(t)

        return redirect('subtask', category=category, task=task)

class SubTaskEditView(LoginRequiredMixin, View):
    def get(self, req, category, task, subtask):
        viewitems = {
            'title': 'Editar Subtarea',
            'username': req.user.username,
            'number_deadlines': number_deadlines_from_user(req.user),
            'category': req.user.category_set.get(id=category),
            'task': req.user.category_set.get(id=category).task_set.get(id=task),
            'subtask': req.user.category_set.get(id=category).task_set.get(id=task).subtask_set.get(id=subtask)
        }
        return render(req, 'gst/subtask_edit.html', viewitems)

    def post(self, req, category, task, subtask):
        t = req.user.category_set.get(id=category).task_set.get(id=task)
        subtask = req.user.category_set.get(id=category).task_set.get(id=task).subtask_set.get(id=subtask)

        if req.POST.get('new_name'):
            subtask.name = req.POST.get('new_name', subtask.name)
        if req.POST.get('new_description'):
            subtask.description = req.POST.get('new_description', subtask.description)
        if 'new_deadline' in req.POST:
            if req.POST['new_deadline'] != "":
                subtask.deadline = req.POST['new_deadline']
        subtask.notify_user = bool(req.POST.get('new_notify_user', subtask.notify_user))
        subtask.complete = bool(req.POST.get('complete', subtask.complete))

        subtask.save()
        _update_progress(t)
        return redirect('subtask', category=category, task=task)

class SubTaskDeleteView(LoginRequiredMixin, View):
    def post(self, req, category, task, subtask):
        req.user.category_set.get(id=category).task_set.get(id=task).subtask_set.get(id=subtask).delete()
        t = req.user.category_set.get(id=category).task_set.get(id=task)
        _update_progress(t)
        return redirect('subtask', category=category, task=task)

def _subtask_data_from_POST(post):
    result = {
        'name': post.get('name', ''),
        'description': post.get('description', ''),
        'notify_user': True if post.get('notify_user', False) else False,
        'deadline': None if post.get('deadline', None) == '' else post.get('deadline'),
        'complete': True if post.get('complete', False) else False
    }

    # Check semantics
    if result['notify_user'] and (result['deadline'] is not None):
        try:
            result['deadline'] = parse_datetime(result['deadline'])
            if result['deadline'] is not None:
                result['deadline'] = timezone.make_aware(result['deadline'])
            else:
                result['notify_user'] = False
        except ValueError:
            result['notify_user'] = False
            result['deadline'] = None
    else:
        result['notify_user'] = False
        result['deadline'] = None

    return result

def _validate_subtask_deadline(task, subtask):
    if (task.deadline and subtask['notify_user'] and
        subtask['deadline'] > timezone.now() and
        subtask['deadline'] < task.deadline):
        print 'Datetime from subtask is invalid.'
        subtask['notify_user'] = False
        subtask['deadline'] = None


    return subtask


def _update_progress(task):

    all_subtask = task.subtask_set.all()
    print "all subtask: ", all_subtask

    quantity_subtask = len(all_subtask)
    print "\n cantidad subtask = ", quantity_subtask

    all_complete_subtask = all_subtask.filter(complete=True)
    print "all complete subtask: ", all_complete_subtask

    quantity_subtask_complete = len(all_complete_subtask)
    print "\n cantidad subtask completos = ", quantity_subtask_complete

    percent = quantity_subtask_complete * 100 / quantity_subtask
    task.progress = percent
    task.save()
