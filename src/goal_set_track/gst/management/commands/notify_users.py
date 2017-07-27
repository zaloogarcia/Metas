from django.core.management.base import BaseCommand, CommandError
from gst.models import Category, Task, SubTask
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.utils import timezone
from email import Email

def get_logged_out_users():
    active_sessions = Session.objects.filter(expire_date__gte=timezone.now())
    user_id_list = []
    for session in active_sessions:
        data = session.get_decoded()
        user_id_list.append(data.get('_auth_user_id', None))
    # Query all logged in users based on id list
    return User.objects.exclude(id__in=user_id_list)

def is_deadline_near(date):
    if date > timezone.now():
        delta = date - timezone.now()
        return delta.days == 0

class Command(BaseCommand):
    help = 'Checks for tasks/subtasks near deadlines and notify users.'

    def handle(self, *args, **options):
        subject = 'Tareas por vencer!'
        for user in get_logged_out_users():
            print(user.username)
            deadlines = []
            for category in user.category_set.all():
                for task in category.task_set.all():
                    if (task.notify_user and not task.complete and
                        is_deadline_near(task.deadline)):
                        deadlines.append(task)
                    for subtask in task.subtask_set.all():
                        if (subtask.notify_user and not subtask.complete and
                            is_deadline_near(subtask.deadline)):
                            deadlines.append(subtask)

            if len(deadlines) > 0:
                message = ''
                message += 'Gracias por usar GST!\n'
                message += 'Usted tiene {} tareas por vencer:\n\n'.format(len(deadlines))
                for deadline in deadlines:
                    message += '\t+ Tarea: {} - Vence: {}'.format(str(deadline.name),
                                                              deadline.deadline.strftime(
                                                                       '%Y-%m-%d %H:%M:%S %z'))

                Email().send(user.email, subject, message)
