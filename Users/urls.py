from django.conf.urls import url, include
from . import views

app_name = 'Users'

urlpatterns = [
    url(r'^logout/$',views.logout_view,name='logout'),
    url(r'^register/$', views.UserRegisterView.as_view(), name='register'),
    url(r'^login/$',views.UserLoginView.as_view(),name='login'),
    url(r'^profile/$',views.UserUpdateView.as_view(),name='profile'),
    url(r'^statistics/$',views.StatisticsView.as_view(),name='statistics'),
    
]
