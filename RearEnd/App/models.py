from django.db import models


# Create your models here.

class UserManage(models.Model):
    id = models.CharField(max_length=64, primary_key=True, verbose_name="用户ID")
    rid = models.IntegerField(verbose_name="用户角色ID", default=0)
    username = models.CharField(max_length=32, verbose_name="用户名", null=True, blank=True)
    password = models.CharField(max_length=32, verbose_name="密码", null=True, blank=True)
    email = models.EmailField(verbose_name="用户邮箱", null=True, blank=True)
    phone = models.CharField(max_length=15, verbose_name="用户手机号", null=True, blank=True)
    token = models.CharField(max_length=255, verbose_name="用户登录Token", blank=True, null=True)
    login_time = models.DateTimeField(verbose_name="用户登陆时间")

    def __str__(self):
        return self.username

    class Meta:
        verbose_name_plural = "user_manage"
        db_table = verbose_name_plural
