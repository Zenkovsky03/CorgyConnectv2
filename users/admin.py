from django.contrib import admin
from .models import Profile, Skill, Message

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'name', 'email', 'location', 'created')
    list_filter = ('location', 'created')
    search_fields = ('username', 'name', 'email', 'location')
    ordering = ('-created',)

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'created')
    list_filter = ('created',)
    search_fields = ('name', 'owner__name', 'owner__username')
    ordering = ('-created',)

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ('subject', 'sender', 'recipient', 'is_read', 'created')
    list_filter = ('is_read', 'created')
    search_fields = ('subject', 'body', 'sender__username', 'recipient__username')
    ordering = ('is_read', '-created')
