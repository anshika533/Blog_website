from django.utils import timezone
from django.db import migrations, models

class Migration(migrations.Migration):

    dependencies = [
        ('myblog_app', '0002_exploretopic'),
    ]

    operations = [
        migrations.AddField(
            model_name='exploretopic',
            name='date',
            field=models.DateField(auto_now_add=True, default=timezone.now),
            preserve_default=False,
        ),
    ]
