#!/usr/bin/env python
# coding: utf-8

# ## pobrabnie danych z webHMI

# In[1]:


from API_webHMI import *
from defs import *
from head import headers, device_adress,filepath
import pandas as pd
import numpy as np


# In[2]:


pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', -1)  # or 199


# In[3]:


filepath


# ## Odczytanie listy połaczen

# In[4]:


def conn():
    print('1: Connection Req\n')
#     displayHeader(headers)
    req1 = connectionList(device_adress, headers)  # pobranie listy polaczen plc.
    return req1
connections=pd.DataFrame(conn()).set_index('id')


# In[5]:


def f(x):
    try:
        return x.astype('int')
    except:
        return x


# ## Odczytanie listy rejstrow

# In[6]:


def reg():
    print('\n2 :Registers Req\n')
#     displayHeader(headers)  # wystarczy podstawowy naglowek
    req2 = registerList(device_adress, headers)  # odczytanie listy rejestrow
    return req2
# registers=pd.DataFrame(reg())
# registers.shape


# ## Odczytanie rejestru z bledami połaczen

# In[7]:


def reg_val(device_adress, headers):
    print('1: Connection Req\n')
#     displayHeader(headers)
    req1 = getCurValue(device_adress, headers)  # pobranie listy polaczen plc.
    return req1


# In[8]:


header1=headers
header1['X-WH-CONNS']='262' # 262 to numer polaczenia w webHMI
val=reg_val(device_adress,header1)


# ## Odczytanie tablicy z scantime

# In[9]:


import ast
scan_time=[ast.literal_eval(x) for x in val['4547']['v'].split(";")]


# ## Stworzenie tablicy

# In[10]:


scan_dict={}
for n,i in enumerate(scan_time):
    scan_dict[n]={'ids':i[0],
                  'title':connections.loc[str(i[0]),'title'],
                  'category':connections.loc[str(i[0]),'category'],
                  'timeout':connections.loc[str(i[0]),'timeout'],
                  'disabled':connections.loc[str(i[0]),'disabled'],
                  'scan_time':int(i[1])}


# In[11]:


scan_frame=pd.DataFrame(scan_dict,).T.apply(f)
frame=scan_frame.sort_values('scan_time',ascending=False)


# In[12]:


pivot_sum=frame.pivot_table(index='category',values='scan_time',aggfunc=[np.mean,np.sum])
pivot_sum.columns=pivot_sum.columns.droplevel(1)
pivot_sum.sort_values('sum',ascending=False,inplace=True)


# ## Nadpisanie pliku wiadomosci

# In[14]:


connectio_problem=val['4546']['v'].split(",") # wiadomosc do zapisania
with open('mail_message.txt', 'w')  as w_writer:
    if len(connectio_problem)>1:
        for i in connectio_problem:
            title = connections.loc[i,'title']
#             print("Błąd połączenia nr {} - {}\n".format(i,title ))
            mesages="<p>Błąd połączenia nr {} - {}</p>\n".format(i,title )
            w_writer.write(mesages)
    else: w_writer.write('<h3>Brak problemow z połączeniami. :)</h3>\n\n')
        


# ## Wyslanie maila

# In[15]:


from envelopes import Envelope, GMailSMTP
import glob

def send_emial(content):

    addr=['tito02@o2.pl', 'norbert.jablonski@elam.pl','michal.marchelewski@elam.pl']
    for i in range(len(addr)):
        print('Wysłanie wiadomosci do {}'.format(addr[i]))
        envelope = Envelope(
            from_addr=( u'WebHMI - Raport'),
            to_addr=(addr[i]),
            subject=u'Raport o komunikacji {} dla {}'.format(i+1,addr[i]),
            html_body=email,
#             text_body=email
        )
        #envelope.add_attachment(str(atachment))

    # Send the envelope using an ad-hoc connection...
        send_msg=envelope.send('smtp.googlemail.com', login='truecapehorn@gmail.com',password='Ptjczinp249', tls=True,)
        print('email do adresata. {} wysłany.'.format(addr[i]))  
    return send_msg


# In[16]:


if len(connectio_problem)>0:
    with open('mail_message.txt', 'r') as content_file:
        content = content_file.read()
        email= u"<h2>WebHMI ma problemy z komunikacją dla następujących urządzeń:</h2>\n{}\n<h4>Czasy skanowania</h4>\n{}".format(str(content),pivot_sum.to_html())
        print(email)
        send_msg=send_emial(email)


# In[ ]:





# In[ ]:




