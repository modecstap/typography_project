from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import (
    CorporateUser, Category, Product, ProductImage,
    Order, OrderItem, Review
)
@admin.register(CorporateUser)
class CorporateUserAdmin(UserAdmin):
    model = CorporateUser

    list_display = (
        "id",
        "email",
        "company_name",
        "inn",
        "phone",
        "is_staff",
        "is_active",
    )
    list_filter = ("is_staff", "is_active")
    search_fields = ("email", "company_name", "inn")
    ordering = ("id",)

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Компания", {"fields": ("company_name", "inn", "phone")}),
        ("Права доступа", {
            "fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")
        }),
        ("Системное", {"fields": ("last_login",)}),
    )

    add_fieldsets = (
        (None, {
            "classes": ("wide",),
            "fields": (
                "email",
                "username",
                "company_name",
                "inn",
                "phone",
                "password1",
                "password2",
                "is_staff",
                "is_active",
            ),
        }),
    )

    USERNAME_FIELD = "email"

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "slug")
    search_fields = ("name",)
    prepopulated_fields = {"slug": ("name",)}

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "title",
        "price",
        "quantity",
        "in_stock",
        "is_active",
        "category",
        "created_at",
    )
    list_filter = ("is_active", "category")
    search_fields = ("title", "description")
    list_editable = ("price", "quantity", "is_active")
    ordering = ("-created_at",)
    date_hierarchy = "created_at"

    prepopulated_fields = {"slug": ("title",)}
    readonly_fields = ("created_at",)

    inlines = [ProductImageInline]

    fieldsets = (
        ("Основное", {
            "fields": ("title", "slug", "category", "description")
        }),
        ("Цена и наличие", {
            "fields": ("price", "quantity", "is_active")
        }),
        ("Системное", {
            "fields": ("created_at",),
        }),
    )

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ("product", "price", "quantity")
    can_delete = False

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "order_number",
        "user",
        "status",
        "total_amount",
        "order_date",
    )
    list_filter = ("status", "order_date")
    search_fields = ("order_number", "user__email")
    ordering = ("-order_date",)
    date_hierarchy = "order_date"

    readonly_fields = (
        "order_number",
        "user",
        "total_amount",
        "order_date",
    )

    inlines = [OrderItemInline]

    fieldsets = (
        ("Заказ", {
            "fields": ("order_number", "status", "description")
        }),
        ("Клиент и сумма", {
            "fields": ("user", "total_amount", "order_date")
        }),
    )

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "author",
        "rating",
        "order_item",
        "created_at",
    )
    list_filter = ("rating", "created_at")
    search_fields = ("author__email", "text")
    ordering = ("-created_at",)

    readonly_fields = ("created_at",)

admin.site.site_header = "Администрирование магазина"
admin.site.site_title = "Admin"
admin.site.index_title = "Управление данными"
