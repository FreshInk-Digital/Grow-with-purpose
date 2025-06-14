# myapp/urls.py
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup', views.signup, name='signup'), 
    path('dashboard', views.dashboard, name='dashboard'),
    path('inquiry', views.inquiry, name='inquiry'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)