from django.contrib import admin
from django.contrib.admin.options import ModelAdmin
from .models import Movie, Character, Category, MovieCategory, MovieCharacter

# Register your models here.

class MovieCategoryInline(admin.TabularInline):
    model = MovieCategory
    extra = 1

class MovieCharacterInline(admin.TabularInline):
    model = MovieCharacter
    extra = 1

class MovieAdmin(admin.ModelAdmin):
    #MovieとCategory、MovieとCharacterを同時に編集できるようにInlineを設定。
    inlines = [MovieCategoryInline, MovieCharacterInline] 
    list_display = (
        # 'id',
        'sort_order',
        'title',
        'publication_date',
        'screening_time',
        'movie_icon',
        'short_sumally',
        'short_detail',
        '_categories',
        '_characters',)

    list_display_links = (
        # 'id',
        'sort_order',
        'title',
        )

    def _categories(self,movie):
        return ','.join([category.title for category in movie.categories.all()])
    _categories.short_description = '楽しみ方'

    def _characters(self,movie):
        return ','.join([character.name for character in movie.characters.all()])
    _characters.short_description = '出演キャラ'
        
    
class CharacterAdmin(admin.ModelAdmin):
    #MovieとCharacterを同時に編集できるようにInlineを設定。
    inlines = [MovieCharacterInline]
    list_display = (
        'id',
        'name',
        '_movies')
    list_display_links = (
        'id',
        'name',)

    def _movies(self,character):
        return ','.join([movie.title for movie in character.movies.all()])

class CategoryAdmin(admin.ModelAdmin):
    #MovieとCategoryを同時に編集できるようにInlineを設定。
    inlines = [MovieCategoryInline] 
    list_display = (
        'id',
        'title',
        '_movies')
    list_display_links = (
        'id',
        'title',)
    
    def _movies(self,category):
        return ','.join([movie.title for movie in category.movies.all()])


admin.site.register(Movie, MovieAdmin)
admin.site.register(Character, CharacterAdmin)
admin.site.register(Category, CategoryAdmin)
