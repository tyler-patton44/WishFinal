from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index),
    url(r'addWish$', views.addWish),
    url(r'add$', views.add),
    url(r'delete/(?P<id>\d+)$', views.deletor),
    url(r'editWish/(?P<id>\d+)$', views.editWish),
    url(r'edit$', views.edit),
    url(r'grant/(?P<id>\d+)$', views.grant),
    url(r'like/(?P<id>\d+)$', views.like),
    url(r'status$', views.status),
    url(r'logout$', views.logout),
]