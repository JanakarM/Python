from os import remove
import xml.etree.ElementTree as ET
from utils import *

path='E:\\Jana\\Github\\Python\\utilities\\'
tree = ET.parse(path+'sample.xml')
root = tree.getroot()

# extract common url templates
url_templates=[] #list of tuples
unique_url_templates=[] #list of tuples
reportIds=[]
report_processed={}
# get report_id as list
for e in root.iter('O365ReportRestAPIs'):
    reportIds.append(e.attrib.get('REPORT_ID'))
flag=True
def verifyTuple(a, b):
    for b_e in b:
        if a[0]==b_e[0] and a[1]==b_e[1] and a[2]==b_e[2]:
            return True
    return False
def compareTupleList(a, b):
    global flag
    if(len(a) != len(b)):
        return False
    for a_e in a:
        if not verifyTuple(a_e, b):
            return False
    flag=False
    return True
def checkExisting(a):
    global unique_url_templates
    for b in unique_url_templates:
        if a[0]==b[0] and a[1]==b[1] and compareTupleList(a[2],b[2]):
            return b[3]
    return -1
def populate_tuples():
    global url_templates
    for e in root.iter("O365ReportRestAPIs"):
        url_1=e.get('REST_API_URL_PATH_ID')
        url_2=e.get('REST_API_LEADING_URL_PATH_ID')
        report_rest_api_id=e.get('UNIQUE_ID')
        report_rest_params=[]
        for ee in root.findall(".*[@REPORT_REST_API_PATH_ID='{0}']".format(report_rest_api_id)):
            report_rest_params.append(
                (
                    ee.get("ATTRIB_ID"),
                    ee.get("TRANSFORMER_MODEL"),
                    ee.get("REST_API_URL_PATH_PARAM_ID"),
                    ee.get("UNIQUE_ID")
                )
            )
        report_rest_params.sort(key = lambda e: e[3])
        url_templates.append(
            (
                url_1,
                url_2,
                report_rest_params,
                e.get('REPORT_ID'),
                report_rest_api_id
            )
        )
            
content_a='' # rest templates
content_b='' # rest template vs params
content_c='' # report vs restapi
rep_id_vs_templates={}
def removeDuplicates():
    global url_templates, unique_url_templates, content_a, content_b, content_c, rep_id_vs_templates
    id_a = 0
    id_b = 0
    for e in url_templates:
        if e[3] not in rep_id_vs_templates:
            rep_id_vs_templates[e[3]] = []
        template_id = checkExisting(e)
        if template_id == -1:
            id_a+=1
            content_a += '<a '
            content_a += 'a="{0}" b="{1}" '.format(id_a, e[0])
            if e[1] != None:
                content_a += 'c="{0}" '.format(e[1])
            content_a += '/>\n'
            for ee in e[2]:
                id_b+=1
                content_b += '<b '
                content_b += 'a="{0}" b="{1}" c="{2}" '.format(id_b, e[4], ee[0])
                if ee[1] != None:
                    content_b += 'd="{0}" '.format(ee[1])
                if ee[2] != None:
                    content_b += 'e="{0}" '.format(ee[2])
                content_b += '/>\n'
            unique_url_templates.append(e + (id_a,))
            rep_id_vs_templates[e[3]].append(id_a)
        else:
            rep_id_vs_templates[e[3]].append(template_id)
    print('id_a : {0}\nid_b: {1}'.format(id_a, id_b))
def constructRepVsRest():
    global reportIds, content_c, rep_id_vs_templates, report_processed
    id_c = 0
    for repId in reportIds:
        if repId != None:
            if repId in report_processed:
                continue
            report_processed[repId]=True
            for t in rep_id_vs_templates[repId]:
                id_c += 1
                content_c += '<c '
                content_c += 'a="{0}" b="{1}" c="{2}" '.format(id_c, repId, t)
                content_c += '/>\n'
    print('id_c : ', id_c)
populate_tuples()
removeDuplicates()
report_processed={}
constructRepVsRest()
writeToFile('a.xml', content_a)
writeToFile('b.xml', content_b)
writeToFile('c.xml', content_c)
print('length of reportIds : {0}'.format(len(reportIds)))
print("url_templates - {0}".format(len(url_templates)))