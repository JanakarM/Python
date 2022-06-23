import xml.etree.ElementTree as ET
from utils import *

tree = ET.parse(path + 'tablecolumns.xml')
root = tree.getroot()

report_vs_transformer_model={}

def popupate_transformer():
    global report_vs_transformer_model
    attrib_map = get_attrib_map()
    for col in root.iter('O365ReportColumnDetails'):
        rep_id = col.get('REPORT_ID')
        trans = col.get('SERVER_TRANSFORMER_MODEL')
        attrib_id = col.get('ATTRIB_ID')
        if trans != None:
            if rep_id not in report_vs_transformer_model:
                report_vs_transformer_model[rep_id] = ''
            if len(report_vs_transformer_model[rep_id]) > 0:
                report_vs_transformer_model[rep_id] += '|'
            if '=' in trans:
                report_vs_transformer_model[rep_id] += trans
            else:
                attrib_name = attrib_map[attrib_id]
                report_vs_transformer_model[rep_id] += attrib_name + '=' + trans # get attrib name
def print_transformer():
    global report_vs_transformer_model
    for e in report_vs_transformer_model:
        print('{0} - {1}'.format(e, report_vs_transformer_model[e]))
def get_trans_content():
    content_trans = ''
    global report_vs_transformer_model
    for e in report_vs_transformer_model:
        content_trans += '{0} - {1}\n\n'.format(e, report_vs_transformer_model[e])
    return content_trans
def get_attrib_map():
    attrib_map = {}
    for attr in root.iter('O365AttributeDetails'):
        attrib_map[attr.get('ATTRIB_ID')] = attr.get('MS_GRAPH_ATTRIB_NAME') if attr.get('MS_GRAPH_ATTRIB_NAME') != None else attr.get('ATTRIB_NAME')
    return attrib_map
def start():
    popupate_transformer()
    writeToFile('trans.xml', get_trans_content())

