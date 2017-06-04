from django.conf.urls import url

from user_menu import views

app_name = 'companies'

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^get_takings/(?P<user_id>[0-9]+)$', views.get_takings, name='get_takings'),
    url(r'^create_test_takings/(?P<user_id>[0-9]+)$', views.create_test_takings, name='create_test_takings'),
]