from django.urls import path
from . import views
urlpatterns = [
    
    path('',views.home ,name='home'),
    path('login/',views.home, name="home"),
    path('landing_page/',views.landing_page,name='landing_page'),
    path('add_record/',views.add_record ,name='add_record'),
    path('logout/',views.logout_user ,name='logout_user'),
    path('register/',views.register_user ,name='register_user'),
    path('record/<int:pk>',views.record ,name='record'),
    path('delete_record/<int:pk>',views.delete_record ,name='delete_record'),
    path('update_record/<int:pk>',views.update_record ,name='update_record')
    
]
