from django.conf.urls import url
from . import views           # This line is new!
urlpatterns = [
  url(r'^$', views.index),
  url(r'^main', views.index),
  url(r'^register', views.register),
  url(r'^login', views.login),
  url(r'^quotes', views.quotes),
  url(r'^logout$', views.logout),
  url(r'^addquotes$', views.addquotes),
  url(r'^addlists$', views.addlists),
  url(r'^relists$', views.relists),
  url(r'^users/(?P<user_id>\d+)$', views.showuser)
  ]



