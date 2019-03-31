from django.shortcuts import reverse, render
from django.urls import re_path, path
from django.utils.decorators import method_decorator
from django.utils.safestring import mark_safe
from django.views.decorators.csrf import csrf_protect

csrf_protect_m = method_decorator(csrf_protect)


class ModelAdmin(object):
    list_display = ["__str__", ]
    list_display_links = []
    modelform_class = None

    def __init__(self, model, site):
        self.model = model
        self.site = site

    def get_action_url(self, action, obj=None):
        model_name = self.model._meta.model_name
        app_label = self.model._meta.app_label
        if obj:
            _url = reverse("myadmin_%s_%s_%s" % (app_label, model_name, action), args=(obj.pk,))
        else:
            _url = reverse("myadmin_%s_%s_%s" % (app_label, model_name, action))
        return _url

    def edit(self, obj=None, header=False):
        if header:
            return "操作"
        _url = self.get_action_url('change', obj)
        return mark_safe("<a href='%s'>编辑</a>" % _url)

    def delete(self, obj=None, header=False):
        if header:
            return "操作"
        _url = self.get_action_url('delete', obj)

        return mark_safe("<a href='%s'>删除</a>" % _url)

    def new_list_play(self):
        temp = []
        temp.extend(self.list_display)
        if not self.list_display_links:
            # 类直接调用类方法，传入编辑方法，如果没有设置 link 则肯定有编辑方法，反之没有
            temp.append(ModelAdmin.edit)
        # 删除方法肯定传入
        temp.append(ModelAdmin.delete)
        return temp

    @csrf_protect_m
    def list_view(self, request):
        data_obj = self.model.objects.all()

        # 构建数据
        data_array = []
        for obj in data_obj:
            temp = []
            for field in self.new_list_play():
                if callable(field):
                    val = field(self, obj)  # 为什么要加self?
                else:
                    val = getattr(obj, field)
                    if field in self.list_display_links:
                        _url = self.get_action_url('change', obj)
                        val = mark_safe("<a href='%s'>%s</a>" % (_url, val))
                temp.append(val)
            data_array.append(temp)

        # 构建表头
        head_display = []
        for field in self.new_list_play():
            if callable(field):
                val = field(self, header=True)
                head_display.append(val)
            else:
                if field == "__str__":
                    # 如果没有写  list_display 变量
                    head_display.append(self.model._meta.model_name.upper())
                else:
                    val = self.model._meta.get_field(field).verbose_name
                    head_display.append(val)
        data_add = self.get_action_url('add')
        return render(request, 'myadmin/views/list_views.html', {
            'data_array': data_array,
            'list_display': head_display,
            'data_add': data_add
        })

    @csrf_protect_m
    def add_view(self, request):
        from django.forms import ModelForm

        class MyAdminModelForm(ModelForm):

            class Meta:
                model = self.model
                fields = "__all__"

        form = MyAdminModelForm()
        add_url = self.get_action_url('add')
        if request.method == "POST":
            data = MyAdminModelForm(request.POST)
            if data.is_valid():
                data.save()
                ret = 1000
        return render(request, 'myadmin/views/add_views.html', locals())

    @csrf_protect_m
    def change_view(self, request, id):

        return render(request, 'myadmin/views/change_views.html')

    @csrf_protect_m
    def delete_view(self, request, id):
        return render(request, 'myadmin/views/delete_views.html')

    def get_urls(self):
        info = self.model._meta.app_label, self.model._meta.model_name
        urlpatterns = [
            path('', self.list_view, name='myadmin_%s_%s' % info),
            path('add/', self.add_view, name='myadmin_%s_%s_add' % info),
            path('<path:object_id>/delete/', self.delete_view, name='myadmin_%s_%s_delete' % info),
            path('<path:object_id>/change/', self.change_view, name='myadmin_%s_%s_change' % info),
        ]
        return urlpatterns

    @property
    def urls(self):
        return self.get_urls()
