from django.db import models
from django.contrib.auth import get_user_model

from autoslug import AutoSlugField

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200)
    unit = models.CharField(max_length=50)

    def __str__(self):
            return self.name


class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=50)
    slug = models.SlugField(unique=True, max_length=50)

    def __str__(self):
            return self.name


class Recipe(models.Model):
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='recipes'
    )
    name = models.CharField(max_length=50)
    image = models.ImageField(upload_to="recipes/")
    description = models.TextField()
    ingredient = models.ManyToManyField(
        Ingredient,
        through='IngredientAmount',
        related_name='recipes')
    tag = models.ManyToManyField(
        Tag,
        related_name='recipes')
    time = models.PositiveIntegerField()
    slug = AutoSlugField(populate_from='name', always_update=True, unique=True)
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    def __str__(self):
            return self.name

    class Meta:
        ordering = ("-pub_date",)


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
    quantity = models.FloatField()

    class Meta:
        unique_together = ('recipe', 'ingredient')

    def save(self, *args, **kwargs):
        print('Save method executed!')
        super(IngredientAmount, self).save(*args, **kwargs)
