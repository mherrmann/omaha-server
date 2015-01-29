# coding: utf8

"""
This software is licensed under the Apache 2 license, quoted below.

Copyright 2014 Crystalnix Limited

Licensed under the Apache License, Version 2.0 (the "License"); you may not
use this file except in compliance with the License. You may obtain a copy of
the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
License for the specific language governing permissions and limitations under
the License.
"""

from rest_framework import serializers

from omaha.models import Application, Channel

from models import SparkleVersion


__all__ = ['SparkleVersionSerializer']



class SparkleVersionSerializer(serializers.HyperlinkedModelSerializer):
    app = serializers.PrimaryKeyRelatedField(queryset=Application.objects.all())
    channel = serializers.PrimaryKeyRelatedField(queryset=Channel.objects.all())
    version = serializers.CharField()

    class Meta:
        model = SparkleVersion
        fields = ('id', 'app', 'channel', 'version', 'short_version',
                  'release_notes', 'file', 'file_size', 'dsa_signature',
                  'created', 'modified')
        read_only_fields = ('created', 'modified')

    def create(self, validated_data):
        if not validated_data.get('file_size'):
            file = validated_data['file']
            validated_data['file_size'] = file.size
        return super(SparkleVersionSerializer, self).create(validated_data)