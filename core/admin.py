from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm, AdminPasswordChangeForm

from .models import *

# Customizing the User model in admin
# @admin.register(User)
# class UserAdmin(admin.ModelAdmin):
#     list_display = ('first_name', 'last_name', 'email', 'phone_number', 'role')
#     search_fields = ('first_name', 'last_name', 'email')
#     list_filter = ('role', 'address_country')
#     ordering = ('last_name',)

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        'title', 'price', 'category',
        'stock', 'product_type', 'author')

    search_fields = ('title', 'category__name')
    list_filter = ('category', 'product_type')
    prepopulated_fields = {'slug': ('title',)}
    autocomplete_fields = ['author']

class OrderLineInline(admin.TabularInline):
    model = OrderLine
    extra = 1  # Number of empty lines

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'customer', 'placed_at', 'total_amount')
    search_fields = ('customer__first_name', 'customer__email')
    list_filter = ('placed_at',)
    inlines = [OrderLineInline]  # Include OrderLine inline

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'parent')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


# ====================================


class CustomUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = User

class CustomUserCreationForm(UserCreationForm):
    usable_password = None

class CustomUserAdmin(UserAdmin):
    form = CustomUserChangeForm
    add_form = CustomUserCreationForm
    model = User
    list_display = ('email', 'first_name', 'last_name', 'phone_number', 'role')
    list_filter = ('role', )
    ordering = ('email',)
    search_fields = ('email', 'first_name', 'last_name', 'phone_number')
    
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'phone_number', 'profile_picture', 'address_country', 'address_city', 'address_street', 'address_postal_code')}),
        ('Permissions', {'fields': ('role',)}),
        ('Important dates', {'fields': ('last_login',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('email', 'first_name', 'last_name', 'phone_number', 'password1', 'password2', 'role')}
        ),
    )

admin.site.register(User, CustomUserAdmin)