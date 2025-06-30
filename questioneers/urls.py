from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inquiry/', views.inquiry, name='inquiry'),
    path('inquiry/results/', views.inquiry_results, name='inquiry_results'),
    path('profile/', views.profile, name='profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)