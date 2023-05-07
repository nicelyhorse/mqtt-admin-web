# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models


# Create your models here.
# 用户信息表
class user_list(models.Model):
    user_name = models.CharField(max_length=50)
    account = models.CharField(max_length=10, primary_key=True)
    pwd = models.CharField(max_length=20)
