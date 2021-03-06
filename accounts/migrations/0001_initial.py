from django.contrib.auth.hashers import make_password
from django.db import migrations, models
import hashlib


def add_users(apps, _schema_editor):
    """
    apps: ? Used; to get apps
    _schema_editor: ?; not used parameter
    return:

    Initialize User models.
    """
    User = apps.get_model('accounts', 'User')
    pwd_hash = make_password('scMN4244', hasher='pbkdf2_sha256')
    User.objects.get_or_create(username='admin', email='irene.chae@uhn.ca', password=pwd_hash, staff=True,
                               admin=True, is_superuser=True, specialist=True, counselor=True, scientist=True)

    users = ['scientist', 'counselor', 'specialist', 'staff']
    for user_str in users:
        pwd_hash = make_password(user_str, hasher='pbkdf2_sha256')
        user = User.objects.create(username=user_str, email=user_str + '@uhn.ca', password=pwd_hash, staff=True)
        if user_str in users[:3]:
            user.specialist = True
        if user_str in users[:2]:
            user.counselor = True
        if user_str == 'scientist':
            user.scientist = True
        user.save()


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(max_length=150, unique=True)),
                ('email', models.EmailField(max_length=255, null=True, verbose_name='email address')),
                ('active', models.BooleanField(default=True)),
                ('is_active', models.BooleanField(default=True)),
                ('staff', models.BooleanField(default=False)),
                ('specialist', models.BooleanField(default=False)),
                ('counselor', models.BooleanField(default=False)),
                ('scientist', models.BooleanField(default=False)),
                ('admin', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),

        migrations.RunPython(add_users),
    ]
