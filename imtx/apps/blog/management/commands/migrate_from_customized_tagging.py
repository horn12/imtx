import os

from django.core import serializers
from django.core.management.base import BaseCommand, CommandError

class Command(BaseCommand):
    def handle(self, *args, **options):
        if len(args) != 1:
            print 'Please enter the file name'
            return
        filename = args[0]
        for obj in serializers.deserialize('json', open(filename).read()):
            obj.save()
