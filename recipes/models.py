from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Ingredient(models.Model):
    ingredient = models.TextField()


class Unit(models.Model):
    unit = models.TextField()


class Recipe(models.Model):
    TAG_CHOICES = [
        ('breakfast', 'завтрак'),
        ('lunch', 'обед'),
        ('dinner', 'ужин'),
    ]
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.TextField()
    image = models.ImageField(upload_to="recipes/", blank=True, null=True)
    description = models.TextField()
    ingredient = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes')
    tag = models.CharField(choices=TAG_CHOICES, max_length=300)
    time = models.DurationField()
    slug = models.SlugField(unique=True)


class IngredientAmount(models.Model):
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='ingredient_amounts'
    )
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.PROTECT,
        related_name='ingredient_amounts'
    )
    unit = models.ForeignKey(
        Unit,
        on_delete=models.PROTECT,
        related_name='ingredient_amounts'
    )
    quantity = models.FloatField()


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="follower"
    )
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following"
    )

    class Meta:
        unique_together = ('user', 'author')


class Favorite(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorites'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorited'
    )

    class Meta:
        unique_together = ('user', 'recipe')
