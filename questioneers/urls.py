from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', views.signin, name='signin'),
    path('signup/', views.signup, name='signup'),
    path('signout/', views.signout, name='signout'),
    path('reset-password/', views.reset_password, name='reset-password'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name='authenticate/password_reset_confirm.html'
    ), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(
        template_name='authenticate/password_reset_complete.html'
    ), name='password_reset_complete'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('inquiry/', views.inquiry, name='inquiry'),
    path('inquiry/results/', views.inquiry_results, name='inquiry_results'),
    path('inquiry/history/', views.inquiry_all_results, name='inquiry_all_results'),
    path('profile/', views.profile, name='profile'),
]
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)