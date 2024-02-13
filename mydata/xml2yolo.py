import os
import sys
import glob
import xml.etree.ElementTree as ET


#选择输入路径
BASE_PATH = sys.path[0]
ANNOTATIONS_PATH = os.path.join(BASE_PATH, 'Annotations')
LABELS_PATH = os.path.join(BASE_PATH, 'JPEGImages')

#类名
# classes = ["powdery mildew", "verticillium wilt", "gray mold", "bacterial wilt", "anthracnose", "leaf spot", "red spider", "thrips", "Beet armyworm", "Spodoptera litura"]   # 改成自己的类别
classes = ["defect"]
with open(os.path.join(BASE_PATH, 'classes.names')) as f:
    class_names = f.readlines()
class_names = [x.strip() for x in class_names]
class_count = [0] * len(class_names)

#转换一个xml文件为txt
def single_xml_to_txt(xml_file):
    tree = ET.parse(xml_file)
    root = tree.getroot()
    #保存txt文件路径
    txt_file = os.path.join(LABELS_PATH, os.path.basename(xml_file)[:-4] + '.txt')
    with open(txt_file, 'w') as tf:
        for member in root.findall('object'):
	        #从xml获取图像的宽和高
            picture_width = int(root.find('size')[0].text)
            picture_height = int(root.find('size')[1].text)
            class_name = member[0].text

            #类名对应的index
            class_num = class_names.index(class_name)
            class_count[class_num] += 1
            box_x_min = int(member[4][0].text)  # 左上角横坐标
            box_y_min = int(member[4][1].text)  # 左上角纵坐标
            box_x_max = int(member[4][2].text)  # 右下角横坐标
            box_y_max = int(member[4][3].text)  # 右下角纵坐标

            # 转成相对位置和宽高（所有值处于0~1之间）
            x_center = (box_x_min + box_x_max) / (2 * picture_width)
            y_center = (box_y_min + box_y_max) / (2 * picture_height)
            width = (box_x_max - box_x_min) / picture_width
            height = (box_y_max - box_y_min) / picture_height
            #print(class_num, x_center, y_center, width, height)
            tf.write(str(class_num) + ' ' + str(x_center) + ' ' + str(y_center) + ' ' + str(width) + ' ' + str(
                height) + '\n')


#
with open('classes.names', 'w') as f:
    for c in class_names:
        f.write(c + '\n')

#  转换文件夹下的所有xml文件为txt
for xml_file in glob.glob(str(os.path.join(ANNOTATIONS_PATH, '*.xml'))):
    #print(xml_file)
    try:
        single_xml_to_txt(xml_file)
    except Exception as e:
        print(e, xml_file)


for c, n in zip(class_names, class_count):
    print(c + ':' + str(n))

