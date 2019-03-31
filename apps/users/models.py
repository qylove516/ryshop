from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class UserProfile(AbstractUser):
    """
    重写用户
    """
    gender = models.CharField('性别', max_length=32, choices=(('male', '男'), ('female', '女')), default='male')
    mobile = models.CharField('联系电话', max_length=11, blank=True, null=True)

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = '用户'
        verbose_name_plural = '用户'
