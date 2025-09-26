# -*- coding: utf-8 -*-
#import spam
from tkinter import *
from tkinter import ttk
from tkinter import font
from tkinter import messagebox

import http.client
from xml.etree import ElementTree
import urllib.parse
import urllib.request

import mimetypes
import mysmtplib
from email.mime.base import MIMEBase
from email.mime.text import MIMEText
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart
from email import encoders
import os
import requests
import re
import subprocess

TEXT= ""
MAIL = ""
favoriteList = []


class MountainSearch:
    def __init__(self):
        self.InitTitle()

    def InitTitle(self):       # 타이틀 윈도우
        self.Twindow = Tk()
        self.Twindow.iconbitmap(default='icon.ico')

        self.f1 = PhotoImage(file="anime01.png")
        self.f2 = PhotoImage(file="anime02.png")
        self.f3 = PhotoImage(file="anime03.png")
        self.f4 = PhotoImage(file="anime04.png")
        self.f5 = PhotoImage(file="anime05.png")
        self.f6 = PhotoImage(file="anime06.png")
        self.n = 0
        self.fn = self.f1

        self.Twindow.title("검색")
        self.Twindow.geometry("480x640+700+100")
        self.Tcanvas = Canvas(self.Twindow, width=480, height=640, relief="solid", bd=1)
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')

        Button(self.Twindow, text="검색",
               font=self.TempFont, command=self.nextWindow).place(x=295, y=250)
        self.e = Entry(self.Twindow, font=self.TempFont)
        self.e.place(x=150, y=250, width=140, height=40)

        self.anim_id = self.Twindow.after(0, self.Animation)

        # 즐겨찾기
        if len(favoriteList) > 0:
            self.comboString = StringVar()
            self.combobox = ttk.Combobox(self.Twindow, width=17, textvariable=self.comboString)
            self.combobox['values'] = tuple(favoriteList)
            self.combobox.place(x=150, y=350)
            Button(self.Twindow, text="즐겨찾기 검색", command=self.FavoriteButton).place(x=295, y=350)

        self.Tcanvas.pack()
        self.Twindow.mainloop()

    def Favorite(self):
        global favoriteList
        favoriteList.append(self.MountainName)
        messagebox.showinfo("알림", "즐겨찾기에 추가되었습니다.\n타이틀 화면에서 확인할 수 있습니다.")

    def FavoriteButton(self):
        self.MountainName = self.comboString.get()  # 타이틀에서 산 이름 받아옴
        self.search_word = urllib.parse.quote(self.comboString.get())

       ##c 연동 부분--------------------------------------------------------------------------------------------------------------------
       #conn = http.client.HTTPConnection("openapi.forest.go.kr")
       #url = spam.strlen(url, "?serviceKey=cuVGydw6yzwC%2B6YdfYKOPzXxvC45arm%2F1M1dpN31ZrgomqlojiWkwCq0jZqneeAvoEZxOqR8WrymypQQvq4hpg%3D%3D")
       #url = spam.strlen(url, "&mntnNm=")
       #url = spam.strlen(url, self.mntnnm)
       ## c 연동 부분--------------------------------------------------------------------------------------------------------------------
        conn = http.client.HTTPConnection("openapi.forest.go.kr")
        service_key = "cuVGydw6yzwC%2B6YdfYKOPzXxvC45arm%2F1M1dpN31ZrgomqlojiWkwCq0jZqneeAvoEZxOqR8WrymypQQvq4hpg%3D%3D"
        url = (
            "https://apis.data.go.kr/1400000/service/cultureInfoService2/mntInfoOpenAPI2"
            f"?serviceKey={service_key}&searchWrd={self.search_word}&pageNo=1&numOfRows=10"
        )

        conn.request("GET", url)
        req = conn.getresponse()
        self.tree = ElementTree.fromstring(req.read().decode('utf-8'))

        try:
            if hasattr(self, 'anim_id') and self.anim_id:
                self.Twindow.after_cancel(self.anim_id)
        except Exception:
            pass

        self.Twindow.destroy()  # 기존에 있던 타이틀 윈도우 파괴
        self.InitResult()  # 결과창 생성

    def Animation(self):
        if 0 <= self.n < 2:
            self.fn = self.f1
            self.n += 1
        elif 2 <= self.n < 4:
            self.fn = self.f2
            self.n += 1
        elif 4 <= self.n < 6:
            self.fn = self.f3
            self.n += 1
        elif 6 <= self.n < 8:
            self.fn = self.f4
            self.n += 1
        elif 8 <= self.n < 10:
            self.fn = self.f5
            self.n += 1
        elif 10 <= self.n < 12:
            self.fn = self.f6
            self.n += 1
        elif self.n == 12:
            self.n = 0

        self.Tcanvas.create_image(240, 320, image=self.fn)
        self.anim_id = self.Twindow.after(90, self.Animation)

    def nextWindow(self):           # 검색 버튼 누르면 실행되는 함수
        self.MountainName = self.e.get()       # 타이틀에서 산 이름 받아옴
        self.search_word = urllib.parse.quote(self.e.get())
        ## c 연동 부분--------------------------------------------------------------------------------------------------------------------
        # url = "http://openapi.forest.go.kr/openapi/service/trailInfoService/getforeststoryservice"
        # url = spam.strlen(url, "?serviceKey=cuVGydw6yzwC%2B6YdfYKOPzXxvC45arm%2F1M1dpN31ZrgomqlojiWkwCq0jZqneeAvoEZxOqR8WrymypQQvq4hpg%3D%3D")
        # url = spam.strlen(url, "&mntnNm=")
        # url = spam.strlen(url, self.mntnnm)
        ## c 연동 부분--------------------------------------------------------------------------------------------------------------------
        conn = http.client.HTTPConnection("openapi.forest.go.kr")
        service_key = "cuVGydw6yzwC%2B6YdfYKOPzXxvC45arm%2F1M1dpN31ZrgomqlojiWkwCq0jZqneeAvoEZxOqR8WrymypQQvq4hpg%3D%3D"
        url = (
            "https://apis.data.go.kr/1400000/service/cultureInfoService2/mntInfoOpenAPI2"
            f"?serviceKey={service_key}&searchWrd={self.search_word}&pageNo=1&numOfRows=10"
        )

        conn.request("GET", url)
        req = conn.getresponse()
        self.tree = ElementTree.fromstring(req.read().decode('utf-8'))

        try:
            if hasattr(self, 'anim_id') and self.anim_id:
                self.Twindow.after_cancel(self.anim_id)
        except Exception:
            pass

        self.Twindow.destroy()   # 기존에 있던 타이틀 윈도우 파괴
        self.InitResult()        # 결과창 생성

    def InitResult(self):        # 결과창 생성
        self.window = Tk()
        self.window.iconbitmap(default='icon.ico')
        self.window.title("검색 결과")
        self.window.geometry("400x402+700+100")
        self.MapCanvas = Canvas(self.window, width=800, height=402)
        self.MapCanvas.pack()
        self.TempFont = font.Font(size=16, weight='bold', family='Consolas')

        Label(self.window, text=self.MountainName).place(x=20, y=5)

        Button(self.window, text="상세정보", width=10, command=self.Information).place(x=0, y=30)
        Button(self.window, text="소재지", width=10, command=self.Address).place(x=0, y=60)
        Button(self.window, text="관리주체명", width=10, command=self.MountainAdmin).place(x=0, y=90)
        Button(self.window, text="관리자번호", width=10, command=self.MountainAdminNum).place(x=0, y=120)
        Button(self.window, text="산행포인트", width=10, command=self.HikingPoint).place(x=0, y=150)
        Button(self.window, text="100대명산", width=10, command=self.SpecialMountain).place(x=0, y=180)
        Button(self.window, text="개관", width=10, command=self.Survey).place(x=0, y=210)
        Button(self.window, text="E-Mail 보내기", width=10, command=self.sendMail).place(x=0, y=240)
        Button(self.window, text="지도", width=10, command=self.Map).place(x=0, y=270)
        Button(self.window, text="재검색", width=10, command=self.reSearch).place(x=0, y=300)
        Button(self.window, text="산높이 그래프", width=10, command=self.Graph).place(x=0, y=330)
        Button(self.window, text="즐겨찾기", width=10, command=self.Favorite).place(x=0, y=360)

        scroll = Scrollbar(self.window)
        self.text = Text(self.window, width=41, height=32, borderwidth=5, relief="ridge", yscrollcommand=scroll.set)
        scroll.place(x=380, y=0, height=402)
        self.text.place(x=80, y=0)

        self.L = []
        self.window.mainloop()

    def reSearch(self):
        self.nameSave = self.MountainName
        self.window.destroy()
        self.InitTitle()

    # --- 헬퍼: 여러 후보 태그에서 텍스트 가져오기 ---
    def _get_text(self, item, *tags):
        for tag in tags:
            el = item.find(tag)
            if el is not None and el.text is not None:
                return el.text.strip()
        return ''

    # --- 헬퍼: HTML 태그 / &amp; 같은 이스케이프 정리 ---
    def _clean_text(self, s):
        if not s:
            return ''
        # <br> -> newline, remove other tags, decode some entities
        s = s.replace('&lt;', '<').replace('&gt;', '>').replace('&amp;', '&')
        s = re.sub(r'(?i)<br\s*/?>', '\n', s)
        s = re.sub(r'<[^>]+>', '', s)  # 남은 태그 제거
        return s.strip()

    def Information(self):
        self.text.delete(1.0, END)

        items = list(self.tree.iter("item"))
        if not items:
            self.text.insert(1.0, "검색 결과가 없습니다.")
            return

        for item in items:
            # 여러 가능한 태그명(구버전/신버전 대비)
            raw_info = self._get_text(item, 'mntninfodtlinfoc', 'mntidetails', 'mntninfodscrt', 'mntidetails')
            info = self._clean_text(raw_info)
            height = self._get_text(item, 'mntninfohght', 'mntihigh')
            sub_name = self._get_text(item, 'mntnsbttlinfo', 'mntisname')
            name = self._get_text(item, 'mntnnm', 'mntiname',)

            # 안전하게 삽입
            if name:
                self.text.insert(1.0, name + '\n\n')
            if sub_name:
                self.text.insert(1.0, "산의 부제 : " + self._clean_text(sub_name) + '\n\n')
            if height:
                self.text.insert(1.0, "높이 : " + height + '\n\n')
            if info:
                self.text.insert(1.0, info + '\n\n')

        global TEXT
        TEXT = self.text.get(1.0, END)

    def Address(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.MountainAddress = item.find("mntiadd")
            self.text.insert(1.0, self.MountainAddress.text + '\n')

    def MountainAdminNum(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.AdminNumInfo = item.find("mntiadminnum")
            self.L.append(self.AdminNumInfo.text)
            self.AdminNumInfo.text = self.AdminNumInfo.text.replace('<BR>', '\n')
            self.AdminNumInfo.text = self.AdminNumInfo.text.replace('br /', '\n')
            self.AdminNumInfo.text = self.AdminNumInfo.text.replace('&lt;', '\n')
            self.AdminNumInfo.text = self.AdminNumInfo.text.replace('&gt;', '\n')
            self.AdminNumInfo.text = self.AdminNumInfo.text.replace('&amp;', '\n')
            self.AdminNumInfo.text = self.AdminNumInfo.text.replace('nbsp;', '\n')
            self.AdminNumInfo.text = self.AdminNumInfo.text.replace('<p>&', '\n')
            self.AdminNumInfo.text = self.AdminNumInfo.text.replace('</p>', '\n')
            self.text.insert(1.0, self.AdminNumInfo.text + '\n')

        if not self.L or self.L[0] == '':
            self.text.insert(1.0, "관리자 전화번호가 없습니다.")

        self.L.clear()

    def MountainAdmin(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.AdminInfo = item.find("mntiadmin")
            self.L.append(self.AdminInfo.text)
            self.AdminInfo.text = self.AdminInfo.text.replace('<BR>', '\n')
            self.AdminInfo.text = self.AdminInfo.text.replace('br /', '\n')
            self.AdminInfo.text = self.AdminInfo.text.replace('&lt;', '\n')
            self.AdminInfo.text = self.AdminInfo.text.replace('&gt;', '\n')
            self.AdminInfo.text = self.AdminInfo.text.replace('&amp;', '\n')
            self.AdminInfo.text = self.AdminInfo.text.replace('nbsp;', '\n')
            self.AdminInfo.text = self.AdminInfo.text.replace('<p>&', '\n')
            self.AdminInfo.text = self.AdminInfo.text.replace('</p>', '\n')
            self.text.insert(1.0, self.AdminInfo.text)

        if not self.L or self.L[0] == '':
            self.text.insert(1.0, "관리자 정보가 없습니다.")

        self.L.clear()

    def HikingPoint(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.HikingPointInfo = item.find("frtrlsectnnm")
            self.L.append(self.HikingPointInfo.text)
            self.HikingPointInfo.text = self.HikingPointInfo.text.replace('<BR>', '\n')
            self.HikingPointInfo.text = self.HikingPointInfo.text.replace('br /', '\n')
            self.HikingPointInfo.text = self.HikingPointInfo.text.replace('&lt;', '\n')
            self.HikingPointInfo.text = self.HikingPointInfo.text.replace('&gt;', '\n')
            self.HikingPointInfo.text = self.HikingPointInfo.text.replace('&amp;', '\n')
            self.HikingPointInfo.text = self.HikingPointInfo.text.replace('nbsp;', '\n')
            self.HikingPointInfo.text = self.HikingPointInfo.text.replace('<p>&', '\n')
            self.HikingPointInfo.text = self.HikingPointInfo.text.replace('</p>', '\n')
            self.text.insert(1.0, self.HikingPointInfo.text)

        if not self.L or self.L[0] == '':
            self.text.insert(1.0, "산행 포인트 정보가 없습니다.")

        self.L.clear()

    def SpecialMountain(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.SM = item.find("mntitop")
            self.SM.text = self.SM.text.replace('<BR>', '\n')
            self.SM.text = self.SM.text.replace('br /', '\n')
            self.SM.text = self.SM.text.replace('&lt;', '\n')
            self.SM.text = self.SM.text.replace('&gt;', '\n')
            self.SM.text = self.SM.text.replace('&amp;', '\n')
            self.SM.text = self.SM.text.replace('nbsp;', '\n')
            self.text.insert(1.0, self.SM.text)

    def Survey(self):
        self.text.delete(1.0, 1000.0)
        for item in self.tree.iter("item"):
            self.Survey = item.find("mntisummary")
            self.Survey.text = self.Survey.text.replace('<BR>', '\n')
            self.Survey.text = self.Survey.text.replace('br /', '\n')
            self.Survey.text = self.Survey.text.replace('&lt;', '\n')
            self.Survey.text = self.Survey.text.replace('&gt;', '\n')
            self.Survey.text = self.Survey.text.replace('&amp;', '\n')
            self.Survey.text = self.Survey.text.replace('nbsp;', '\n')

            self.text.insert(1.0, self.Survey.text)

            if not self.L or self.L[0] == '':
                self.text.insert(1.0, "개관 정보가 없습니다.")

    def sendMail(self):
        # global value
        global MAIL
        self.Twindow2 = Tk()
        self.Twindow2.title("이메일 주소 입력")
        self.Twindow2.geometry("300x100+700+250")
        self.TempFont2 = font.Font(size=5, weight='bold', family='Consolas')

        Button(self.Twindow2, text="보내기",
               font=self.TempFont2, command=self.mailSend).place(x=120, y=50)

        self.e2 = Entry(self.Twindow2, font=self.TempFont2)
        self.e2.place(x=10, y=10, width=280, height=30)

    def mailSend(self):
        global MAIL
        global TEXT
        MAIL = self.e2.get()
        host = "smtp.gmail.com"  # Gmail SMTP 서버 주소.
        port = "587"
        messagebox.showinfo("Loading", "이메일 보내는 중...")

        senderAddr = "35379289p@gmail.com"  # 보내는 사람 email 주소.
        recipientAddr = MAIL  # 받는 사람 email 주소.

        msg = MIMEMultipart()

        msg['Subject'] = "산 상세정보"
        msg['From'] = senderAddr
        msg['To'] = recipientAddr

        self.Information()      # 상세정보 누르지 않아도 여기서 다시 실행

        # ----- 본문 추가 -----
        # TEXT 변수를 html 본문으로
        body = MIMEText(TEXT, "html", "utf-8")
        msg.attach(body)

        # ----- 이미지 첨부 -----
        with open("Searched_Result_Map.png", "rb") as f:
            img = MIMEImage(f.read(), _subtype="png")
            img.add_header("Content-Disposition", "attachment", filename="Searched_Result_Map.png")
            msg.attach(img)

        # 메일 전송
        s = mysmtplib.MySMTP(host, port)
        s.ehlo()
        s.starttls()
        s.login("35379289p@gmail.com", "lyqt vnld amnz xzvg")  # 앱 비밀번호
        s.sendmail(senderAddr, [recipientAddr], msg.as_string())
        s.close()

        messagebox.showinfo("Complete", "이메일 보내기 완료!")

    def Map(self):
        import pdfcrowd
        import sys

        self.URL = 'https://maps.googleapis.com/maps/api/geocode/json?key=' \
                   'AIzaSyBFVqFYHLQNOYuSVfkiHCv1GkyfUpnpAIY&sensor=false&language=ko&address={}'\
            .format(self.MountainName)

        self.response = requests.get(self.URL)

        self.data = self.response.json()

        self.lat = self.data['results'][0]['geometry']['location']['lat']
        self.lng = self.data['results'][0]['geometry']['location']['lng']

        self.map_url = 'https://www.google.co.kr/maps/search/' + self.MountainName + '/@' + \
                       str(self.lat) + ',' + str(self.lng) + ',12z'

        messagebox.showinfo("알림", "지도 그리는 중...")

        # html file to png file
        try:
            # Create an API client instance.
            client = pdfcrowd.HtmlToImageClient('janghoparkdev', 'd63ba72280fa2a4edce5a6813af47934')

            # Configure the conversion.
            client.setOutputFormat('png')
            client.setScreenshotWidth(1280)
            client.setScreenshotHeight(720)

            # Run the conversion and save the result to a file.
            client.convertUrlToFile(self.map_url, 'Searched_Result_Map.png')

        except pdfcrowd.Error as why:
            sys.stderr.write('PDFCrowd Error: {}\n'.format(why))
            raise

        self.image = PhotoImage(file='Searched_Result_Map.png')
        self.window.geometry("800x402")
        self.MapCanvas.create_image(600, 201, image=self.image)

        messagebox.showinfo("알림", "지도가 완성되었습니다!")

        Button(self.window, text="구글 지도 연동", overrelief="solid", width=15,
               command=self.WebViewer).place(x=600, y=350)

        # google map api로 경도 위도 받아와 pdfcrowd로 email 전송을 위한 png 파일 저장.
        # 지도 버튼 누르면 웹뷰 윈도우로 아예 구글 맵 검색되도록 구현.

    def WebViewer(self):
        subprocess.Popen([sys.executable, 'webview_launcher.py', self.map_url])

    def Graph(self):
        self.f = open("100대산(중복제외95).txt", 'r+')
        self.string = ''
        self.string += self.f.read()
        self.MountainList = []
        self.MountainList += self.string.split('\n')
        self.HeightList = []
        self.NameList = []

        conn = http.client.HTTPConnection("openapi.forest.go.kr")
        service_key = "cuVGydw6yzwC%2B6YdfYKOPzXxvC45arm%2F1M1dpN31ZrgomqlojiWkwCq0jZqneeAvoEZxOqR8WrymypQQvq4hpg%3D%3D"
        graph_url = (
            "https://apis.data.go.kr/1400000/service/cultureInfoService2/mntInfoOpenAPI2"
            f"?serviceKey={service_key}&searchWrd="
        )
        url = ''
        messagebox.showinfo("알림", "확인을 누르면 그래프 그리기를 시작합니다.")

        for i in range(95):
            name = urllib.parse.quote(self.MountainList[i])
            url += graph_url + name + "&pageNo=1&numOfRows=10"
            conn.request("GET", url)
            req = conn.getresponse()
            graph_tree = ElementTree.fromstring(req.read().decode('utf-8'))
            url = ''
            for item in graph_tree.iter("item"):
                self.HeightList.append(item.find("mntihigh").text)
                self.NameList.append(item.find("mntiname").text)

        self.GraphWindow = Tk()
        self.GraphWindow.iconbitmap(default='icon.ico')
        self.GraphWindow.title("100대 명산 높이 그래프")
        self.GraphWindow.geometry("1280x680")
        self.GraphCanvas = Canvas(self.GraphWindow, width=1280, height=670)
        scrollbar = Scrollbar(self.GraphWindow, orient="horizontal", command=self.GraphCanvas.xview)
        self.GraphCanvas.configure(xscrollcommand=scrollbar.set)
        scrollbar.pack(side="bottom", fill="x")

        interval = 20
        for i in range(len(self.HeightList)):
            # 높이를 실수로 변환
            height = float(self.HeightList[i])
            # 캔버스는 정수 좌표만 받으니 int 변환
            rect_height = int(height * 0.3)
            self.GraphCanvas.create_rectangle(
                i * 10 + interval, 650,
                (i + 1) * 10 + interval, 650 - rect_height,
                outline="black", fill="blue"
            )
            self.GraphCanvas.create_text(i * 10 + interval + 5, 660, text=self.NameList[i])
            self.GraphCanvas.create_text(i * 10 + interval + 5, 650 - rect_height - 20, text=f"{height:.1f}")
            interval += 50

        self.f.close()
        self.NameList.clear()
        self.HeightList.clear()
        self.GraphCanvas.pack()
        self.GraphWindow.bind("<Configure>", self.on)
        self.GraphWindow.mainloop()

    def on(self, event):
        self.GraphCanvas.configure(scrollregion=self.GraphCanvas.bbox("all"))


MountainSearch()
