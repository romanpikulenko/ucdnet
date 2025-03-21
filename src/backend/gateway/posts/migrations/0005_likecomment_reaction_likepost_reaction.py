# Generated by Django 5.1.5 on 2025-03-08 10:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0004_alter_post_content'),
    ]

    operations = [
        migrations.AddField(
            model_name='likecomment',
            name='reaction',
            field=models.CharField(blank=True, choices=[('like', 'Like'), ('love', 'Love'), ('wow', 'Wow'), ('sad', 'Sad'), ('angry', 'Angry')], max_length=50, null=True),
        ),
        migrations.AddField(
            model_name='likepost',
            name='reaction',
            field=models.CharField(blank=True, choices=[('like', 'Like'), ('love', 'Love'), ('wow', 'Wow'), ('sad', 'Sad'), ('angry', 'Angry')], max_length=50, null=True),
        ),
    ]
