from django.contrib import admin
from .models import Post, Category, PostCategory, Comment, Author

admin.site.register(Category)
admin.site.register(Post)
admin.site.register(PostCategory)
admin.site.register(Comment)
admin.site.register(Author)




# Register your models here.
