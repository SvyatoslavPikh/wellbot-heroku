from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

from user_menu import views


urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^db', views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^user_menu/', views.index, name="user_menu"),
]
