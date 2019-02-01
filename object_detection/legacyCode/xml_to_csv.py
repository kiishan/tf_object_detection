import os
import glob
import pandas as pd
import xml.etree.ElementTree as ET
import sys

path1 = os.path.abspath(os.path.join(os.getcwd(), os.pardir))
path2 = path1+'\\object_detection'
path3 = path1+'\\slim'
sys.path.append(path1)
sys.path.append(path2)
sys.path.append(path3)

def update_xml_path(path):
    xml_files = [file for file in os.listdir(path) if file.endswith('.xml')]
    for file in xml_files:
        file_name = os.path.splitext(file)[0]
        file_path = path+'\\'+file
        tree = ET.parse(file_path)
        tree.find('.//path').text = path+'\\'+file_name+'.jpg'
        tree.write(file_path)

def xml_to_csv(path):
    xml_list = []
    for xml_file in glob.glob(path + '/*.xml'):
        tree = ET.parse(xml_file)
        root = tree.getroot()
        for member in root.findall('object'):
            value = (root.find('filename').text,
                     int(root.find('size')[0].text),
                     int(root.find('size')[1].text),
                     member[0].text,
                     int(member[4][0].text),
                     int(member[4][1].text),
                     int(member[4][2].text),
                     int(member[4][3].text)
                     )
            xml_list.append(value)
    column_name = ['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']
    xml_df = pd.DataFrame(xml_list, columns=column_name)
    return xml_df


def main():
    for folder in ['train','test']:
        image_path = os.path.join(os.getcwd(), ('images\\' + folder))
        update_xml_path(image_path)
        print('Successfully updated path in xml')
        xml_df = xml_to_csv(image_path)
        xml_df.to_csv(('images\\' + folder + '_labels.csv'), index=None)
        print('Successfully converted xml to csv.')

main()
