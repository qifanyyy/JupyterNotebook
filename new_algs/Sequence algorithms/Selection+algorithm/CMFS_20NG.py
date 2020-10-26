
# coding: utf-8

# # Implementation of CMFS, iCMFS on 20NG

# In[1]:

"""
Authors: Abhirav Gholba
         Bhargav Srinivasa
         Devashish Deshpande
         Gauri Kholkar
         Mrunmayee Nasery
"""
from sklearn.datasets import fetch_20newsgroups
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.feature_selection import SelectKBest, chi2
from sklearn.naive_bayes import MultinomialNB
from sklearn import metrics
import matplotlib.pyplot as plt
import numpy as np
import operator
import math
get_ipython().magic(u'matplotlib inline')


# In[2]:

newsgroups_train = fetch_20newsgroups(subset='train', remove=('headers', 'footers', 'quotes'))
vec = CountVectorizer(stop_words='english')
document_term_mat = vec.fit_transform(newsgroups_train.data)
term_document_mat = document_term_mat.T
documents = len(newsgroups_train.filenames)
categories = len(newsgroups_train.target_names)
terms = term_document_mat.shape[0]


# In[3]:

print "No. of documents: %d\nNo. of categories: %d" % (documents, categories)
print "matrix.shape: {0}".format(term_document_mat.shape)
print newsgroups_train.target[10]
print type(term_document_mat)


# ### Create Term-category feature-appearance matrix

# In[4]:

term_category_mat = np.zeros((terms, categories))
for doc in range(documents):
    cat = newsgroups_train.target[doc]
    for row in term_document_mat.getcol(doc).nonzero()[0]:
        term_category_mat[row][cat] += 1


# In[5]:

print "Term-category matrix shape: {0} \n".format(term_category_mat.shape)


# ### Perform CMFS, iCMFS and CC term-category matrix
# 
# \begin{equation}
# iCMFS(T_k, C_i) = P(T_k|C_i) * P(C_i, T_k) / P(C_i)
# \end{equation}

# In[6]:

cc_term_category_mat = np.copy(term_category_mat)
icmfs_term_category_mat = np.copy(term_category_mat)
cmfs_term_category_mat = np.copy(term_category_mat)


# In[7]:

term_freq = np.sum(term_category_mat)
term_freq_per_cat = np.cumsum(term_category_mat, axis=0)[-1, :]

for term in range(terms):
    # Frequency of the term across all categories
    # ICMFS(tk,ci) = (P(tk|ci)*P(ci|tk))/P(ci)
    total_term_freq = sum(term_category_mat[term, :])
    for cat in range(categories):
        p_ci = float((term_freq_per_cat[cat] / term_freq))
        p_tk = float((total_term_freq / term_freq))
        p_ci_tk = float(term_category_mat[term][cat] + 1) / (total_term_freq + categories)
        p_tk_ci = float(term_category_mat[term][cat] + 1) / (term_freq_per_cat[cat] + terms)
        p_ntk_nci = float(term_freq - total_term_freq - term_freq_per_cat[cat] + term_category_mat[term][cat] + 1) / (term_freq - term_freq_per_cat[cat] + terms)
        p_tk_nci = float(total_term_freq - term_category_mat[term][cat] - 1) / (term_freq - term_freq_per_cat[cat] + terms)
        p_ntk_ci = float(term_freq_per_cat[cat] - term_category_mat[term][cat] - 1) / (term_freq_per_cat[cat] + terms)
        
        cc_term_category_mat[term][cat] = (math.sqrt(documents) * ((p_tk_ci * p_ntk_nci) - (p_tk_nci * p_ntk_ci))) / math.sqrt(p_tk * (1-p_tk) * p_ci * (1-p_ci))
        icmfs_term_category_mat[term][cat] = p_ci_tk * p_tk_ci / p_ci
        cmfs_term_category_mat[term][cat] = p_ci_tk * p_tk_ci
    
# Final CMFS matrix
print cc_term_category_mat
print icmfs_term_category_mat
print cmfs_term_category_mat


# ### Create term-cmfs dictionary

# In[8]:

# Create term id (i.e. row no) - iCMFS dict, CMFS dict
term_icmfs_dict = {}
icmfs_max = np.max(icmfs_term_category_mat, axis=1)
term_cmfs_dict = {}
cmfs_max = np.max(cmfs_term_category_mat, axis=1)
for i in range(terms):
    term_icmfs_dict[i] = icmfs_max[i]
    term_cmfs_dict[i] = cmfs_max[i]    


# ### Extract top 2000 features

# In[9]:

sorted_feature_list_cmfs = sorted(term_cmfs_dict.items(), key=operator.itemgetter(1), reverse=True)[:2000]
sorted_feature_list_icmfs = sorted(term_icmfs_dict.items(), key=operator.itemgetter(1), reverse=True)[:2000]
# to use for IGFSS
sorted_feature_list_icmfs_4000 = sorted(term_icmfs_dict.items(), key=operator.itemgetter(1), reverse=True)[:4000]
sorted_feature_list_cmfs_4000 = sorted(term_cmfs_dict.items(), key=operator.itemgetter(1), reverse=True)[:4000]


# ### Plug in IGFSS

# In[10]:

max_feature_column_cc = np.argmax(np.abs(cc_term_category_mat), axis = 1)
max_feature_sign_cc = np.empty_like(max_feature_column_cc)
for term in range(len(max_feature_column_cc)):
    max_val_col = max_feature_column_cc[term]
    max_feature_sign_cc[term] = np.sign(cc_term_category_mat[term][max_val_col])


# In[11]:

cat_positive_negative = np.zeros(shape=(categories, 2), dtype=int)
nfrs = 0.4

final_term_list_ICMFS = []
for term, icmfs in sorted_feature_list_icmfs_4000:
    sign = max_feature_sign_cc[term]
    cat = max_feature_column_cc[term]
    if (((float(cat_positive_negative[cat, 1]) / 100) < nfrs) and
        ((cat_positive_negative[cat, 0] + cat_positive_negative[cat, 1]) < 10)):
        if sign > 0:
            if (((float(cat_positive_negative[cat, 0]) / 10) < (1 - nfrs))):
                cat_positive_negative[cat, 0] += 1
                final_term_list_ICMFS.append(term)
        else:
            cat_positive_negative[cat, 1] += 1
            final_term_list_ICMFS.append(term)

cat_positive_negative = np.zeros(shape=(categories, 2), dtype=int)
final_term_list_CMFS = []
for term, icmfs in sorted_feature_list_cmfs_4000:
    sign = max_feature_sign_cc[term]
    cat = max_feature_column_cc[term]
    if (((float(cat_positive_negative[cat, 1]) / 100) < nfrs) and
        ((cat_positive_negative[cat, 0] + cat_positive_negative[cat, 1]) < 10)):
        if sign > 0:
            if (((float(cat_positive_negative[cat, 0]) / 10) < (1 - nfrs))):
                cat_positive_negative[cat, 0] += 1
                final_term_list_CMFS.append(term)
        else:
            cat_positive_negative[cat, 1] += 1
            final_term_list_CMFS.append(term)


# In[12]:

for term, icmfs in sorted_feature_list_icmfs:
    if term not in final_term_list_ICMFS and len(final_term_list_ICMFS) < 2000:
        final_term_list_ICMFS.append(term)
        
for term, cmfs in sorted_feature_list_cmfs:
    if term not in final_term_list_CMFS and len(final_term_list_CMFS) < 2000:
        final_term_list_CMFS.append(term)


# ### Naive bayes

# In[13]:

feature_list_cmfs = [term for term, _ in sorted_feature_list_cmfs]
# Create matrix for only the selected features. Note that the features are being extracted
# on the original document-term matrix. This will help in mapping with the targets easily.
selected_feature_matrix_cmfs = document_term_mat[:, feature_list_cmfs]
print selected_feature_matrix_cmfs.shape

feature_list_icmfs = [term for term, _ in sorted_feature_list_icmfs]
# Create matrix for only the selected features. Note that the features are being extracted
# on the original document-term matrix. This will help in mapping with the targets easily.
selected_feature_matrix_icmfs = document_term_mat[:, feature_list_icmfs]
print selected_feature_matrix_icmfs.shape

selected_feature_matrix_final_ICMFS = document_term_mat[:, final_term_list_ICMFS]
print selected_feature_matrix_final_ICMFS.shape

selected_feature_matrix_final_CMFS = document_term_mat[:, final_term_list_CMFS]
print selected_feature_matrix_final_CMFS.shape


# In[14]:

newsgroups_test = fetch_20newsgroups(subset='test', remove=('headers', 'footers', 'quotes'))
document_term_mat_test = vec.transform(newsgroups_test.data)
clf_cmfs = MultinomialNB().fit(selected_feature_matrix_cmfs, newsgroups_train.target)
clf_icmfs = MultinomialNB().fit(selected_feature_matrix_icmfs, newsgroups_train.target)
clf_final_ICMFS = MultinomialNB().fit(selected_feature_matrix_final_ICMFS, newsgroups_train.target)
clf_final_CMFS = MultinomialNB().fit(selected_feature_matrix_final_CMFS, newsgroups_train.target)


# ### Evaluate accuracy

# In[15]:

pred_cmfs = clf_cmfs.predict(document_term_mat_test[:, feature_list_cmfs])
print metrics.f1_score(newsgroups_test.target, pred_cmfs, average='micro')

pred_final_cmfs = clf_final_CMFS.predict(document_term_mat_test[:, final_term_list_CMFS])
print metrics.f1_score(newsgroups_test.target, pred_final_cmfs, average='micro')

pred_icmfs = clf_icmfs.predict(document_term_mat_test[:, feature_list_icmfs])
print metrics.f1_score(newsgroups_test.target, pred_icmfs, average='micro')

pred_final_icmfs = clf_final_ICMFS.predict(document_term_mat_test[:, final_term_list_ICMFS])
print metrics.f1_score(newsgroups_test.target, pred_final_icmfs, average='micro')



# In[16]:

icmfs_scores = []
for i in range(200, 2001, 200):
    feature_list_icmfs = [term for term, _ in sorted_feature_list_icmfs[:i]]
    selected_feature_matrix_icmfs = document_term_mat[:, feature_list_icmfs]
    clf_icmfs = MultinomialNB().fit(selected_feature_matrix_icmfs, newsgroups_train.target)
    pred_icmfs = clf_icmfs.predict(document_term_mat_test[:, feature_list_icmfs])
    f1_score_icmfs = metrics.f1_score(newsgroups_test.target, pred_icmfs, average='micro')
    icmfs_scores.append(f1_score_icmfs * 100)

cmfs_scores = []
for i in range(200, 2001, 200):
    feature_list_cmfs = [term for term, _ in sorted_feature_list_cmfs[:i]]
    selected_feature_matrix_cmfs = document_term_mat[:, feature_list_cmfs]
    clf_cmfs = MultinomialNB().fit(selected_feature_matrix_cmfs, newsgroups_train.target)
    pred_cmfs = clf_cmfs.predict(document_term_mat_test[:, feature_list_cmfs])
    f1_score_cmfs = metrics.f1_score(newsgroups_test.target, pred_cmfs, average='micro')
    cmfs_scores.append(f1_score_cmfs * 100)

final_scores_ICMFS = []
for i in range(200, 2001, 200):
    feature_list_final_ICMFS = [term for term in final_term_list_ICMFS[:i]]
    selected_feature_matrix_final_ICMFS = document_term_mat[:, feature_list_final_ICMFS]
    clf_final_ICMFS = MultinomialNB().fit(selected_feature_matrix_final_ICMFS, newsgroups_train.target)
    pred_final_ICMFS = clf_final_ICMFS.predict(document_term_mat_test[:, feature_list_final_ICMFS])
    f1_score_final_ICMFS = metrics.f1_score(newsgroups_test.target, pred_final_ICMFS, average='micro')
    final_scores_ICMFS.append(f1_score_final_ICMFS * 100)
    
final_scores_CMFS = []
for i in range(200, 2001, 200):
    feature_list_final_CMFS = [term for term in final_term_list_CMFS[:i]]
    selected_feature_matrix_final_CMFS = document_term_mat[:, feature_list_final_CMFS]
    clf_final_CMFS = MultinomialNB().fit(selected_feature_matrix_final_CMFS, newsgroups_train.target)
    pred_final_CMFS = clf_final_CMFS.predict(document_term_mat_test[:, feature_list_final_CMFS])
    f1_score_final_CMFS = metrics.f1_score(newsgroups_test.target, pred_final_CMFS, average='micro')
    final_scores_CMFS.append(f1_score_final_CMFS * 100)


# ### Test with chi2

# In[17]:

ch2_scores = []
for i in range(200, 2001, 200):
    ch2 = SelectKBest(chi2, k=i)
    ch2_train = ch2.fit_transform(document_term_mat, newsgroups_train.target)
    ch2_test = ch2.transform(document_term_mat_test)
    clf = MultinomialNB().fit(ch2_train, newsgroups_train.target)
    pred = clf.predict(ch2_test)
    f1_score = metrics.f1_score(newsgroups_test.target, pred, average='micro')
    ch2_scores.append(f1_score * 100)


# ### Plot Accuracy vs Number of features graph

# In[18]:

x = [i for i in range(200, 2001, 200)]
plt.plot(x, icmfs_scores, x, ch2_scores, x, cmfs_scores, x, final_scores_ICMFS, x, final_scores_CMFS)
plt.xlabel("No of features")
plt.ylabel("Accuracy")
plt.legend(("ICMFS", "chi2", "CMFS", "IGFSS+ICMFS","IGFSS+CMFS"), loc='best')
plt.show()

