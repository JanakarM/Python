import xml.etree.ElementTree as ET

from utils import writeToFile

tree = ET.parse('change_values.xml')
root = tree.getroot()

# get new id map for rest api path
path_id_map = {}
id = 1
for e in root.iter('O365RestAPIURLPaths'):
    path_id_map[e.get('REST_API_URL_PATH_ID')] = '{0}'.format(id)
    e.set('REST_API_URL_PATH_ID', path_id_map[e.get('REST_API_URL_PATH_ID')])
    id += 1

for e in root.iter('O365RestAPIURLPathParams'):
    e.set('REST_API_URL_PATH_ID', path_id_map[e.get('REST_API_URL_PATH_ID')])

for e in root.iter('O365RestAPIPathSet'):
    e.set('REST_API_URL_PATH_ID', path_id_map[e.get('REST_API_URL_PATH_ID')])
    if e.get('REST_API_LEADING_URL_PATH_ID') != None:
        e.set('REST_API_LEADING_URL_PATH_ID', path_id_map[e.get('REST_API_LEADING_URL_PATH_ID')])

tree.write('change_values_new.xml',encoding='UTF-8',xml_declaration=True)  