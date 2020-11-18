import io
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect 
from django import template
from django.contrib import messages
from django.contrib.auth.models import Group, User
from django.template import RequestContext
from django.views.generic import CreateView, ListView
from django.urls import reverse
from django.core.exceptions import PermissionDenied
from .models import *
from .forms import *
from app import tasks
from core import settings
import logging
import sqlite3
import pandas as pd
import nltk
from nltk.corpus import stopwords
from wordcloud import WordCloud, STOPWORDS  
import numpy as np  
import matplotlib.pyplot as plt
import urllib, base64
import json
import string
import spacy
from spacy_spanish_lemmatizer import SpacyCustomLemmatizer


# nltk.download('stopwords')
# pip install spacy_spanish_lemmatizer
# python -m spacy_spanish_lemmatizer download wiki
# python -m spacy download es_core_news_sm 


STOPLIST = set(stopwords.words('spanish'))
SYMBOLS = " ".join(string.punctuation).split(" ")+ ["-", "...", "..","'"]

nlp = spacy.load('en_core_web_sm')

lemmatizer = SpacyCustomLemmatizer()
nlp.add_pipe(lemmatizer, name="lemmatizer", after="tagger")



def normalize(text):
    doc = nlp(text)
    words = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
    lexical_tokens = str([t.lower() for t in words if len(t) > 3 and t.isalpha()])
    return lexical_tokens
    
# **************************
# Nube de palabras Twitter
# **************************
def nube_de_palabras_t (text):       
        twitter_red_social = red_social.objects.get(nombre_red_social="Twitter")
        twitter_data_to_list = data_red.objects.filter(data_red_social = twitter_red_social).values('publicacion_texto')
        text = str(twitter_data_to_list)        
        word_list = normalize(text)    
        
        stopwords = set(STOPWORDS)           
        stopwords.add("queryset'")
        # stopwords.add('publicacion_texto')
        # stopwords.add("publicacion_texto'")
        # stopwords.add('publicacion_texto RT')
        # stopwords.add('una')
        
        wordcloud = WordCloud(background_color='white', stopwords=stopwords).generate(word_list)
        plt.imshow(wordcloud)
        plt.axis("off")
        #plt.show()
        image = io.BytesIO()
        plt.savefig(image, format='png')
        image.seek(0)  # rewind the data
        string = base64.b64encode(image.read())

        image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
        return image_64            
        # 
        # plt.imshow(wordcloud)
        # plt.axis("off")
        # s = plt.show()

def cloud_gen_t(request):
    twitter_red_social = red_social.objects.get(nombre_red_social="Twitter")
    twitter_data_to_list = data_red.objects.filter(data_red_social = twitter_red_social).values('publicacion_texto')
    texto = str(twitter_data_to_list)
    word_list = normalize(texto)
    text = ''
    
    for i in word_list:
        if __name__ == '__main__':
            text += i.text

    wordcloud = nube_de_palabras_t(text)
    return render(request, "nube_de_palabras_twitter.html",{'wordcloud':wordcloud})


 # **************************
# Nube de palabras Facebook
# **************************
def nube_de_palabras_fb (text):       
        fb_red_social = red_social.objects.get(nombre_red_social="Facebook")
        fb_data_to_list = data_red.objects.filter(data_red_social = fb_red_social).values('publicacion_texto')
        text = str(fb_data_to_list)
        word_list = normalize(text)    
        
        stopwords = set(STOPWORDS)           
        stopwords.add("queryset'")
        # stopwords.add('publicacion_texto')
        # stopwords.add("publicacion_texto'")
        # stopwords.add('publicacion_texto RT')
        # stopwords.add('una')
        
        wordcloud = WordCloud(background_color='white', stopwords=stopwords).generate(word_list)
        plt.imshow(wordcloud)
        plt.axis("off")
        #plt.show()
        image = io.BytesIO()
        plt.savefig(image, format='png')
        image.seek(0)  # rewind the data
        string = base64.b64encode(image.read())

        image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
        return image_64            
        # 
        # plt.imshow(wordcloud)
        # plt.axis("off")
        # s = plt.show()

def cloud_gen_fb(request):
    fb_red_social = red_social.objects.get(nombre_red_social="Facebook")
    fb_data_to_list = data_red.objects.filter(data_red_social = fb_red_social).values('publicacion_texto')
    texto = str(fb_data_to_list)
    word_list = normalize(texto)
    text = ''
    
    for i in word_list:
        if __name__ == '__main__':
            text += i.text

    wordcloud = nube_de_palabras_fb(text)
    return render(request, "nube_de_palabras_fb.html",{'wordcloud':wordcloud})   


