from django.urls import path
from . import views

urlpatterns = [
    path("add/<int:product_id>/", views.add_cart, name="add_cart"),
    path("cart/", views.cart_detail, name="cart_detail"),
    path("cart/remove/<int:product_id>/", views.cart_remove, name="cart_remove"),
    path(
        "cart/delete/<int:product_id>/",
        views.cart_delete_product,
        name="cart_delete_product",
    ),
    path("thankyou/<int:order_id>/", views.thankyou_page, name="thanks_page"),
    path("order_history/", views.orderHistory, name="order_history"),
    path("order/<int:order_id>/", views.viewOrder, name="order_detail"),
]