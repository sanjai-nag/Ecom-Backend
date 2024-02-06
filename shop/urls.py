from django.urls import path,include
from rest_framework import routers

from .views import *
from . import views
router = routers.DefaultRouter()
router.register('cart',MyCart,basename="MyCart")
router.register('orders',OrderViewset,basename="OrderViewset")
router.register('review',ReviewViewset,basename="ReviewViewset")
router.register('category',CatagoryViewset,basename="CatagoryViewset")

urlpatterns = [
    path("",include(router.urls)),
    path("updateuser/",Updateuser.as_view(),name=" updateuser"),
    path("profile/",ProfileView.as_view(),name="profile"),
    path("register/",RegisterView.as_view(),name="register"),
    path("Cproduct/",Cos_ProductView.as_view(),name="cosproduct"),
    path("Cproduct/<int:id>/",Cos_ProductView.as_view(),name="cosproductdetal"),
    path("product/",ProductView.as_view(),name="product"),
    path("product/<int:id>/",ProductView.as_view(),name="productdetal"),
    path("addtocart/",AddtoCartView.as_view(),name="addtocart"),
    path("updatecartproduct/",UpdateCartProduct.as_view(),name="updatecartproduct"),
    path("editcartproduct/",EditCartProduct.as_view(),name="editcartproduct"),
    path("delatecartproduct/",Delatecartproduct.as_view(),name="delatecartproduct"),
    path("delatefullcart/",Delatefullcart.as_view(),name="delatefullcart"),
    path("updateprofile/",Updateprofile.as_view(),name="updateprofile"),
    path("upprofile/",Upprofile.as_view(),name="upprofile"),
    path("urofile/",Urofile.as_view(),name="urofile"),
    path("uprofile/",Uprofile.as_view(),name="uprofile"),
    path("send_otp/",views.send_otp,name="send_otp"),
    path('checkOTP/', views.checkOTP),
    path('registerr/', views.registerr,name="registerr"),
    path('reset/', views.reset,name="reset"),
    path('contact/', views.contact,name="contact"),
    path('posts/', views.PostView.as_view(), name= 'posts_list'),
    path('call/', views.CallView.as_view(), name= 'call'),
    path('hoome/', mike.as_view(),name='hoome'),
    path("tprofile/",tprofile.as_view(),name="tprofile"),
    path("likecountprofile/",likecountprofile.as_view(),name="likecountprofile"),
    path("filterr/",filterr.as_view(),name="filterr"),
    path("InstagramPostView/",InstagramPostView.as_view(),name="InstagramPostView"),
    path('api/search/', SearchView.as_view(), name='search'),

]
