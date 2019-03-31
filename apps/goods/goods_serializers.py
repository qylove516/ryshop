from rest_framework import serializers
from goods import models


class GoodsSerializers(serializers.ModelSerializer):
    # price = serializers.CharField(source='price.name')
    discount = serializers.CharField(source='get_discount_display')
    price = serializers.HyperlinkedIdentityField(view_name='price', lookup_field='price_id', lookup_url_kwarg='pk')

    class Meta:
        model = models.Goods
        fields = ['id', 'name', 'price', 'discount']
        # depth = 1

