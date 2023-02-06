from django.urls import path, include
# from .views import

urlpatterns = [
    path('todo/v1/client/', include("todo.todo_v1_client.urls"))
]