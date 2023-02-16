import ctypes
import time as t
import mouse as mo
from PIL import ImageGrab
from pytesseract import pytesseract
import cv2
import numpy as np

# Define path to tessaract.exe
path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
# Point tessaract_cmd to tessaract.exe
pytesseract.tesseract_cmd = path_to_tesseract
SendInput = ctypes.windll.user32.SendInput

########################################################################################
# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
########################################################################################
#Key direct codes assigned to letters
w = 0x11
a = 0x1E
s = 0x1F
d = 0x20
shift = 0x2A
enter = 0x1C
esc = 0x01
alt = 0x38
tab = 0x0F
e = 0x12
left = 0xCB
right = 0xCD
m = 0x32
down = 0xD0
up = 0xC8
space = 0x39
r = 0x13
pgup=0xC9
kend=0xCF
pgdown=0xD1
#########################
#variable naming rules:
#variables ending with "_p" are  to be predicted
#variables ending with "_a" are actual values got
#variables which dont have a use (used in for loops) are named "unnamedvar" followed by a number
################
#currently there are 22 "unnamed" variables (starting with 0 to 21)in for loop and one named variable (which is of use)
#this code has -23- for loops and -7- while loops including one main loop


# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)


class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


# Actuals Functions
def MouseMoveTo(x: object, y: object) -> object:
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x, y, 0, 0x0001, 0, ctypes.pointer(extra))

    command = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))


def PressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def ReleaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(0, hexKeyCode, 0x0008 | 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def click_down(button):
    if button == "left":
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, 0x0002, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    else:
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, 0x0008, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def click_up(button):
    if button == "left":
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, 0x0004, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))
    else:
        extra = ctypes.c_ulong(0)
        ii_ = Input_I()
        ii_.mi = MouseInput(0, 0, 0, 0x0010, 0, ctypes.pointer(extra))
        x = Input(ctypes.c_ulong(0), ii_)
        ctypes.windll.user32.SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def click(button, duration=0.05):
    if True:
        click_down(button)
        t.sleep(duration)
        click_up(button)


def set_pos(x, y):
    x = 1 + int(x * 65536. / 1920.)
    y = 1 + int(y * 65536. / 1080.)
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.mi = MouseInput(x, y, 0, (0x0001 | 0x8000), 0, ctypes.pointer(extra))
    command = Input(ctypes.c_ulong(0), ii_)
    ctypes.windll.user32.SendInput(1, ctypes.pointer(command), ctypes.sizeof(command))


def imgcheck(im1, im2):
    im1 = cv2.cvtColor(im1, cv2.COLOR_BGR2GRAY)
    im2 = cv2.cvtColor(im2, cv2.COLOR_BGR2GRAY)
    height, width = im1.shape
    diff = cv2.subtract(im1, im2)
    err = np.sum(diff ** 2)
    mse = err / (float(height * width))
    return mse


def becoming_ceo():
    PressKey(m)
    t.sleep(0.2)
    ReleaseKey(m)
    for unnamedvar0 in range(7):
        t.sleep(0.2)
        PressKey(down)
        t.sleep(0.1)
        ReleaseKey(down)
    t.sleep(0.2)
    ss_region = (28, 377, 459, 413)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("sscheck1.jpg")
    securo_serv_check_p = cv2.imread("sscheck.jpg")
    securo_serv_check_a = cv2.imread("sscheck1.jpg")
    if imgcheck(securo_serv_check_p, securo_serv_check_a) < 1:
        for unnamedvar1 in range(2):
            t.sleep(0.2)
            PressKey(enter)
            t.sleep(0.2)
            ReleaseKey(enter)
        t.sleep(1)
        PressKey(m)
        t.sleep(0.2)
        ReleaseKey(m)
        for unnamedvar2 in range(5):
            t.sleep(0.2)
            PressKey(down)
            t.sleep(0.1)
            ReleaseKey(down)
        t.sleep(0.2)
        PressKey(enter)
        t.sleep(0.2)
        ReleaseKey(enter)
        t.sleep(0.2)
        PressKey(down)
        t.sleep(0.1)
        ReleaseKey(down)
        t.sleep(0.2)
        PressKey(enter)
        t.sleep(0.2)
        ReleaseKey(enter)
        t.sleep(0.2)
        PressKey(right)
        t.sleep(0.1)
        ReleaseKey(right)
        for unnamedvar3 in range(3):
            t.sleep(0.1)
            click("right")
    else:
        for unnamedvar4 in range(2):
            PressKey(up)
            t.sleep(0.1)
            ReleaseKey(up)
            t.sleep(0.5)
        PressKey(enter)
        t.sleep(0.2)
        ReleaseKey(enter)
        t.sleep(0.1)
        PressKey(down)
        t.sleep(0.1)
        ReleaseKey(down)
        t.sleep(0.2)
        PressKey(enter)
        t.sleep(0.2)
        ReleaseKey(enter)
        t.sleep(0.2)
        PressKey(right)
        t.sleep(0.1)
        ReleaseKey(right)
        for unnamedvar5 in range(3):
            t.sleep(0.1)
            click("right")


def newsession(tem=0.7):
    for unnamedvar6 in range(4):
        click("right")
        t.sleep(0.5)
    PressKey(esc)
    t.sleep(0.5)
    ReleaseKey(esc)
    t.sleep(1)
    PressKey(right)
    t.sleep(0.1)
    ReleaseKey(right)
    ss_region = (528, 180, 742, 219)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("oncheck1.jpg")
    online_menu_check_p = cv2.imread("oncheck.jpg")
    online_menu_check_a = cv2.imread("oncheck1.jpg")
    if imgcheck(online_menu_check_p, online_menu_check_a) < 5.5:
        t.sleep(3)
        PressKey(enter)
        t.sleep(0.1)
        ReleaseKey(enter)
        t.sleep(2)
        for unnamedvar7 in range(4):
            PressKey(up)
            t.sleep(0.1)
            ReleaseKey(up)
            t.sleep(tem)
        PressKey(enter)
        t.sleep(0.1)
        ReleaseKey(enter)
        t.sleep(1)
        PressKey(down)
        t.sleep(0.1)
        ReleaseKey(down)
        t.sleep(0.1)
        PressKey(enter)
        t.sleep(0.5)
        ReleaseKey(enter)
        t.sleep(2)
        PressKey(enter)
        t.sleep(0.5)
        ReleaseKey(enter)
        set_pos(686, 620)
        t.sleep(16)
        t.sleep(4)

    else:
        t.sleep(0.3)
        for unnamedvar8 in range(4):
            PressKey(right)
            t.sleep(0.1)
            ReleaseKey(right)
            t.sleep(0.3)
        t.sleep(3)
        PressKey(enter)
        t.sleep(0.1)
        ReleaseKey(enter)
        t.sleep(2.5)
        PressKey(up)
        t.sleep(0.1)
        ReleaseKey(up)
        t.sleep(0.1)
        PressKey(enter)
        t.sleep(0.1)
        ReleaseKey(enter)
        t.sleep(1)
        PressKey(down)
        t.sleep(0.1)
        ReleaseKey(down)
        t.sleep(0.1)
        PressKey(enter)
        t.sleep(0.5)
        ReleaseKey(enter)
        t.sleep(1.5)
        PressKey(enter)
        t.sleep(0.5)
        ReleaseKey(enter)
        t.sleep(55)
        ss_region = (433, 267, 1540, 855)
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save("onscheck1.jpg")
        alert_return_togtav_onlinecheck_p = cv2.imread("onscheck.jpg")
        alert_return_togtav_onlinecheck_a = cv2.imread("onscheck1.jpg")
        if imgcheck(alert_return_togtav_onlinecheck_p, alert_return_togtav_onlinecheck_a) < 1:
            PressKey(enter)
            t.sleep(0.5)
            ReleaseKey(enter)
            t.sleep(30)
            newsession()

        #else:
            #becoming_ceo()
def depositmoney():
    PressKey(up)
    t.sleep(0.1)
    ReleaseKey(up)
    t.sleep(0.8)
    PressKey(down)
    t.sleep(0.1)
    ReleaseKey(down)
    t.sleep(0.6)
    PressKey(enter)
    t.sleep(0.1)
    ReleaseKey(enter)
    t.sleep(1.2)
    set_pos(968,414)
    t.sleep(0.2)
    click("left")
    t.sleep(0.6)
    PressKey(pgdown)
    t.sleep(0.8)
    ReleaseKey(pgdown)
    set_pos(635, 903)
    t.sleep(0.2)
    click("left")
    t.sleep(0.6)
    set_pos(908, 715)
    t.sleep(0.2)
    click("left")
    t.sleep(0.6)
    set_pos(912, 535)
    t.sleep(0.2)
    click("left")
    t.sleep(2)
    set_pos(1108,764)
    t.sleep(0.2)
    click("left")
    t.sleep(2)
    set_pos(697,710)
    t.sleep(0.2)
    click("left")
    t.sleep(2)
    for unnamedvar23 in range(10):
        click("right",duration=0.3)
        t.sleep(0.6)
    deposit=0
PressKey(alt)
t.sleep(0.5)
# CHANGING WINDOW
set_pos(686, 620)
PressKey(tab)
ReleaseKey(tab)
ReleaseKey(alt)
deposit=0
while True:

    t.sleep(1)
    #if deposit==1:
        #depositmoney()
    t.sleep(2)

    ss_region = (27, 870, 298, 1043)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("ST.jpg")
    starting_map_kostaka_p = cv2.imread('startingc.jpg')
    starting_map_kostaka_a = cv2.imread('ST.jpg')
    while (imgcheck(starting_map_kostaka_p, starting_map_kostaka_a)) > 16:
        newsession()
        ss_region = (27, 870, 298, 1043)
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save("ST.jpg")
        starting_map_kostaka_a = cv2.imread('ST.jpg')

    MouseMoveTo(1, 0)
    #depositmoney()
    becoming_ceo()
    # First right beside bed
    MouseMoveTo(1200, 0)
    # MouseMoveTo(2450,0)
    t.sleep(0.5)
    PressKey(w)
    t.sleep(4.71)
    # FIRST LEFT BELOW STAIRS
    MouseMoveTo(-1450, 0)
    t.sleep(3.2)
    # fIRST LEFT BESIDE STAIRS
    MouseMoveTo(-1640, 0)
    t.sleep(0.9)
    # FIRST LEFT AT STAIRS
    MouseMoveTo(-1600, 0)
    t.sleep(4.7)
    # FIRST LEFT AT UPSTAIRS
    MouseMoveTo(-1500, 0)
    t.sleep(1)
    # SECOND LEFT AT UPSTAIRS
    MouseMoveTo(-1500, 0)
    t.sleep(3.85)
    # FIRST LEFT UP STAIRS BEHIND
    MouseMoveTo(-1680, 0)
    t.sleep(6.5)
    # FIRST LEFT BESIDE SCREEN
    MouseMoveTo(-1700, 0)
    t.sleep(1.2)
    click("right")
    t.sleep(0.2)
    # Firt left at screen
    MouseMoveTo(-1700, 0)
    t.sleep(0.2)
    ReleaseKey(w)
    #depositmoney()
    #t.sleep(1)
    t.sleep(0.5)

    PressKey(e)
    t.sleep(1)
    ReleaseKey(e)
    t.sleep(5.5)
    ss_region = (129, 54, 666, 104)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("fcheck0.jpg")
    heist_board_p = cv2.imread('fcheck1.jpg')
    heist_board_a = cv2.imread('fcheck0.jpg')
    #change it to 27
    if (imgcheck(heist_board_p, heist_board_a)) > 40:
        newsession()
        continue
    # navigating to finale
    for unnamedvar9 in range(2):
        t.sleep(0.2)
        PressKey(e)
        t.sleep(0.2)
        ReleaseKey(e)
    # navigating to start
    PressKey(right)
    t.sleep(0.2)
    ReleaseKey(right)
    PressKey(enter)
    t.sleep(0.2)
    ReleaseKey(enter)
    t.sleep(8)
    # confirm at green screen
    PressKey(w)
    t.sleep(0.1)
    ReleaseKey(w)
    PressKey(enter)
    t.sleep(0.2)
    ReleaseKey(enter)
    t.sleep(2)
    # start at green screen
    PressKey(w)
    t.sleep(0.1)
    ReleaseKey(w)
    PressKey(enter)
    t.sleep(0.1)
    ReleaseKey(enter)
    t.sleep(1)
    # confirm at black screen
    PressKey(enter)
    t.sleep(0.2)
    ReleaseKey(enter)
    t.sleep(5)
    # approach vehicle
    for unnamedvar10 in range(2):
        t.sleep(0.2)
        PressKey(enter)
        t.sleep(0.2)
        ReleaseKey(enter)
    t.sleep(0.2)
    PressKey(esc)
    t.sleep(0.2)
    ReleaseKey(esc)
    # infiltration point
    t.sleep(0.2)
    PressKey(s)
    t.sleep(0.2)
    ReleaseKey(s)
    t.sleep(0.2)
    PressKey(enter)
    t.sleep(0.2)
    ReleaseKey(enter)
    t.sleep(0.2)
    PressKey(w)
    t.sleep(0.2)
    ReleaseKey(w)
    t.sleep(0.2)
    PressKey(enter)
    t.sleep(0.2)
    ReleaseKey(enter)
    t.sleep(0.2)
    PressKey(esc)
    t.sleep(0.2)
    ReleaseKey(esc)
    t.sleep(0.2)
    # compound entry point
    t.sleep(0.2)
    PressKey(s)
    t.sleep(0.2)
    ReleaseKey(s)
    for unnamedvar11 in range(2):
        t.sleep(0.2)
        PressKey(enter)
        t.sleep(0.2)
        ReleaseKey(enter)
    t.sleep(0.2)
    PressKey(esc)
    t.sleep(0.2)
    ReleaseKey(esc)
    # escape point
    t.sleep(0.2)
    PressKey(s)
    t.sleep(0.2)
    ReleaseKey(s)
    t.sleep(0.2)
    PressKey(enter)
    t.sleep(0.2)
    ReleaseKey(enter)
    t.sleep(0.2)
    PressKey(w)
    t.sleep(0.2)
    ReleaseKey(w)
    t.sleep(0.2)
    PressKey(enter)
    t.sleep(0.2)
    ReleaseKey(enter)
    t.sleep(0.2)
    PressKey(esc)
    t.sleep(0.2)
    ReleaseKey(esc)
    # time of day
    t.sleep(0.2)
    PressKey(s)
    t.sleep(0.2)
    ReleaseKey(s)
    t.sleep(0.2)
    PressKey(enter)
    t.sleep(0.2)
    ReleaseKey(enter)
    t.sleep(0.2)
    PressKey(w)
    t.sleep(0.2)
    ReleaseKey(w)
    t.sleep(0.2)
    PressKey(enter)
    t.sleep(0.2)
    ReleaseKey(enter)
    t.sleep(0.2)
    PressKey(esc)
    t.sleep(0.2)
    ReleaseKey(esc)
    t.sleep(0.1)
    # SUPPRESSOR
    PressKey(down)
    t.sleep(0.1)
    ReleaseKey(down)
    PressKey(enter)
    t.sleep(0.2)
    ReleaseKey(enter)
    t.sleep(0.2)
    PressKey(down)
    t.sleep(0.1)
    ReleaseKey(down)
    for unnamedvar12 in range(2):
        PressKey(enter)
        t.sleep(0.2)
        ReleaseKey(enter)
        t.sleep(0.2)
    PressKey(esc)
    t.sleep(0.2)
    ReleaseKey(esc)
    t.sleep(0.1)
    # continue heist
    t.sleep(0.2)
    PressKey(d)
    t.sleep(0.2)
    ReleaseKey(d)
    t.sleep(0.2)
    PressKey(enter)
    t.sleep(0.2)
    ReleaseKey(enter)
    t.sleep(0.2)
    PressKey(enter)
    t.sleep(0.2)
    ReleaseKey(enter)
    # skipping cutscene
    t.sleep(1)
    PressKey(enter)
    t.sleep(0.2)
    ReleaseKey(enter)
    # unskippable cutscene
    ss_region = (433, 267, 1540, 855)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("scheck1.jpg")
    alert_return_togtav_p = cv2.imread('scheck.jpg')
    alert_return_togtav_a = cv2.imread('scheck1.jpg')
    ss_region = (86, 898, 307, 970)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save('wowzer.jpg')
    heist_swim_started_p = cv2.imread('wow.jpg')
    heist_swim_started_a = cv2.imread('wowzer.jpg')
    errors = 0
    start = t.time()
    end = t.time()
    while (imgcheck(heist_swim_started_p, heist_swim_started_a) > 1.69) and (end - start) < 50:
        end = t.time()
        print(imgcheck(heist_swim_started_p, heist_swim_started_a))
        ss_region = (86, 898, 307, 970)
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save('wowzer.jpg')
        heist_swim_started_a = cv2.imread('wowzer.jpg')
        ss_region = (433, 267, 1540, 855)
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save("scheck1.jpg")
        alert_return_togtav_a = cv2.imread('scheck1.jpg')
        if imgcheck(alert_return_togtav_p, alert_return_togtav_a) == 0:
            errors = 1
            break
    if (end - start) >98:
        newsession()
        continue
    if errors == 1:
        PressKey(enter)
        t.sleep(0.5)
        ReleaseKey(enter)
        t.sleep(30)
        newsession()
        continue
    t.sleep(12)
    # pehel 18.5 tha change kiye abhi 28/12/2022

    # swimming in sea first

    """PressKey(s)
    t.sleep(10)
    ReleaseKey(s)
    MouseMoveTo(-216, 0)
    PressKey(w)
    t.sleep(63.28)
    PressKey(space)
    t.sleep(1)
    ss_region = (241, 361, 1402, 811)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("lrcheck1.jpg")
    ReleaseKey(space)
    lrcheck=cv2.imread("lrcheck.jpg")
    lrcheck1 = cv2.imread("lrcheck1.jpg")
    if imgcheck(lrcheck,lrcheck1)>15:
        print("right janaa")
        PressKey(d)
        t.sleep(0.5)
        ReleaseKey(d)
        t.sleep(0.5)
        ReleaseKey(w)
        t.sleep(0.1)
        ReleaseKey(shift)
        t.sleep(0.1)
        PressKey(s)
        t.sleep(0.5)
        ReleaseKey(s)
        PressKey(shift)
        t.sleep(5)
        PressKey(d)
        t.sleep(0.2)
        ReleaseKey(d)
    elif imgcheck(lrcheck,lrcheck1)<15:
        print("left janaa")
        PressKey(a)
        t.sleep(0.5)
        ReleaseKey(a)
        t.sleep(0.5)
        ReleaseKey(w)
        t.sleep(0.1)
        ReleaseKey(shift)
        t.sleep(0.1)
        PressKey(s)
        t.sleep(0.5)
        ReleaseKey(s)
        PressKey(shift)
        t.sleep(5)
        PressKey(a)
        t.sleep(0.2)
        ReleaseKey(a)"""
    MouseMoveTo(60,13)
    PressKey(shift)
    t.sleep(24)
    PressKey(s)
    t.sleep(0.63)
    ReleaseKey(s)
    t.sleep(0.6)

    # PressKey(w)W
    t.sleep(0.1)
    # ReleaseKey(w)
    t.sleep(5.4)

    # PressKey(w)
    # eReleaseKey(w)
    ss_region = (324, 292, 1370, 652)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("dcheck1.jpg")
    swim_pos_1_p = cv2.imread("dcheck.jpg")
    swim_pos_1_a = cv2.imread("dcheck1.jpg")
    """if imgcheck(swim_pos_1_p, swim_pos_1_a) > 7.2:"""
    print("swim_pos_1 done")
    MouseMoveTo(-120, 11)

    for unnamedvar13 in range(2):
        PressKey(w)
        t.sleep(0.20)
        ReleaseKey(w)
        t.sleep(2)
    ss_region = (139, 0, 1132, 395)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("ycheck2.jpg")
    swim_pos_2_p = cv2.imread('ycheck1.jpg')
    swim_pos_2_a = cv2.imread('ycheck2.jpg')
    if imgcheck(swim_pos_2_p, swim_pos_2_a) < 6:
        print("swim_pos_2 done")
        PressKey(w)
        t.sleep(0.21)
        ReleaseKey(w)
        t.sleep(2)
    else:
        t.sleep(2.95)
        MouseMoveTo(0, -106)
    """t.sleep(2.95)
    MouseMoveTo(0, -106)"""
    MouseMoveTo(-28, 106)
    PressKey(w)
    t.sleep(0.28)
    ReleaseKey(w)
    MouseMoveTo(-25, -120)
    ss_region = (474, 19, 1237, 887)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("check-3.jpg")
    swim_pos_3_p = cv2.imread("check-2.jpg")
    swim_pos_3_a = cv2.imread("check-3.jpg")
    #if imgcheck(swim_pos_3_p, swim_pos_3_a) < 15.6:
    print("swim_pos_3 done")
    t.sleep(0.5  )
    # t.sleep(0.5)
    for unnamedvar14 in range(2):
        PressKey(a)
        t.sleep(0.18)
        ReleaseKey(a)
        t.sleep(0.25)
        PressKey(w)
        t.sleep(1.2)
        ReleaseKey(w)
        t.sleep(2)

    """else:
        for unnamedvar15 in range(2):
            MouseMoveTo(-33, 0)
            t.sleep(0.5)
            PressKey(w)
            t.sleep(0.6)
            ReleaseKey(w)
            t.sleep(0.5)
        t.sleep(3)
        PressKey(a)
        t.sleep(0.2)
        ReleaseKey(a)
        t.sleep(3)"""


    """else:
        t.sleep(4.48)
        PressKey(w)
        t.sleep(0.24)
        ReleaseKey(w)
        t.sleep(2)
        MouseMoveTo(-48, 76)
        PressKey(w)
        t.sleep(0.1)
        ReleaseKey(w)
        MouseMoveTo(-35, -20)
        t.sleep(2.5)
        t.sleep(0.5)
        for unnamedvar16 in range(2):
            PressKey(a)
            t.sleep(0.25)
            ReleaseKey(a)
            t.sleep(0.00005)
            PressKey(s)
            t.sleep(0.85)
            ReleaseKey(s)
            t.sleep(2)"""
    t.sleep(3)
    ReleaseKey(shift)

    # PressKey(shift)we
    # t.sleep(8)
    # PressKey(d)
    # t.sleep(0.6)
    # ReleaseKey(d)
    # t.sleep(7)
    # ReleaseKey(shift)
    # cutting grates
    t.sleep(0.2)
    PressKey(e)
    t.sleep(0.2)
    ReleaseKey(e)
    t.sleep(10)
    ss_region = (28, 17, 203, 45)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("check1.jpg")
    cutting_grate_reached_p = cv2.imread('check.jpg')
    cutting_grate_reached_a = cv2.imread('check1.jpg')
    if (imgcheck(cutting_grate_reached_p, cutting_grate_reached_a)) > 3.5:
        newsession(tem=1.3)
        continue
    mo.press()
    for unnamedvar17 in range(4):
        PressKey(d)
        t.sleep(1.3)
        ReleaseKey(d)
        t.sleep(0.2)
        PressKey(s)
        t.sleep(1.7)
        ReleaseKey(s)
        t.sleep(0.2)
        PressKey(a)
        t.sleep(1.3)
        ReleaseKey(a)
        t.sleep(0.2)
        PressKey(w)
        t.sleep(1.6)
        ReleaseKey(w)
    mo.release()
    # swimming in tunnel
    PressKey(shift)
    t.sleep(17)
    ReleaseKey(shift)
    t.sleep(0.2)
    PressKey(e)
    t.sleep(0.5)
    ReleaseKey(e)
    """ss_region = (27,870,298,1043)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save('map1.jpg')
    map=cv2.imread('map.jpg')
    map1=cv2.imread('map1.jpg')"""
    ss_region = (113, 872, 297, 996)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("nnmap1.jpg")

    surface_reached_map_p = cv2.imread('nnmap.jpg')
    surface_reached_map_a = cv2.imread('nnmap1.jpg')
    start = t.time()
    end = t.time()
    t.sleep(33)

    while (imgcheck(surface_reached_map_p, surface_reached_map_a)) > 2.5:
        print(imgcheck(surface_reached_map_p, surface_reached_map_a))
        end = t.time()
        if (end - start) >= 250:
            errors = 1
            break

        ss_region = (113, 872, 297, 996)
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save("nnmap1.jpg")
        surface_reached_map_a = cv2.imread('nnmap1.jpg')
        ss_region = (30, 16, 449, 89)
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save("nsscheck1.jpg")
        error_launching_job_p = cv2.imread('nsscheck.jpg')
        error_launching_job_a = cv2.imread('nsscheck1.jpg')
        if imgcheck(error_launching_job_p, error_launching_job_a) < 2.8:
            errors = 1
            break
    if errors == 1:
        newsession(tem=1)
        continue
    # moving after tunnel (turn around)
    MouseMoveTo(3200, 0)
    t.sleep(0.1)
    PressKey(w)
    t.sleep(8)
    # slight mouse right
    MouseMoveTo(110, 0)
    t.sleep(3)
    MouseMoveTo(1700, 0)
    t.sleep(2.6)
    MouseMoveTo(-1700, 0)
    t.sleep(6)

    MouseMoveTo(1700, 0)
    t.sleep(4.75)
    MouseMoveTo(-110, 0)
    t.sleep(4.75)
    MouseMoveTo(-110, 0)
    t.sleep(4.75)
    MouseMoveTo(-110, 0)
    t.sleep(4.75)
    MouseMoveTo(1500, 0)
    t.sleep(2.81)
    MouseMoveTo(-1550, 0)
    t.sleep(9)
    MouseMoveTo(1500, 0)
    t.sleep(3.6)
    MouseMoveTo(-1600, 0)
    t.sleep(4)
    ReleaseKey(w)
    MouseMoveTo(-1600, 0)
    """ PressKey(w)
    t.sleep(0.425)
    ReleaseKey(w)"""
    MouseMoveTo(1350, 0)
    PressKey(shift)
    PressKey(w)
    t.sleep(2)
    MouseMoveTo(-1600, 0)
    t.sleep(0.1)

    t.sleep(2.9)
    MouseMoveTo(-1300, 0)

    t.sleep(3)

    MouseMoveTo(1500, 0)
    t.sleep(8)
    ReleaseKey(shift)
    t.sleep(0.5)
    MouseMoveTo(1500, 0)
    t.sleep(4.18)
    ReleaseKey(w)


    PressKey(tab)
    t.sleep(0.1)
    ReleaseKey(tab)
    t.sleep(0.3)
    MouseMoveTo(826, -200)
    t.sleep(0.5)
    click_down("right")
    t.sleep(1)
    click("left", duration=0.1)
    t.sleep(0.1)
    click_up("right")
    t.sleep(0.3)
    PressKey(r)
    t.sleep(0.3)
    ReleaseKey(r)
    t.sleep(1)
    PressKey(tab)
    t.sleep(0.1)
    ReleaseKey(tab)
    t.sleep(2)
    # MouseMoveTo(1600, -150)
    MouseMoveTo(-850, 0)
    PressKey(w)
    t.sleep(2)
    MouseMoveTo(1600, 0)
    t.sleep(4.5)
    MouseMoveTo(1590, 0)
    t.sleep(8)
    MouseMoveTo(-1500, 0)
    t.sleep(3.35)
    ReleaseKey(w)
    MouseMoveTo(-1, 0)
    t.sleep(2)
    t.sleep(0.1)
    PressKey(tab)
    t.sleep(0.1)
    ReleaseKey(tab)
    t.sleep(2)
    # t.sleep(4)
    # PressKey(shift)
    PressKey(w)
    # t.sleep(1.9)
    t.sleep(2.9)
    t.sleep(1)

    ReleaseKey(w)
    MouseMoveTo(100,0)
    t.sleep(0.5)
    PressKey(r)
    t.sleep(0.3)
    ReleaseKey(r)
    t.sleep(0.1)
    # ReleaseKey(shift)
    t.sleep(0.2)

    """PressKey(tab)
    t.sleep(0.1)
    ReleaseKey(tab)"""

    """ PressKey(tab)
    t.sleep(0.1 )
    ReleaseKey(tab)
    t.sleep(0.2)
    MouseMoveTo(58, -150)w
    t.sleep(0.2)
    click_down("right")
    t.sleep(10)
    click("left",duration=0.1)
    t.sleep(0.5)
    click_up("right")
    PressKey(tab)
    t.sleep(0.1)
    ReleaseKey(tab)"""
    t.sleep(2)
    PressKey(shift)
    PressKey(w)
    MouseMoveTo(-2300, 0)

    t.sleep(3.6)
    ReleaseKey(w)
    ReleaseKey(shift)
    t.sleep(1)
    MouseMoveTo(-1100, 0)
    t.sleep(0.8)
    PressKey(w)
    t.sleep(5.8)
    # t.sleep(2)
    MouseMoveTo(-1700, 0)
    t.sleep(2.5)
    MouseMoveTo(-1100, 0)
    PressKey(shift)
    t.sleep(0.99)
    ReleaseKey(shift)
    ReleaseKey(w)
    t.sleep(1)
    PressKey(e)
    t.sleep(0.2)
    ReleaseKey(e)
    start = t.time()
    end = t.time()
    ss_region = (501, 96, 734, 119)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("co1.jpg")
    fgp_hax_p = cv2.imread("co.jpg")
    fgp_hax_a = cv2.imread("co1.jpg")
    while imgcheck(fgp_hax_p, fgp_hax_a) > 7:
        fgp_hax_a = cv2.imread("co1.jpg")
        ss_region = (501, 96, 734, 119)
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save("co1.jpg")
        end = t.time()
        if (end - start)>8.5:
            errors=1
            break
    if errors==1:
        newsession()
        t.sleep(7.2)
        continue
    t.sleep(1)66666
    while imgcheck(fgp_hax_p, fgp_hax_a) < 7:
        ss_region = (980,354,1440,416)
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save("crfp.jpg")
        fst_fgp_p = cv2.imread("crfp.jpg")
        x1 = 386
        x2 = 846
        y1 = 355
        y2 = 417
        for unnamedvar18 in range(8):
            PressKey(down)
            t.sleep(0.03)
            ReleaseKey(down)
            ss_region = (x1, y1, x2, y2)
            ss_img = ImageGrab.grab(ss_region)
            ss_img.save("heh1.jpg")
            fgp_a = cv2.imread("heh1.jpg")
            leasterror = 100.1862
            listoferrorfgp = []
            # while (imgcheck(map,map1))>22:
            for unnamedvar19 in range(9):
                PressKey(up)
                t.sleep(0.03)
                ReleaseKey(up)
                #t.sleep(0.1)
                #t.sleep(0.1)
                PressKey(right)
                t.sleep(0.03)
                ReleaseKey(right)
                # t.sleep(0.1)6
                PressKey(down)
                t.sleep(0.03)
                ReleaseKey(down)
                # t.sleep(0.2)
                ss_region = (x1, y1, x2, y2)
                ss_img = ImageGrab.grab(ss_region)
                ss_img.save(f"heh1{unnamedvar19}.jpg")
                fgp_a = cv2.imread(f"heh1{unnamedvar19}.jpg")
                fst_fgp_p = cv2.imread("crfp.jpg")
                if leasterror > imgcheck(fst_fgp_p, fgp_a):
                    leasterror = imgcheck(fst_fgp_p, fgp_a)
                listoferrorfgp.append(imgcheck(fst_fgp_p, fgp_a))
            print(listoferrorfgp)
            listoferrorfgp = sorted(listoferrorfgp)
            while imgcheck(fst_fgp_p, fgp_a) != listoferrorfgp[-1]:
                PressKey(up)
                t.sleep(0.03)
                ReleaseKey(up)
                # t.sleep(0.1)
                # t.sleep(0.1)w
                PressKey(right)
                t.sleep(0.03)
                ReleaseKey(right)
                # t.sleep(0.1)
                PressKey(down)
                t.sleep(0.03)
                ReleaseKey(down)
                # t.sleep(0.2)
                ss_region = (x1, y1, x2, y2)
                ss_img = ImageGrab.grab(ss_region)
                ss_img.save("fgplowcheck.jpg")
                fgp_a = cv2.imread("fgplowcheck.jpg")
                fst_fgp_p = cv2.imread("crfp.jpg")

            y1 += 76
            y2 += 76
            #PressKey(down)
            #t.sleep(0.1)
            #ReleaseKey(down)
        PressKey(down)
        t.sleep(0.03)
        ReleaseKey(down)
        for num_of_rights in range(7):
            for unnamedvar20 in range(num_of_rights + 1):
                # t.sleep(0.1)
                PressKey(right)
                t.sleep(0.03)
                ReleaseKey(right)
                t.sleep(0.03)
            # t.sleep(0.1)
            PressKey(down)
            t.sleep(0.03)
            ReleaseKey(down)
        t.sleep(0.1)
        # if_wrong_lowest_value

        ss_region = (830, 492, 1099, 528)
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save("processing_fgp_a.jpg")
        processing_fgp_p = cv2.imread("processing_fgp_p.jpg")
        processing_fgp_a = cv2.imread("processing_fgp_a.jpg")
        counter = 0
        while imgcheck(processing_fgp_p, processing_fgp_a) > 10 and counter <= 5:
            for unnamedvar21 in range(8):
                # t.sleep(0.03)
                PressKey(right)
                t.sleep(0.03)
                ReleaseKey(right)
                # t.sleep(0.03)
                PressKey(down)
                t.sleep(0.03)
                ReleaseKey(down)
                ss_region = (830, 492, 1099, 528)
                ss_img = ImageGrab.grab(ss_region)
                ss_img.save("processing_fgp_a.jpg")
                processing_fgp_p = cv2.imread("processing_fgp_p.jpg")
                processing_fgp_a = cv2.imread("processing_fgp_a.jpg")
                if imgcheck(processing_fgp_p, processing_fgp_a) < 10:
                    break
            counter += 1
            ss_region = (830, 492, 1099, 528)
            ss_img = ImageGrab.grab(ss_region)
            ss_img.save("processing_fgp_a.jpg")
            processing_fgp_p = cv2.imread("processing_fgp_p.jpg")
            processing_fgp_a = cv2.imread("processing_fgp_a.jpg")
        if counter == 5:
            continue
        #PressKey(down)
        #t.sleep(0.03)
        #ReleaseKey(down)
        #PressKey(right)
        #t.sleep(0.03)
        #ReleaseKey(right)
        # t.sleep(0.03)
        t.sleep(5.6)
        ss_region = (501, 96, 734, 119)
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save("co1.jpg")
        fgp_hax_p = cv2.imread("co.jpg")
        fgp_hax_a = cv2.imread("co1.jpg")

    t.sleep(9)
    # MouseMoveTo(600, 0)
    PressKey(d)
    t.sleep(1)
    ReleaseKey(d)
    t.sleep(0.1)
    PressKey(a)
    t.sleep(1)
    ReleaseKey(a)
    t.sleep(0.1)
    PressKey(w)
    t.sleep(2)
    ReleaseKey(w)
    t.sleep(0.1)
    PressKey(e)
    t.sleep(0.4)
    ReleaseKey(e)
    t.sleep(5)
    MouseMoveTo(200, 0)
    t.sleep(0.1)
    PressKey(w)
    t.sleep(3.2)
    MouseMoveTo(-325, 0)
    t.sleep(3.8)
    ReleaseKey(w)
    t.sleep(0.1)
    PressKey(e)
    t.sleep(1)
    ReleaseKey(e)
    t.sleep(9)
    PressKey(d)
    t.sleep(0.9)
    ReleaseKey(d)
    t.sleep(0.1)
    """PressKey(a)
    t.sleep(0.6)
    ReleaseKey(a)
    t.sleep(0.1)"""
    PressKey(w)
    t.sleep(1)
    MouseMoveTo(-329,0)
    t.sleep(2)
    ReleaseKey(w)
    t.sleep(0.1)
    PressKey(e)
    t.sleep(0.3)
    ReleaseKey(e)
    t.sleep(4.8)
    for unnamedvar22 in range(5):
        PressKey(pgup)
        t.sleep(2.3)
        ReleaseKey(pgup)
        t.sleep(2)
    t.sleep(1.9)
    MouseMoveTo(2600,0)
    t.sleep(0.1)
    #for unnamedvar23 in range(4):
    PressKey(w)
    t.sleep(5.5)
    MouseMoveTo(-150, 0)
    t.sleep(1)
    MouseMoveTo(-350, 0)
    t.sleep(1.5)
    #MouseMoveTo(-100,0)
    ReleaseKey(w)
    t.sleep(0.1)
    PressKey(e)
    t.sleep(1)
    ReleaseKey(e)
    t.sleep(4)
    PressKey(shift)
    PressKey(w)
    t.sleep(1.2)
    # first right to door
    MouseMoveTo(1600, 0)
    t.sleep(2.3)
    # first right out of door
    MouseMoveTo(1400, 0)
    t.sleep(3.7)
    # first right near flower pot
    MouseMoveTo(1500, 0)
    t.sleep(3.2)
    # first right near dead body of office guard
    MouseMoveTo(1490, 0)
    t.sleep(3.4)
    # first right at  second flower pot
    MouseMoveTo(1300, 0)
    t.sleep(3.4)
    # first right at office stairs bodygurad
    MouseMoveTo(1380, 0)
    t.sleep(3.2)
    # first jump near first steel gate
    PressKey(space)
    t.sleep(0.3)
    ReleaseKey(space)
    #running after jump 1
    t.sleep(1)
    t.sleep(1)
    # first jump near first steel gate
    PressKey(space)
    t.sleep(0.5)
    ReleaseKey(space)
    # running after jump 2
    t.sleep(1)
    MouseMoveTo(-1600, 0)
    t.sleep(1.8)
    ReleaseKey(w)
    ReleaseKey(shift)
    t.sleep(22)
    PressKey(w)
    PressKey(shift)
    t.sleep(3.3)
    MouseMoveTo(-1600, 0)
    click("left",duration=0.5)
    PressKey(e)
    t.sleep(1)
    ReleaseKey(e)

    """# first left near second steel gate
    MouseMoveTo(-1300, 0)
    t.sleep(4)
    # second left near  second steel gate
    MouseMoveTo(-1300, 0)
    t.sleep(3.7)
    # first left near first steel gate
    MouseMoveTo(-1500, 0)
    t.sleep(2.5)
    # second right near first steel gate
    MouseMoveTo(1500, 0)
    t.sleep(2.8)
    MouseMoveTo(-1100, 0)
    t.sleep(4)"""
    ReleaseKey(w)
    ReleaseKey(shift)
    t.sleep(25)
    #t.sleep(2)
    PressKey(w)
    PressKey(shift)
    MouseMoveTo(1600,0)
    t.sleep(11)
    MouseMoveTo(1630, 0)
    t.sleep(14)
    PressKey(space)
    t.sleep(0.5)
    ReleaseKey(space)
    t.sleep(5)
    MouseMoveTo(500, 0)
    t.sleep(15)
    MouseMoveTo(300,0)
    ss_region = (40, 62, 1859, 910)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("heist_passed_a.jpg")
    heist_passed_p = cv2.imread("heist_passed_p.jpg")
    heist_passed_a = cv2.imread("heist_passed_a.jpg")
    start = t.time()
    end = t.time()
    while imgcheck(heist_passed_a, heist_passed_p) > 5:
        end=t.time()
        ss_region = (40, 62, 1859, 910)
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save(f"heist_passed_a.jpg")
        heist_passed_p = cv2.imread("heist_passed_p.jpg")
        heist_passed_a = cv2.imread(f"heist_passed_a.jpg")
        if (end-start)>235:
            errors=1
            break
    if errors==1:
        ReleaseKey(w)
        ReleaseKey(shift)
        newsession()
        t.sleep(4)
        continue
    ss_region = (40, 62, 1859, 910)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("heist_passed1_a.jpg")
    heist_passed_p = cv2.imread("heist_passed1_p.jpg")
    heist_passed_a = cv2.imread("heist_passed1_a.jpg")

    while imgcheck(heist_passed_p, heist_passed_a) > 5:
        ss_region = (40, 62, 1859, 910)
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save(f"heist_passed1_a.jpg")
        heist_passed_p = cv2.imread("heist_passed1_p.jpg")
        heist_passed_a = cv2.imread(f"heist_passed1_a.jpg")
    ReleaseKey(w)
    ReleaseKey(shift)
    PressKey(alt)
    t.sleep(0.1)
    PressKey(tab)
    t.sleep(0.2)
    ReleaseKey(alt)
    t.sleep(0.1)
    ReleaseKey(tab)
    t.sleep(0.1)
    t.sleep(0.5)
    PressKey(alt)
    t.sleep(0.1)
    PressKey(tab)
    t.sleep(0.2)
    ReleaseKey(alt)
    t.sleep(0.1)
    ReleaseKey(tab)
    t.sleep(0.5)
    t.sleep(0.5)
    """ss_region = (91, 330, 1829, 714)
    ss_img = ImageGrab.grab(ss_region)
    ss_img.save("heist_passed_p.jpg")
    heist_passed_p = cv2.imread('heist_passed_p.jpg')
    heist_passed_a = cv2.imread('heist_passed_a.jpg')
    while imgcheck(heist_passed_a,heist_passed_p)>5:
        ss_region = (91, 330, 1829, 714)
        ss_img = ImageGrab.grab(ss_region)
        ss_img.save("heist_passed_p.jpg")
        heist_passed_p = cv2.imread('heist_passed_p.jpg')"""
    t.sleep(11.819)

    PressKey(alt)
    t.sleep(0.1)
    PressKey(tab)
    t.sleep(0.2)
    ReleaseKey(alt)
    t.sleep(0.1)
    ReleaseKey(tab)
    t.sleep(0.1)
    set_pos(945, 386)
    click("left", duration=0.1)
    t.sleep(0.5)
    PressKey(alt)
    t.sleep(0.1)
    PressKey(tab)
    t.sleep(0.2)
    ReleaseKey(alt)
    t.sleep(0.1)
    t.sleep(0.5)
    set_pos(1195, 310)
    t.sleep(0.5)
    click("left", duration=0.1)
    t.sleep(16)
    PressKey(alt)
    t.sleep(0.1)
    PressKey(tab)
    t.sleep(0.2)
    ReleaseKey(alt)
    t.sleep(0.1)
    ReleaseKey(tab)
    t.sleep(0.5)
    set_pos(945, 386)
    t.sleep(0.5)
    click("left", duration=0.1)
    t.sleep(1)
    PressKey(alt)
    t.sleep(0.1)
    PressKey(tab)
    t.sleep(0.2)
    ReleaseKey(alt)
    t.sleep(0.1)
    ReleaseKey(tab)
    t.sleep(1)
    set_pos(1195, 310)
    t.sleep(0.5)
    click("left", duration=0.1)
    t.sleep(0.5)
    PressKey(enter)
    t.sleep(0.1)
    ReleaseKey(enter)
    t.sleep(18)
    PressKey(kend)
    t.sleep(0.5)
    ReleaseKey(kend)
    t.sleep(2)
    set_pos(1195, 310)
    t.sleep(0.5)
    click("left", duration=0.1)
    PressKey(esc)
    t.sleep(0.2)
    ReleaseKey(esc)
    t.sleep(24)
    PressKey(esc)
    t.sleep(0.2)
    ReleaseKey(esc)
    deposit=1
    newsession()
    errors=0
    t.sleep(630)
    """t.sleep(0.1)
    PressKey(space)
    t.sleep(0.6)
    ReleaseKey(space)
    t.sleep(4.6)
    MouseMoveTo(-1700,0)
    PressKey(shift)
    PressKey(w)
    t.sleep(3)
    MouseMoveTo(600,0)
    t.sleep(3)
    ReleaseKey(w)
    ReleaseKey(shift)
    t.sleep(200)"""
    """t.sleep(0.1)
    PressKey(a)
    t.sleep(0.8)
    ReleaseKey(a)
    t.sleep(0.1)
    PressKey(w)
    t.sleep(0.8)
    ReleaseKey(w)
    t.sleep(0.1)
    PressKey(e)
    t.sleep(0.3)
    ReleaseKey(e)
    t.sleep(5)
    PressKey(d)
    t.sleep(0.8)
    ReleaseKey(d)
    t.sleep(0.1)
    MouseMoveTo(5000, 0)
    t.sleep(1)
    PressKey(shift)
    PressKey(w)
    t.sleep(1)
    PressKey(d)
    t.sleep(0.4)
    ReleaseKey(d)
    t.sleep(1.7)
    PressKey(a)
    t.sleep(0.3)
    ReleaseKey(a)
    t.sleep(2)
    #MouseMoveTo(-900, 0)
    t.sleep(5)
    ReleaseKey(w)"""
    # newsession(tem=1.3)A

"""MouseMoveTo(2100,0)
t.sleep(5)
ReleaseKey(w)
t.sleep(8)6666
PressKey(w)
MouseMoveTo(1500,0)
t.sleep(1)
MouseMoveTo(-1600,0)
t.sleep(2)
MouseMoveTo(1600,0)
t.sleep(8)
ReleaseKey(w)"""

# first right before (2nd)stairs
# PressKey(w)
# t.sleep(1)
# MouseMoveTo(-600,0)
# t.sleep(10)
# ReleaseKey(w)
# first right before (3rd)stairs
# MouseMoveTo(1700,0)
# t.sleep(0.1)
# PressKey(w)
# t.sleep(3)
# ReleaseKey(w)
# t.sleep(0.1)
# MouseMoveTo(1700,0)
# t.sleep(0.1)
# PressKey(w)
# t.sleep(5)
# ReleaseKey(w)
# directx scan codes http://www.gamespp.com/directx/directInputKeyboardScanCodes.html
# MouseMoveTo(-1500,0)
