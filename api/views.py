from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.shortcuts import get_object_or_404
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required

from recipes.models import Ingredient, Recipe, Favorite

from users.models import Profile

User = get_user_model()


@api_view(['GET'])
def get_ingredients(request):
    query = request.GET.get('query', None)
    ingredients = [{"title": ing.name, "dimension": ing.unit} for ing in Ingredient.objects.filter(name__icontains=query)]
    return Response(ingredients) 


@login_required
@api_view(['POST'])
def add_favorites(request):
    recipe = get_object_or_404(Recipe, id=request.data.get('id'))
    user = request.user
    resp = False
    if recipe.author != user and not user.profile.favorites.filter(id=recipe.id).exists():
        user.profile.favorites.add(recipe)
        resp = True
    print({'success': resp})
    return Response({'success': resp})


@login_required
@api_view(['DELETE'])
def remove_favorites(request, recipe_id):
    recipe = get_object_or_404(Recipe, id=recipe_id)
    user = request.user
    resp = False
    if user.profile.favorites.filter(id=recipe.id).exists():
        user.profile.favorites.remove(recipe)
        resp = True
    print({'success': resp})
    return Response({'success': resp})


@login_required
@api_view(['POST'])
def add_favorites_2(request):
    recipe_id = request.data.get('id')
    recipe = get_object_or_404(Recipe, id=recipe_id)
    resp = False
    if recipe.author != request.user:
        Favorite.objects.get_or_create(user=request.user, recipe=recipe)
        resp = True
    print({'success': resp})
    return Response({'success': resp})
