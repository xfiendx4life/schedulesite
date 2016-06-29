import requests
import xml.etree.ElementTree  as ET
import datetime
from get_class import check_primary
import simplejson
import time
import os


def set_dates(day):
    date  = datetime.date.today()
    delta = day
    date = date + datetime.timedelta(days=delta)
    StartDate = date.strftime("%d.%m.%Y.")
    EndDate = date.strftime("%d.%m.%Y.")
    return StartDate, EndDate

     
def check_cache(ClassID, day):
    json = {}
    expire = str(float(time.time()) + 3*60*60)
    path = os.path.dirname(os.path.realpath(__file__))+ '\\sched_cache.sch'
    try:
        cache_file = open(path, 'r')
        json = simplejson.load(cache_file)
        cache_file.close()
        if float(time.time()) > float(json['expire']):
            json = {}
            json['expire'] = str(float(time.time()))
            cache_file = open(path,'w')
            cache_file.close()
        StartDate, EndDate = set_dates(day)
        ClassID_Date = ClassID + '|' + StartDate
        if ClassID_Date not in json:
            d = get_schedule_for_class(ClassID, day)
            json[ClassID_Date] = d
            cache_file = open(path, 'w')
            simplejson.dump(json,cache_file)
            cache_file.close()
            return d
        else:
            print('From Cache %s'% ClassID_Date)
            return json[ClassID_Date]
    except:
        StartDate, EndDate = set_dates(day)
        ClassID_Date = ClassID + '|' + StartDate
        if ClassID_Date not in json:
            d = get_schedule_for_class(ClassID, day)
            json[ClassID_Date] = d
            json['expire'] = expire
            cache_file = open(path, 'w')
            simplejson.dump(json,cache_file)
            cache_file.close()
            return d
#75265
def get_schedule_for_class(ClassID, day):
    StartDate, EndDate = set_dates(day)
    payload = {"Function":"GetScheduleForClass","ClassID":ClassID,
               "StartDate":StartDate, "EndDate":EndDate}
    r = requests.post("http://sgo.volganet.ru/lacc.asp", params = payload)
    doc = ET.fromstring(r.text)
    week = []
    for child in doc[0]:
        lessons  = {}
        lessons['Subject'] = child.find('subjname').text
        lessons['Date'] = child.find('day').text
        lessons['Start_time'] = child.find('starttime').text
        lessons['End_time'] = child.find('endtime').text
        lessons['Teacher'] = '%s %s %s' %(child.find('tlastname').text,
         child.find('tfirstname').text, child.find('tmidname').text )
        lessons['Room'] = child.find('roomname').text
        week.append(lessons)
    return week

#сделать эту процелуру с set_dates()
def check_weekend(ClassID, day):
    date = set_dates(day)[0]
    date = datetime.datetime.strptime(date,"%d.%m.%Y.")
    if date.weekday() == 6:
        return True
    if date.weekday() == 5 and ClassID in check_primary():
        return True
    return False

    
def Make_a_message(ClassID, date):
    #day = get_schedule_for_class(ClassID, *day)
    day = check_cache(ClassID, date)#ошибка из-за этого говна, разобраться
    try:
        if not check_weekend(ClassID, date):
            table = '''<table class="table table-striped">
                     <tr class="success" align="center">
                        <td style="font-size: 130%" align="center"><b>Время</b></td>
                        <td style="font-size: 130%" align="center"><b>Предмет</b></td>
                        <td style="font-size: 130%" align="center"><b>Кабинет</b></td>
                        <td style="font-size: 130%" align="center"><b>Учитель</b></td>
                     </tr>'''
            message =   '<h1 align="center"><small>%s</small></h1><BR>' % day[0]['Date'] + table 
            for lesson in day:
                message += '''<tr>
                              <td align="center">%s - %s</td> <td align="center">%s</td> <td align="center">%s</td>
                              <td align="center">%s %s.%s. </tr>''' % (lesson['Start_time'],lesson['End_time'],lesson['Subject'],
                                            lesson['Room'],lesson['Teacher'].split()[0],
                                                      lesson['Teacher'].split()[1][0],
                                                      lesson['Teacher'].split()[2][0])
            message += '</table>'
        else:
            message = '<h1 align="center">В этот день нет уроков</h1>'
    except:
        message = "Похоже в этот день произошло непоправимое"
    return message
