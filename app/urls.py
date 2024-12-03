from django.urls import path

from . import views


urlpatterns = [
    path('',views.home,name='home'),
    path('products',views.product_view,name='products'),
    path('category',views.category_view,name='category'),
    path('productcat/<int:id>/', views.prod, name='prodscat'),
    path('viewproduct/<int:id>/',views.viewproduct,name='viewprod'),
    path('productby_category/<int:id>/',views.catcategory_products,name='sub'),
    path('menswear', views.mens_wear, name='mens_wear'),
    path('womenswear', views.womens_wear, name='womenswear'),
    path('westernwear', views.westernwear, name='westernwear'),
    path('signup',views.signup,name='signup'),
    path('login',views.loginpage,name='loginpage'),
    path('logout',views.logoutpage,name='logout'),
    path('search/', views.product_search, name='product_search'),
    path('addcart/<int:id>/',views.addcart,name='addcart'),
    path('cartpage',views.cartpage,name='cartpage'),
    path('remove/<int:id>/',views.remove,name='remove'),
    path('addwish/<int:id>/',views.wishlist,name='wishlist'),
    path('wishpage',views.wishpage,name='wishpage'),
    path('removewish/<int:id>/',views.removewish,name='removewish'),
    path('order',views.place_order,name='order'),
    path('confirm',views.order_confirmation,name='confirm'),
    path('cart',views.logincart,name='loginpagecart'),
    path('cartsignup',views.signupcart,name='signupcart'),
    path('wishlist',views.loginwishlist,name='loginpagewish'),
    path('wishlistignup',views.signupwishlist,name='signupwish'),


]