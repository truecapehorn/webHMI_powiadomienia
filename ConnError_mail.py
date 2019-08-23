#!/usr/bin/env python
# coding: utf-8

# ## pobrabnie danych z webHMI

# In[38]:


from API_webHMI import *
from defs import *
from head import headers, device_adress,filepath
import pandas as pd


# In[39]:


pd.set_option('display.max_columns', None)  # or 1000
pd.set_option('display.max_rows', None)  # or 1000
pd.set_option('display.max_colwidth', -1)  # or 199


# In[40]:


filepath


# ## Odczytanie listy połaczen

# In[41]:


def conn():
    print('1: Connection Req\n')
#     displayHeader(headers)
    req1 = connectionList(device_adress, headers)  # pobranie listy polaczen plc.
    return req1
connections=pd.DataFrame(conn()).set_index('id')


# In[42]:


def f(x):
    try:
        return x.astype('int')
    except:
        return x


# ## Odczytanie listy rejstrow

# In[43]:


def reg():
    print('\n2 :Registers Req\n')
#     displayHeader(headers)  # wystarczy podstawowy naglowek
    req2 = registerList(device_adress, headers)  # odczytanie listy rejestrow
    return req2
# registers=pd.DataFrame(reg())
# registers.shape


# ## Odczytanie rejestru z bledami połaczen

# In[44]:


def reg_val(device_adress, headers):
    print('1: Connection Req\n')
#     displayHeader(headers)
    req1 = getCurValue(device_adress, headers)  # pobranie listy polaczen plc.
    return req1


# In[45]:


header1=headers
header1['X-WH-CONNS']='262' # 262 to numer polaczenia w webHMI
val=reg_val(device_adress,header1)
val


# ## Nadpisanie pliku wiadomosci

# In[46]:


connectio_problem=val['4546']['v'].split(",") # wiadomosc do zapisania
with open('mail_message.txt', 'w')  as w_writer:
    if len(connectio_problem)>1:
        for i in connectio_problem:
            title = connections.loc[i,'title']
            print("Błąd połączenia nr {} - {}\n".format(i,title ))
            mesages="Błąd połączenia nr {} - {}\n".format(i,title )
            w_writer.write(mesages)
    else: w_writer.write('Brak problemow z połączeniami. :)')
        


# ## Wyslanie maila

# In[10]:


from envelopes import Envelope, GMailSMTP
import glob

def send_emial(content):

    addr=['tito02@o2.pl', 'norbert.jablonski@elam.pl','michal.marchelewski@elam.pl']
    email= u"WebHMI ma problemy z komunikacją dla następujących urządzeń:\n{}".format(str(content))
    for i in range(len(addr)):
        print('Wysłanie wiadomosci do {}'.format(addr[i]))
        envelope = Envelope(
            from_addr=( u'WebHMI - Raport'),
            to_addr=(addr[i]),
            subject=u'Raport o komunikacji {} dla {}'.format(i+1,addr[i]),
            text_body=email)
        #envelope.add_attachment(str(atachment))

    # Send the envelope using an ad-hoc connection...
        envelope.send('smtp.googlemail.com', login='truecapehorn@gmail.com',password='Ptjczinp249', tls=True)
        print('email do adresata. {} wysłany.'.format(addr[i]))


# In[11]:


if len(connectio_problem)>0:
    with open('mail_message.txt', 'r') as content_file:
        content = content_file.read()
        send_emial(content)


# In[ ]:





# In[ ]:





# In[ ]:




