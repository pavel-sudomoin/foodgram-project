from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from recipes.models import Ingredient, Recipe

User = get_user_model()


@api_view(["GET"])
def get_ingredients(request):
    query = request.GET.get("query", None)
    ingredients = [
        {"title": ing.name, "dimension": ing.unit}
        for ing in Ingredient.objects.filter(name__icontains=query)
    ]
    return Response(ingredients)


@login_required
@api_view(["POST"])
def add_favorites(request):
    recipe = get_object_or_404(Recipe, id=request.data.get("id"))
    user = request.user
    if recipe.author == user:
        return Response({"success": False})
    user.profile.favorites.add(recipe)
    return Response({"success": True})


@login_required
@api_view(["DELETE"])
def remove_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    user.profile.favorites.remove(recipe)
    return Response({"success": True})


@login_required
@api_view(["POST"])
def add_subscriptions(request):
    author = get_object_or_404(User, id=request.data.get("id"))
    user = request.user
    if author == user:
        return Response({"success": False})
    user.profile.following.add(author)
    return Response({"success": True})


@login_required
@api_view(["DELETE"])
def remove_subscriptions(request, author_id):
    author = get_object_or_404(User, id=author_id)
    user = request.user
    user.profile.following.remove(author)
    return Response({"success": True})


@login_required
@api_view(["GET", "POST"])
def add_or_get_purchases(request):
    recipe = get_object_or_404(Recipe, id=request.data.get("id"))
    user = request.user
    user.profile.shoplist.add(recipe)
    return Response({"success": True})


@login_required
@api_view(["DELETE"])
def remove_purchases(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    user.profile.shoplist.remove(recipe)
    return Response({"success": True})
