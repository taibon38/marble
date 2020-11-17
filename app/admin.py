from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Movie, Character, Category ,MovieCategory, MovieCharacter

# Register your models here.

class MovieCategoryInline(admin.TabularInline):
    model = MovieCategory
    extra = 1

class MovieCharacterInline(admin.TabularInline):
    model = MovieCharacter
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    inlines = [MovieCategoryInline, MovieCharacterInline] #MovieとCategoryを同時に編集できるようにInlineを設定。
    list_display = (
        'id',
        'title',
        'publication_date',
        'screening_time',
        'movie_icon')
    list_display_links = (
        'id',
        'title',
        'publication_date',
        'screening_time',
        'movie_icon')
    

class CaracterAdmin(admin.ModelAdmin):
    inlines = [MovieCharacterInline]
    list_display = (
        'id',
        'name',)
    list_display_links = (
        'id',
        'name',)


class CategoryAdmin(admin.ModelAdmin):
    inlines = [MovieCategoryInline] #MovieとCategoryを同時に編集できるようにInlineを設定。
    list_display = (
        'id',
        'title',)
    list_display_links = (
        'id',
        'title',)


admin.site.register(Movie, MovieAdmin)
admin.site.register(Character, CaracterAdmin)
admin.site.register(Category, CategoryAdmin)
