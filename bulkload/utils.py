import os
import time

import django
from django.db.transaction import atomic

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'settings')
django.setup()

from crudgenerics import models

import logging
logger = logging.getLogger(__name__)


def timed(fn):
    logger.debug("In timed method")
    n_records = 10000

    start = time.time()
    with atomic():
        fn(n_records)
    end = time.time()

    count = models.Speaker.objects.count()
    models.Speaker.objects.all().delete()
    assert count == n_records

    logger.debug("Created " + n_records + " in " + ((end - start) * 1000) + " milliseconds")
 