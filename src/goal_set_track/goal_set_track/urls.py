"""goal_set_track URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.conf.urls import url
from django.contrib import admin
from gst.views import user, task, subtask, category, comment, deadline, file, statistics

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', user.home, name='home'),
    url(r'^about/$', user.AboutView.as_view(), name='about'),

    url(r'^login/$', user.LoginView.as_view(), name='login'),
    url(r'^logout/$', user.LogoutView.as_view(), name='logout'),
    url(r'^register/$', user.RegisterView.as_view(), name='register'),
    url(r'^me/$', user.UserView.as_view(), name='user'),
    url(r'^me/edit/$', user.UserEditView.as_view(), name='user_edit'),

    url(r'^deadlines/$', deadline.DeadlinesView.as_view(), name='deadlines'),
    url(r'^number_deadlines/$', deadline.DeadlinesAmmountView.as_view(), name='number_deadlines'),

    url(r'^statistics/$', statistics.StatisticsView.as_view(), name='statistics'),

    url(r'^category/$', category.CategoryView.as_view(), name='category'),
    url(r'^category/create/$', category.CategoryCreateView.as_view(), name='category_create'),
    url(r'^category/(?P<category>[\w]+)/edit/$', category.CategoryEditView.as_view(), name='category_edit'),
    url(r'^category/(?P<category>[\w]+)/delete/$', category.CategoryDeleteView.as_view(), name='category_delete'),

    url(r'^category/(?P<category>[\w]+)/$', task.TaskView.as_view(), name='task'),
    url(r'^category/(?P<category>[\w]+)/task/create/$', task.TaskCreateView.as_view(), name='task_create'),
    url(r'^category/(?P<category>[\w]+)/task/(?P<task>[\w]+)/edit/$', task.TaskEditView.as_view(), name='task_edit'),
    url(r'^category/(?P<category>[\w]+)/task/(?P<task>[\w]+)/delete/$', task.TaskDeleteView.as_view(), name='task_delete'),

    url(r'^category/(?P<category>[\w]+)/task/(?P<task>[\w]+)/comment/create/$', comment.CommentCreateView.as_view(), name='comment_create'),
    url(r'^category/(?P<category>[\w]+)/task/(?P<task>[\w]+)/comment/(?P<comment>[\w]+)/delete/$', comment.CommentDeleteView.as_view(), name='comment_delete'),
    url(r'^category/(?P<category>[\w]+)/task/(?P<task>[\w]+)/comment/(?P<comment>[\w]+)/edit/$', comment.CommentEditView.as_view(), name='comment_edit'),


    #  Attached Files ****
    url(r'^category/(?P<category>[\w]+)/task/(?P<task>[\w]+)/file/$',     file.FileView.as_view(), name='file'),
    url(r'^category/(?P<category>[\w]+)/task/(?P<task>[\w]+)/file/add/$', file.FileAddView.as_view(), name='file_add'),
    url(r'^category/(?P<category>[\w]+)/task/(?P<task>[\w]+)/file/(?P<file>[\w]+)/delete/$', file.FileDeleteView.as_view(), name='file_delete'),
    url(r'^category/(?P<category>[\w]+)/task/(?P<task>[\w]+)/file/(?P<file>[\w]+)/dowload/$', file.FileDowloadView.as_view(), name='file_dowload'),
    # ********

    url(r'^category/(?P<category>[\w]+)/task/(?P<task>[\w]+)/$', subtask.SubTaskView.as_view(), name='subtask'),
    url(r'^category/(?P<category>[\w]+)/task/(?P<task>[\w]+)/subtask/create/$', subtask.SubTaskCreateView.as_view(), name='subtask_create'),
    url(r'^category/(?P<category>[\w]+)/task/(?P<task>[\w]+)/subtask/(?P<subtask>[\w]+)/edit/$', subtask.SubTaskEditView.as_view(), name='subtask_edit'),
    url(r'^category/(?P<category>[\w]+)/task/(?P<task>[\w]+)/subtask/(?P<subtask>[\w]+)/delete/$', subtask.SubTaskDeleteView.as_view(), name='subtask_delete'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
