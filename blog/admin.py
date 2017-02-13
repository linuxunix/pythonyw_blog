from django.contrib import admin
from  blog import models
# Register your models here.

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title','category','publish_date')
admin.site.register(models.Article,ArticleAdmin)
admin.site.register(models.Category)
admin.site.register(models.UserProfile)


