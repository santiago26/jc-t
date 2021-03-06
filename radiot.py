#!/usr/bin/python
# -*- coding: utf-8 -*-

import xmpp, time, sys
import random

from text import is_txt

assert len(sys.argv[1:]) == 3, 'params required: <login> <password> <name>'

is_txt['help!'] = "commands - " + ", ".join(is_txt.keys())


#keys = {}
#for keys_list in [ x for x in is_txt.keys() if type(is_txt[x]) == list ]:
#    if len(is_txt[keys_list]) > 0:
#        keys[keys_list] = [ x for x in range(1, len(is_txt[keys_list])+1 ) if len(is_txt[keys_list]) > 0 ]

def send(conn, mess):
    try:
        mess = mess.decode('UTF-8')
    except:
        pass
    mymess = xmpp.protocol.Message(body=mess)
    mymess.setTo('online@conference.radio-t.com')
    mymess.setType('groupchat')
    conn.send(mymess)

def message_handler(conn, mess):
    try:
        text = mess.getBody()
        if text in is_txt and is_txt[text]:
            txt = is_txt[text]
            if type(txt) == list:
                txt = random.choice(txt)
            time.sleep(0.9)
            send(conn, txt)
    except:
        pass

cl = xmpp.Client('yandex.ru', debug=[])
cl.connect(server=('xmpp.ya.ru',5223))

cl.RegisterHandler('message', message_handler)

cl.auth(sys.argv[1], sys.argv[2], 'Python-JCB')

p = xmpp.Presence(to='online@conference.radio-t.com/%s' % sys.argv[3])
p.setTag('x',namespace=xmpp.NS_MUC).setTagData('password','')
p.getTag('x').addChild('history',{'maxchars':'0','maxstanzas':'0'})

cl.send(p)
cl.sendInitPresence()

while True:
    try:
        cl.Process(1)
    except:
        cl.disconnect()
        cl.send(xmpp.Presence(typ = 'unavailable'))
        exit()

