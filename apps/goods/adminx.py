import xadmin
from goods import models


class GoodsAdmin(object):
    list_display = ['name', 'desc']


class PriceAdmin(object):
    list_display = ['name', 'num']


class OrderAdmin(object):
    list_display = ['name', 'num']


xadmin.site.register(models.Goods, GoodsAdmin)
xadmin.site.register(models.Price, PriceAdmin)
xadmin.site.register(models.Order, OrderAdmin)
