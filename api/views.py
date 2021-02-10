from rest_framework.decorators import api_view
from rest_framework.response import Response

from django.contrib.auth.decorators import login_required

from recipes.models import Ingredient, Tag

@api_view(['GET'])
def get_ingredients(request):
    query = request.GET.get('query', None)
    ingredients = [{"title": ing.name, "dimension": ing.unit} for ing in Ingredient.objects.filter(name__icontains=query)]
    return Response(ingredients) 


@login_required
@api_view(['POST'])
def add_favorites(request):
    print(request)
    return Response({"test": 1213})
