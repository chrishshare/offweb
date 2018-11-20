from django.shortcuts import render
from officalweb.models import Menus
from django.db.models import F
from officalweb.serialize2json import queryset_to_json
from django.http import HttpResponse
from officalweb.models import Logo
from officalweb.models import Advertise
from officalweb.models import ProductList
from officalweb.models import ProductDetail
from officalweb.models import ProductType
from officalweb.models import Menus
from officalweb.models import AboutCmic, Honor, Culture
import json
from officalweb.funcs import query_product_detail, query_friendly_link, query_product_cat, query_new_product, \
    query_menu_list, query_product_list_v2, menu_list

SUCCESS = [{"retcode": 0, "retmsg": "successed!"}]


def index_view(request):
    """
    首页
    :param request:
    :return:
    """
    image = Logo.objects.all().values('logo')
    new_product_list = query_new_product('new')
    cat_product_list = query_product_cat()
    link_list = query_friendly_link()
    menu_list_l = menu_list()
    return render(request, 'index.html', locals())


def product_center_view(request, **kwargs):
    """
    查询产品分类列表，新的直接渲染
    :param request:
    :param kwargs:
    :return:
    """
    product_list = query_product_list_v2(kwargs.get('typeid'))
    product_type_list = query_product_cat()
    link_list = query_friendly_link()
    menu_list_l = menu_list()
    return render(request, 'productcenter.html', locals())


def product_detail_view_v2(request, **kwargs):
    """
    查询产品详情
    :param request:
    :param kwargs:
    :return:
    """
    detail_list = query_product_detail(typeid=kwargs.get('typeid'), productcode=kwargs.get('productcode'))
    link_list = query_friendly_link()
    menu_list_l = menu_list()
    return render(request, 'productdetail.html', locals())


def footer_view(request):
    link_list = query_friendly_link()
    return render(request, 'common/footer.html', locals())


def culture_view(request):
    menu_list_l = menu_list()
    aboutbrand = AboutCmic.objects.all().values('title')
    honor_list = Honor.objects.all().values('honorname', 'honorimage', 'sortorder').order_by('sortorder')
    culture_list = Culture.objects.all().values('title', 'content', 'sortorder').order_by('sortorder')
    print(aboutbrand, honor_list, culture_list)
    return render(request, 'aboutbrand.html', locals())

# 接口
def menu_list_view(request):
    """
    菜单列表，返回json串
    :param request: 传空
    :return:
    """
    if request.method == 'POST':
        try:
            # 没有子菜单部分

            no_child_menu = Menus.objects.filter(status__dict_id='normal', parentid__menu_id__isnull=True).values(
                menuid=F('menu_id'),
                menuname=F('menu_name'))
            # json_data = queryset_to_json(querylist=no_child_menu, resultinfo=SUCCESS)

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
            json_data = queryset_to_json(no_child_menu_list, resultinfo=SUCCESS)

            # no_child_menu = Menus.objects.filter(status__dict_id='normal', has_child=0).values(
            #     menuid=F('menu_id'),
            #     menuname=F('menu_name'))
            #
            # has_child_menu = Menus.objects.filter(status__dict_id='normal', has_child=1).values(
            #     menuid=F('parentid__menu_id'),
            #     menuname=F('parentid__menu_name')).order_by('parentid__menu_id').distinct()

            # 有子菜单部分
            return HttpResponse(json_data)
        except Exception as e:
            json_data = queryset_to_json(querylist='', resultinfo=[{"retcode": -1, "retmsg": e}])
            return HttpResponse(json_data)
    else:
        json_data = queryset_to_json(querylist='', resultinfo=[{"retcode": -1, "retmsg": "不支持该请求方法"}])
        return HttpResponse(json_data)


def banner_list_view(request):
    """
    banner列表，返回json串
    :param request: 入参需要传入type
    :return:
    """
    if request.method == 'POST':
        try:
            banner_list = Advertise.objects.filter(
                status__dict_id='normal', status__group_id='status').values(
                'carousel', mediaid=F('media_id'), mediainfo=F('media_info'), mediatypeid=F('media_type__dict_id'),
                mediatypename=F('media_type__dict_name'), menuid=F('page__menu_id'), menuname=F('page__menu_name'),
                fill=F('fill_color'), imgsrc=F('image'), linkaddr=F('link_addr'))
            json_data = queryset_to_json(querylist=banner_list, resultinfo=SUCCESS)
            return HttpResponse(json_data)
        except Exception as e:
            json_data = queryset_to_json(querylist='', resultinfo=[{"retcode": -1, "retmsg": e}])
            return HttpResponse(json_data)
    else:
        json_data = queryset_to_json(querylist='', resultinfo=[{"retcode": -1, "retmsg": "不支持该请求方法"}])
        return HttpResponse(json_data)


def product_type_view(request):
    """
     查询产品分类列表接口
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            prodtype = ProductType.objects.filter().values('typeid', 'typename', 'image', 'order')
            json_data = queryset_to_json(querylist=prodtype, resultinfo=SUCCESS)
            return HttpResponse(json_data)
        except Exception as e:
            json_data = queryset_to_json(querylist='', resultinfo=[{"retcode": -1, "retmsg": e}])
            return HttpResponse(json_data)
    else:
        json_data = queryset_to_json(querylist='', resultinfo=[{"retcode": -1, "retmsg": "不支持该请求方法"}])
        return HttpResponse(json_data)


def product_detail_view(request):
    if request.method == 'POST':
        product_code = json.loads(request.body, encoding='utf-8').get('productcode')
        product_typeid = json.loads(request.body, encoding='utf-8').get('typeid')

        if product_code is not None and product_typeid is not None:
            try:
                detail = ProductDetail.objects.filter(product_code__product_code=product_code,
                                                      product_code__type_id__typeid=product_typeid).values(
                    productcode=F('product_code__product_code'), image=F('detail_image'), desc=F('image_desc'))
                json_data = queryset_to_json(querylist=detail, resultinfo=SUCCESS)
                return HttpResponse(json_data)
            except Exception as e:
                json_data = queryset_to_json(querylist='', resultinfo=[{"retcode": -1, "retmsg": e}])
                return HttpResponse(json_data)
        else:
            json_data = queryset_to_json(querylist='', resultinfo=[{"retcode": -1, "retmsg": "请传入正确的参数"}])
            return HttpResponse(json_data)
    else:
        json_data = queryset_to_json(querylist='', resultinfo=[{"retcode": -1, "retmsg": "不支持该请求方法"}])
        return HttpResponse(json_data)


def product_list_view(request):
    """
    产品列表，需要传入产品分类typeid，该值从product_type_view接口来的
    :param request:
    :return:
    """
    if request.method == 'POST':
        try:
            # prod_type = request.POST.get('typeid')
            prod_type = json.loads(request.body, encoding='utf-8').get('typeid')
            if prod_type == 'new':
                new_product_list = ProductList.objects.filter().values(
                    typeid=F('type_id__typeid'), typename=F('type_id__typename'), productcode=F('product_code'),
                    productname=F('product_name'),
                    productdesc=F('product_desc'), image=F('image_url'), price=F('product_price'),
                    unit=F('product_unit'),
                    size=F('product_size'))[:5]
                json_data = queryset_to_json(querylist=new_product_list, resultinfo=SUCCESS)
                return HttpResponse(json_data)

            elif prod_type == 'all':
                new_product_list = ProductList.objects.filter().values(
                    typeid=F('type_id__typeid'), typename=F('type_id__typename'), productcode=F('product_code'),
                    productname=F('product_name'),
                    productdesc=F('product_desc'), image=F('image_url'), price=F('product_price'),
                    unit=F('product_unit'),
                    size=F('product_size'))
                json_data = queryset_to_json(querylist=new_product_list, resultinfo=SUCCESS)
                return HttpResponse(json_data)
            else:

                product_list = ProductList.objects.filter(type_id__typeid=prod_type).values(
                    typeid=F('type_id__typeid'), typename=F('type_id__typename'), productcode=F('product_code'),
                    productname=F('product_name'),
                    productdesc=F('product_desc'), image=F('image_url'), price=F('product_price'),
                    unit=F('product_unit'),
                    size=F('product_size'))
                json_data = queryset_to_json(querylist=product_list, resultinfo=SUCCESS)
                return HttpResponse(json_data)
        except Exception as e:
            json_data = queryset_to_json(querylist='', resultinfo=[{"retcode": -1, "retmsg": e}])
            return HttpResponse(json_data)
    else:
        json_data = queryset_to_json(querylist='', resultinfo=[{"retcode": -1, "retmsg": "只支持POST方法"}])
        return HttpResponse(json_data)
