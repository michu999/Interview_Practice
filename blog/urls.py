from django.urls import path
from . import views

app_name = 'blog'

urlpatterns = [
    path('', views.post_list, name='post_list'),
    path('post/<int:pk>/', views.post_detail, name='post_detail'),
    path('post/<int:pk>/rate/', views.submit_rating, name='submit_rating'),
    path('ai/add/', views.add_ai_post, name='add_ai_post'),
]

