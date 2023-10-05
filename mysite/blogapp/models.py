'''
Модели приложения Блог
'''

from django.db import models
from django.utils.translation import gettext_lazy as _

class Author(models.Model):
    class Meta:
        ordering = ["name"]
        verbose_name = _("Author")
        verbose_name_plural = _("Authors")

    name = models.CharField(max_length=100, null=False, blank=False, db_index=True)
    bio = models.TextField(null=False, blank=True)

    def __str__(self) -> str:
        description = _("Author")
        return f"{description} {self.name!r} (pk={self.pk})"
    
class Category(models.Model):
    class Meta:
        verbose_name = _("Category")
        verbose_name_plural = _("Categories")

    name = models.CharField(max_length=40, null=False, blank=False, db_index=True)

    def __str__(self) -> str:
        description = _("Category")
        return f"{description} {self.name!r} (pk={self.pk})"

class Tag(models.Model):
    class Meta:
        verbose_name = _("Tag")
        verbose_name_plural = _("Tags")

    name = models.CharField(max_length=20, null=False, blank=False, db_index=True)

    def __str__(self) -> str:
        description = _("Tag")
        return f"{description} {self.name!r} (pk={self.pk})"
    
class Article(models.Model):
    class Meta:
        ordering = ["pub_date", "title"]
        verbose_name = _("Article")
        verbose_name_plural = _("Articles")

    title = models.CharField(max_length=200, null=False, blank=False, db_index=True)
    content = models.TextField(null=False, blank=True)
    pub_date = models.DateTimeField(auto_now_add=True)
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tags = models.ManyToManyField(Tag,  related_name="article")

    def __str__(self) -> str:
        description = _("Article")
        return f"{description} {self.title!r} (pk={self.pk})"