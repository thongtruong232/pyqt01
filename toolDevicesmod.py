import os,time
try:
 import threading,subprocess,base64,cv2,random,requests,pyautogui
 import numpy as np
except:
    os.system("pip install pyautogui")
    os.system("pip install Pillow")
    os.system("pip install --force-reinstall --no-cache opencv-python==4.5.5.64")
    os.system("pip install numpy")
    os.system("pip install requests")
    os.system("pip install pyqt6")
    os.system("pip install pyqt6-tools")
import threading,subprocess,base64,cv2,random,hashlib,sys,requests,pyautogui
import numpy as np
from datetime import datetime
from  xml.dom.minidom import parse
import re


def proxy():
    https_proxy = requests.get(f'http://proxy.shoplike.vn/Api/getNewProxy?access_token=198e93ed1c3818afab7fdee82d519d67&location=&provider=')
    if https_proxy.json()["status"] == "error":
        return
    else :
     https_proxyz = https_proxy.json()["data"] 
    yz = https_proxyz["proxy"]
    return yz 
    
def resetServer():
        """
        Reset Server ADB
        """
        subprocess.call("adb kill-server", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(2)
        subprocess.call("adb start-server", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
        time.sleep(3)
def bypass_slide(devices):
    pipe = subprocess.Popen(f'adb -s {devices} exec-out screencap -p',
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, shell=True)
        #image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
    image_bytes = pipe.stdout.read()
    image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
    # img = image[430:765, 102:648] # cắt chỗ có captcha # cut zone captcha
    img = image[360:580, 100:440]
    # img = image[400:1505, 80:1248]
    #cv2.imshow("a", img)
    #cv2.waitKey(0)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    img3 = cv2.Canny(gray, 200, 200, L2gradient=True)
    kernel = np.ones([23,23]) # Tạo kernel
    kernel[2:,2:] = -0.1
    im = cv2.filter2D(img3/255, -1, kernel)
    im1 = im[:,:125]
    y1,x1 = np.argmax(im1)//im1.shape[1], np.argmax(im1)%im1.shape[1] # Tìm vị trí 1 chính xác
    im2 = im[:,125:]
    y2,x2 = np.argmax(im2)//im2.shape[1], np.argmax(im2)%im2.shape[1] + 125 # Tìm vị trí 1 chính xác
    # cv2.rectangle(img, (x1,y1), (x1+50, y1+50), 255, 2)
    # cv2.rectangle(img, (x2,y2), (x2+50, y2+50), 255, 2)
    # plt.imshow(img)
    # plt.show()
    return x2-x1

class Auto:
    def __init__(self,handle):
        self.handle = handle
    def screen_capture(self):
        #os.system(f'adb -s {self.handle} exec-out screencap -p > {name}.png')
        pipe = subprocess.Popen(f'adb -s {self.handle} exec-out screencap -p',
                        stdin=subprocess.PIPE,
                        stdout=subprocess.PIPE, shell=True)
        #image_bytes = pipe.stdout.read().replace(b'\r\n', b'\n')
        image_bytes = pipe.stdout.read()
        image = cv2.imdecode(np.fromstring(image_bytes, np.uint8), cv2.IMREAD_COLOR)
        return image
    def changeProxy(self, ip):
        """
        Input Proxy Http IP:PORT
        Thêm Proxy Http IP:PORT
        """
        subprocess.call(f'adb -s {self.handle} shell settings put global http_proxy {ip}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def remProxy(self):
        """
        Input Proxy Http IP:PORT
        Thêm Proxy Http IP:PORT
        """
        subprocess.call(f'adb -s {self.handle} shell settings put global http_proxy :0', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    def click(self,x,y):
        subprocess.call(f'adb -s {self.handle} shell input tap {x} {y}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def swipe(self, x1, y1, x2, y2):
        subprocess.call(f"adb -s {self.handle} shell input touchscreen swipe {x1} {y1} {x2} {y2} 1000", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def Back(self):
        subprocess.call(f"adb -s {self.handle} shell input keyevent 3", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def DeleteCache(self, package):
        subprocess.check_output(f"adb -s {self.handle} shell pm clear {package}", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def off(self, package):
        subprocess.call(f"adb -s {self.handle} shell am force-stop {package}", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def InputText(self, text=None, VN=None):
        if text == None:
            text =  str(base64.b64encode(VN.encode('utf-8')))[1:]
            subprocess.call(f"adb -s {self.handle} shell ime set com.android.adbkeyboard/.AdbIME", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            subprocess.call(f"adb -s {self.handle} shell am broadcast -a ADB_INPUT_B64 --es msg {text}", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
            return
        subprocess.call(f"adb -s {self.handle} shell input text '{text}'", stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def find(self,img='',threshold=0.99):
        img = cv2.imread(img) #sys.path[0]+"/"+img)
        img2 = self.screen_capture()    
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        #image = cv2.rectangle(img2, retVal[0],(retVal[0][0]+img.shape[0],retVal[0][1]+img.shape[1]), (0,250,0), 2)
        #cv2.imshow("test",image)
        #cv2.waitKey(0)
        #cv2.destroyWindow("test")
        return retVal
    def tapimg(self,img='',tap='',threshold=0.99):
        img = cv2.imread(img) #sys.path[0]+"/"+img)
        tap = cv2.imread(tap)
        img2 = self.screen_capture()    
        result = cv2.matchTemplate(img,img2,cv2.TM_CCOEFF_NORMED)
        loc = np.where(result >= threshold)
        retVal = list(zip(*loc[::-1]))
        result2 = cv2.matchTemplate(img,tap,cv2.TM_CCOEFF_NORMED)
        loc2 = np.where(result2 >= threshold)
        retVal2 = list(zip(*loc2[::-1]))
        if retVal > [(0, 0)]:
            self.click(retVal2[0][0],retVal2[0][1])
        else:
            return 0
    def slideCaptcha(self,x,y):
        # adb.excuteAdb(sr, "adb shell screencap -p /sdcard/cap.png")
        # adb.excuteAdb(sr, f"adb pull /sdcard/cap.png {sr}/captcha.png")
        captcha = bypass_slide(self.handle)
        self.swipe(round(x), round(y), int(x)+int(captcha), round(y))
        return True
    def showDevice(self, width: int, height: int, x:int , y: int, title: str):
        """Hiển thị điện thoại của bạn lên màn hình máy tính"""
        subprocess.Popen(f'scrcpy -s {self.handle} --window-title "{title}" --window-x {x} --window-y {y} --window-width {width} --window-height {height}', stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)
    def DumpXML(self):
        name = self.handle
        if ":" in self.handle:
            name = name.replace(":", "").replace(".", "")
        #print(name)
        os.system(f"adb -s {self.handle} shell uiautomator dump && adb -s {self.handle} pull /sdcard/window_dump.xml {name}.xml")
        return name
    def GetXml(self):
        self.DumpXML()
        with parse(self.handle.replace(":", "").replace(".", "")+".xml") as file:
            node = file.getElementsByTagName("node")
            for element in node:
                text = element.getAttribute("text")
                classname = element.getAttribute("class")
                contentdesc = element.getAttribute("content-desc")
                print(classname, text, contentdesc)

    def TapXml(self, text=None, classname=None, content=None, taps=1, typesearch="text&class"):
        self.DumpXML()
        devices = self.handle
        with parse(devices.replace(":", "").replace(".", "")+".xml") as file:
            node = file.getElementsByTagName("node")
            for element in node:
                name = element.getAttribute("text")
                classnames = element.getAttribute("class")
                contentdesc = element.getAttribute("content-desc")
                x, y = element.getAttribute("bounds").split("][")[0].replace("[", "").split(",")
                if name == text and classnames == classname and typesearch == "text&class" or typesearch == "text&class":
                    print("x:"+x, "y:"+y, "Text:"+name)
                    for tap in range(taps):
                        self.click(x, y)
                elif contentdesc == content and classnames == classname and typesearch == "content&class" or typesearch == "class&content":
                    print("x:"+x, "y:"+y, "Text:"+name)
                    for tap in range(taps):
                        self.Click(x, y)
                elif name == text and contentdesc == content and typesearch == "content&text" or typesearch == "text&content":
                    print("x:"+x, "y:"+y, "Text:"+name)
                    for tap in range(taps):
                        self.Click(x, y)

    resetServer()
def GetDevices():
        devices = subprocess.check_output("adb devices")
        p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached',"")
        if int(len(p)) > 0:
            listDevices = p.split("\\tdevice")
            listDevices.pop()
            return listDevices
        else:
            return 

thread_count = len(GetDevices())


class starts(threading.Thread):
    def __init__(self, nameLD,min_sleep,max_sleep, i):
        super().__init__()
        self.nameLD = nameLD
        self.device = i
        self.min_sleep = min_sleep
        self.max_sleep = max_sleep
    def run(self):
        device = self.device
        d = Auto(device)
        def step1(d):
            n = 0
            while True:
                try: 
                    point = d.find('image\\3.png')
                    n+=1
                    if point > [(0,0)]:
                        d.click(point[0][0],point[0][1])
                        print('Click app')
                        step2(d)
                        break
                    if n == 10:
                        print('C == 10', n)
                        step1(d)
                        break
                except: 
                    print('False')
                    return 0
        def step2(d):
            for n in range(2):
                time.sleep(3)
                print('Sleep 10s step 2')
                d.swipe(675,526,617,57)
                print('Step 2')
                print(n)
            else:
                print("Finally finished!")
        def step3(d):
            point = d.find('image\\4.png')
            if point > [(0,0)]:
                name = open('text\\name.txt').readline()
                print(name)
                d.click(point[0][0],point[0][1])
                print('Click app')
                d.InputText(name)
                sys.exit(0)

        #step3(d)
        

        

#min_sleep = int(input(">> Nhập số min sleep (s): "))
#max_sleep = int(input(">> Nhập số max sleep (s): "))
max_sleep = 5
min_sleep = 1
GetDevices()
def main(m):
        GetDevices()
        device = GetDevices()[m]
        print(device)
        print('ok')
        for i in range(m, 10000, thread_count):
                run = starts(device,min_sleep,max_sleep,device,)
                run.run()
        
def strew():
    """
    pyautogui.doubleClick('image\\1.png')
    print('Double Click')
    time.sleep(2)
    
    pyautogui.click('image\\2.png')
    print('Click')
    time.sleep(40)
    print('Sleep 40s')
    devices = subprocess.check_output("adb devices")
    p = str(devices).replace("b'List of devices attached","").replace('\\r\\n',"").replace(" ","").replace("'","").replace('b*daemonnotrunning.startingitnowonport5037**daemonstartedsuccessfully*Listofdevicesattached',"")
    # Sử dụng regular expression để tìm tất cả các chuỗi có dạng "emulator-xxxx"
    matches = re.findall(r'emulator-\d+', p)
    # In ra các kết quả
    for match in matches:
        print(match)
    """
    
    for m in range(thread_count):
        threading.Thread(target=main, args=(m,)).start()

strew()

        
