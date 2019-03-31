from django.contrib import admin
from django.template.loader import render_to_string
from django.utils.safestring import mark_safe
from django.contrib.admin import SimpleListFilter

from goods import models


class EventAdminSite(admin.AdminSite):
    def get_app_list(self, request):
        """ Return a sorted list of all the installed apps that have been registered in this site. """
        ordering = {"Shop": 1, "Goods": 2, "Price": 3, "Order": 4}
        app_dict = self._build_app_dict(request)  # a.sort(key=lambda x: b.index(x[0])) # Sort the apps alphabetically.
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        # Sort the models alphabetically within each app.
        for app in app_list:
            app['models'].sort(key=lambda x: ordering[x['name']])
        return app_list


class GoodsAdmin(admin.ModelAdmin):

    # 这种方式可以让图片在编辑内容页面以只读的方法显示
    def image_onload(self, obj):
        try:
            img = mark_safe('<img src="{}" width=50px>'.format(obj.image.url))
        except Exception as e:
            # 此处可以展示一个图片的默认路径
            img = '请上传图片'
        return img

    image_onload.short_description = '预览'
    image_onload.allow_tags = True
    # 显示的字段，字段可以在model处理，如：加html标签（添加着色，加粗...）
    list_display = ['name', 'colored_desc', 'date', 'price', 'image_onload']
    readonly_fields = ['image_onload']
    # 排序,可以使用多个字段进行排序
    ordering = ['name', 'date', 'price']
    # 过虑字段 这里如果写 ‘date'则 可选择任意两个日期,注：日期搜索有bug
    list_filter = ['shop', 'price']
    # 日期字段特殊处理，...即在选项框上面显示  2019 三月6  此种形式
    date_hierarchy = 'date'
    # 搜索字段
    search_fields = ('name',)
    # 多对多字段编辑美化处理(并排显示)
    filter_horizontal = ('shop',)
    # 多对多字段编辑美化处理(并列显示)
    # filter_vertical = ('shop', )
    # 分布，每页显示的数据量
    list_per_page = 2
    # 通过 date 可以点击进入编辑
    list_display_links = ['date']
    # 在展示页面进行编辑
    list_editable = ('name',)
    # 字段可以分开按分类进行显示，此字段与fields字段有冲突，只能使用其中的一个
    fieldsets = [
        ('基本信息', {'fields': ['name', 'price', 'discount', 'desc', 'image', 'image_onload']}),
        ('商家', {'fields': ['shop']})
    ]


class ShopAdmin(admin.ModelAdmin):
    list_display = ['name', 'address', 'image_img']


class PriceFilter(admin.SimpleListFilter):
    """
    自定义价格过滤器
    """
    title = '价格'
    parameter_name = 'nums'
    lookup_kwarg = 'nums'

    def lookups(self, request, model_admin):
        return (
            ('0', '高价'),
            ('1', '中价'),
            ('3', '低价'),
        )

    def queryset(self, request, queryset):
        if self.value() == '0':
            return queryset.filter(num__gt='555')
        if self.value() == '1':
            return queryset.filter(num__gte='222', num__lte='555')
        if self.value() == '3':
            return queryset.filter(num__lt='222')


class PriceAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', 'num']
    ordering = ['-num']
    list_filter = [PriceFilter, ]


admin.site.register(models.Goods, GoodsAdmin)
admin.site.register(models.Shop, ShopAdmin)
admin.site.register(models.Price, PriceAdmin)

admin.site.site_header = '积分平台'
admin.site.site_title = '瑞银'


class OrderAdmin(admin.ModelAdmin):
    list_filter = ['name']
    list_display = ['name', 'num', 'content']


admin.site.register(models.Order, OrderAdmin)


from django.utils.translation import ugettext_lazy as _
from django.template.loader import render_to_string


class AdminThumbnail(object):
    """
    重写函数
    """
    short_description = _('Thumbnail')
    allow_tags = True

    def __init__(self, image_field, template=None, image_name=None):
        """
        :param image_field: 展示的字段.
        :param template: 模板文件

        """
        self.image_name = image_name
        self.image_field = image_field
        self.template = template

    def __call__(self, obj):
        if callable(self.image_field):
            thumbnail = self.image_field(obj)
        else:
            try:
                thumbnail = getattr(obj, self.image_field)
            except AttributeError:
                raise Exception('The property %s is not defined on %s.' %
                        (self.image_field, obj.__class__.__name__))

        original_image = getattr(thumbnail, 'source', None) or thumbnail
        template = self.template or 'imagekit/admin/thumbnail.html'

        return render_to_string(template, {
            'image_name': self.image_name,
            'model': obj,
            'thumbnail': thumbnail,
            'original_image': original_image,
        })


@admin.register(models.Profile)
class ProfileAdmin(admin.ModelAdmin):
    # image_name 使用  'id_' + 图片模型字段名称
    admin_thumbnail = AdminThumbnail(image_field='avatar_thumbnail', template='admin/thumbnail.html', image_name='id_avatar')
    list_display = ('id',)
    admin_thumbnail.short_description = '预览'
    readonly_fields = ('admin_thumbnail',)
