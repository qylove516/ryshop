from django.urls import path, re_path, reverse, include
from django.shortcuts import HttpResponse, render, redirect
from django.utils.safestring import mark_safe
from django.apps.registry import apps

# 路由分发
from django.utils.text import capfirst
from django.views.decorators.cache import never_cache


# class ModelAdmin(object):
#     list_display = ["__str__", ]
#     list_display_links = []
#     modelform_class = None
#
#     def __init__(self, model, site):
#         self.model = model
#         self.site = site
#
#     def get_action_url(self, action, obj=None):
#         model_name = self.model._meta.model_name
#         app_label = self.model._meta.app_label
#         if obj:
#             _url = reverse("myadmin_%s_%s_%s" % (app_label, model_name, action), args=(obj.pk,))
#         else:
#             _url = reverse("myadmin_%s_%s_%s" % (app_label, model_name, action))
#         return _url
#
#     def edit(self, obj=None, header=False):
#         if header:
#             return "操作"
#         _url = self.get_action_url('change', obj)
#         return mark_safe("<a href='%s'>编辑</a>" % _url)
#
#     def delete(self, obj=None, header=False):
#         if header:
#             return "操作"
#         _url = self.get_action_url('delete', obj)
#
#         return mark_safe("<a href='%s'>删除</a>" % _url)
#
#     def new_list_play(self):
#         temp = []
#         temp.extend(self.list_display)
#         if not self.list_display_links:
#             # 类直接调用类方法，传入编辑方法，如果没有设置 link 则肯定有编辑方法，反之没有
#             temp.append(ModelAdmin.edit)
#         # 删除方法肯定传入
#         temp.append(ModelAdmin.delete)
#         return temp
#
#     def list_view(self, request):
#         data_obj = self.model.objects.all()
#
#         # 构建数据
#         data_array = []
#         for obj in data_obj:
#             temp = []
#             for field in self.new_list_play():
#                 if callable(field):
#                     val = field(self, obj)  # 为什么要加self?
#                 else:
#                     val = getattr(obj, field)
#                     if field in self.list_display_links:
#                         _url = self.get_action_url('change', obj)
#                         val = mark_safe("<a href='%s'>%s</a>" % (_url, val))
#                 temp.append(val)
#             data_array.append(temp)
#
#         # 构建表头
#         head_display = []
#         for field in self.new_list_play():
#             if callable(field):
#                 val = field(self, header=True)
#                 head_display.append(val)
#             else:
#                 if field == "__str__":
#                     # 如果没有写  list_display 变量
#                     head_display.append(self.model._meta.model_name.upper())
#                 else:
#                     val = self.model._meta.get_field(field).verbose_name
#                     head_display.append(val)
#         data_add = self.get_action_url('add')
#         return render(request, 'myadmin/views/list_views.html', {
#             'data_array': data_array,
#             'list_display': head_display,
#             'data_add': data_add
#         })
#
#     def add_view(self, request):
#         from django.forms import ModelForm
#
#         class MyAdminModelForm(ModelForm):
#
#             class Meta:
#                 model = self.model
#                 fields = "__all__"
#
#         form = MyAdminModelForm()
#         add_url = self.get_action_url('add')
#         if request.method == "POST":
#             data = MyAdminModelForm(request.POST)
#             if data.is_valid():
#                 data.save()
#                 ret = 1000
#         return render(request, 'myadmin/views/add_views.html', locals())
#
#     def change_view(self, request, id):
#
#         return render(request, 'myadmin/views/change_views.html')
#
#     def delete_view(self, request, id):
#         return render(request, 'myadmin/views/delete_views.html')
#
#     def get_urls2(self):
#         tmp = []
#         app_label = self.model._meta.app_label
#         model_name = self.model._meta.model_name
#         tmp.append(path('', self.list_view, name="myadmin_{}_{}".format(app_label, model_name)))
#         tmp.append(path('add/', self.add_view, name="myadmin_{}_{}_add".format(app_label, model_name)))
#         tmp.append(
#             re_path(r'^(\d+)/change/', self.change_view, name="myadmin_{}_{}_change".format(app_label, model_name)))
#         tmp.append(re_path(r'^(\d+)/delete/', self.delete, name="myadmin_{}_{}_delete".format(app_label, model_name)))
#         return tmp
#
#     @property
#     def urls2(self):
#         return self.get_urls2(), None, None


class MyAdminSite(object):
    def __init__(self, name='myadmin'):
        self.name = name
        self._registry = {}

    def dashboard(self, request):
        """返回面板主页，展示数据量"""
        return render(request, 'myadmin/dashboard.html')

    def _build_app_dict(self, reqeust, label=None):
        """
        :param reqeust:
        :param label:
        :return: 获取
        1、已注册的app
        2、app下的model名称
        3、model对应的url
        """
        app_dict = {}
        models = self._registry
        for model, model_admin in models.items():
            app_label = model._meta.app_label
            info = (app_label, model._meta.model_name)
            model_dict = {
                'name': capfirst(model._meta.verbose_name_plural),
                'object_name': model._meta.object_name,
                'myadmin_url': 'myadmin_{}_{}'.format(app_label, model._meta.model_name)
            }
            if app_label in app_dict:
                app_dict[app_label]['models'].append(model_dict)
            else:
                app_dict[app_label] = {
                    'name': apps.get_app_config(app_label).verbose_name,
                    'app_label': app_label,
                    'models': [model_dict]
                }
        return app_dict

    def get_app_list(self, request):
        """
        :param request:
        :return: 获取已注册的app
        """
        app_dict = self._build_app_dict(request)
        app_list = sorted(app_dict.values(), key=lambda x: x['name'].lower())
        for app in app_list:
            app['models'].sort(key=lambda x: x['name'])
        return app_list

    @never_cache
    def index(self, request):
        """
        返回首页显示内容:
        左边导航栏：
            一级：APP名称（显示每个app）
            二级：数据表（对应app下的数据表）
        :return:
        """
        app_list = self.get_app_list(request)
        return render(request, 'myadmin/index.html', {'app_list': app_list})

    def login(self, request):

        return render(request, 'myadmin/login.html')

    def get_urls(self):
        urlpatterns = [
            path('', self.login, name='login'),
            path('index/', self.index, name='index'),
            path('dashboard/', self.dashboard, name='dashboard')
        ]
        for model, model_class in self._registry.items():
            app_name = model._meta.app_label
            model_name = model._meta.model_name
            urlpatterns.append(path('{0}/{1}/'.format(app_name, model_name), include(model_class.urls)))
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls(), None, None

    def register(self, model, admin_class=None, **option):
        from myadmin.service.options import ModelAdmin
        if not admin_class:
            admin_class = ModelAdmin
        self._registry[model] = admin_class(model, self)


site = MyAdminSite()
