import json
from django.db import models
from django.utils import timezone
from django.conf import settings
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import ugettext_lazy as _, ugettext
from django.utils.encoding import smart_text

from django.db.models.signals import post_migrate
from django.contrib.auth.models import Permission

AUTH_USER_MODEL = getattr(settings, 'AUTH_USER_MODEL', 'auth.User')


def add_view_permissions(sender, **kwargs):
    """
    生成权限系统
    """
    # 循环每个数据表
    for content_type in ContentType.objects.all():
        # 权限方式
        codename = "view_%s" % content_type.model
        # 如果对某个数据库的权限不存在，就创建
        if not Permission.objects.filter(content_type=content_type, codename=codename):
            Permission.objects.create(
                content_type=content_type,
                codename=codename,
                name="Can view %s" % content_type.name
            )


# 执行migrate命令之后触发
post_migrate.connect(add_view_permissions)


class Log(models.Model):
    action_time = models.DateTimeField(
        _('action time'),
        default=timezone.now,
        editable=False,
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL,
        models.CASCADE,
        verbose_name=_('user'),
        related_name='log_user_item'
    )
    ip_addr = models.GenericIPAddressField(_('action ip'), blank=True, null=True)
    content_type = models.ForeignKey(
        ContentType,
        models.SET_NULL,
        verbose_name=_('content type'),
        blank=True, null=True,
        related_name='log_content_type_item'
    )
    object_id = models.TextField(_('object id'), blank=True, null=True)
    object_repr = models.CharField(_('object repr'), max_length=200)
    action_flag = models.CharField(_('action flag'), max_length=32)
    message = models.TextField(_('change message'), blank=True)

    class Meta:
        verbose_name = _('log entry')
        verbose_name_plural = _('log entries')
        ordering = ('-action_time',)

    def __repr__(self):
        return smart_text(self.action_time)

    def __str__(self):
        if self.action_flag == 'create':
            return ugettext('Added "%(object)s".') % {'object': self.object_repr}
        elif self.action_flag == 'change':
            return ugettext('Changed "%(object)s" - %(changes)s') % {
                'object': self.object_repr,
                'changes': self.message,
            }
        elif self.action_flag == 'delete' and self.object_repr:
            return ugettext('Deleted "%(object)s."') % {'object': self.object_repr}

        return self.message

    def get_edited_object(self):
        """
        :return: 已编辑的对象
        """
        return self.content_type.get_object_for_this_type(pk=self.object_id)
