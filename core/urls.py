from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin

from .import views

urlpatterns = [
    path('', views.index_view, name='index'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/', views.profile_view, name='profile'),
    path('profile_edit/', views.profile_edit_view, name='profile_edit'),

    path('products/', views.product_list_view, name='products'),
    path('product/<slug:slug>/', views.product_view, name='product'),
    path('cart/', views.cart_view, name='cart'),

    path('add-to-cart/<int:product_id>/', views.add_to_cart, name='add_to_cart'),
    path('update-cart/', views.update_cart, name='update_cart'),
    path('remove-from-cart/<int:product_id>/', views.remove_from_cart, name='remove_from_cart'),
    path('checkout/', views.checkout, name='checkout'),

    path('order_details/<int:order_id>/', views.order_details_view, name='order_details'),
    path('thanks/', views.thanks_view, name='thanks'),

    # ======================    
    
    path("admin/", admin.site.urls) 
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
