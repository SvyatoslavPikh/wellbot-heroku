from user_menu import views
from django.conf.urls import url
from django.contrib import admin

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^user_menu/', views.index, name="user_menu"),
]
