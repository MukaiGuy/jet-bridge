# Generated by Django 2.1.8 on 2019-10-07 17:05

from django.db import connection, migrations


def load(apps, schema_editor):
    with connection.cursor() as cursor:
        cursor.execute('SELECT token, date_add FROM jet_django_token')
        old_token = cursor.fetchone()

        if not old_token:
            return

        cursor.execute('SELECT id FROM __jet__token')
        new_token = cursor.fetchone()

        if new_token is None:
            cursor.execute('INSERT INTO __jet__token (token, date_add) VALUES (%s, %s)', [
                old_token[0].hex,
                old_token[1]
            ])
        else:
            cursor.execute('UPDATE __jet__token SET token = %s, date_add = %s WHERE id = %s', [
                old_token[0].hex,
                old_token[1],
                new_token[0]
            ])


class Migration(migrations.Migration):

    dependencies = [
        ('jet_django', '0002_auto_20181014_2002'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='token',
            options={'managed': False, 'verbose_name': 'token', 'verbose_name_plural': 'tokens'},
        ),
        migrations.RunPython(load, reverse_code=lambda a, b: ()),
    ]