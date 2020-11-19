from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.utils.translation import ugettext_lazy as _
from .models import WatchedMovie, FavedMovie,   FavedCharacter, User

# Register your models here.


class MyUserChangeForm(UserChangeForm):
    """User情報を変更するフォーム"""
    class Meta:
        model = User
        fields = '__all__'  # 全ての情報を変更可能


class MyUserCreationForm(UserCreationForm):
    """User を作成するフォーム"""
    class Meta:
        model = User
        fields = ('email',)  # email とパスワードが必要


class MyUserAdmin(UserAdmin):
    """カスタムユーザーモデルの Admin"""
    fieldsets = (
        (None, {
            'fields': ('username','email', 'password', 'profile_icon')}),
        (_('Permissions'), {'fields':
                            ('is_active', 'is_staff', 'is_superuser', 'groups',
                                'user_permissions')}),
        (_('Important dates'), {'fields':
                                ('last_login', 'date_joined')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'password1', 'password2'),
        }),
    )
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    list_display = ('username', 'email', 'is_staff')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'groups')
    search_fields = ('email',)
    ordering = ('email',)


class FavedCharacterAdmin(admin.ModelAdmin):
    list_display = ('user','character', 'created_at')


class FavedMovieAdmin(admin.ModelAdmin):
    list_display = ('user','movie', 'created_at')


class WatchedMovieAdmin(admin.ModelAdmin):
    list_display = ('user','movie', 'created_at')


admin.site.register(User, MyUserAdmin)
admin.site.register(FavedCharacter, FavedCharacterAdmin)
admin.site.register(FavedMovie, FavedMovieAdmin)
admin.site.register(WatchedMovie, WatchedMovieAdmin)