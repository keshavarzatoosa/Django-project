from django.utils.html import format_html
from django.db import models
from account.models import User
from django.utils import timezone
from extensions.utils import jalali_converter
from django.urls import reverse
from django.contrib.contenttypes.fields import GenericRelation
from comment.models import Comment
from django.utils.translation import pgettext_lazy as _


class ArticleManager(models.Manager):
    def published(self):
        return self.filter(status="p")


class CategoryManager(models.Manager):
    def active(self):
        return self.filter(status=True)


class Category(models.Model):
    parent = models.ForeignKey('self', default=None, null=True, blank=True, on_delete=models.SET_NULL, related_name="children", verbose_name=_("Category field", "Parent"))
    title = models.CharField(max_length=200, verbose_name=_("Category field", "Title"))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_("Category field", "Slug"))
    status = models.BooleanField(default=True, verbose_name=_("Category field", "Status"))
    position = models.IntegerField(verbose_name=_("Category field", "Position"))

    class Meta:
        verbose_name = _("Category model", "Category")
        verbose_name_plural = _("Category model", "Categories")
        ordering = ['parent__id', 'position']

    def __str__(self):
        return self.title
    
    objects = CategoryManager()

class Article(models.Model):
    STATUS_CHOICES = (
        ('d', _('Article status', 'Draf')),
        ('p', _('Article status', 'Publish')),
        ('i', _('Article status', 'Identify')),
        ('b', _('Article status', 'Back'))
    )

    author = models.ForeignKey(User, null=True, on_delete=models.SET_NULL, related_name='articles', verbose_name=_("Article field", "Author"))
    title = models.CharField(max_length=200, verbose_name=_("Article field", "Title"))
    slug = models.SlugField(max_length=100, unique=True, verbose_name=_("Article field", "Slug"))
    category = models.ManyToManyField(Category, verbose_name=_("Article field", "Category"), related_name="articles")
    description = models.TextField(verbose_name=_("Article field", "Description"))
    thumbnail = models.ImageField(upload_to="images", verbose_name=_("Article field", "Thumbnail"))
    publish = models.DateTimeField(default=timezone.now, verbose_name=_("Article field", "Publish"))
    created = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)
    is_special = models.BooleanField(default=False, verbose_name=_("Article field", "Is Special"))
    status = models.CharField(max_length=1, choices=STATUS_CHOICES, verbose_name=_("Article field", "Status"))
    comments = GenericRelation(Comment)

    class Meta:
        verbose_name = _("Article model", "article")
        verbose_name_plural = _("Article model", "articles")

    def __str__(self):
        return self.title
    
    def get_absolute_url(self):
        return reverse("account:home")
    
    def jpublish(self):
        return jalali_converter(self.publish)
    
    jpublish.short_description = _('Article method', 'Jpublish')
    
    def thumbnail_tag(self):
        return format_html(f"<img width=70 src={self.thumbnail.url}>")
    
    thumbnail_tag.short_description = _('Article method', 'ThumbnailTag')

    def category_to_str(self):
        return ",".join([category.title for category in self.category.active()])
    
    category_to_str.short_description = _('Article method', 'CategoryToStr')

    objects = ArticleManager()

class Settings(models.Model):
    title = models.CharField(max_length=200, verbose_name="عنوان وبلاگ")

    class Meta:
        verbose_name = "تنظیمات"
        verbose_name_plural = "تنظیمات"

    def __str__(self):
        return self.title


