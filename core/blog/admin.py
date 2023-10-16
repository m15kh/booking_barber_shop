from django.contrib import admin
from .models import Post , Comment
# Register your models here.


class CommentAdmin(admin.TabularInline):
    model = Comment
    extra = 1


class PostAdmin(admin.ModelAdmin):
    list_display = ('title','id',  'author', 'created_at', 'updated_at' ,'image')
    inlines = [CommentAdmin]


admin.site.register(Post, PostAdmin)
admin.site.register(Comment)
