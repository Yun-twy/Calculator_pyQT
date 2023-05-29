import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import uic
# ui 파일 연결 - 코드 파일과 같은 폴더내에 위치해야함
#from_class = uic.loadUiType("C:/Users/User/Downloads/update_0323/QT/calculator.ui")[0]
from_class = uic.loadUiType("C:/Users/82105/Desktop/amr_ws/update_0323/QT/calculator.ui")[0]
#from_class = uic.loadUiType("C:\Users\82105\Desktop\amr_ws\update_0323\QT\calculator.ui")[0]

# 화면 클래스
class WindowClass(QMainWindow, from_class) :
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setWindowTitle("CALCULATOR")
        #지우기 함수
        self.AC.clicked.connect(self.allClear)
        self.CE.clicked.connect(self.clearEntry)
        self.Back.clicked.connect(self.backSpace)
        #숫자 0-9
        self.Nine.clicked.connect(lambda: self.addText("9"))
        self.Eight.clicked.connect(lambda: self.addText("8"))
        self.Seven.clicked.connect(lambda: self.addText("7"))
        self.Six.clicked.connect(lambda: self.addText("6"))
        self.Five.clicked.connect(lambda: self.addText("5"))
        self.Four.clicked.connect(lambda: self.addText("4"))
        self.Three.clicked.connect(lambda: self.addText("3"))
        self.Two.clicked.connect(lambda: self.addText("2"))
        self.One.clicked.connect(lambda: self.addText("1"))
        self.Zero.clicked.connect(lambda: self.addText("0"))
        # 점 / 부호 처리
        self.Dot.clicked.connect(self.addDot)
        self.Sign.clicked.connect(self.addSign)
        #사칙연산
        self.Devide.clicked.connect(lambda: self.addText("/"))
        self.Multiple.clicked.connect(lambda: self.addText("*"))
        self.Plus.clicked.connect(lambda: self.addText("+"))
        self.Minus.clicked.connect(lambda: self.addText("-"))
        #등호(계산)
        self.Equal.clicked.connect(self.evaluate)
    
    
    def addText(self, x):
        value = self.Result.text() #현재 값 불러오기
        last_value = self.resultList() # 맨 뒤 요소 찾기
        operator = ['+','-','*','/']
        result = '0' #임시 값
        x = str(x)

        if value == '0':
            if x=='/' or x=='*' or x=='-' or x=='+' : #처음에 * / 는 입력 불가
                result = '0'
            else:
                result = x # 입력값 출력

        #마지막이 연산자인데 또 연산자가 들어온 경우
        elif (last_value[-1] in operator) and (x in operator):
            result = value[:-1] + x  #새로운 연산자로 대체

        #괄호 처리 되어 있는 경우
        elif last_value[-1] == ')':
            if x in operator:
                result = value + x
            else:
                result = value[:-1] + x + ')'
        else:
            result = value + x #기존의 숫자에 추가

        self.Result.setText(result)


    def evaluate(self):
        value = self.Result.text() #현재 값 받아오기
        last_value = self.resultList()
        operator = ['+','-','*','/']
        #맨 끝에 연산자가 있으면 빼고 연산
        if last_value[-1] in operator:
            value = value[:-1]
        result = eval(value)
        self.Result.setText(str(result))

    def addDot(self):
        value = self.Result.text() #전체
        last_value = self.resultList() #연산자 기준 마지막
        #print(last_value)
        operator = ['+','-','*','/']

        if last_value in operator: #연산자로 끝났을 경우
            value = value + "0."

        else:
            if "." not in last_value:
                if last_value[-1] == ')':
                    if last_value[-2] == '-':
                        value = value[:-1] + '0.)'
                    else:
                        value = value[:-1] + '.' + ')'
                else:
                    value = value + "."
            else:
                value = value # 이미 . 이 포함되어 있는 경우 무시

        self.Result.setText(value)

    def addSign(self):
        value = self.Result.text()
        last_value = self.resultList()
        first_value = value[:-1*len(last_value)] # 연사자 앞 부분
        operator = ['+','-','*','/']
        # print('value : ', value)
        # print(type(value))
        # print('first_value : ',first_value)
        # print(type(first_value))
        # print('last_value : ', last_value)
        
        #끝이 부호인 경우
        if value == '0':
            last_value = '(-)'

        elif value == '(-)':
            #first_value = ''
            last_value = '0'

        else:
            if first_value =='': #앞부분이 없는 경우
                if last_value[-1] == ')':
                    last_value = last_value[2:-1] # (-x) -> x 처리
                else:
                    last_value = '(' + '-' + last_value + ')' # ㅌ -> (-x) 처리
            
            else: # 앞부분이 존재
                #앞부분이 연산자일 경우 *,/는 단독으로 올수 없음
                if first_value == '-':
                    first_value = '+'

                elif first_value == '+':
                    first_value = '-'

                #마지막 입력이 연산자일 경우
                elif last_value =='/' or last_value =='*':
                    last_value = last_value + '(-)' #연산자 끝으로 *,/ 이면 무신

                elif last_value == '-':
                    last_value = '+'

                elif last_value == '+':
                    last_value = '-'

                #앞부분이 존재하고 뒤에 숫자가 오는경우
                elif first_value[-1] in ['*', '/']:
                    if last_value[-1] != ')':
                        last_value = '(' + '-' + last_value  + ')'
                    else:
                        last_value = last_value[2:-1]

                elif first_value[-1] =='+':
                    if last_value[-1] !=')':
                        first_value = first_value[:-1] + '-'
                        #last_value = '(' + '-' + last_value  + ')'
                    else:
                        last_value = last_value[2:-1]

                elif first_value[-1] == '-':
                    first_value = first_value[:-1] + '+'

                else:
                    last_value = '(' + '-' + last_value  + ')'

        result = first_value + last_value

        self.Result.setText(result)
        
    def allClear(self): #다 지우고 0 출력
        self.Result.clear()
        self.Result.setText('0')

    def clearEntry(self):
        last_value = self.resultList()
        now_value = self.Result.text()

        if len(now_value) == len(last_value):
            result = '0'
        else:
            result = now_value[:-1*len(last_value)]
        self.Result.setText(result)
        

    def backSpace(self):
        value = self.Result.text()
        if len(value) == 1:
            result = '0'
        else:
            result = value[:-1]
        self.Result.setText(result)

    def resultList(self): #연산자 기준으로 마지막 원소 찾아주는 함수
        value = self.Result.text()
        number = ['0','1','2','3','4','5','6','7','8','9','.']
        operator = ['+','-','*','/']
        new_value = '0'
        
        if value[-1] != ')':
            for i in reversed(range(len(value))):
                if value[i] in operator:
                    if i == len(value)-1:
                        new_value = value[-1] #operator가 끝에 있는 경우
                    else:
                        new_value = value[i+1:] #operator가 중간에 있느 경우
                    
                    break
                else:
                    new_value = value

        elif value[-1] == ')':
            for i in reversed(range(len(value))):
                if value[i] == '(':
                    new_value = value[i:]

                    break

        print('new_value : ', new_value)
                
        return new_value

# Python Main 함수
if __name__ == "__main__":
    app = QApplication(sys.argv) # 프로그램 실행
    myWindows = WindowClass() # 화면 클래스 생성
    myWindows.show() # 프로그램 화면 보이기
    sys.exit(app.exec_()) # 프로그램을 종료까지 동작시킴
