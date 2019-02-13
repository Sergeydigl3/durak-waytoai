import win32con
import win32gui
import win32ui

from PIL import Image

# Масти
suits = [
    'C',  # крестья
    'D',  # Бубны
    'H',  # Червы
    'S',  # Пики
]

# Достоинства
values = [
    '6',
    '7',
    '8',
    '9',
    'T',  # 10
    'J',  # Валет
    'Q',  # Дама
    'K',  # Король
    'A',  # Туз
]


class Game:
    def __init__(self):
        self.__is_test = True

    def scan(self):
        if self.__is_test:
            img = Image.open('screen.JPG')
            return img
        else:
            return self.screenshot()

    def screenshot(self):
        showcursor = False
        # hwnd = win32gui.GetForegroundWindЯow()
        hwnd = win32gui.FindWindow(None, "Streaming game from BlueStacks")

        l, t, r, b = win32gui.GetWindowRect(hwnd)
        w = r - l
        h = b - t

        hwndDC = win32gui.GetWindowDC(hwnd)
        mfcDC = win32ui.CreateDCFromHandle(hwndDC)
        saveDC = mfcDC.CreateCompatibleDC()

        saveBitMap = win32ui.CreateBitmap()
        saveBitMap.CreateCompatibleBitmap(mfcDC, w, h)
        saveDC.SelectObject(saveBitMap)

        saveDC.BitBlt((0, 0), (w, h), mfcDC, (0, 0), win32con.SRCCOPY)

        # add cursor
        if showcursor:
            curFlags, curH, (curX, curY) = win32gui.GetCursorInfo()
            saveDC.DrawIcon((curX, curY), curH)

        # load into PIL image
        """http://stackoverflow.com/questions/4199497/image-frombuffer-with-16-bit-image-data"""
        bmpinfo = saveBitMap.GetInfo()
        bmpstr = saveBitMap.GetBitmapBits(True)
        im = Image.frombuffer(
            'RGB',
            (bmpinfo['bmWidth'], bmpinfo['bmHeight']),
            bmpstr, 'raw', 'BGRX', 0, 1)

        win32gui.DeleteObject(saveBitMap.GetHandle())
        saveDC.DeleteDC()
        mfcDC.DeleteDC()
        win32gui.ReleaseDC(hwnd, hwndDC)

        return im
