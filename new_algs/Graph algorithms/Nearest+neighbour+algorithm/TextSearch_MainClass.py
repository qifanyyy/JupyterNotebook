from sklearn.feature_extraction.text import CountVectorizer, TfidfTransformer, TfidfVectorizer
import pandas as pd
from sklearn.neighbors import NearestNeighbors
import gzip
import _pickle as cPickle
from abc import ABCMeta, abstractmethod
import collections

class umbrella(object):
    '''
    Main class to be inherited
    '''
    __metaclass__ = ABCMeta
    
    def __init__(self,dbase_path):
        self.dbpath = dbase_path   # The path to where data is stored
    
    #Method to read pickled data
    def read_pickle(self,filename) :
        lfn = filename
        if lfn.endswith('gz') :
            # Unzip, open, read
            f = gzip.open(self.dbpath+lfn, 'rb')
            inp_fl=cPickle.load(f)
            f.close()
            
        return inp_fl

    # Method to write pickled data
    def write_pickle(self,filename,data) :
        with gzip.open(self.dbpath+filename+'.gz','wb') as out_tfdif:
            cPickle.dump(data,out_tfdif)
    
    # Method to read text file
    def read_text(self,filename) :
        fl1 = open(self.dbpath+filename, 'r') 
        txt_data=fl1.read()
        return txt_data
    
    # Method to read Pandas Dataframe
    def read_df(self,filename) :
        df = pd.read_pickle(self.dbpath+filename)
        return df
    
    # Method to add to existing Pandas Dataframe
    def add_textTOdf(self,df,textlist):
        idx=-len(textlist)
        list_idx=0
        self.df=df
        for i in range(idx,0):
            self.df.loc[idx] =textlist[list_idx]
            self.df.index = self.df.index + 2  # shifting index
            self.df = self.df.sort_index()  # sorting by index
            
            list_idx+=1
            
        return self.df
    
    # Show the common n-grams of the target text
    def show_common_ngrams(self,tfidf_matrix,features,ref_idx,num):
        
        self.ref_idx=ref_idx
        
        print ('Common',num,'n-grams:')
        self.target_ngrams=tfidf_matrix.getrow(self.ref_idx).toarray().flatten()
        self.d = pd.Series(self.target_ngrams, index = features).sort_values(ascending=False)
        print (self.d[0:num])
                
        return None
    
    # Method to print the results and write to file
    def print_results(self,fin_list,df,analysis_column,print_columns,ref_idx,kywd,file_prefix,n_gram_type,dbase_path,save):
            
        tot=0;kywd_count=0
        flname=dbase_path+'Results/'+file_prefix+'_'+df['Name'].iloc[ref_idx]+'_'+n_gram_type+'.txt'
        
        with open(flname,"w") as savefile:
            savefile.write('#############################################\n')
            savefile.write('RESULTS FOR {0} \n' .format(file_prefix))
            savefile.write('N-gram Analysis Type = {0} \n' .format(n_gram_type))
            savefile.write('Target Text = {0} \n' .format(df['Name'].iloc[ref_idx]))
            savefile.write('#############################################\n')
            savefile.write('\n')
            
            for l in fin_list:
                if kywd!=None:
                    if kywd in df[analysis_column].iloc[l[0]]:
                        a='YES'
                        kywd_count+=1     
                    else: a='NO'
                else:
                    a='NA'
                    kywd_count='NA'

                savefile.write('----------------------({0},{1},{2})----------------------' .format(tot,a,round(l[1],2)))
                savefile.write('\n')
                for column in print_columns:
                    savefile.write(df[column].iloc[l[0]])
                    savefile.write('\n')

                tot+=1
            
            savefile.write('#############################################\n')
            savefile.write('Keyword Count = {0}/{1}' .format(kywd_count,tot))
            savefile.close()
            
        return None
        

class textSIM(umbrella):
    '''
    Class containing text similarity analysis methods
    '''
    
    # Vectorize text using Tfidf Vectorizer
    def vectorize(self,data,ngr_range):
        
        self.tfidf_vectorizer = TfidfVectorizer(ngram_range=ngr_range)
        print ('All Text Vectorized')
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(data)
        print ('TF-DIF Calculated')
        self.features=self.tfidf_vectorizer.get_feature_names()
        return self.tfidf_vectorizer, self.tfidf_matrix, self.features
    
    # Vectorize text using Tfidf Vectorizer
    def vectorize_sw(self,data,ngr_range):
        
        self.tfidf_vectorizer = TfidfVectorizer(ngram_range=ngr_range,stop_words='english')
        print ('All Text Vectorized')
        self.tfidf_matrix = self.tfidf_vectorizer.fit_transform(data)
        print ('TF-DIF Calculated')
        self.features=self.tfidf_vectorizer.get_feature_names()
        return self.tfidf_vectorizer, self.tfidf_matrix, self.features
    
    # Find similar text using the k-nearest neighbors algorithm
    def get_kneighbors(self,k,metric,tfidf_matrix,ref_idx):
        
        self.ref_idx=ref_idx
        
        self.nbrs = NearestNeighbors(n_neighbors=k,
                        radius=1.0,
                        algorithm='auto',
                        leaf_size=30,
                        metric=metric,
                        p=2,
                        n_jobs=1).fit(tfidf_matrix)
        self.distances, self.indices = self.nbrs.kneighbors(tfidf_matrix.getrow(self.ref_idx))
        
        return self.distances, self.indices
    

    # MERGER method for different set of results using different n-gram combinations
    def results_merger(self,ind_list,coeffs):
        
        tot_list=[];seq_list=[]
        
        #First form separate lists for the paper indices and their sequence number in each appearance (and the coeffs)
        for j in range(len(ind_list)):
            for i in range(len(ind_list[j])):    
                tot_list.append(ind_list[j][i])
                seq_list.append((i+1,coeffs[j]))
        
        counter=collections.Counter(tot_list) # Count how many times each paper occured across different n-gram analyses
        
        #Create the dataframe to make calculations on
        df_list=[]
        for i in range(len(tot_list)):
            df_list.append((tot_list[i],counter[tot_list[i]],seq_list[i][0],seq_list[i][1]))
        df_ind = pd.DataFrame(df_list)
        
        # Calculations and queueing
        max_app=df_ind[1].max()    
        res_list=[]
        
        #Start with the texts that appear in most of the searches [Redundant]
        for j in range(max_app,0,-1):
            inds=df_ind[df_ind[1]==j][0].drop_duplicates().tolist()
            for ind in inds:
                seqs=df_ind[df_ind[0]==ind][2].tolist() #sequence numbers
                cfs=df_ind[df_ind[0]==ind][3].tolist() #coeffs
                c_seqs=[a*b for a,b in zip(seqs,cfs)] # Multiplying each paper sequence with n-gram coeff
                #print (ind,seqs,sum(c_seqs)/j) #LATER IMPROVE TO OUTPUT results for each NGRAM
                res_list.append((ind,sum(c_seqs)/j)) #Creating the list with the weighted paper appearance
      
        self.fin_list = sorted(res_list, key=lambda tup: tup[1]) #Sorting the list for final similarity results
                
        return self.fin_list
    
    # SIMPLE MERGER method for different set of results using different n-grams 
    def results_merger_simp(self,data_list):
        
        tot_list=[];seq_list=[]
        for l in ind_list:
            for i in range(len(l)):    
                tot_list.append(l[i])
                seq_list.append(i+1)
        
        counter=collections.Counter(tot_list)
        
        df_list=[]
        for i in range(len(tot_list)):
            df_list.append((tot_list[i],counter[tot_list[i]],seq_list[i]))
        
        df_ind = pd.DataFrame(df_list)
        max_app=df_ind[1].max()    
        
        res_list=[]
        #Start with the texts that appear in most of the searches
        for j in range(max_app,0,-1):
            inds=df_ind[df_ind[1]==j][0].drop_duplicates().tolist()
            for ind in inds:
                seqs=df_ind[df_ind[0]==ind][2].tolist()
                print (ind,seqs,sum(seqs)/j)
                res_list.append((ind,sum(seqs)/j))
      
        self.fin_list = sorted(res_list, key=lambda tup: tup[1])
                
        return self.fin_list
    
    # Method to manipulate the tfdief coefficient of a specific feature (keyword) 
    def scale_feature(self,tfidf_matrix,features,kywd,target_idx,coeff):
        self.tfidf=tfidf_matrix
        try:
            maxval=self.tfidf[target_idx].max()
            print (maxval)
            kywd_idx=features.index(kywd)
            #self.tfidf[0,kywd_idx]=self.tfidf[0,kywd_idx]*coeff
            self.tfidf[target_idx,kywd_idx]=maxval*1.5
        except:
            print (kywd, 'not found!')
            
        return self.tfidf
        
    
if __name__ == '__main__':
    
    # Start with creating a Text Similarity Instance
    dbase_path='/Users/syor0001/Documents/Scrape/Text_scikit/TextSimilarity/dbase/AMS/'
    ts=textSIM(dbase_path)
    
    #################
    # DATABASE WORK #
    #################
    df=ts.read_df('JOURNAL_df')
    print ('Raw Dataframe Size=',df.index.size)
    
