from django.db import models

# Create your models here.
from django.utils.html import format_html
from django.utils.safestring import mark_safe
from stdimage import StdImageField


class Goods(models.Model):
    name = models.CharField('名称', max_length=64, blank=True, null=True)
    desc = models.TextField('描述', blank=True, null=True)
    date = models.DateField('日期', auto_now_add=True)
    image = models.ImageField('图片', upload_to='img', blank=True, null=True)
    discount = models.CharField('是否促销', max_length=32, choices=(('1', '促销'), ('2', '非促销')), default='1')
    shop = models.ManyToManyField(
        'Shop',
        verbose_name='商家',
        related_name='goods_shop_item'
    )
    price = models.ForeignKey(
        'Price',
        on_delete=models.SET_NULL,
        blank=True,
        null=True,
        verbose_name='价格',
        related_name='goods_price_item'
    )

    def colored_desc(self):
        return format_html(
            '<span style="color: blue;">{}</span>',
            self.date
        )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商品'
        verbose_name_plural = '商品'


class Shop(models.Model):
    name = models.CharField('名称', max_length=64, blank=True, null=True)
    address = models.CharField('地址', max_length=64, blank=True, null=True)
    # 第二种显示图片的方法
    image = StdImageField(
        max_length=100,
        upload_to='img',
        verbose_name=u"轮播图",
        variations={'thumbnail': {'width': 75, 'height': 75}},
        blank=True,
        null=True
    )

    def image_img(self):
        if self.image:
            return mark_safe('<img src="%s" />' % self.image.thumbnail.url)
        else:
            return u'上传图片'

    image_img.short_description = '轮播图'
    image_img.allow_tags = True

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '商家'
        verbose_name_plural = '商家'


class Price(models.Model):
    name = models.CharField('名称', max_length=64, blank=True, null=True)
    num = models.IntegerField('价格', blank=True, null=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '价格'
        verbose_name_plural = '价格'


from DjangoUeditor.models import UEditorField


class Order(models.Model):
    # num_id = models.CharField('订单编号', max_length=10, default=0000000000)
    name = models.CharField('名称', max_length=64, blank=True, null=True)
    desc = models.CharField('描述', max_length=5, blank=True, null=True)
    num = models.IntegerField('数量', blank=True, null=True)
    content = UEditorField(
        width=800,
        height=400,
        toolbars="full",
        imagePath="images/",
        filePath="files/",
        upload_settings={"imageMaxSize": 1204000},
        settings={}, verbose_name='内容',
        blank=True,
        null=True,
    )

    # def profile(self):
    #     if len(self.num_id) < 10:
    #         return self.num_id.zfill(10)
    #
    # profile.allow_tags = True

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = '订单'
        verbose_name_plural = '订单'


from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill


class Profile(models.Model):
    avatar = models.ImageField(upload_to='avatars')
    # ResizeToFill 参数： height width
    avatar_thumbnail = ImageSpecField(source='avatar',
                                      processors=[ResizeToFill(120, 100, None, False)],
                                      format='JPEG',
                                      options={'quality': 60})

    def __str__(self):
        return str(self.id)


class Post(models.Model):
    title = models.CharField(max_length=128)
    body = models.CharField(max_length=400)


import uuid


def get_image_filename(instance, filename):
    only_name = str(uuid.uuid4())
    return "post_images/{}-{}".format(only_name, filename)


class Images(models.Model):
    post = models.ForeignKey(Post, blank=True, null=True, default=None, on_delete=models.SET_NULL)
    image = models.ImageField(
        upload_to=get_image_filename,
        verbose_name='Image'
    )


class ImageBootstrap(models.Model):
    # 自定义主键，使用uuid生成，保证唯一性
    id = models.CharField(max_length=64, primary_key=True)
    image = models.ImageField(
        upload_to=get_image_filename,
        verbose_name='Image'
    )

