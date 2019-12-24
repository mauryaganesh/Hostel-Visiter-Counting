from django.conf.urls import url,include
from . import views
from django.urls import path
from login.views import login_form
urlpatterns = (
    url(r'^admno/$', views.admno, name='add_request'),
    url(r'^display/$', views.display),
    url(r'^$', views.login_form,name='home'),
    url(r'^login/$', views.login),
    url(r'^refuse/$', views.refuse),
    url(r'^allow/$', views.allow),
    url(r'^send_data/$', views.send_data),
    url(r'^post_send_data/$', views.post_send_data),
    url(r'^fetch_data/$', views.fetch_data),
    url(r'^logout/$', views.logout, name="logout")
    #url(r'^search/$', views.search),
    #url(r'^delete/$', views.delete),
    #url(r'^update/$', views.update),
    #url(r'^insert/$', views.insert),
)