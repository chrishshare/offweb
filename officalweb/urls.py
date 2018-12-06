"""offweb URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from officalweb import views

urlpatterns = [
    # views
    path('', views.index_view, name='index'),
    path('productdetail/', views.product_detail_view),
    # path('footer/', views.footer_view),
    path('productdetailv2/<str:typeid>/<str:productcode>/', views.product_detail_view_v2, name='productdetailv2'),
    path('prodcenter/<str:typeid>', views.product_center_view, name='prodcenter'),
    path('culture/', views.culture_view, name='culture'),

    #     api
    path('menu/', views.menu_list_view),
    path('banner/', views.banner_list_view),
    path('prodtype/', views.product_type_view),
    path('prod/', views.product_list_view),

]
