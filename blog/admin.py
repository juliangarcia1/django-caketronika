from django.contrib import admin


from .models import (Author, Post, Category, SubCategory,
                     Comment)


class PostAdmin(admin.ModelAdmin):
    list_display = ('title',
                    'author',
                    'published')
    fields = ['title','author',
              ('published', 'category', 'subcategory'),
              'body']
class CommentAdmin(admin.ModelAdmin):
    list_display = ( 'author',
                     'post',
                     'created_at',
                     'active')
    list_filter = ( 'active',
                    'created_at',
                    'updated_at')
    search_fields = ('author',
                     'body')


admin.site.register(Author)
admin.site.register(Post, PostAdmin)
admin.site.register(Category)
admin.site.register(SubCategory)
admin.site.register(Comment, CommentAdmin)
