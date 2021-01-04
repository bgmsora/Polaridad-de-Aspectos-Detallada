# -*- coding: utf-8 -*-
"""
Created on Fri Jun  5 18:21:07 2020

@author: Brandon
"""
import nltk 
from operator import itemgetter

#Leer directorios
from os import listdir
from os.path import isfile, isdir
def ls1(path):
    return [obj for obj in listdir(path) if isfile(path + obj)]

#Funciones para el calculo de los ngramas
def flatten_corpus(corpus):
    return ' '.join([document.strip()
                     for document in corpus])
def compute_ngrams(sequence, n):
    return zip(*[sequence[index:]
                 for index in range(n)])
def get_top_ngrams(corpus, ngram_val=1, limit=5):
    corpus = flatten_corpus(corpus)
    tokens = nltk.word_tokenize(corpus)
    ngrams = compute_ngrams(tokens, ngram_val)
    ngrams_freq_dist = nltk.FreqDist(ngrams)
    sorted_ngrams_fd = sorted(ngrams_freq_dist.items(),
                              key=itemgetter(1), reverse=True)
    sorted_ngrams = sorted_ngrams_fd[0:limit]
    sorted_ngrams = [(' '.join(text), freq)
                     for text, freq in sorted_ngrams]
    return sorted_ngrams

def quitarCaracter(cadena,letra):
	return cadena.replace(letra," ")

if __name__ == "__main__":
    #Leemos todos lo sarchivos que tiene la carpeta
    criticas=list()
    files=ls1("/Users/USUARIO/Desktop/Lenguaje/Programas/Polaridad/hoteles/")
    rows=list()
    for file in files:
        #print(file)
        di='./hoteles/'+file
        #print(di)
        f=open(di)
        text=f.read().lower()
        f.close()
        Trows=list()
        row=' '
        for word in text:
            row=row+word
            if word == '\n':
                Trows.append(row)
                row=''
        rows.append(Trows)
    
    f=open("stopwords.txt",encoding='utf-8')
    text=f.read()
    texto=nltk.word_tokenize(text)
    new=list()
    for row1 in rows:
        for row in row1:
            aux=row
            #print('renglon sin quitar: ',aux)
            for w in texto:
                aux=quitarCaracter(aux,' '+w+' ' )
                aux=quitarCaracter(aux,',')
                aux=quitarCaracter(aux,'!')
                aux=quitarCaracter(aux,'.')
                aux=quitarCaracter(aux,'?')
                aux=quitarCaracter(aux,')')
                aux=quitarCaracter(aux,'(')
                aux=quitarCaracter(aux,':')
                aux=quitarCaracter(aux,'``')
                aux=quitarCaracter(aux,"''")
                aux=quitarCaracter(aux,"<")
                aux=quitarCaracter(aux,">")
                aux=quitarCaracter(aux,"/li")
                for i in range(0,10):
                    aux=quitarCaracter(aux,str(i))
                #print(aux)
            #print('renglon con quitar: ',aux)
            new.append(aux)
    #Para hacer el uno grama
    '''
    w=get_top_ngrams(corpus=new, ngram_val=1,limit=100)
    print(w)
    f=open('Unograma.txt','w')
    ngrama=list()
    prueba=' '
    for palabra in w:
        prueba=prueba+palabra[0]+' '
        ngrama.append(palabra[0])
    print(prueba)
    prueba=nltk.word_tokenize(prueba)
    print(nltk.pos_tag(prueba))
    prueba=nltk.pos_tag(prueba)
    for w in prueba:
        #print(w[1])
        if w[1]=='NN' or w[1]=='NNS':
            f.write(str(w[0])+'\n')
    f.close()
    '''
    #Para el dosgrama
    '''
    w=get_top_ngrams(corpus=new, ngram_val=2,limit=100)
    print(w)
    f=open('Dosgrama.txt','w')
    for z in w:
        f.write(str(z)+'\n')
    f.close()
    '''
    #para sacar el trigrama
    w=get_top_ngrams(corpus=new, ngram_val=3,limit=100)
    print(w)
    f=open('Trigrama.txt','w')
    for z in w:
        f.write(str(z)+'\n')
    f.close()