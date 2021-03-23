from django.contrib import admin
from .models import Order, OrderItem


class OrderItemAdmin(admin.TabularInline):
    model = OrderItem
    fieldsets = [
        (
            "Product",
            {
                "fields": ["product"],
            },
        ),
        (
            "Quantity",
            {
                "fields": ["quantity"],
            },
        ),
        (
            "Price",
            {
                "fields": ["price"],
            },
        ),
    ]

    readonly_fields = ["product", "quantity", "price"]
    can_delete = False
    max_num = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ["id", "billingName", "created"]
    list_display_links = ("id", "billingName")
    readonly_fields = [
        "id",
        "token",
        "total",
        "emailAddress",
        "created",
        "billingName",
        "billingAddress1",
        "billingCity",
        "billingPostcode",
        "billingCountry",
        "shippingName",
        "shippingAddress1",
        "shippingCity",
        "shippingPostcode",
        "shippingCountry",
    ]

    fieldsets = [
        ("ORDER INFO", {"fields": ["id", "token", "total", "created"]}),
        (
            "BILLING INFO",
            {
                "fields": [
                    "billingName",
                    "billingAddress1",
                    "billingCity",
                    "billingPostcode",
                    "billingCountry",
                    "emailAddress",
                ]
            },
        ),
        (
            "SHIPPING INFO",
            {
                "fields": [
                    "shippingName",
                    "shippingAddress1",
                    "shippingCity",
                    "shippingPostcode",
                    "shippingCountry",
                ]
            },
        ),
    ]

    inlines = [
        OrderItemAdmin,
    ]
