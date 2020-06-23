from django.conf.urls import url
from django.contrib import admin

from lists import views

urlpatterns = [
    url(r'^new$', views.new_list, name="new_list"),
    url(r'^(\d+)/$', views.view_lists, name="view_lists"),
    url(r'^(\d+)/share/$', views.share_list, name="share_lists"),
    url(r'^users/(.+)/$', views.my_lists, name="my_lists"),
]
