from django.utils.html import format_html
from django.db import models
from account.models import User
from django.utils import timezone
from extensions.utils import jalali_converter
from django.urls import reverse


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status="p")
   

class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name="children", verbose_name="زیر دسته")
    title = models.CharField(max_length=200, verbose_name="عنوان دسته بندی")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="آدرس دسته بندی")
    status = models.BooleanField(default=True, verbose_name="آیا نمایش داده شود؟")
    position = models.IntegerField(verbose_name="پوزیشن")

    class Meta:
        verbose_name = "دسته بندی"
        verbose_name_plural = "دسته بندی ها"
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title
    
    objects = CategoryManager()

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', 'پیش نویس'),
        ('p', 'منتشرشده'),
        ('i', 'درحال بررسی'),
        ('b', 'برگشت داده شده')
    )
    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles', verbose_name="نویسنده")
    title = models.CharField(max_length=200, verbose_name="عنوان مقاله")
    slug = models.SlugField(max_length=100, unique=True, verbose_name="اسلاگ مقاله")
    category = models.ManyToManyField(Category, verbose_name="دسته بندی", related_name="articles")
    description = models.TextField(verbose_name="توضیحات")
    thumbnail = models.ImageField(upload_to="images", verbose_name="تصویر")
    publish = models.DateTimeField(default=timezone.now, verbose_name="زمان انتشار")
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False, verbose_name="مقاله ویژه")
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name="وضعیت")

    class Meta:
        verbose_name = "مقاله"
        verbose_name_plural = "مقالات"

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("account:home")
    
    def jpublish(self):
        return jalali_converter(self.publish)
    
    jpublish.short_description = "زمان انتشار"

    
    def thumbnail_tag(self):
        return format_html(f"<img width=70 src={self.thumbnail.url}>")
    
    thumbnail_tag.short_description = "عکس مقاله"

    def category_to_str(self):
        return ",".join([category.title for category in self.category.active()])
    
    category_to_str.short_description = "دسته بندی"

    objects = ArticleManager()

class Settings(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان وبلاگ")

    class Meta:
        verbose_name = "تنظیمات"
        verbose_name_plural = "تنظیمات"

    def __str__(self):
        return self.title


