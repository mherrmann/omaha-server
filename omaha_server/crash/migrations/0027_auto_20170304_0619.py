# -*- coding: utf-8 -*-
# Generated by Django 1.9.6 on 2017-03-04 06:19

import os

from django.db import migrations
from django.conf import settings


def update_symbols_urls(apps, schema_editor):
    if settings.DEFAULT_FILE_STORAGE == 'omaha_server.s3utils.S3Storage':
        Symbols = apps.get_model("crash", "Symbols")
        symbols = Symbols.objects.filter(debug_file__contains=' ').iterator()
        for symbol in symbols:
            old_name = symbol.file.name
            if symbol.file.storage.exists(old_name):
                head, tail = os.path.split(old_name)
                new_name = os.path.join(head, '%s.sym' % symbol.debug_file)
                storage = symbol.file.storage
                file_obj = storage._open(old_name)
                symbol.file.save(new_name, file_obj)
                file_obj.close()
                storage.delete(old_name)
            else:
                print("File %s was not found" % old_name)


class Migration(migrations.Migration):

    dependencies = [
        ('crash', '0026_auto_20170304_0601'),
    ]

    operations = [
        migrations.RunPython(
            update_symbols_urls,
            reverse_code=migrations.RunPython.noop
        ),
    ]