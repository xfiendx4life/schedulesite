#!/usr/bin/env python3
from get_data import *
import cgi
from get_class import *
import datetime
import os
import simplejson
import time

def request_or_cache():
    json = {}
    expire = str(float(time.time()) + 24*60*60)
    path = os.path.dirname(os.path.realpath(__file__))+ '\\cache.sch'
    try:
        cache = open(path, 'r')
        json = simplejson.load(cache)
        cache.close()
        if float(time.time()) > float(json['expire']):
            raise
        else:
            class_list = json['class_list']
            #print('from cache')
    
    except:
        cache = open(path, 'w')
        #print('not cache')
        class_list = get_class_list()
        json['class_list'] = class_list
        json['expire'] = expire
        simplejson.dump(json,cache)
        cache.close()
    return class_list
bootstrap_path = os.path.dirname(os.path.realpath(__file__)) + '\\css\\bootstrap.min.css'
#http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css
print("Content-type: text/html charset='windows1251'")
print()
print('<!DOCTYPE html>')
print('''<html>
           <head>
             <meta charset='windows1251'>
             <meta name="viewport" content="width=device-width, initial-scale=1">
             <link href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" type="text/css">
             <style>
              p:{
                font-family: Geneva, Arial, Helvetica, sans-serif;
                font-size: 16pt;
              }
              a {
                color: inherit;
                font-size: 18pt; 
              }
             </style>
           </head>
        <body>''') #% bootstrap_path)

print('<h1 align="center">Выберите класс</h1>')
print('<div class="container">')
print('<table class="table table-striped">')
print('<tr>')
#replace={'а':'a','б':'b','в':'v','г':'g'}
big_string = ''
class_list = request_or_cache()


count = 0 
for item in class_list:
    s = item['classname']
    big_string += '<td><a href="schedule.py?class=%s&day=0"><p align="center">%s</p></a></td>'%(item['classid'],s)
    count += 1
    if count == 3:
        big_string += '</tr><tr>'
        count = 0
print(big_string)
print('</tr>')
print('</table>')
print('</div>')
print('''</body></html>''')


