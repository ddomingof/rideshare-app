# -*- coding: utf-8 -*-

"""URL routes for the CarPool web application."""

from django.conf.urls import url
from django.contrib import admin

from ui.views import (
    logout_view, my_commutes, new_commute, save_commute, search_commute, signin, signup, user_home,
    welcome, delete_commutes
)

admin.autodiscover()

urlpatterns = [
    url(r'^$', welcome, name='home_page'),
    url(r'^new_commute$', new_commute, name='new_commute'),
    url(r'^user_home$', user_home, name='user_home'),
    url(r'^signup', signup, name='signup'),
    url(r'^login', signin, name='login'),
    url(r'^save_commute$', save_commute, name='save_commute'),
    url(r'^logout$', logout_view, name='logout'),
    url(r'^search_commute$', search_commute, name='search_commute'),
    url(r'^my_commutes', my_commutes, name='my_commutes'),
    url(r'^delete_commutes', delete_commutes, name='delete_commutes'),
    url(r'^admin/', admin.site.urls),
]
