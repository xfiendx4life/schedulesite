from get_data import *
import cgi
import os
from get_class import get_by_id


query = os.environ['QUERY_STRING']
classid = query.split('=')[1].split('&')[0]
day = int(query.split('=')[2])
next_day = day + 1
pre_day = day - 1
classname = get_by_id(classid)
print(day)
print ("Content-type:text/html")
print()
print('<!DOCTYPE html>')
print('''<html>
           <head>
             <meta charset='windows1251'>
             <meta name="viewport" content="width=device-width, initial-scale=1">
             <link href="http://maxcdn.bootstrapcdn.com/bootstrap/3.3.6/css/bootstrap.min.css" rel="stylesheet" type="text/css">
             <style>
              .intable:{
                font-family: Geneva, Arial, Helvetica, sans-serif;
                font-size: 24pt;
              }
              a { color: inherit; }
              td {font-size: 18pt; }
              h1 {font-size: 30pt; }
             </style>
           </head>
        <body>''')
print('<h1 align="center">%s</h1>' % classname.upper())
print('<div>')
print(Make_a_message(classid,day))
print('</div>')
print('<table class="table">')
print('''<tr><td align="center">
         <a href="/cgi-bin/schedule.py?class=%s&day=%s"> <h1><small>Предыдущий день</small></h1></a>
         </td>'''% (classid,pre_day))
print('<td align="center"><h1 align="center"><small><a href="/cgi-bin/index.py">Главная</a></small></h1></td>')
print('''<td align="center">
          <a href="/cgi-bin/schedule.py?class=%s&day=%s"> <h1><small>Следующий день</small></h1></a>
        </td>''' % (classid,next_day))
print('''</tr>
           </table>''')
print ("</body>")
print ("</html>")

