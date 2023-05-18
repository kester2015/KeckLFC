import csv
import xml.etree.ElementTree as ET
import xml.dom.minidom

def csv_to_xml(csv_file_path, xml_file_path):

    with open(csv_file_path, 'r') as csv_file:
        reader = csv.DictReader(csv_file)
        
        root = ET.Element('bundle', name="LFC", service="nsmine")#, xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance")
        
        dispatcher = ET.SubElement(root, 'dispatcher')
        dispatcher_name = ET.SubElement(dispatcher, 'name')
        dispatcher_name.text = "+service+_dispatch_3"
        
        for row in reader:
            keyword = ET.SubElement(root, 'keyword')
            
            name = ET.SubElement(keyword, 'name')
            name.text = row['name']
            
            keyword_type = ET.SubElement(keyword, 'type')
            keyword_type.text = row['type']
            
            help_brief = ET.SubElement(keyword, 'help', level="brief")
            help_brief.text = row['brief_help']
            
            #help_verbose = ET.SubElement(keyword, 'help', level="verbose")
            #help_verbose.text = row['verbose_help']
            
            capability = ET.SubElement(keyword, 'capability', type="write")
            if row['capability'] == 'R/W': capability.text = "True"
            if row['capability'] == 'R'  : capability.text = "False"

            if (row['min'] != '' or row['max'] != ''):
                ranges = ET.SubElement(keyword, 'range')
                
                if row['min'] != '':                
                    minval = ET.SubElement(ranges, 'minimum')
                    minval.text = row['min']
                if row['max'] != '':                
                    maxval = ET.SubElement(ranges, 'maximum')
                    maxval.text = row['max']

            if row['type'] in ['double array', 'integer array']:
                elements = ET.SubElement(keyword, 'elements')
                
                for i in range(3):
                    entry = ET.SubElement(elements, 'entry')
                    index = ET.SubElement(entry, 'index')
                    index.text = str(i)
                    label = ET.SubElement(entry, 'label')
                    label.text = 'Element_%d' % i


            if row['units'] != '':
                units = ET.SubElement(keyword, 'units')
                units.text = row['units']

            if row['type'] in ['enumerated', 'boolean']:
               values = ET.SubElement(keyword, 'values')
               
               for value in row['values'].split(','):
                   entry = ET.SubElement(values, 'entry')
                   key = ET.SubElement(entry, 'key')
                   key.text = value.strip().split(':')[0]
                   value_element = ET.SubElement(entry, 'value')
                   value_element.text = value.strip().split(':')[1]
            
            if row['type'] == 'double':
                formats = ET.SubElement(keyword, 'format')
                formats.text = '%.1f'
        tree = ET.ElementTree(root)
        xml_string = ET.tostring(root, encoding='utf-8')

        xml_dom = xml.dom.minidom.parseString(xml_string)
        prettified_xml_string = xml_dom.toprettyxml(indent="\t")

        with open(xml_file_path, 'w') as output_file:
            output_file.write(prettified_xml_string)

csv_file_path = 'keywords.csv'
xml_file_path = 'LFC.xml.sin'

csv_to_xml(csv_file_path, xml_file_path)