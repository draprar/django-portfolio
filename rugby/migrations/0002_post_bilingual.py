from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('rugby', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='title',
            new_name='title_pl',
        ),
        migrations.RenameField(
            model_name='post',
            old_name='text',
            new_name='text_pl',
        ),
        migrations.AddField(
            model_name='post',
            name='title_en',
            field=models.CharField(blank=True, max_length=255, verbose_name='Title (EN)'),
        ),
        migrations.AddField(
            model_name='post',
            name='text_en',
            field=models.TextField(blank=True, verbose_name='Text (EN)'),
        ),
    ]