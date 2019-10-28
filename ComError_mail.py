#!/usr/bin/env python
# coding: utf-8

# ## pobrabnie danych z webHMI

# In[1]:


from API_webHMI import ApiWebHmi
from settings import device_adress, APIKEY

import pandas as pd
import numpy as np


# In[2]:


pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', -1)  # or 199


# In[3]:


# zamiana na inty
def f(x):
    try:
        return x.astype('int')
    except:
        return x


# ## Zrobinie obiektu webHMI

# In[4]:


web = ApiWebHmi(device_adress, APIKEY)


# ## Odczytanie listy połaczen

# In[5]:


req1=web.make_req('connectionList')
connections=pd.DataFrame(req1).set_index('id')


# ## Odczytanie rejestru z bledami połaczen

# In[6]:


X_WH_CONNS='262' # id polaczania z informacja
val=web.make_req('getCurValue',X_WH_CONNS=X_WH_CONNS)


# ## Odczytanie tablicy z scantime

# In[7]:


import ast
scan_time=[ast.literal_eval(x) for x in val['4547']['v'].split(";")]


# ## Stworzenie tablicy

# In[8]:


scan_dict={}
for n,i in enumerate(scan_time):
    scan_dict[n]={'ids':i[0],
                  'title':connections.loc[str(i[0]),'title'],
                  'category':connections.loc[str(i[0]),'category'],
                  'timeout':connections.loc[str(i[0]),'timeout'],
                  'disabled':connections.loc[str(i[0]),'disabled'],
                  'scan_time':int(i[1])}


# In[9]:


scan_frame=pd.DataFrame(scan_dict,).T.apply(f) # zamiana na inty
frame=scan_frame.sort_values('scan_time',ascending=False)


# In[10]:


pivot_sum=frame[['category','scan_time']].groupby('category').agg(['sum','mean'])


# In[11]:


pivot_sum.sort_values(('scan_time','sum'),ascending=False,inplace=True)


# In[12]:


worsts=frame.set_index('ids').sort_values('scan_time',ascending=False).head(10)


# ## Napisanie wiadomosci

# In[13]:


connectio_problem=val['4546']['v'].split(",") # wiadomosc do zapisania
errors=[]
if len(connectio_problem)>1:
    for i in connectio_problem:
        title = connections.loc[i,'title']
        errors.append("<li>Błąd połączenia z urządzeniem o id {} - {}</li>".format(i,title ))
else: errors.append("<h3>Brak problemow z połączeniami. :)</h3>")

mesages="\n".join(errors)
mesages


# ## Wyslanie maila

# In[14]:


from envelopes import Envelope, GMailSMTP
import glob

def send_emial(content):

    addr=['tito02@o2.pl', 'norbert.jablonski@elam.pl']#,'michal.marchelewski@elam.pl']
    addr = ['jablonski.norbert@gmail.com','tito02@o2.pl']
    for i in range(len(addr)):
        print('Wysłanie wiadomosci do {}'.format(addr[i]))
        envelope = Envelope(
            from_addr=( u'WebHMI - Raport'),
            to_addr=(addr[i]),
            subject=u'Raport o komunikacji {} dla {}'.format(i+1,addr[i]),
            html_body=email,
        )
        #envelope.add_attachment(str(atachment))

    # Send the envelope using an ad-hoc connection...
        send_msg=envelope.send('smtp.googlemail.com', login='truecapehorn@gmail.com',password='Ptjczinp249', tls=True,)
        print('email do adresata. {} wysłany.'.format(addr[i]))  
    return send_msg


# ### Pobrnaie czasu

# In[15]:


czas=web.make_req('getLocTime')
czas=web.string_time(czas['timestamp'])
czas


# In[16]:


if len(connectio_problem)>0:
    email=u"""<h4>{}</h4><h2>WebHMI ma problemy z komunikacją dla następujących urządzeń:</h2>
    \n{}
    \n<h4>Czasy skanowania</h4>
    {}
    \n<h4>10 najgorszych</h4>
    {}
    """.format(czas,mesages,pivot_sum.to_html(),worsts.to_html())

    print(email)
    send_msg=send_emial(email)


# In[ ]:




