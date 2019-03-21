# Generated by Django 2.1.7 on 2019-03-20 05:12

import django.contrib.auth.models
import django.contrib.auth.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0009_alter_user_last_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='UserInfor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=30, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
                ('avatar', models.FileField(default='avatars/default.png', upload_to='avatars/', verbose_name='头像')),
                ('email', models.CharField(max_length=32, null=True, verbose_name='邮箱')),
                ('create_time', models.DateTimeField(auto_now_add=True, verbose_name='注册时间')),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups')),
            ],
            options={
                'verbose_name_plural': '12.用户信息',
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='bathAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('num_bath', models.IntegerField(verbose_name='洗浴人数')),
                ('num_brand', models.IntegerField(default='', verbose_name='洗浴手牌号')),
                ('num_back', models.IntegerField(verbose_name='搓背人数')),
                ('remark_bath', models.CharField(default='', max_length=225, verbose_name='备注（洗浴）')),
                ('day_bath', models.CharField(default='', max_length=32, verbose_name='洗浴时间')),
                ('price_bath', models.IntegerField(verbose_name='洗浴价格')),
            ],
            options={
                'verbose_name_plural': '2.洗浴',
            },
        ),
        migrations.CreateModel(
            name='cataHouse',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('house_name', models.CharField(default='', max_length=20, verbose_name='住房类型')),
            ],
            options={
                'verbose_name_plural': '3.房间类型',
            },
        ),
        migrations.CreateModel(
            name='electricityAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_elect', models.CharField(default='', max_length=60, verbose_name='缴费时间')),
                ('num_elect', models.CharField(default='', max_length=60, verbose_name='用电度数')),
                ('price_elect', models.IntegerField(null=True, verbose_name='电费')),
            ],
            options={
                'verbose_name_plural': '8.电费',
            },
        ),
        migrations.CreateModel(
            name='expenseAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('expen_cate', models.CharField(default='', max_length=20, verbose_name='支出类型')),
                ('price_account', models.IntegerField(verbose_name='支出金额')),
                ('day_expense', models.CharField(default='', max_length=20, verbose_name='时间')),
                ('remark_account', models.CharField(default='', max_length=225, verbose_name='支出（备注）')),
            ],
            options={
                'verbose_name_plural': '4.支出',
            },
        ),
        migrations.CreateModel(
            name='houseAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(default='', max_length=20, verbose_name='房客姓名')),
                ('sex', models.CharField(default='', max_length=20, verbose_name='房客性别')),
                ('identity', models.CharField(default='', max_length=20, verbose_name='房客身份证')),
                ('num_house', models.IntegerField(verbose_name='房间号')),
                ('day_house', models.IntegerField(verbose_name='订房天数')),
                ('price_house', models.IntegerField(verbose_name='房价')),
                ('day_time', models.DateTimeField(auto_now_add=True, verbose_name='住房时间')),
                ('remark_house', models.CharField(default='', max_length=225, verbose_name='备注（住房）')),
                ('cata_house', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app01.cataHouse', verbose_name='住房类型')),
            ],
            options={
                'verbose_name_plural': '1.住房',
            },
        ),
        migrations.CreateModel(
            name='incomeAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('day_income', models.CharField(default='', max_length=32, verbose_name='住房类型')),
                ('total_bath', models.IntegerField(null=True, verbose_name='洗浴总收入')),
                ('total_house', models.IntegerField(null=True, verbose_name='住房总收入')),
                ('total_store', models.IntegerField(null=True, verbose_name='百货总收入')),
                ('total_bath_house', models.IntegerField(null=True, verbose_name='住房和洗浴总收入')),
                ('total_pay', models.IntegerField(null=True, verbose_name='总支出')),
                ('total_income', models.IntegerField(null=True, verbose_name='总收入')),
                ('remark_income', models.CharField(default='', max_length=225, verbose_name='备注（收入）')),
            ],
            options={
                'verbose_name_plural': '5.总收入',
            },
        ),
        migrations.CreateModel(
            name='Menu',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='菜单名称')),
                ('icon', models.CharField(max_length=32, verbose_name='图标')),
            ],
            options={
                'verbose_name_plural': '9.菜单',
            },
        ),
        migrations.CreateModel(
            name='otherAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cata_other', models.CharField(default='', max_length=32, verbose_name='其他收入类型')),
                ('price_other', models.IntegerField(null=True, verbose_name='住房其他收入价格')),
                ('day_other', models.CharField(default='', max_length=32, verbose_name='时间')),
                ('remark_other', models.CharField(default='', max_length=225, verbose_name='备注（其他）')),
            ],
            options={
                'verbose_name_plural': '7.其他收入',
            },
        ),
        migrations.CreateModel(
            name='Role',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=32, verbose_name='角色名称')),
            ],
            options={
                'verbose_name_plural': '11.角色',
            },
        ),
        migrations.CreateModel(
            name='storeAccount',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cata_store', models.CharField(default='', max_length=32, verbose_name='百货类型')),
                ('price_store', models.IntegerField(null=True, verbose_name='百货价格')),
                ('day_store', models.CharField(default='', max_length=32, verbose_name='时间')),
                ('remark_store', models.CharField(default='', max_length=225, verbose_name='备注（百货）')),
            ],
            options={
                'verbose_name_plural': '6.百货收入',
            },
        ),
        migrations.AddField(
            model_name='userinfor',
            name='roles',
            field=models.ManyToManyField(blank=True, to='app01.Role', verbose_name='拥有的所有角色'),
        ),
        migrations.AddField(
            model_name='userinfor',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]