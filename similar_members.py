import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import csv
import math
from numpy.linalg import norm

def readfile(filename):
    df = pd.read_csv(filename, usecols = ['membername','sittingdate','parliamentaryperiod','parliamentarysession','parliamentarysitting','politicalparty','government','memberregion','roles','membergender','speech'])
    unique_members=unique(df['membername'].values.astype('U'))
    return df,unique_members


def unique(list1):
  
    # initialize a null list
    unique_list=[]
    # traverse for all elements
    for x in list1:
        # check if exists in unique_list or not
        if x=="nan":
            continue
        elif x not in unique_list:
            unique_list.append(x)
    return unique_list
#'politicalparty' or 'membername' for type
def createdict(df,unique,type):
    dictionary={}
    t=0
    for i in unique:
        q=0
        string=""
        for j, rows in df.iterrows():
            content = df.at[j, 'speech']
            if(df.at[j, type]==""):
                continue
            if i==df.at[j,type]:
                string=(string+content+" ")
            q=q+1
        dictionary[unique[t]]=string
        t=t+1
    return dictionary,t

#'vouleftes2.csv' or 'parties.csv' for file
def writecsv(unique_members,dictionary,t,file):
    if(file=='vouleftes2.csv'):
        header=['membername','speech']
    else:
        header=['politicalparty','speech']
    with open(file, 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(header)

        # write the data
        for i in range(0,t):
            data=[unique_members[i],dictionary.get(unique_members[i])]
            writer.writerow(data)

def termFrequency(term, all_words, sum_of_words):
    return all_words.count(term) / float(sum_of_words)

# Function that calculates term frequency for every word in all docs
def TF_Process(data):
    
    # Dictionary where key = term and value = document ids where the word appears
    globalDict = {}

    # List that stores dictionaries
    documentsTF = []

    for i, rows in data.iterrows():
        content = data.at[i, 'speech']
        all_words = content.split()

        sum_of_words = len(all_words)

        # Dictionary where key = term and value = TF in the document
        TF={}
        # Updating global dictionary 
        for term in all_words:
            if not term in globalDict:
                globalDict[term] = [i]
            elif not term in TF:
                doc_list = globalDict.get(term)
                doc_list.append(i)
                globalDict[term] = doc_list
        
            TF[term] = termFrequency(term, all_words, sum_of_words)
        
        documentsTF.append(TF)
    
    return globalDict, documentsTF

# Function that calculates IDF for every term
def IDF_Process(globalDict, total_docs):
    dictionaryIDF = globalDict.copy()
    for i in dictionaryIDF.keys():
        dictionaryIDF[i] = 1 + math.log(float(total_docs/len(dictionaryIDF[i])))
    
    return dictionaryIDF

# Function that creates a 2d array which contains a vertex for each (political party,member,speech)
def arraycr(listlen,globalDict, documentsTF,dictionaryIDF):
    tf_idf_dictionary={}
    for t in range(0,listlen):
        q=0
        for line in globalDict:
            #if word is in the document
            if (line in documentsTF[t]):
                #put tf*idf as value else 0
                tf_idf_dictionary.setdefault(t, {})[line]=dictionaryIDF.get(line)*documentsTF[t].get(line)
            q=q+1  
    #return array
    return tf_idf_dictionary 


def cosinearraycalc(array,globalDict):
    cosine_dictionary={}
    dummy=np.empty(len(globalDict),float)
    dummy2=np.empty(len(globalDict),float)
    for i in range(len(array)):
        for k in array: 
            if(i<k):
                t=0
                for word in globalDict:
                    if array.get(k).get(word)!=None:
                        dummy2[t]=array.get(k).get(word)
                    else:
                        dummy2[t]=0
                    if array.get(i).get(word)!=None:
                        dummy[t]=array.get(i).get(word)
                    else:
                        dummy[t]=0
                    t=t+1
                cosine_dictionary.setdefault(i, {})[k]=float(f'{cosine(dummy,dummy2):.4f}')
                        
    return cosine_dictionary

def cosine(query1,query2):
    return np.dot(query1,query2)/(norm(query1)*norm(query2))


#read from the file
df,unique_members=readfile('stemmed_mini.csv')
#create dictionary with unique members and their speeches
members_dict,t=createdict(df,unique_members,'membername')
#write the dictionary to a file
writecsv(unique_members,members_dict,t,'vouleftes.csv')
#read from the file we wrote at the speeches
data = pd.read_csv("vouleftes.csv")
#TF-IDF
globalDict, documentsTF = TF_Process(data)
dictionaryIDF = IDF_Process(globalDict, data.shape[0])
#create array with vertex for each member
tf_idf_dictionary=arraycr(t,globalDict, documentsTF,dictionaryIDF)
cosinearray=cosinearraycalc(tf_idf_dictionary,globalDict)
for a in cosinearray:
    print(a)
    print(cosinearray.get(a)) 