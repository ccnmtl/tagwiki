import sets
from django.db import models
from django.contrib.auth.models import User
from django.http import Http404
from django.shortcuts import get_object_or_404
from django import forms
from tagging.models import Tag
from tagging.fields import TagField
from django.contrib import admin

class Page(models.Model):
    title = models.CharField(max_length=256)
    slug = models.SlugField()
    body = models.TextField(blank=True,default="")

    def get_all_tags(self):
        """ for templatetag compatibility """
        alltags = sets.Set()
        for pu in self.pageuser_set.all():
            for tag in pu.get_tags():
                alltags.add(tag)
        return alltags

    def get_user_tags(self,user):
        """ for templatetag compatibility """
        try:
            pu = self.pageuser_set.filter(user=user)[0]
        except IndexError:
            return []
        return pu.get_tags()

    def get_absolute_url(self):
        return "/page/%s/" % self.slug
        

class PageUser(models.Model):
    page = models.ForeignKey(Page)
    user = models.ForeignKey(User)
    tags = TagField()

    def set_tags(self, tags):
        Tag.objects.update_tags(self, tags)

    def get_tags(self):
        return Tag.objects.get_for_object(self)      

    def get_item(self):
        """ for templatetag compatibility """
        return self.page

class PageAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}

admin.site.register(Page,PageAdmin)
