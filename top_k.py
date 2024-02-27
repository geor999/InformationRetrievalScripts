import pandas as pd
import csv
import math
from operator import itemgetter

def readfile(filename):
    df = pd.read_csv(filename, usecols = ['membername','sittingdate','parliamentaryperiod','parliamentarysession','parliamentarysitting','politicalparty','government','memberregion','roles','membergender','speech'])
    unique_politicalparties=unique(df['politicalparty'].values.astype('U'))
    unique_members=unique(df['membername'].values.astype('U'))
    return df,unique_politicalparties,unique_members


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
        print(i)
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


def createdictspeeches(df):
    dictionary={}
    
    t=0
    for j, rows in df.iterrows():
        string=""
        content = df.at[j, 'speech']
        if(df.at[j, 'membername']==""):
            continue
        else:
            string=(string+content+" ")
        dictionary[t]=string
        t=t+1

    return dictionary,t

#'vouleftes2.csv' or 'parties.csv' for file
def writecsv(unique_members,dictionary,t,file):
    if(file=='vouleftes.csv'):
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

# Function that calculates and prints the top-k for each political party or member
def topk(k,dictionary,list):
    # for array length
    for i in range(len(dictionary)):
        #find top-k 
        res = dict(sorted(dictionary.get(i).items(), key = itemgetter(1), reverse = True)[:k])
        #create a string with the name of political party or member and top-k
        string=list[i]+" "+str(res)
        #because it might have less that k words the one we search in we check 
        #print the string
        print(string)

#Function that calculates and prints the top-k for each speech
def topk_speeches(k,dictionary):
    # for speeches length
    for i in range(len(dictionary)):
        #find top-k 
        
        res = dict(sorted(dictionary.get(i).items(), key = itemgetter(1), reverse = True)[:k])
        #create a string with the name of political party or member and top-k
        string=str(i)+" "+str(res)
        #because it might have less that k words the one we search in we check 
        #print the string
        print(string)



#q=0 political parties q=1 members q=2 speeches
q=0
#create the unique member or political party arrays
#change the name of the file here if needed
df,unique_politicalparties,unique_members=readfile('stemmed_mini.csv')
if(q==0):
    #create the dictionary
    politicalparties_dict,t=createdict(df,unique_politicalparties,'politicalparty')
    #write the dictionary to a file
    writecsv(unique_politicalparties,politicalparties_dict,t,'parties.csv')
    #read from the file we wrote at the speeches
    data = pd.read_csv('parties.csv')
    #TF-IDF
    globalDict, documentsTF = TF_Process(data)
    dictionaryIDF = IDF_Process(globalDict, data.shape[0])
    #create array with a vertex for each political party
    tf_idf_dictionary=arraycr(t,globalDict, documentsTF,dictionaryIDF)
    print(tf_idf_dictionary)
    #search for the top-k(default 5) for each political party
    topk(5,tf_idf_dictionary,unique_politicalparties)
elif(q==1):
    #create the dictionary
    members_dict,t=createdict(df,unique_members,'membername')
    #write the dictionary to a file
    writecsv(unique_members,members_dict,t,'vouleftes.csv')
    #read from the file we wrote at the speeches
    data = pd.read_csv("vouleftes.csv")
    #TF-IDF
    globalDict, documentsTF = TF_Process(data)
    dictionaryIDF = IDF_Process(globalDict, data.shape[0])
    #create array with a vertex for each member
    tf_idf_dictionary=arraycr(t,globalDict, documentsTF,dictionaryIDF)
    #search for the top-k(default 5) for each member
    topk(5,tf_idf_dictionary,unique_members)
elif(q==2):
    #TF-IDF
    dictionary,t=createdictspeeches(df)
    globalDict, documentsTF = TF_Process(df)
    dictionaryIDF = IDF_Process(globalDict, df.shape[0])
    #create array with a vertex for speech
    tf_idf_dictionary=arraycr(t,globalDict, documentsTF,dictionaryIDF)
    #search for the top-k(default 5) for each speech
    topk_speeches(5,tf_idf_dictionary) 
