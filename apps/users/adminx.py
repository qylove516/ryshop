import xadmin
from users import models
from django.contrib.auth.models import User


class UserAdmin(object):
    list_display = ['username', 'gender', 'email']
    search_fields = ['username']
    list_filter = ['username']
    refresh_times = (3,)  # 数据刷新时间
    show_detail_fields = ['username', 'gender']  # 在admin字段下面会有一个标志，点击显示详细信息
    list_editable = ['username', 'gender']  # 即时编辑字段信息


xadmin.site.unregister(models.UserProfile)  # 因为UserProfile已经注册过了，所以要先把注册去掉
xadmin.site.register(models.UserProfile, UserAdmin)

# xadmin全局配置
from xadmin import views


class BaseSetting(object):
    enable_themes = True
    use_bootswatch = True


xadmin.site.register(views.BaseAdminView, BaseSetting)


# 全局页头和页脚配置
class GlobalSetting(object):
    site_title = '瑞银积分商城后台管理系统'
    site_footer = '瑞银产业'
    menu_style = "accordion"  # 折叠左侧app菜单，必须放在 GlobalSetting 中


xadmin.site.register(views.CommAdminView, GlobalSetting)
