from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('Users/', views.user_list, name='user_list'),
    path('Users/Create/', views.user_create, name='user_create'),
    path('Users/Edit/<int:pk>/', views.user_update, name='user_update'),
    path('Users/Delete/<int:pk>/', views.user_delete, name='user_delete'),
    path('Users/Details/<int:pk>/', views.user_details, name='user_details'),

    path('Articles/', views.article_list, name='article_list'),
    path('Articles/Create/', views.article_create, name='article_create'),
    path('Articles/Edit/<int:pk>/', views.article_update, name='article_update'),
    path('Articles/Delete/<int:pk>/', views.article_delete, name='article_delete'),
    path('Articles/Details/<int:pk>/', views.article_details, name='article_details'),
    path('Articles/Search/', views.article_search, name='article_search'),

    path('Images/', views.image_list, name='image_list'),
    #path('images/<int:pk>/process/', views.image_process, name='image_process'),
    
    #path('images/<int:pk>/grayscale/', views.image_grayscale, name='image_grayscale'),
    #path('images/<int:pk>/resize/', views.image_resize, name='image_resize'),
    #path('images/<int:pk>/crop/', views.image_crop, name='image_crop'),
    path('Images/MultiModifications/', views.image_multi_modification, name='image_multi'),
    path('Images/Delete/', views.image_delete, name='image_delete'),

    #http://localhost:5277/Images/Details?fileName=jmeter_elements.drawio.png
    #http://localhost:5277/Images/Grayscale?fileName=jmeter_elements.drawio.png
    #http://localhost:5277/Images/Resize?fileName=jmeter_elements.drawio.png&width=256&height=256
    #http://localhost:5277/Images/Crop?fileName=jmeter_elements.drawio.png&x=100&y=100&width=200&height=200

    path('Images/Details', views.image_details, name='image_details'),
    path('Images/Grayscale', views.image_grayscale, name='image_grayscale'),
    path('Images/Resize', views.image_resize, name='image_resize'),
    path('Images/Crop', views.image_crop, name='image_crop'),

]