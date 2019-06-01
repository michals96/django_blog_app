from django.contrib import admin

from wykop.posts.models import Post, Vote,Comment


class PostAdmin(admin.ModelAdmin):
    list_display = ('__str__', 'author')


admin.site.register(Post, PostAdmin)
admin.site.register(Vote)
admin.site.register(Comment)
