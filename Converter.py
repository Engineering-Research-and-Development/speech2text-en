#!/usr/bin/env python
# coding: utf-8

# In[1]:


import grpc
from concurrent import futures
import threading
import time

import speechtotext_pb2 as pb2
import speechtotext_pb2_grpc as grpc2

from grpc_interceptor import ExceptionToStatusInterceptor
from grpc_interceptor.exceptions import NotFound

from pydub import AudioSegment

import os
import io
import speech_recognition as sr 

import logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)


# In[2]:


port = 8061
r = sr.Recognizer()


# In[3]:


def AppendSpeechToText(prev_text, chunk, segid):
    
    chunk = AudioSegment.from_file(io.BytesIO(chunk), format="wav")
    filename = "./tmp{}.wav".format(segid)
    chunk.export(filename, format="wav")
    
    
    with sr.AudioFile(filename) as source:
        audio_listened = r.record(source)
    
        try:
            text = r.recognize_google(audio_listened)
        except sr.UnknownValueError as e:
            print("Error:", str(e))
        else:
            text = f"{text.capitalize()}. "
            newtext = prev_text + text
        # return the text for all chunks detected
        return newtext


# In[4]:

def Myprint(msg):
       
    debug = open("dbg.txt", "a")
    debug.write(msg + "\n")
    debug.close()


class ConverterServiceImpl(grpc2.ConverterServicer):


    def Convert(self, request_iterator, context):
    
        
        
        if not request_iterator:
            Myprint("Client Request Incorrect")
            raise NotFound("Client Request Incorrect")

        prev_text = ""
        prev = -1

        Myprint("NEW REQUEST ARRIVED")

        
        try:
            for item in request_iterator:
                prev_text = AppendSpeechToText(prev_text, item.audiosegment, item.audiosegmentid)
                Myprint("Current segment: {}, prev segment: {}".format(item.audiosegmentid, prev))
                if item.audiosegmentid > prev + 5:
                    raise StopIteration
                else:
                    prev = item.audiosegmentid
            
        except StopIteration:
            Myprint("AUDIO ENDED! current id: {}, prev_id: {}".format(item.audiosegmentid, prev))
            Myprint(prev_text)
            T = pb2.Text()
            T.audioid = item.audioid
            T.text = prev_text
            return T
            Myprint("returned")
                    
        
        
        

                
        
        


# In[5]:

interceptors = [ExceptionToStatusInterceptor()]
server = grpc.server(futures.ThreadPoolExecutor(max_workers = 10), interceptors=interceptors)
grpc2.add_ConverterServicer_to_server(ConverterServiceImpl(), server)
print("Starting server, Listening on port:" + str(port))
server.add_insecure_port("[::]:{}".format(port))
server.start()
server.wait_for_termination()


# In[ ]:




