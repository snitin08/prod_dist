import pytesseract
from pytesseract import Output
import numpy as np
import cv2
import subprocess
from table_detect import table_detect, colfilter, get_text, get_annotations_xlsx, find_table, find_below_table
from pdf2image import convert_from_path,convert_from_bytes


pytesseract.pytesseract.tesseract_cmd = 'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

def process_invoice(filename, templatename):
    images = convert_from_path(filename, size = (901,1200))
    annotate_dict = get_annotations_xlsx(templatename)
    tab_result = list()
    start_of_table = annotate_dict['page 1']['Start Of Table'][1]
    result = get_text(annotate_dict, np.copy(images[0]), 901, 1200)
    flg = False
    below_tab_result = list()
    for image in images:
        image.save('page_1.jpeg', 'JPEG')  
        cmd = 'convert page_1.jpeg -type Grayscale -negate -define morphology:compose=darken -morphology Thinning "Rectangle:1x15+0+0<" -negate page_1-t.jpeg'
        subprocess.call(cmd, shell=True)
        new_img = cv2.imread('page_1-t.jpeg')
        new_img2 = cv2.imread('page_1.jpeg')
        new_img2 = cv2.bilateralFilter(new_img2,5,75,75)
#        print(annotate_dict)
#        print(new_img.shape[0],new_img.shape)
        rgb = np.copy(new_img)
        new_crd = table_detect(rgb)
        NO_OF_COLS = annotate_dict['ncols']
        new_lst = list()
        below_table = list()
        for x in new_crd: 
            if colfilter(x,rgb,NO_OF_COLS,start_of_table) == int(NO_OF_COLS):
                new_lst.append(x)
            elif x[3] > start_of_table:
                below_table.append(x)
            else:
                pass
        tmp3 = np.copy(rgb)
        tab_result += find_table(tmp3, new_img2, new_lst)
        if flg==False:
            below_tab_result = find_below_table(np.copy(new_img2), below_table)
            flg = True
    return result, tab_result, below_tab_result
    

a,b,c = process_invoice('annotate/invoice3b.pdf', 'annotate/invoice3b-new.csv')
#print(new_lst)

print(a)

print(c)

for ele in b:
    for e in ele:
        print(e, end="   ")
    print()