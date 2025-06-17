from django.contrib import admin
from .models import Dog, Review, Tag

@admin.register(Dog)
class DogAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'vote_ratio', 'vote_total', 'created')
    list_filter = ('tags', 'created')
    search_fields = ('name', 'description')
    ordering = ('-vote_ratio', '-vote_total')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('dog', 'owner', 'value', 'created')
    list_filter = ('value', 'created')
    search_fields = ('dog__name', 'owner__name', 'body')
    ordering = ('-created',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)
    search_fields = ('name',)
