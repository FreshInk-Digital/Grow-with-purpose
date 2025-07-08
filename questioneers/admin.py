from django.contrib import admin
from .models import UserProfile, Inquiry


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'bio')
    search_fields = ('user__username', 'user__email', 'bio')


@admin.register(Inquiry)
class InquiryAdmin(admin.ModelAdmin):
    list_display = ('user', 'submitted_at', 'create', 'study', 'work')
    list_filter = ('submitted_at',)
    search_fields = ('user__username', 'create', 'study', 'work', 'feel', 'move', 'be', 'connect')
    ordering = ('-submitted_at',)
