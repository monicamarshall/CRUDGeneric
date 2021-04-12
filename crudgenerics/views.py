from django.shortcuts import render

from crudgenerics.models import Speaker
from crudgenerics.serializers import SpeakerSerializer

from rest_framework.generics import CreateAPIView
from rest_framework import generics

from rest_framework.pagination import PageNumberPagination

import logging
logger = logging.getLogger(__name__)

class StandardResultsSetPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100

class SpeakerDisplayCreate(generics.ListCreateAPIView):
    logger.debug("In SpeakerDisplayCreate")
    queryset = Speaker.objects.all()
    #pagination_class = StandardResultsSetPagination
    #logger.debug("Getting all speakers whose first name matches James");
    #queryset = Speaker.objects.filter(first_name = "James")    
    serializer_class = SpeakerSerializer 

    def get_serializer(self, *args, **kwargs):
        serializer_class = SpeakerSerializer

        draft_request_data = self.request.data.copy()
        logger.debug(draft_request_data);
        return serializer_class(*args, **kwargs)

class SpeakerUpdateDelete(generics.RetrieveUpdateDestroyAPIView):
    logger.debug("View/Update/Delete speaker");
    queryset = Speaker.objects.all()
    serializer_class = SpeakerSerializer
    


"""
class SpeakerCreate(CreateAPIView):
    serializer_class = SpeakerSerializer

    def get_serializer(self, *args, **kwargs):
        # leave this intact
        serializer_class = self.get_serializer_class()
        logger.debug("getting serializer_class")
        kwargs["context"] = self.get_serializer_context()
 

        Intercept the request and see if it needs tweaking
   
        if (name := self.request.data.get("name")) and (
            surname := self.request.data.get("name")
        ):

            #
            # Copy and manipulate the request
        draft_request_data = self.request.data.copy()
        logger.debug(draft_request_data);
        #draft_request_data["first_name"] = name
        #draft_request_data["last_name"] = surname
        kwargs["data"] = draft_request_data
        return serializer_class(*args, **kwargs)

        If not mind your own business and move on
     
        return serializer_class(*args, **kwargs)

class SpeakerCreate(generics.CreateAPIView):
    logger.debug("In SpeakerCreate")
    queryset = Speaker.objects.all()
     

    def get_serializer(self, *args, **kwargs):
        serializer_class = SpeakerSerializer
        draft_request_data = self.request.data.copy()
        #logger.debug(draft_request_data);
        return serializer_class(*args, **kwargs)
   """

