from django.contrib import admin
from .models import Article, Category, Settings

# admin header change
admin.site.site_header = "پنل ادمین"

# delete an action in general
admin.site.disable_action('delete_selected')

# add an action
def make_published(modeladmin, request, queryset):
    row_updated = queryset.update(status="p")
    if row_updated == 1:
        message_bit = "منتشر شد"
    else:
        message_bit = "منتشر شدند"
    modeladmin.message_user(request, f"تعداد {row_updated} مقاله {message_bit}")
make_published.short_description = "انتشار مقالات انتخاب شده"


class CategoryAdmin(admin.ModelAdmin):
    list_display = ('position', 'title', 'slug', 'status', 'parent')
    list_filter = (['status'])
    search_fields = ('title', 'slug')
    prepopulated_fields = {'slug': ('title',)}
admin.site.register(Category, CategoryAdmin)


class ArticleAdmin(admin.ModelAdmin):
    list_display = ('title', 'thumbnail_tag', 'slug', 'jpublish', 'status', 'category_to_str')
    list_filter = ('publish', 'status')
    search_fields = ('title', 'description')
    prepopulated_fields = {'slug': ('title',)}
    ordering = ['-status', 'publish']
    actions = [make_published]

    def category_to_str(self, obj):
        return ",".join([category.title for category in obj.active()])
    
    category_to_str.short_description = "دسته بندی"

admin.site.register(Article, ArticleAdmin)


class SettingsAdmin(admin.ModelAdmin):
    list_display = ('title',)
    list_filter = (['title'])
    search_fields = ('title',)
admin.site.register(Settings, SettingsAdmin)
