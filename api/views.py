from rest_framework.decorators import api_view
from rest_framework.response import Response

from recipes.models import Ingredient, Tag

@api_view(['GET'])
def get_ingredients(request):
    query = request.GET.get('query', None)
    ingredients = [{"title": ing.name, "dimension": ing.unit} for ing in Ingredient.objects.filter(name__icontains=query)]
    return Response(ingredients) 
