from django.db import migrations


def add_tags(apps, schema_editor):
    Tag = apps.get_model('recipes', 'Tag')
    Tag(name='завтрак', slug='breakfast', color='orange').save()
    Tag(name='обед', slug='lunch', color='green').save()
    Tag(name='ужин', slug='dinner', color='purple').save()


class Migration(migrations.Migration):
    dependencies = [('recipes', '0001_initial')]
    operations = [migrations.RunPython(add_tags)]