# Generated by Django 4.0 on 2022-03-15 21:52

from django.db import migrations, models
import django.db.models.deletion
import django_countries.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='SaasConfiguration',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64, verbose_name='name')),
                ('language', models.CharField(max_length=10, verbose_name='language')),
                ('value', models.CharField(max_length=250, verbose_name='value')),
            ],
            options={
                'db_table': 'saas_configuration',
            },
        ),
        migrations.CreateModel(
            name='SaasProduct',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('slug', models.CharField(default='invalid', max_length=50, unique=True, verbose_name='slug')),
                ('name', models.CharField(max_length=16, verbose_name='name')),
                ('activation_url', models.CharField(default='https://%prefix%identifier.example.org/activate', max_length=250, verbose_name='Activation URL')),
                ('instance_url', models.CharField(default='https://%prefix%identifier.example.org', max_length=250, verbose_name='Instance URL')),
                ('is_active', models.BooleanField(default=False, verbose_name='is active')),
                ('number_of_ports', models.IntegerField(default=1, verbose_name='number of ports')),
                ('instance_prefix', models.CharField(default='xy', max_length=10, verbose_name='instance prefix')),
            ],
            options={
                'db_table': 'saas_product',
            },
        ),
        migrations.CreateModel(
            name='SaasProductLanguage',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('language', models.CharField(default='DE', max_length=10, verbose_name='language')),
                ('payment_details', models.CharField(default='', max_length=300, verbose_name='payment_details')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.saasproduct')),
            ],
            options={
                'db_table': 'saas_product_language',
            },
        ),
        migrations.CreateModel(
            name='SaasPlan',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16, verbose_name='name')),
                ('period_length_in_months', models.IntegerField(verbose_name='Period Length in Months')),
                ('currency_code', models.CharField(default='EUR', max_length=3, verbose_name='currency')),
                ('cost_per_period', models.DecimalField(decimal_places=2, max_digits=10, verbose_name='Cost per Period')),
                ('notice_period_in_days', models.IntegerField(verbose_name='Notice Period in Days')),
                ('language', models.CharField(default='DE', max_length=10, verbose_name='Language')),
                ('descr_target', models.CharField(default='TODO', max_length=200, verbose_name='Description Target')),
                ('descr_caption', models.CharField(default='TODO', max_length=200, verbose_name='Description Caption')),
                ('descr_1', models.CharField(default='TODO', max_length=200, verbose_name='Description 1')),
                ('descr_2', models.CharField(default='TODO', max_length=200, verbose_name='Description 2')),
                ('descr_3', models.CharField(default='TODO', max_length=200, verbose_name='Description 3')),
                ('descr_4', models.CharField(default='TODO', max_length=200, verbose_name='Description 4')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.saasproduct')),
            ],
            options={
                'db_table': 'saas_plan',
            },
        ),
        migrations.CreateModel(
            name='SaasInstance',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=16, verbose_name='identifier')),
                ('hostname', models.CharField(default='localhost', max_length=128, verbose_name='hostname')),
                ('pacuser', models.CharField(default='xyz00', max_length=128, verbose_name='pacuser')),
                ('channel', models.CharField(default='stable', max_length=128, verbose_name='channel')),
                ('first_port', models.IntegerField(default=-1, verbose_name='first port')),
                ('last_port', models.IntegerField(default=-1, verbose_name='last port')),
                ('activation_token', models.CharField(max_length=64, null=True)),
                ('status', models.CharField(default='in_preparation', max_length=16, verbose_name='Status')),
                ('db_password', models.CharField(default='topsecret', max_length=64, verbose_name='DB Password')),
                ('initial_password', models.CharField(default='topsecret', max_length=64, verbose_name='Initial Password')),
                ('last_interaction', models.DateTimeField(null=True, verbose_name='Last Interaction')),
                ('reserved_token', models.CharField(max_length=64, null=True)),
                ('reserved_until', models.DateTimeField(null=True, verbose_name='Reserved Until')),
                ('product', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.saasproduct')),
                ('reserved_for_user', models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='auth.user')),
            ],
            options={
                'db_table': 'saas_instance',
            },
        ),
        migrations.CreateModel(
            name='SaasCustomer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('newsletter', models.BooleanField(default=True, verbose_name='newsletter')),
                ('newsletter_subscribed_on', models.DateTimeField(null=True, verbose_name='newsletter_subscribed_on')),
                ('newsletter_cancelled', models.DateTimeField(null=True, verbose_name='newsletter_cancelled')),
                ('language_code', models.CharField(default='de', max_length=16, verbose_name='language_code')),
                ('verified', models.BooleanField(default=True, verbose_name='verified')),
                ('verification_token', models.CharField(max_length=64, null=True, verbose_name='verification_token')),
                ('verification_until', models.DateTimeField(null=True, verbose_name='verification_until')),
                ('organisation_name', models.CharField(max_length=64, null=True, verbose_name='organisation_name')),
                ('title', models.CharField(blank=True, choices=[('Mr', 'Mr'), ('Mrs', 'Mrs'), ('Mr Dr', 'Mr Dr'), ('Mrs Dr', 'Mrs Dr')], max_length=64, verbose_name='Title')),
                ('first_name', models.CharField(default='', max_length=64, verbose_name='first_name')),
                ('last_name', models.CharField(default='', max_length=64, verbose_name='last_name')),
                ('street', models.CharField(default='', max_length=64, verbose_name='street')),
                ('post_code', models.CharField(default='', max_length=10, verbose_name='post_code')),
                ('city', models.CharField(default='', max_length=16, verbose_name='city')),
                ('country_code', django_countries.fields.CountryField(default='DE', max_length=2, verbose_name='country')),
                ('email_address', models.EmailField(max_length=254, verbose_name='email_address')),
                ('is_active', models.BooleanField(default=True, verbose_name='is_active')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user')),
            ],
            options={
                'db_table': 'saas_customer',
            },
        ),
        migrations.CreateModel(
            name='SaasContract',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_date', models.DateField(null=True, verbose_name='start_date')),
                ('end_date', models.DateField(null=True, verbose_name='end_date')),
                ('latest_cancel_date', models.DateField(null=True, verbose_name='latest_cancel_date')),
                ('auto_renew', models.BooleanField(default=True, verbose_name='auto_renew')),
                ('customer', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.saascustomer')),
                ('instance', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.saasinstance')),
                ('plan', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='%(app_label)s_%(class)s_list', to='core.saasplan')),
            ],
            options={
                'db_table': 'saas_contract',
            },
        ),
        migrations.AddConstraint(
            model_name='saasinstance',
            constraint=models.UniqueConstraint(fields=('identifier', 'product'), name='identifier and product'),
        ),
    ]
