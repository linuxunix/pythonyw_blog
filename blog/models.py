#_*_coding:utf-8_*_
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User

class Article(models.Model):
    title = models.CharField(max_length=254,verbose_name=u'标题')
    type_choices=(
        (u'Linux运维',u'Linux运维'),
        (u'Python编程',u'Python编程'),
    )

    type = models.CharField(choices=type_choices, max_length=128,verbose_name=u'分类')
    category = models.ForeignKey('Category',verbose_name=u'标签')
    summary = models.TextField(max_length=500)
    author = models.ForeignKey('UserProfile')
    content = models.TextField(max_length=100000)
    head_img = models.ImageField(upload_to="static/imgs/upload")
    publish_date =models.DateTimeField(auto_now_add=True,verbose_name=u'创建时间')
    def __unicode__(self):
        return self.title

class Category(models.Model):
    name = models.CharField(unique=True,max_length=64)
    def __unicode__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    name = models.CharField(max_length=32)
    def __unicode__(self):
        return self.name
