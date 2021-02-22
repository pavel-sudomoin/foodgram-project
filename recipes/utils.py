from django.core.paginator import Paginator

from .models import Tag


def get_ingredients(data):
    ingredients = {}
    for key, value in data.items():
        if 'nameIngredient' in key:
            ingredient_id = key.split('_')[1]
            ingredients[value] = round(
                float(data[f'valueIngredient_{ingredient_id}']), 1
            )
    return ingredients


def create_paginator(request, recipes):
    paginator = Paginator(recipes, 3)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return (paginator, page)


def tag_status_handler(selected_tags):
    tags = []
    current_href = ''
    if selected_tags:
        current_href = f'&tag={"&tag=".join(selected_tags)}'
    for tag in Tag.objects.all():
        href = selected_tags.copy()
        is_selected = False
        if tag.slug in href:
            href.remove(tag.slug)
            is_selected = True
        else:
            href.append(tag.slug)
        href = '&tag='.join(href)
        if href:
            href = f'?tag={href}'
        tags.append({
            'name': tag.name,
            'slug': tag.slug,
            'color_class': f'tags__checkbox_style_{tag.color}',
            'is_selected': is_selected,
            'href': href,
        })
    return tags, current_href
