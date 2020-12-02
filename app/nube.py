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
        # ' ''.join(twitter_data_to_list)
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

# **************************
# Nube de palabras Instagram
# **************************

def nube_de_palabras_ig (text):       
        ig_red_social = red_social.objects.get(nombre_red_social="Instagram")
        ig_data_to_list = data_red.objects.filter(data_red_social = ig_red_social).values('publicacion_texto')
        text = str(ig_data_to_list)
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

def cloud_gen_ig(request):
    ig_red_social = red_social.objects.get(nombre_red_social="Instagram")
    ig_data_to_list = data_red.objects.filter(data_red_social = ig_red_social).values('publicacion_texto')
    texto = str(ig_data_to_list)
    word_list = normalize(texto)
    text = ''
    
    for i in word_list:
        if __name__ == '__main__':
            text += i.text

    wordcloud = nube_de_palabras_ig(text)
    return render(request, "nube_de_palabras_ig.html",{'wordcloud':wordcloud})  


# **************************
# Red de palabras
# **************************

def tokenizeText(sample):    
    doc = nlp(sample)
    lemmas = [token.lemma_ for token in doc]
    a_lemmas = [lemma for lemma in lemmas if (lemma.isalpha()  and lemma != '-PRON-') and lemma not in STOPLIST and lemma not in SYMBOLS]
    return a_lemmas
'''
df=pd.read_csv('C:\\Users\\Jaime\\Documents\\Luisa\\git\\descarga.csv')
df=df.fillna(" ")
'''

def generador(nombre,texto,User):
    arreglo=[]
    for i in range(0,len(texto)):
        if len(texto[i])>10:
            data=tokenizeText(texto[i])
            data_tree=dict()
            data_tree['submissionID']=str(i)
            data_tree['keywords']=data
            data_tree['year']=nombre[i]
            data_tree['cleanTitle']=User[i]
            arreglo.append(data_tree)
    return json.dumps(arreglo,ensure_ascii=False)

#print('var keywords1='+generador(df["data red social"].values.tolist(),df["Text"].values.tolist(),df["User"].values.tolist())+";")


def red(request):
    return render(request, "red.html") 