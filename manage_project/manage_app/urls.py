
from django.conf.urls import url
from manage_app import views

urlpatterns=[
    url('',views.index,name='index'),
    url('/userAddUser',views.addUser,name='addUser'),
    ]