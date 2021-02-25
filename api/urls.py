from django.urls import path
from . import views


urlpatterns = [
    path('ingredients/', views.get_ingredients),
    path('favorites/', views.add_favorites),
    path('favorites/<str:recipe_id>/', views.remove_favorites),
    path('subscriptions/', views.add_subscriptions),
    path('subscriptions/<str:author_id>/', views.remove_subscriptions),
    path('purchases/', views.add_or_get_purchases),
    path('purchases/<str:recipe_id>/', views.remove_purchases),
]
