import matplotlib.pyplot as plt
import pandas as pd
from gensim import corpora
from gensim.models import LsiModel
from gensim.matutils import corpus2dense
from gensim.models.coherencemodel import CoherenceModel
import matplotlib.pyplot as plt

def load_data():
    """
    Input  : path and file_name
    Purpose: loading text file
    Output : list of paragraphs/documents and
             title(initial 100 words considred as title of document)
    """
    documents_list = []
    titles=[]
    df=pd.read_csv("stemmed_mini.csv")
    for j, rows in df.iterrows():
        text = df.at[j, 'speech']
        documents_list.append(text)
    print("Total Number of Documents:",len(documents_list))
    titles.append( text[0:min(len(text),100)] )
    return documents_list,titles


def prepare_corpus(doc_clean):
    """
    Input  : clean document
    Purpose: create term dictionary of our courpus and Converting list of documents (corpus) into Document Term Matrix
    Output : term dictionary and Document Term Matrix
    """
    # Creating the term dictionary of our courpus, where every unique term is assigned an index. dictionary = corpora.Dictionary(doc_clean)
    dictionary = corpora.Dictionary(doc_clean)
    # Converting list of documents (corpus) into Document Term Matrix using dictionary prepared above.
    doc_term_matrix = [dictionary.doc2bow(doc) for doc in doc_clean]
    # generate LDA model
    return dictionary,doc_term_matrix

def preprocess_data(doc_set):
    
    texts = []
    # loop through document list
    for i in doc_set:
        content=i.split()
        texts.append(content)
    return texts

def create_gensim_lsa_model(doc_clean,number_of_topics,words):
    """
    Input  : clean document, number of topics and number of words associated with each topic
    Purpose: create LSA model using gensim
    Output : return LSA model
    """
    dictionary,doc_term_matrix=prepare_corpus(doc_clean)
    # generate LSA model
    lsamodel = LsiModel(doc_term_matrix, num_topics=number_of_topics, id2word = dictionary,chunksize=1000)  # train model
    print(lsamodel.print_topics(num_topics=number_of_topics, num_words=words))
    # Transform your documents into LSI vectors
    lsi_vectors = lsamodel[doc_term_matrix]

# Convert LSI vectors to a dense matrix
    lsi_matrix = corpus2dense(lsi_vectors, num_terms=number_of_topics).T

# Now lsi_matrix contains the documents as n-dimensional vectors based on LSI topics
    print(lsi_matrix)
    return lsamodel

def compute_coherence_values(dictionary, doc_term_matrix, doc_clean, stop, start=2, step=3):
    """
    Input   : dictionary : Gensim dictionary
              corpus : Gensim corpus
              texts : List of input texts
              stop : Max num of topics
    purpose : Compute c_v coherence for various number of topics
    Output  : model_list : List of LSA topic models
              coherence_values : Coherence values corresponding to the LDA model with respective number of topics
    """
    coherence_values = []
    model_list = []
    for num_topics in range(start, stop, step):
        # generate LSA model
        print(num_topics)
        model = LsiModel(doc_term_matrix, num_topics, id2word = dictionary)  # train model
        model_list.append(model)
        coherencemodel = CoherenceModel(model=model, texts=doc_clean, dictionary=dictionary, coherence='c_v')
        coherence_values.append(coherencemodel.get_coherence())
    return model_list, coherence_values

def plot_graph(doc_clean,start, stop, step):
    dictionary,doc_term_matrix=prepare_corpus(doc_clean)
    model_list, coherence_values = compute_coherence_values(dictionary, doc_term_matrix,doc_clean,
                                                            stop, start, step)
    # Show graph
    x = range(start, stop, step)
    plt.plot(x, coherence_values)
    plt.xlabel("Number of Topics")
    plt.ylabel("Coherence score")
    plt.legend(("coherence_values"), loc='best')
    plt.show()

#q=0 find number of ideal topics based on coherence 
#q=1 find those topics. need to change number_of_topics to the result of q=0
q=1
if __name__ == '__main__':
    if q==0:
        documents_list,titles=load_data()
        texts=preprocess_data(documents_list)
        #start is the starting index of topics and stop is the finishing index of topics
        #it will iterate (stop-start)/step times
        start,stop,step=1,20,1
        plot_graph(texts,start,stop,step)
    else:
        number_of_topics=7
        words=5
        documents_list,titles=load_data()
        texts=preprocess_data(documents_list)
        model=create_gensim_lsa_model(texts,number_of_topics,words)
