import pandas as pd
from difflib import SequenceMatcher,get_close_matches
import numpy as np
from IPython.display import display
import re
from tqdm.notebook import tqdm
from operator import add
from deep_translator import GoogleTranslator
t = GoogleTranslator(source='auto', target='en')

def adding_new_cols(df):
  matched_companies_names = np.zeros((df.shape[0],1))
  matched_companies_Street_Addresses = np.zeros((df.shape[0],1))
  matched_companies_telephones = np.zeros((df.shape[0],1))
  matched_companies_names_score = np.zeros((df.shape[0],1))
  matched_companies_Street_Addresses_score = np.zeros((df.shape[0],1))
  matched_companies_telephones_score = np.zeros((df.shape[0],1))
  df.insert(loc=1,column = 'Bovag_Matched_Name', value = matched_companies_names)  
  df.insert(loc=2,column = 'Bovag_Matched_Street_Address', value = matched_companies_Street_Addresses)
  df.insert(loc=3,column = 'Bovag_Matched_Telephone', value = matched_companies_telephones)  
  df.insert(loc=4,column = 'Bovag_Matched_Name_score', value = matched_companies_names_score)  
  df.insert(loc=5,column = 'Bovag_Matched_Street_Address_score', value = matched_companies_Street_Addresses_score)
  df.insert(loc=6,column = 'Bovag_Matched_Telephone_score', value = matched_companies_telephones_score) 
  new_cols=['name', 'Bovag_Matched_Name','Bovag_Matched_Name_score','vicinity', 'Bovag_Matched_Street_Address','Bovag_Matched_Street_Address_score',
       'formatted_phone_number','Bovag_Matched_Telephone', 
        'Bovag_Matched_Telephone_score', 'place_id', 'rating',
       'reference', 'scope', 'types', 'user_ratings_total']
  df=df.reindex(columns=new_cols)
  return df

def eng_translation(df1,df2):
  translated_c_names =[t.translate(name) for name in tqdm(df1['company_name'].tolist())]
  translated_api_c_names =[t.translate(name) for name in tqdm(df2['name'].tolist())]

  bovag_add = [t.translate(add) for add in tqdm(df1['Street_Address'].tolist())]
  api_splitted_add = [t.translate(add[:-10]) for add in tqdm(df2['vicinity'])]

  df2['name'] = translated_api_c_names
  df1['company_name'] = translated_c_names

  df1['Street_Address'] = bovag_add
  df2['vicinity'] =api_splitted_add
  return df1, df2

def exact_comp_name_match(df1,df2):
  '''This cell finds out the exact match of the company name in the both files and place the name of the matched company name from Bovag database at the Bovag_Matched column with the highest similarity'''
  for i,name in enumerate(df2['name'].tolist()):
    for k,name_1 in enumerate(df1['company_name'].tolist()):
      if name == name_1: 
        df2['Bovag_Matched_Name'][i] = name_1
        df2['Bovag_Matched_Street_Address'][i] = df1['Street_Address'][k]
        df2['Bovag_Matched_Telephone'][i] = df1['Telephone'][k]
        df2['Bovag_Matched_Name_score'][i] =  SequenceMatcher(a=name,b=name_1).ratio()
        df2['Bovag_Matched_Street_Address_score'][i] =  SequenceMatcher(a=df1['Street_Address'][k],b=df2['vicinity'][i]).ratio()
        df2['Bovag_Matched_Telephone_score'][i] =  SequenceMatcher(a=df1['Telephone'][k].replace("-","").replace(" ",""),b=df2['formatted_phone_number'][i].replace("-","").replace(" ","")).ratio()
  return df1,df2

def exact_Street_Address_match(df1,df2):
  for i,add1 in enumerate(df2['vicinity'].tolist()):
    for k,add2 in enumerate(df1['Street_Address'].tolist()):
      if df2['Bovag_Matched_Name'][i] == 0.0:
        if add2 in add1 and len(add2)>4: 
          df2['Bovag_Matched_Name'][i] = df1['company_name'][k]
          df2['Bovag_Matched_Street_Address'][i] = add2
          df2['Bovag_Matched_Telephone'][i] = df1['Telephone'][k]
          df2['Bovag_Matched_Name_score'][i] =  SequenceMatcher(a=df2['name'][i],b=df1['company_name'][k]).ratio()
          df2['Bovag_Matched_Street_Address_score'][i] =  SequenceMatcher(a=add2,b=add1).ratio()
          df2['Bovag_Matched_Telephone_score'][i] =  SequenceMatcher(a=df1['Telephone'][k].replace("-","").replace(" ",""),b=df2['formatted_phone_number'][i].replace("-","").replace(" ","")).ratio()
  return df1,df2

def exact_telephone_match(df1,df2):
  for i,tel1 in enumerate(df2['formatted_phone_number'].tolist()):
    for k,tel2 in enumerate(df1['Telephone'].tolist()):
      if df2['Bovag_Matched_Name'][i] == 0.0:
        tel1=tel1.replace("-","").replace(" ","")
        tel2=tel2.replace("-","").replace(" ","")
        if tel1 == tel2:
          df2['Bovag_Matched_Name'][i] = df1['company_name'][k]
          df2['Bovag_Matched_Street_Address'][i] = df1['Street_Address'][k]
          df2['Bovag_Matched_Telephone'][i] = tel2
          df2['Bovag_Matched_Name_score'][i] =  SequenceMatcher(a=df2['name'][i],b=df1['Company_name'][k]).ratio()
          df2['Bovag_Matched_Street_Address_score'][i] =  SequenceMatcher(a=df1['Street_Address'][k],b=df2['vicinity'][i]).ratio()
          df2['Bovag_Matched_Telephone_score'][i] =  SequenceMatcher(a=tel2,b=tel1).ratio()
  return df1,df2

def keywords_matching(df1,df2,stop_words):
  '''Matching the kewords common in the names from the both of the companies'''
  company_names = df1['company_name'].tolist()
  for i,data in enumerate(df2[['name','vicinity']].values.tolist()):
    if df2['Bovag_Matched_Name'][i]==0.0:
      flag =True
      for w in data[0].lower().split():
        if w not in stop_words and len(w)>=4:
          add_scores,tel_scores,name_scores,namess,tel,add=[],[],[],[],[],[]
          l=0
          for k,name in enumerate(company_names):
            name=name.lower()
            if name.find(w)!=-1:
              l+=1
              add_scores.append(SequenceMatcher(a=df1['Street_Address'][k],b=df2['vicinity'][i]).ratio())
              tel_scores.append(0)
              name_scores.append(SequenceMatcher(a=df1['company_name'][k],b=df2['name'][i]).ratio())
              add.append(df1['Street_Address'][k])
              namess.append(df1['company_name'][k])
              tel.append(df1['Telephone'][k].replace('-','').replace(' ',''))
              sum1=[a + b for a, b in zip( add_scores, tel_scores)]
              max_index = np.argmax([a + b for a, b in zip(sum1,name_scores)])
          break
      if l>=1:
        df2['Bovag_Matched_Name'][i] = namess[max_index]
        df2['Bovag_Matched_Street_Address'][i] = add[max_index]
        df2['Bovag_Matched_Telephone'][i] = tel[max_index]
        df2['Bovag_Matched_Name_score'][i] =  name_scores[max_index]
        df2['Bovag_Matched_Street_Address_score'][i] =  add_scores[max_index]
        df2['Bovag_Matched_Telephone_score'][i] =  tel_scores[max_index]
  return df1,df2

def sentence_similarity(df1,df2,stop_words):
  '''This cell calculates the similarity between remaining bovag registered company and the place api scraped company names, similarity score of the names and Street_Addresses are calculated,
   highest similarity scored company is selected as the matched company name '''
  matched_companies=[]
  company_names = df1['company_name'].values.tolist()
# add overall similarity 
  for i,name in enumerate(df2[['name']].values.tolist()):
    if df2['Bovag_Matched_Name'][i] == 0.0:
      similarity = [SequenceMatcher(a=stopwords_removal2(name[0],stop_words),b= stopwords_removal2(c_name,stop_words)).ratio() for c_name in company_names]
      actual_similarity = SequenceMatcher(a=df1['company_name'].iloc[np.argmax(similarity)],b=df2['name'][i]).ratio()
      df2['Bovag_Matched_Name'][i] = df1['company_name'].iloc[np.argmax(similarity)]
      df2['Bovag_Matched_Name_score'][i] = actual_similarity
      df2['Bovag_Matched_Street_Address'][i] = df1['Street_Address'].iloc[np.argmax(similarity)]
      df2['Bovag_Matched_Telephone'][i] = df1['Telephone'].iloc[np.argmax(similarity)]
      df2['Bovag_Matched_Street_Address_score'][i] =   SequenceMatcher(a=df1['Street_Address'].iloc[np.argmax(similarity)],b=df2['vicinity'][i]).ratio()
      df2['Bovag_Matched_Telephone_score'][i] =  0
  return df1,df2

def finding_stopwords(df1):
  '''rare words in the company names are stored and frequent words are discarded, whose count is less than threshold is stored'''
  word_counts={}
  for name in df1['company_name'].tolist():
    for word in name.split():
      if word in word_counts.keys():
        word_counts[word] += 1
      else:
        word_counts[word] = 1
  word_counts= {k.lower(): v for k, v in word_counts.items() if v >5}
  stop_words = list(word_counts.keys())

  rms = ['kia','louwman','davo','zoetermeer','leiden','rotterdam','katwijk','noordwijk','leiderdorp']
  for w in rms:
    stop_words.remove(w)
  adds = ['repair','succes','class','haag','automobielen','sales','classic','classics','Automobielbedrijf','automobielbedrijf','kerketuinen','forepark','motorhuis','brand','group','dealer','automotives','Automotive company','automotive company','kerketuinen','forepark','motor home','automobiles','cars','car','Car','Cars','car service','autobedrijf','auto','company','AutoCenter','house','garage','the hague','autobedrijf']
  for w in adds:
    stop_words.append(w)

  return stop_words

#removing frequent words
def stopwords_removal2(text,stop_words):
  query=''
  text = ''.join(re.findall("[A-Za-z0-9 ]",text))
  for word in text.split():
    if word.lower() not in stop_words:
      query=query+word.lower()+' '
  return query

def company_name_matching(Bovag_csv_path,place_api_csv_path):
  df1 = pd.read_csv(Bovag_csv_path)
  df2 = pd.read_csv(place_api_csv_path)
  df2 = adding_new_cols(df2)
  stop_words = finding_stopwords(df1)
  df1,df2 = exact_comp_name_match(df1,df2)
  df1,df2 = exact_Street_Address_match(df1,df2)
  df1,df2 = exact_telephone_match(df1,df2)
  df1,df2 = keywords_matching(df1,df2,stop_words)
  df1,df2 = sentence_similarity(df1,df2,stop_words)
  overall_score = [(row['Bovag_Matched_Name_score']+row['Bovag_Matched_Street_Address_score']+row['Bovag_Matched_Telephone_score'])/3 for i,row in df2.iterrows()]
  df2.insert(loc=9,column = 'Overall_Similarity_score', value = overall_score) 
  df2.rename(columns ={'vicinity':'api_Street_Address'}, inplace = True)
  return df2

Bovag_csv_path = 'bovag_dataset.csv'
place_api_csv_path = 'place_api_companies.csv'
df2 = company_name_matching(Bovag_csv_path,place_api_csv_path)