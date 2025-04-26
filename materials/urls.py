from django.urls import path
from . import views
urlpatterns = [
    path('add-subject/', views.add_subject_view, name='add_subject'),
    path('add-content/', views.add_content_view, name='add_content'),
    path('choose/', views.choose_subject, name='choose'),
    path('show/<int:id>', views.show_content, name='show'),
    path('home/', views.home_view, name='home'),
    path('detail/<int:pk>/', views.detail_view, name='detail'),
    path('chatbot/', views.chatbot_view, name='chatbot'),
    path('edit/<int:id>', views.edit_view, name='edit'),
    path('delete/<int:id>', views.delete_view, name='delete'),
]


