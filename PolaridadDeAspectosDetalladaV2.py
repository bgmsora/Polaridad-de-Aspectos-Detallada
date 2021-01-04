# -*- coding: utf-8 -*-
"""
Created on Fri Jun 12 21:18:47 2020

@author: Brandon
"""
import nltk 
from tabulate import tabulate
from nltk.corpus import wordnet

#Leer directorios
from os import listdir
from os.path import isfile, isdir
def ls1(path):
    return [obj for obj in listdir(path) if isfile(path + obj)]

def ObtenerCriticas(files):
    criticas=list()
    for file in files:
        di='./hoteles/'+file
        f=open(di)
        text=critica(f)
        criticas.append(text)
        f.close()
    return criticas

def critica(f):
    text=f.read().lower()
    f.close()
    rows=list()
    row=' '
    for word in text:
        row=row+word
        if word == '\n':
            rows.append(row)
            row=''
    palabras=list()
    wnlm = nltk.WordNetLemmatizer()
    for row in rows:
        palabra=nltk.word_tokenize(row)
        doc=list()
        doc=list()
        for w in palabra:
            doc.append(wnlm.lemmatize(w))
        palabras.append(doc)
        try: 
            palabras.append(palabra)
        except Exception:
            pass
    return palabras

def ObtenerDiccionario():
    #contextoChido={}
    f=open('./Spanish_sentiment_lexicon/fullStrengthLexicon.txt',encoding='utf-8')
    dic=f.read()
    f.close()
    f=open('./Spanish_sentiment_lexicon/mediumStrengthLexicon.txt',encoding='utf-8')
    dic2=f.read()
    f.close()
    dic=dic+dic2
    #print(dic)
    rows=list()
    row=' '
    for word in dic:
        row=row+word
        if word == '\n':
            rows.append(row)
            row=''
    diccionario={}
    for row in rows:
        row=nltk.word_tokenize(row)
        try:
            diccionario[row[0]]=row[3]
        except Exception:
            diccionario[row[0]]=row[2]
            pass
    return diccionario

def PolaridadCriticas(criticas,diccionario,Aspectos):
    polCriticas=list()
    i=0
    for critica in criticas:
        y=0
        for row in critica:
            y+=1
            result=[0,0,0,0,0,0,0]
            pos=[0,0,0,0,0,0,0]
            neg=[0,0,0,0,0,0,0]
            no=0
            for aspecto in Aspectos:
                if aspecto in row:
                    #print(aspecto, 'esta en ', no)
                    for w in row:
                        try:
                            if diccionario[w]=='pos':
                                pos[no]=pos[no]+1
                            else:
                                neg[no]=neg[no]+1
                        except Exception:
                            pass
                    #print('suma vale ',suma[no],' en ',no, 'entre cuantos ',cuantosList[no])
                no+=1
            zz=0
            for aspecto in Aspectos:
                if pos[zz] > neg[zz]:
                    result[zz]='pos'
                if pos[zz] < neg[zz]:
                    result[zz]='neg'
                if pos[zz] == neg[zz]:
                    result[zz]='neutral'
                zz+=1
            polCriticas.append(result)
        i+=1
    return polCriticas

def PolaridadCriticasPalabras(criticas,diccionario,Aspectos):
    palabrasPos=[list(),list(),list(),list(),list(),list(),list()]
    palabrasNeg=[list(),list(),list(),list(),list(),list(),list()]
    for critica in criticas:
        for row in critica:
            no=0
            for aspecto in Aspectos:
                if aspecto in row:
                    #print(aspecto, 'esta en ', no)
                    for w in row:
                        try:
                            if diccionario[w]=='pos':
                                palabrasPos[no].append(w)
                            else:
                                palabrasNeg[no].append(w)
                        except Exception:
                            pass
                    #print('suma vale ',suma[no],' en ',no, 'entre cuantos ',cuantosList[no])
                no+=1
    #Partes positiva
    #Obtenemos el vocabulario de cada una
    vocabularioPos=[list(),list(),list(),list(),list(),list(),list()]
    for i in range(len(palabrasPos)):
        vocabularioPos[i]=palabrasPos[i]
        vocabularioPos[i]=set(vocabularioPos[i])
    value=[list(),list(),list(),list(),list(),list(),list()]
    #obtener la frecuencia
    for i in range(len(palabrasPos)):
        for abc in vocabularioPos[i]:
            value[i].append(palabrasPos[i].count(abc))
    #suma de totales
    totales=[0,0,0,0,0,0,0]
    for i in range(len(palabrasPos)):
        j=0
        for abc in vocabularioPos[i]:
            totales[i]+=value[i][j]
            j+=1
    
    #Parte de los negativos
    vocabularioNeg=[list(),list(),list(),list(),list(),list(),list()]
    for i in range(len(palabrasNeg)):
        vocabularioNeg[i]=palabrasNeg[i]
        vocabularioNeg[i]=set(vocabularioNeg[i])
    value2=[list(),list(),list(),list(),list(),list(),list()]
    #obtener la frecuencia
    for i in range(len(palabrasNeg)):
        for abc in vocabularioNeg[i]:
            value2[i].append(palabrasNeg[i].count(abc))
    #suma de totales
    totales2=[0,0,0,0,0,0,0]
    for i in range(len(palabrasNeg)):
        j=0
        for abc in vocabularioNeg[i]:
            totales2[i]+=value2[i][j]
            j+=1
    #Sumo los 2 totales para contar todas las opiniones---------------------
    for i in range(len(totales)):
        totales[i]= totales[i]+ totales2[i]
    
    #De nuevo lo positivo
    #calculo de probabiliad
    for i in range(len(palabrasPos)):
        j=0
        for abc in vocabularioPos[i]:
            #print('\t',abc,' ---> ',value[i][j])
            value[i][j]=value[i][j]/totales[i]
            j+=1
    #obtenemos los mas altos
    c = list(zip(vocabularioPos, value))
    z=[list(),list(),list(),list(),list(),list(),list()]
    i=0
    for dat in c:
        #0 estan las palabras y en 1 los datos
        palabras=tuple(dat[0])
        datos=tuple(dat[1])
        y = list(zip(palabras, datos))
        z[i]=sorted(y, key=lambda tup: tup[1], reverse=True)
        i+=1
    
    #De nuevo los negativos
    #calculo de probabiliad
    for i in range(len(palabrasNeg)):
        j=0
        for abc in vocabularioNeg[i]:
            #print('\t',abc,' ---> ',value[i][j])
            value2[i][j]=value2[i][j]/totales[i]
            j+=1
    #obtenemos los mas altos
    c2 = list(zip(vocabularioNeg, value2))
    zz=[list(),list(),list(),list(),list(),list(),list()]
    i=0
    for dat in c2:
        #0 estan las palabras y en 1 los datos
        palabras=tuple(dat[0])
        datos=tuple(dat[1])
        y = list(zip(palabras, datos))
        zz[i]=sorted(y, key=lambda tup: tup[1], reverse=True)
        i+=1
    return z,zz

def ConstruirTabla(polCriticas,Aspectos):
    pos=[0,0,0,0,0,0,0]
    neg=[0,0,0,0,0,0,0]
    result=[0,0,0,0,0,0,0]
    for oracion in polCriticas:
        for i in range(len(Aspectos)):
            if oracion[i]!='neutral':
                if oracion[i]=='pos':
                    pos[i]=pos[i]+1
                else:
                    neg[i]=neg[i]+1
    
    for i in range(len(Aspectos)):
        if pos[i] > neg[i]:
            result[i]='pos'
        if pos[i] < neg[i]:
            result[i]='neg'
        if pos[i] == neg[i]:
            result[i]='neutral'
    return result

if __name__ == "__main__":
    Aspectos=['habitación','recepción','precio','baño','servicio','hotel','desayuno']
    files=ls1("/Users/USUARIO/Desktop/Lenguaje/Programas/Polaridad detallada/hoteles/")
    diccionario=ObtenerDiccionario()
    #partir yes y no
    filesNo=list()
    filesYes=list()
    for fil in files:
        w=fil.split('_')
        if w[0]=='no':
            filesNo.append(fil)
        else:
            filesYes.append(fil)
    
    #Polaridad No
    criticasNo=ObtenerCriticas(filesNo)
    polCriticas=PolaridadCriticas(criticasNo,diccionario,Aspectos)
    polaridadNo=ConstruirTabla(polCriticas,Aspectos)
    
    #Polaridad Yes
    criticasYes=ObtenerCriticas(filesYes)
    polCriticas=PolaridadCriticas(criticasYes,diccionario,Aspectos)
    polaridadYes=ConstruirTabla(polCriticas,Aspectos)
    
    #5 palabras de polaridad positiva y negativa en yes
    ListaYesPositiva,ListaYesNegativa=PolaridadCriticasPalabras(criticasYes,diccionario,Aspectos)
    
    #5 palabras de polaridad positiva y negativa en no
    ListaNoPositiva,ListaNoNegativa=PolaridadCriticasPalabras(criticasNo,diccionario,Aspectos)
    
    #Impresion de los datos finales
    resultado=list()
    titulos=['Aspectos','Polaridad en "NO"','Polaridad en "YES"','Palabras Pos de "YES"','Palabras Neg de "YES"','Palabras Pos de "NO"','Palabras Neg de "NO"']
    resultado.append(titulos)
    for i in range(len(Aspectos)):
        TextoPos=' '
        z=0
        for w in ListaYesPositiva[i]:
            TextoPos=TextoPos+str(w)+' \n'
            if z>=5:
                break
            z+=1
        TextoNeg=' '
        z=0
        for w in ListaYesNegativa[i]:
            TextoNeg=TextoNeg+str(w)+' \n'
            if z>=5:
                break
            z+=1
        #negativos
        TextPos=' '
        z=0
        for w in ListaNoPositiva[i]:
            TextPos=TextPos+str(w)+' \n'
            if z>=5:
                break
            z+=1
        TextNeg=' '
        z=0
        for w in ListaNoNegativa[i]:
            TextNeg=TextNeg+str(w)+' \n'
            if z>=5:
                break
            z+=1
        x=[Aspectos[i],polaridadNo[i],polaridadYes[i],TextoPos,TextoNeg,TextPos,TextNeg]
        resultado.append(x)
    print(tabulate(resultado,headers='firstrow',tablefmt='fancy_grid'))