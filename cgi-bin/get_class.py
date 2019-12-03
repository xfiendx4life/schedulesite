
import requests
import xml.etree.ElementTree  as ET
def get_class_list():
        r = requests.post('https://sgo.volganet.ru/api/lacc.asp?Function=GetClassListForSchool&SchoolID=1460')
        root = ET.fromstring(r.text)
        class_list = []
        print(root)
        for child in root[0]:
                class_voc = {}
                class_voc['classid'] = child.find('classid').text
                class_voc['classname'] = child.find('classname').text
                class_list.append(class_voc)
        return class_list

def check_primary():
        primary_ids = []
        class_list = get_class_list()
        for item in class_list:
                if int(item['classname'][0]) < 5:
                        primary_ids.append(item['classid'])
        return primary_ids
        
def get_by_id(ClassID):
        class_list = get_class_list()
        for item in class_list:
                if item['classid'] == ClassID:
                        return item['classname']
