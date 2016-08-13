
from django.conf.urls import include, url
from .views import mindeview

urlpatterns = [
	url(r'^091bc6e289d9c872b4afb3f25827870b584a42e6f89ffc5516/?$', mindeview.as_view()) 
]