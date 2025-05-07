from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('communities', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='Post',
            name='visibility',
            field=models.CharField(
                choices=[('public', 'Public'), ('members_only', 'Members Only')],
                default='public',
                max_length=20
            ),
        ),
    ] 