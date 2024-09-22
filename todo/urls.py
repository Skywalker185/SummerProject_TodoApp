

from django.urls import path
from . import views

from .views import index, toggle_task_completion,category_tasks_view, create_task_from_template, DeleteTemplateView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('', index, name='list'),
    path('tasks/category/<str:category>/', category_tasks_view, name='category_tasks'),
    path('create-from-template/<int:template_id>/', create_task_from_template, name='create_task_from_template'),
    path('<int:pk>/delete_template', DeleteTemplateView.as_view(), name='delete_template'),
    path('<str:pk>/update_task/', login_required(views.updateTask), name='update_task'),
    path('<str:pk>/delete_task/', login_required(views.deleteTask), name='delete_task'),
    path('logout/', views.logout_view, name='logout'),
    path('toggle/<int:pk>/', toggle_task_completion, name='toggle_task_completion'),
]