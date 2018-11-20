from django.contrib import admin
from officalweb.models import DictItem
from officalweb.models import Menus
from officalweb.models import Advertise
from officalweb.models import ProductList
from officalweb.models import Logo
from officalweb.models import ProductDetail
from officalweb.models import ProductType
from officalweb.models import FrendlyLink
from officalweb.models import AboutCmic
from officalweb.models import Honor
from officalweb.models import Culture

class ShowDictItem(admin.ModelAdmin):
    list_display = ('dict_id', 'dict_name', 'group_id', 'group_name')


admin.site.register(DictItem, ShowDictItem)


admin.site.register(Logo)


class ShowMenulist(admin.ModelAdmin):
    list_display = ('menu_id', 'menu_name', 'parentid', 'status')
    ordering = ('sort_order',)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            kwargs['queryset'] = DictItem.objects.filter(group_id='status')
        if db_field.name == 'parentid':
            kwargs['queryset'] = Menus.objects.filter(parentid__menu_id__isnull=True)
        return super(ShowMenulist, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Menus, ShowMenulist)


class ShowAdvertise(admin.ModelAdmin):
    list_display = ('media_id', 'media_info', 'status', 'page')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            kwargs['queryset'] = DictItem.objects.filter(group_id='status')
        return super(ShowAdvertise, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(Advertise, ShowAdvertise)


class ShowProductList(admin.ModelAdmin):
    list_display = ('product_name', 'product_desc', 'status')

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        if db_field.name == 'status':
            kwargs['queryset'] = DictItem.objects.filter(group_id='status')
        return super(ShowProductList, self).formfield_for_foreignkey(db_field, request, **kwargs)


admin.site.register(ProductList, ShowProductList)


admin.site.register(ProductDetail)

admin.site.register(AboutCmic)

admin.site.register(Honor)

admin.site.register(Culture)

admin.site.register(ProductType)

admin.site.register(FrendlyLink)

