# encoding = utf-8

# Author:Administrator
# Email: siyzhou@163.com
# Date: 20181118
# Description:
from django.db.models import F
from officalweb.models import ProductList
from officalweb.models import ProductDetail
from officalweb.models import ProductType
from officalweb.models import FrendlyLink
from officalweb.models import Menus


def query_new_product(ptype):
    """
    查询新品列表
    :param ptype:
    :return:
    """
    if ptype is not None:
        prod_list = ProductList.objects.filter(product_type=ptype).values(typeid=F('type_id__typeid'),
                                                                          productcode=F('product_code'),
                                                                          prodductname=F('product_name'),
                                                                          productdesc=F('product_desc'),
                                                                          image=F('image_url'))
        return prod_list
    elif ptype is None:
        prod_list = ProductList.objects.all().values(typeid=F('type_id__typeid'),
                                                                          productcode=F('product_code'),
                                                                          prodductname=F('product_name'),
                                                                          productdesc=F('product_desc'),
                                                                          image=F('image_url'))

        return prod_list
    else:
        pass


def query_product_list_v2(typeid):
    """
    根据产品分类id查询产品列表
    :param typeid:
    :return:
    """
    prod_list = ProductList.objects.filter(type_id__typeid=typeid).values(typeid=F('type_id__typeid'),
                                                                          productcode=F('product_code'),
                                                                          productname=F('product_name'),
                                                                          productdesc=F('product_desc'),
                                                                          image=F('image_url'),
                                                                          size=F('product_size'),
                                                                          price=F('product_price'),
                                                                          unit=F('product_unit'))

    return prod_list


def query_product_cat():
    """
    查询产品分类
    :return:
    """
    product_cat_list = ProductType.objects.all().values('typeid', 'typename', 'image', 'order').order_by('order')
    print(product_cat_list)
    return product_cat_list


def query_friendly_link():
    """
    查询友情链接
    :return:
    """
    link_list = FrendlyLink.objects.all().values('name', 'address')
    return link_list


def menu_list():

    # 有子菜单的部分
    has_child_menu = Menus.objects.filter(status__dict_id='normal', parentid__menu_id__isnull=False).values(
        menuid=F('parentid__menu_id'),
        menuname=F('parentid__menu_name')).order_by('parentid__menu_id').distinct()

    no_child_menu_list = []

    # 父子菜单合并，生成字典
    for i in range(len(has_child_menu)):
        parent = has_child_menu[i]
        parent_menu_id = parent.get('menuid')
        child_menu = Menus.objects.filter(status__dict_id='normal', parentid__menu_id=parent_menu_id).values(
            menuid=F('menu_id'),
            menuname=F('menu_name'), linkaddr=F('link'))
        parent['childmenu'] = list(child_menu)
        no_child_menu_list.append(parent)
    return no_child_menu_list


def query_menu_list():
    """
    查询菜单列表
    :return:
    """
    no_child_menu = Menus.objects.filter(status__dict_id='normal', parentid__menu_id__isnull=True).values(
        menuid=F('menu_id'),
        menuname=F('menu_name'))

    # 有子菜单的部分
    has_child_menu = Menus.objects.filter(status__dict_id='normal', parentid__menu_id__isnull=False).values(
        menuid=F('parentid__menu_id'),
        menuname=F('parentid__menu_name')).order_by('parentid__menu_id').distinct()

    no_child_menu_list = []

    # 父子菜单合并，生成字典
    for i in range(len(has_child_menu)):
        parent = has_child_menu[i]
        parent_menu_id = parent.get('menuid')
        child_menu = Menus.objects.filter(status__dict_id='normal', parentid__menu_id=parent_menu_id).values(
            menuid=F('menu_id'),
            menuname=F('menu_name'))
        parent['childmenu'] = list(child_menu)
        no_child_menu_list.append(parent)
    # no_child_menu_list.append(no_child_menu)
    print(no_child_menu_list)
    return no_child_menu_list


def query_product_detail(typeid, productcode):
    """
    查询产品详情
    :return:
    """
    details = ProductDetail.objects.filter(product_code__product_code=productcode,
                                           product_code__type_id__typeid=typeid).values(
        productcode=F('product_code__product_code'), image=F('detail_image'), desc=F('image_desc'))
    return details