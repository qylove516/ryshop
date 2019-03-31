###后台管理系统主要点
**********
* 单例对象
* url分发
* FBV模式实现路由视图
**********
### 使用
*********
1、编辑 myadmin.py 并注册
    
    eg:
    from django.utils.safestring import mark_safe
    
    
    class GoodsConfig(ModelAdmin):

        list_display_links = ['id']
        list_display = ['id', 'name', 'desc', 'price']
        
     site.register(models.Goods, GoodsConfig)

2、