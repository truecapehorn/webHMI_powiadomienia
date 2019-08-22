#!/usr/bin/env python
# coding: utf-8

# ## pobrabnie danych z webHMI

# In[1]:


from API_webHMI import *
from defs import *
from head import headers, device_adress,filepath
import pandas as pd


# In[2]:


pd.set_option('display.max_columns', None)
pd.set_option('display.max_rows', None)


# In[3]:


filepath


# ## Odczytanie listy połaczen

# In[4]:


def conn():
    print('1: Connection Req\n')
#     displayHeader(headers)
    req1 = connectionList(device_adress, headers)  # pobranie listy polaczen plc.
    return req1
connections=pd.DataFrame(conn())


# ## Odczytanie listy rejstrow

# In[5]:


def reg():
    print('\n2 :Registers Req\n')
#     displayHeader(headers)  # wystarczy podstawowy naglowek
    req2 = registerList(device_adress, headers)  # odczytanie listy rejestrow
    return req2
# registers=pd.DataFrame(reg())
# registers.shape


# ## Odczytanie rejestru z bledami połaczen

# In[6]:


def reg_val(device_adress, headers):
    print('1: Connection Req\n')
#     displayHeader(headers)
    req1 = getCurValue(device_adress, headers)  # pobranie listy polaczen plc.
    return req1


# In[7]:


header1=headers
header1['X-WH-CONNS']='262'
val=reg_val(device_adress,header1)
val


# ## Nadpisanie pliku wiadomosci

# In[8]:


connectio_problem=val['4546']['v'].split(",") # wiadomosc do zapisania
with open('mail_message.txt', 'w')  as w_writer:
    if len(connectio_problem)>1:
        for i in connectio_problem:
            title = connections.loc[i,'title']
            print("Błąd połaczenia nr. {} - {}".format(i,title ))
            mesages="Błąd połaczenia nr {} - {}\n".format(i,title )
            w_writer.write(mesages)
    else: w_writer.write('Brak problemow z połaczeniami. :)')
        


# ## Wyslanie maila

# In[9]:


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
            text_body=email
        )
        #envelope.add_attachment(str(atachment))

    # Send the envelope using an ad-hoc connection...
        envelope.send('smtp.googlemail.com', login='truecapehorn@gmail.com',password='Ptjczinp249', tls=True)
        print('email do adresata. {} wysłany.'.format(addr[i]))


# In[10]:


if len(connectio_problem)>0:
    with open('mail_message.txt', 'r') as content_file:
        content = content_file.read()
        send_emial(content)


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:




