from django.shortcuts import render

from django.http import HttpResponse
from bulkload import utils

from contextlib import closing
import csv
from io import StringIO
import io

from django.db import connection
from django.utils import timezone
from django.conf import settings
import os
import time
from crudgenerics import models

from collections import defaultdict
from django.apps import apps

import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

import logging
logger = logging.getLogger(__name__)

class BulkCreateManager(object):
    """
    This helper class keeps track of ORM objects to be created for multiple
    model classes, and automatically creates those objects with `bulk_create`
    when the number of objects accumulated for a given model class exceeds
    `chunk_size`.
    Upon completion of the loop that's `add()`ing objects, the developer must
    call `done()` to ensure the final set of objects is created for all models.
    """

    def __init__(self, chunk_size=10000):
        self._create_queues = defaultdict(list)
        self.chunk_size = chunk_size

    def _commit(self, model_class):
        model_key = model_class._meta.label
        model_class.objects.bulk_create(self._create_queues[model_key])
        self._create_queues[model_key] = []

    def add(self, obj):
        """
        Add an object to the queue to be created, and call bulk_create if we
        have enough objs.
        """        
        model_class = type(obj)
        model_key = model_class._meta.label
        self._create_queues[model_key].append(obj)
        if len(self._create_queues[model_key]) >= self.chunk_size:
            self._commit(model_class)

    def done(self):
        """
        Always call this upon completion to make sure the final partial chunk
        is saved.
        """
        for model_name, objs in self._create_queues.items():
            if len(objs) > 0:
                self._commit(apps.get_model(model_name))    



def index(request):
    return render(request, 'bulkload/index.html')

def results(request):
    return render(request, 'bulkload/results.html')

def bulk_create(request):
    logger.debug("In django ORM bulk_create")
    file_name = "{}speakers2.csv".format(settings.MEDIA_ROOT)   
    #if( file_name != None):
        #logger.debug("csv_file_path = " + file_name) 
    stream = StringIO()
    stream = open(file_name, "r", encoding="utf-8")
    #stream.seek(0)   
    start = time.time()
    with open(file_name, 'rb') as csv_file:
        bulk_mgr = BulkCreateManager(chunk_size=10000)
        try:
            for row in csv.reader(stream):
                bulk_mgr.add(models.Speaker(first_name=row[0], 
                                        last_name=row[1],
                                        title=row[2],
                                        company=row[3],
                                        speaker_bio=row[4],
                                        speaker_photo=row[5].encode("utf-8"),))
        except Exception as e: 
            logger.debug("Error while importing data: " + e)  
        bulk_mgr.done()
        
    end = time.time()
    count = models.Speaker.objects.count()
    duration = end - start
    logger.debug ("duration in seconds: " + str(duration))    
    models.Speaker.objects.all().delete()
    result = "Created " + str(count)   + " rows in " + str(duration * 1000) + " milliseconds"
    logger.debug(result)
    return render(request, 'bulkload/results.html', {'result': result})

def copy_from(request):
    logger.debug("In Postgres copy_from")
 
    file_name = "{}speakers2.csv".format(settings.MEDIA_ROOT)
    #if( file_name != None):
        #logger.debug("csv_path = " + file_name)
    stream = open(file_name, "r", encoding="utf-8")
    stream.seek(0)
    start = time.time()
    with closing(connection.cursor()) as cursor:
        cursor.copy_from(
            file=stream,
            table='speakers',
            sep=',',
            columns=('first_name', 'last_name', 'title', 'company', 'speaker_bio', 'speaker_photo'),
        )
    end = time.time()
    count = models.Speaker.objects.count()
    duration = end - start
    logger.debug ("duration in seconds: " + str(duration))    
    #models.Speaker.objects.all().delete()
    result = "Created " + str(count)   + " rows in " + str(duration * 1000) + " milliseconds"
    logger.debug(result)
    return render(request, 'bulkload/results.html', {'result': result})




