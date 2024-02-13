import glob
import random
import os
import sys

val_percent = 0.15
test_percent = 0.05

BASE_PATH = sys.path[0]
print(BASE_PATH)
XML_PATH = os.path.join(BASE_PATH, 'Annotations')
JPG_PATH = os.path.join(BASE_PATH, 'JPEGImages')
TXT_PATH = os.path.join(BASE_PATH, 'ImageSets')

def split(full_list, shuffle=False):
    n_total = len(full_list)
    offset1 = int(n_total * test_percent)
    offset2 = int(n_total * (1 - test_percent - val_percent))
    if n_total == 0:
        return [], full_list
    if shuffle:
        random.shuffle(full_list)

    sublist_1 = full_list[:offset1]
    sublist_2 = full_list[offset1:offset2]
    sublist_3 = full_list[offset2:]
    return sublist_1, sublist_2, sublist_3

def generate_train_and_val():
    file_list = []
    for xml_file in glob.glob(str(os.path.join(XML_PATH,'*.xml'))):
        base_name = os.path.basename(xml_file)
        jpg_file = os.path.join(JPG_PATH, base_name[:-4]+'.png')
        if os.path.exists(jpg_file):
            file_list.append(jpg_file)

    file_list = [''.join([x + '\n']) for x in file_list]

    test, val, train = split(file_list, True)
    with open(os.path.join(TXT_PATH, 'all.txt'), 'w') as tf:
        for t in file_list:
            tf.write(t)
    with open(os.path.join(TXT_PATH, 'train.txt'),'w') as tf:
        for t in train:
            tf.write(t)
    with open(os.path.join(TXT_PATH, 'val.txt'),'w') as tf:
        for t in val:
            tf.write(t)
    with open(os.path.join(TXT_PATH, 'test.txt'),'w') as tf:
        for t in test:
            tf.write(t)

generate_train_and_val()
