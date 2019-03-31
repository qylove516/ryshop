from myadmin.service.myadmin import site
from myadmin.service.options import ModelAdmin
from goods import models


class GoodsConfig(ModelAdmin):

    list_display_links = ['id']
    list_display = ['id', 'name', 'desc', 'price']


class ShopConfig(ModelAdmin):
    list_display = ['name', 'address']


class PriceConfig(ModelAdmin):
    list_display = ['name', 'num']


site.register(models.Goods, GoodsConfig)
site.register(models.Shop, ShopConfig)
site.register(models.Price)
