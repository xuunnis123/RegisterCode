
from django.conf.urls import url
from manage_app import views
from django.urls import path
app_name='manage_app'
urlpatterns=[
    #url('',views.index,name='index'),
    path('', views.CodeListView.as_view(),name='list'),
    path('<int:pk>/', views.CodeDetailView.as_view(), name='detail'),
    path('create/',views.CodeCreateView.as_view(), name='create'),
    path('update/<int:pk>/', views.CodeUpdateView.as_view(), name='update'),
    path('delete/<int:pk>/', views.CodeDeleteView.as_view(), name='delete'),
    path('generate/',views.CodeGenView.as_view() , name='generate'),
    path('gen/',views.CodeGen, name='gen'),
    ]