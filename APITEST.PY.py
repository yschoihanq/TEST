import requests
import json
from tkinter import *
import urllib3
import pandas as pd
import pymysql

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# API_HOST_읽기 (TXT 파일 내 수정)
host_load = pd.read_csv("data/config.txt", header=0)
host = host_load['API_host'][0]

# # LocalDB 연결
# conn = pymysql.connect(host='127.0.0.1', user='root', password='asdf1234', db='hanq_data', charset='utf8')
# cur = conn.cursor()
#
# # 테이블 생성 쿼리
# # cur.execute("CREATE TABLE userTable(id char(4), userName char(15), email char(20), birthYear int)")
#
# # 검색쿼리 : cur.execute("SELECT * FROM tb_member WHERE mem_handi='%d'" % param1)
# # 수정쿼리 : cur.execute("UPDATE tb_member SET mem_nick='%s' WHERE mem_name='%s'" % ('아도2스', '최윤석'))
#
#
# # cur.execute("SELECT * FROM tb_member WHERE mem_handi=:id", {"id": 23})
# # for row in cur.fetchall():
# #    print(row)
#
# param1 = 23
# param2 = 0.5
#
# # cur.execute("SELECT * FROM tb_member WHERE mem_handi='%f' AND mem_avg>='%f'", %)
#
# sql = "SELECT * FROM tb_member WHERE mem_handi=%f AND mem_avg >=%f"
# cur.execute(sql % (param1, param2))
# for row in cur.fetchall():
#     print(row)
#
# cur.execute("SELECT * FROM tb_member WHERE mem_handi='%f' AND mem_avg>='%f'" % (param1, param2))
#
#
# conn.commit() # 내용 커밋
# conn.close() # DB 닫기

# 창 셋팅--------------------------------------------------------------------------
win = Tk()
win.geometry("1920x1080")
win.title("HanQ Server Management Program")
win.option_add("*Font", "CoreGothicD 15")

# 이미지 로딩
img_top = PhotoImage(file="data/IMG/top.png")
img_main = PhotoImage(file="data/IMG/main.png")
img_btn = PhotoImage(file="data/IMG/btn.png")

# 메인이미지 삽입
canvas_1 = Canvas(win, background="white")
canvas_1.place(x=0, y=0, width=1920, height=1080)
canvas_1.create_image(960, 540, image=img_main)

# 메뉴 UI


# 함수-----------------------------------------------------------------------------
# 버튼 클릭 함수

def pressed():
    text = input_txt.get()
    mem_search(text, "HQAA00000001")


# 회원조회 함수 (GET)
def mem_search(mem_hp, hq_store_cd):
    global host
    mem_url = host + "/member/search?"
    params = {'mem_hp': mem_hp, 'hq_store_cd': hq_store_cd}
    res = requests.get(mem_url, verify=False, params=params)
    resp = res.json()

    # data 는 배열
    print(json.dumps(resp, indent=4))

    # data 내 배열 0번 인덱스 내의 dic 오브젝트 출력
    label.configure(text=resp['data'][0]['mem_nick'])
    # label.configure(text=resp['data'])
    print(resp['data'][0]['mem_seq'])

# 게임조회 함수 (GET)
def gm_search(hq_store_cd, hq_table_cd):
    global host
    gm_search_url = host + "/game?"
    params = {'hq_store_cd' : hq_store_cd, 'hq_table_cd' : hq_table_cd}
    res = requests.get(gm_search_url, verify=False, params=params)
    resp = res.json()

    print(json.dumps(resp, indent=4))



# 디자인 ------------------------------------------------------------------------------

canvas_0 = Canvas(win, background="white")
canvas_0.place(x=0, y=0, width=1920, height=100)
canvas_0.create_image(960, 50, image=img_top)

label = Label(win, text="휴대폰 뒷번호 입력", font=("돋음", 12))
label.place(x=150, y=150, width=150, height=160)

label_1 = Label(win, text="서버연결상태 : ", font=("돋음", 12))
label_1.place(x=1680, y=40, width=150, height=22)

label_2 = Label(win, text="확인", font=("돋음", 12))
label_2.place(x=1830, y=40, width=90, height=22)

input_txt = Entry(win, width = 30)
input_txt.place(x=100, y=100, width=150, height=22)

btn = Button(win, image=img_btn)
btn.configure(command=pressed)
btn.place(x=266, y=167, width=345, height=183)

btn1 = Button(win, image=img_btn)
btn1.configure(command=pressed)
btn1.place(x=646, y=167, width=345, height=183)


# main 부
# mem_search("5641", "HQAA00000001")

# 연결 확인 코드
store_url = host + "/store/tables?hq_store_cd=HQAA00000001"
store = requests.get(store_url, verify=False)
store_resp = store.json()
print(json.dumps(store_resp, indent=4))

if store_resp['resp']['code'] == 200:
    # print(store_resp['resp']['code'])
    label_2.configure(text="성공")

# TEST BOARD

# gm_search('HQAA00000001', 'HQTB0001')

# 창실행
win.mainloop()