import pytesseract as tes
from PIL import Image,ImageOps
import cv2
import matplotlib.pyplot as plt
import urllib.request as ur
import numpy as np
import hashlib
import time
import json

def OCR_local():
    o = cv2.imread(r'C:\Users\Avinash\Desktop\test.jpg')
    print("ORIGINAL IMAGE")
    plt.imshow(o)
    plt.show()
    denoise = cv2.fastNlMeansDenoisingColored(o, None, 10, 10, 7, 15)              
    i = cv2.cvtColor(o, cv2.COLOR_BGR2GRAY)
    ret, bw_img = cv2.threshold(i,127,255,cv2.THRESH_BINARY)
    print("GREYSCALE IMAGE")
    plt.imshow(i)
    plt.show()
    print("BINARY IMAGE")
    plt.imshow(bw_img)
    plt.show()

    result = tes.image_to_string(i,lang='eng')
    print('OUTPUT: ',result)
    return result

def OCR_server():
    f='1'
    while(f=='1'):
        url='http://192.168.137.44:8080/shot.jpg'
        imgResp = ur.urlopen(url)
        imgNp = np.array(bytearray(imgResp.read()),dtype=np.uint8)
        i = cv2.imdecode(imgNp,-1)
        plt.imshow(i)
        plt.show()
        
        text = tes.image_to_string(i,lang='eng')
        img = cv2.fastNlMeansDenoisingColored(i, None, 10, 10, 7, 15)              
        i=cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        result = tes.image_to_string(i,lang='eng')
        print('OUTPUT: ',result)    
        f=input()
        return result

def hashing(result):
    t1 = 'In time: ' + time.asctime(time.localtime())
    hashobj = hashlib.sha384(result.encode()) 
    hash = hashobj.hexdigest()
    print(hash)
    return hash ,t1

def database_manager(f):
    if(f == 's'):result = OCR_server()
    if(f == 'l'):result = OCR_local()
    if(f == 'm'):result = input()
    else:print('Give correct input')
    hash ,t1 = hashing(result)

    file = open(r'C:\Users\Avinash\Documents\codes\mini project\data.json', 'r')
    datadic = json.load(file)
    file.close()
    
    if hash in list(datadic.keys()):
        t2 = 'Out time: ' + time.asctime(time.localtime())
        t1 = datadic[hash]
        print(t1)
        print(t2)
    else:   
        data = {hash:t1}
        datadic.update(data)
        file = open(r'C:\Users\Avinash\Documents\codes\mini project\data.json', 'w')
        json.dump(datadic,file)
        file.close()
    
def main():
    print('press s for server input')
    print('press l for local input')
    print('press m for manual input')
    f = input()
    database_manager(f)

main()