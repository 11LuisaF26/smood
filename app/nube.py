import io
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.template import loader
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
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
from django.db.models import Q
from sklearn.feature_extraction.text import CountVectorizer

nltk.download('punkt')
nltk.download('stopwords')
#pip install spacy_spanish_lemmatizer
#python -m spacy_spanish_lemmatizer download wiki
#python -m spacy download es_core_news_sm 


STOPLIST = set(stopwords.words('spanish'))
SYMBOLS = " ".join(string.punctuation).split(" ")+ ["-", "...", "..","'"]

nlp = spacy.load('es_core_news_sm')

# lemmatizer = SpacyCustomLemmatizer()
# nlp.add_pipe(lemmatizer, name="lemmatizer", after="tagger")



def normalize(text):
    doc = nlp(text)
    words = [t.orth_ for t in doc if not t.is_punct | t.is_stop]
    lexical_tokens = str([t.lower() for t in words if len(t) > 3 and t.isalpha()])
    return lexical_tokens
    
def nube_de_palabras(text):  
    words = nltk.tokenize.word_tokenize(text)
    stopwords = set(STOPWORDS)           
    stopwords.add("queryset")    
    stopwords.add("'")                               
    plt.figure(figsize = (20,5))
        
    wordcloud = WordCloud(background_color='white', stopwords=stopwords).generate(text)
    plt.figure(figsize = (10,5))
    plt.imshow(wordcloud, interpolation= 'bilinear')
    plt.axis("off")
    
    #------------------------------------------------------------------------------
    #Crear diccionario de frecuencias
    text_dictionary = wordcloud.process_text(text)
    #Ordenar por frecuencia
    word_freq={k: v for k, v in sorted(text_dictionary.items(),reverse=True, key=lambda item: item[1])}
    rel_freq=wordcloud.words_
    tuplas = list(word_freq.items())[:5]
    print(tuplas)
    
    cv=CountVectorizer(stop_words=STOPWORDS, ngram_range=(1, 3))
  
    #------------------------------------------------------------------------------
    image = io.BytesIO()
    plt.savefig(image, format='png')
    image.seek(0)  # rewind the data
    string = base64.b64encode(image.read())

    image_64 = 'data:image/png;base64,' + urllib.parse.quote(string)
    return image_64

# **************************
# Palabras mas usadas
# **************************
def palabras_mas_usadas(text):  
    words = nltk.tokenize.word_tokenize(text)
    stopwords = set(STOPWORDS)           
    stopwords.add("queryset")    
    stopwords.add("'")                               
    plt.figure(figsize = (3,2))
        
    wordcloud = WordCloud(background_color='white', stopwords=stopwords).generate(text)

    #------------------------------------------------------------------------------
    #Crear diccionario de frecuencias
    text_dictionary = wordcloud.process_text(text)
    #Ordenar por frecuencia
    word_freq={k: v for k, v in sorted(text_dictionary.items(),reverse=True, key=lambda item: item[1])}
    rel_freq=wordcloud.words_
    tuplas = list(word_freq.items())[:5]
    print(tuplas)
    arr = np.array(tuplas)
    df = pd.DataFrame.from_records(arr, columns=['Palabras', 'Cantidad'])
    tabla = df.to_html
    return tabla


# **************************
# Nube de palabras Twitter
# **************************
def cloud_gen_t(request, id):  
    if request.method == 'GET':
            if id!=0:
                emp = empresa.objects.get(pk=id)   
                camp = campana_publicitaria.objects.get(empresa_campana=emp)             
                twitter_red_social = red_social.objects.get(nombre_red_social="Twitter")                
                twitter_data = data_red.objects.filter(data_red_campana =camp,data_red_social =twitter_red_social ).values('publicacion_texto')        
                
                texto = str(twitter_data)    
                word_list = normalize(texto)
                text =  word_list.replace("'", '')
                wordcloud = nube_de_palabras(text)
                barras = palabras_mas_usadas(text)                
                return render(request, "nube_de_palabras_twitter.html",{'form': camp,'wordcloud':wordcloud ,'barras':barras})


# **************************
# Nube de palabras Facebook
# **************************
def cloud_gen_fb(request, id=0):
    emp = campana_publicitaria.objects.get(pk=id)        
    fb_red_social = red_social.objects.get(nombre_red_social="Facebook")
    fb_data_to_list = data_red.objects.filter(data_red_campana =emp,data_red_social =fb_red_social).values('publicacion_texto')        
    texto = str(fb_data_to_list)    
    word_list = normalize(texto)
    text =  word_list.replace("'", '')
    wordcloud = nube_de_palabras(text)

    return render(request, "nube_de_palabras_fb.html",{'wordcloud':wordcloud})   

# **************************
# Nube de palabras Instagram
# **************************
def cloud_gen_ig(request, id=0):
    emp = campana_publicitaria.objects.get(pk=id)        
    ig_red_social = red_social.objects.get(nombre_red_social="Instagram")
    ig_data_to_list = data_red.objects.filter(data_red_campana =emp,data_red_social =ig_red_social).values('publicacion_texto')        
    texto = str(ig_data_to_list)
    word_list = normalize(texto)
    text =  word_list.replace("'", '')
    
    wordcloud = nube_de_palabras(text)

    return render(request, "nube_de_palabras_ig.html",{'wordcloud':wordcloud})


# **************************
# Red de palabras
# **************************

def tokenizeText(sample):    
    doc = nlp(sample)
    stopwords = set(STOPLIST)           
    stopwords.add("queryset")    
    lemmas = [token.lemma_ for token in doc if not token.is_stop]
    a_lemmas = [lemma for lemma in lemmas if (lemma.isalpha()  and lemma != '-PRON-') and lemma not in stopwords and lemma not in SYMBOLS]    
    return a_lemmas


def generador(texto):    
    arreglo=[]
    for i in range(0,len(texto)):                
        if len(texto[i])>5:            
            data=tokenizeText(texto[i])
            data_tree=dict()
            data_tree['submissionID']=str(i)
            data_tree['keywords']=data           
            
            arreglo.append(data_tree)
    return json.dumps(arreglo,ensure_ascii=False)


def red_palabras_t(request, id=0):
    #texto
    emp = empresa.objects.get(pk=id)  
    camp = campana_publicitaria.objects.get(empresa_campana=emp)         
    twitter_red_social = red_social.objects.get(nombre_red_social="Twitter")                
    twitter_data = data_red.objects.filter(data_red_campana =camp,data_red_social =twitter_red_social ).values_list('publicacion_texto') 
    word = list(twitter_data)
    texto = [i for (i,) in word[0:50]]          
    red_palabras = generador(texto)
    
    return render(request, "red_palabras_twitter.html", {'form': camp,'red_palabras':red_palabras})
    

def red_palabras_fb(request, id=0):
    #texto
    emp = campana_publicitaria.objects.get(pk=id)        
    fb_red_social = red_social.objects.get(nombre_red_social="Facebook")                
    fb_data = data_red.objects.filter(data_red_campana =emp,data_red_social =fb_red_social ).values_list('publicacion_texto') 
    word = list(fb_data)
    texto = [i for (i,) in word]           
    red_palabras = generador(fb_red_social,texto)
    
    return render(request, "red_palabras_fb.html", {'red_palabras':red_palabras})

def red_palabras_ig(request, id=0):
    #texto
    emp = campana_publicitaria.objects.get(pk=id)        
    ig_red_social = red_social.objects.get(nombre_red_social="Instagram")                
    ig_data = data_red.objects.filter(data_red_campana =emp,data_red_social =ig_red_social ).values_list('publicacion_texto') 
    word = list(ig_data)
    texto = [i for (i,) in word]           
    red_palabras = generador(ig_red_social,texto)
    
    return render(request, "red_palabras_ig.html", {'red_palabras':red_palabras})
