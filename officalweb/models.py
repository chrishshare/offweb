from django.db import models
from ckeditor.fields import RichTextField


class DictItem(models.Model):
    """
    字典配置
    """
    dict_id = models.CharField(max_length=50, null=False, blank=False, verbose_name='字典编码')
    dict_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='字典名称')
    group_id = models.CharField(max_length=50, null=False, blank=False, verbose_name='字典组编码')
    group_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='字典组名称')

    class Meta:
        verbose_name = '字典配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.dict_name


class Logo(models.Model):
    """
    logo配置
    """
    logo = models.ImageField(upload_to='logo', verbose_name='Logo图标', null=False, blank=False)


class Menus(models.Model):
    """
    菜单配置
    """
    menu_id = models.CharField(max_length=50, null=False, blank=False, verbose_name='菜单编码')
    menu_name = models.CharField(max_length=50, null=False, blank=False, verbose_name='菜单名称')
    sort_order = models.IntegerField(blank=False, null=False, verbose_name='菜单排序')
    parentid = models.ForeignKey('self', null=True, blank=True, related_name='menus_parentid', verbose_name='上级菜单',
                                 on_delete=models.CASCADE)
    status = models.ForeignKey(DictItem, verbose_name='菜单状态', related_name='menus_status',
                               on_delete=models.CASCADE)
    link = models.CharField(max_length=50, null=True, blank=True, verbose_name='跳转地址')

    class Meta:
        verbose_name = '菜单配置'
        verbose_name_plural = verbose_name
        ordering = ['sort_order']

    def __str__(self):
        return self.menu_name


class Advertise(models.Model):
    """
    banner配置
    """
    carousel = models.IntegerField(blank=False, null=False, verbose_name='轮播时间间隔', default=5)
    media_id = models.CharField(max_length=50, null=False, blank=False, verbose_name='图片/视频编码')
    media_info = models.CharField(max_length=100, null=False, blank=False, verbose_name='图片视频/描述')
    sort_order = models.IntegerField(null=False, blank=False, verbose_name='图片/视频排序')
    image = models.ImageField(upload_to='Advertise_img', verbose_name='图片', null=False, blank=False)
    media_type = models.ForeignKey(DictItem, verbose_name='媒体分类', related_name='advertise_media_type',
                                   on_delete=models.CASCADE)
    status = models.ForeignKey(DictItem, verbose_name='媒体状态', related_name='advertise_status',
                               on_delete=models.CASCADE)
    page = models.ForeignKey(Menus, verbose_name='关联页面', related_name='advertise_page', on_delete=models.CASCADE)
    fill_color = models.CharField(max_length=10, null=True, blank=True, verbose_name='图片填充色')
    link_addr = models.CharField(max_length=300, null=True, blank=True, verbose_name='链接地址')

    class Meta:
        verbose_name = '轮播图片配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.media_info


class ProductType(models.Model):
    """
    产品分类
    """
    typeid = models.CharField(max_length=20, blank=False, null=False, verbose_name='产品分类编码')
    typename = models.CharField(max_length=50, blank=False, null=False, verbose_name='产品分类名称')
    image = models.ImageField(upload_to='prodtype', blank=False, null=False, verbose_name='分类图片')
    order = models.IntegerField(null=False, blank=False, verbose_name='排序')

    class Meta:
        verbose_name = '产品分类'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.typename


class ProductList(models.Model):
    """
    产品列表
    """
    type_id = models.ForeignKey(ProductType, blank=False, null=False, verbose_name='产品编码', on_delete=models.CASCADE)
    product_code = models.CharField(max_length=50, blank=False, null=False, verbose_name='产品编码')
    product_name = models.CharField(max_length=200, blank=False, null=False, verbose_name='产品名称')
    product_desc = models.CharField(max_length=500, blank=False, null=False, verbose_name='产品描述')
    product_size = models.CharField(max_length=50, blank=True, null=True, verbose_name='规格')
    product_price = models.FloatField(blank=True, null=True, verbose_name='价格')
    product_unit = models.CharField(max_length=5, blank=True, null=True, verbose_name='计价方式')
    product_type = models.CharField(max_length=20, blank=False, null=False, verbose_name='产品类别（如：新品、常规)')
    image_url = models.ImageField(upload_to='product_img', verbose_name='图片/视频', null=False, blank=False)
    status = models.ForeignKey(DictItem, verbose_name='产品状态', related_name='productList_status',
                               on_delete=models.CASCADE)

    class Meta:
        verbose_name = '产品配置'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.product_name


class ProductDetail(models.Model):
    """
    产品详情
    """
    product_code = models.ForeignKey(ProductList, verbose_name='产品名称', on_delete=models.CASCADE)
    detail_image = models.ImageField(upload_to='product', null=True, blank=True, verbose_name='产品图片')
    image_desc = models.CharField(max_length=200, null=False, blank=False, verbose_name='图片描述')

    class Meta:
        verbose_name = '产品详情'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.image_desc


class FrendlyLink(models.Model):
    name = models.CharField(max_length=30, verbose_name='链接名称')
    address = models.URLField(max_length=200, verbose_name='链接地址')

    class Meta:
        verbose_name = '友情链接'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class AboutCmic(models.Model):
    title = RichTextField(max_length=2000, verbose_name='企业简介')

    class Meta:
        verbose_name = '企业简介'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title


class Honor(models.Model):
    honorname = models.CharField(max_length=100, null=False, blank=False, verbose_name='荣誉名称')
    honorimage = models.ImageField(upload_to='honor', null=False, blank=False, verbose_name='荣誉照片')
    sortorder = models.IntegerField(null=False, blank=False, verbose_name='显示顺序')

    class Meta:
        verbose_name = '品牌荣誉'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.honorname


class Culture(models.Model):
    title = models.CharField(max_length=20, null=False, blank=False, verbose_name='文化标题')
    content = models.CharField(max_length=20, null=False, blank=False, verbose_name='文化描述')
    sortorder = models.IntegerField(null=False, blank=False, verbose_name='显示顺序')

    class Meta:
        verbose_name = '企业文化'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.title
