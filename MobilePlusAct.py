#-*- coding:utf-8 -*-

# Mobile Plus Action Module (Android/IOS)

import os

from time import sleep

from MobileBasicAct import *
from appium.webdriver.common.touch_action import TouchAction                    # long key쓰기 위한 라이브러리
from appium.webdriver.common.multi_action import MultiAction                    # Pinch IN/OUT을 위한 라이브러리
import MobileBasicAct
from appium import webdriver
import unittest
from time import localtime, strftime                                        #로컬 시간 받아오기 위한 라이브러리

global osType
global delayTime, logFileName
global MPAL_VERSION, iosSettingInfo
global aosSettingInfo, aosfindXpath

MPAL_VERSION = "20221227_API_update1"

iosSettingInfo = ""
aosSettingInfo = ""
aosfindXpath = ""

longDelay = 5                   # 모바일 기기별 나누는 용도
middleDelay = 3

shortDelay = 1

delayTime = 2
strftime("%y-%m-%d %I:%M:%S", localtime())
strTime = strftime("%y%m%d_%H%M%S", localtime())
# testPhone = "Note10"                                                             # 테스트 Device(유동적으로 변경 필요)
# # folderPath = f'{testPhone} {strTime}'                                            # 스크린샷 저장파일 경로
# originFolderPath = testPhone + " " + strTime

logFileName = "test_log.txt"										              # 디버그 로그 파일 이름

#--------Start_App--------
# Mobile Plus 실행 동작

def Start_App(driver, osType, delayTime):
    writeLog(logFileName, "앱 실행 TC 시작")
    # try:
    if osType == "android":
        print("Android")
        # while True:
        for loopNum in range(0,3):
            try:
                element = "com.android.permissioncontroller:id/permission_allow_foreground_only_button"  # App초기 동작 시 권한 승인 버튼
                mobile_click(driver, osType, 'id', element, delayTime)
                sleep(delayTime)
            except:
                break

        # while True:
        for loopNum in range(0, 3):
            try:
                element = "com.android.permissioncontroller:id/permission_allow_button"             # App초기 동작 시 권한 승인 버튼
                mobile_click(driver, osType, 'id', element, delayTime)
            except:
                break
    else:
        # try:
        #     sleep(delayTime)
        #     element = "허용"
        #     mobile_click(driver, osType, 'iosId', element, delayTime)  # app실행 시, 푸시 허용 버튼 (only IOS)
        # except:
        #     pass
        try:
            sleep(delayTime)
            element = "허용 안 함"
            mobile_click(driver, osType, 'iosId', element, delayTime)  # app실행 시, 푸시 허용 안 함 버튼 (only IOS)
            sleep(delayTime)
            element = "취소"  # app실행 시, 장치가져오기 취소 버튼
            mobile_click(driver, osType, 'id', element, delayTime)

        except:
            pass

    sleep(middleDelay)

    for loopNum in range(0, 3):
        try:
            element = "android:id/button2"  # app실행 시, 장치가져오기 취소 버튼
            mobile_click(driver, osType, 'id', element, delayTime)

        except:
            sleep(delayTime)
            pass

    sleep(delayTime)


#--------IOS_find--------
# IOS 텍스트 찾기 함수 -> IOS_Read_Setting_Info 사용


def IOS_find(driver, className, targetString):
	elements = driver.find_element(by=AppiumBy.CLASS_NAME, value=className)
	if len(elements) == 0:
		return -1

	if targetString == '':
		return elements

	for element in elements:
		if targetString in element.text:
			return element
	return -1

#--------IOS_Read_Setting_Info--------
# Mobile Plus Setting 정보 읽기

def IOS_Setting_Info(driver, findText):
    global iosSettingInfo
    allSettingCells = IOS_find(driver, 'XCUIElementTypeCell', '')
    time.sleep(1)
    print('finding Text...')
    for cell in allSettingCells:
        # print('=======')
        # elements = cell.find_elements_by_class_name('XCUIElementTypeStaticText')
        elements = cell.find_element(by=AppiumBy.CLASS_NAME, value='XCUIElementTypeStaticText')
        isTarget = False
        for element in elements:
            # print(element.text)
            if isTarget == True:
                #print(element.text)                                                ; 읽어온 텍스트 확인
                iosSettingInfo = element.text
                break
            # if element.text == '듀얼-스트림 재생 우선순위':
            if element.text == findText:
                isTarget = True
                continue
        if isTarget == True:
            break
    time.sleep(1)
    return iosSettingInfo

#--------Android_Read_Setting_Info--------
# Mobile Plus Setting 정보 읽기
def AOS_Setting_Info(driver, findText):
    global aosSettingInfo, aosfindXpath
    time.sleep(1)
    print('finding Text...')
    # textViewList = driver.find_elements_by_class_name('android.widget.TextView')
    # # print(elements)
    #
    # for textViewName in textViewList:
    #     print(textViewName.text)

    try:
        for layoutNum in range(1,30):
            # print('=======')
            isTarget = False
            try:
                for textViewNum in range(1, 3):
                    elements = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[{0}]/android.widget.RelativeLayout/android.widget.TextView[{1}]".format(layoutNum,textViewNum)
                    element = driver.find_element(by=AppiumBy.XPATH, value=elements)
                    # print(textViewNum, element)
                    if isTarget == True:                                                    # isTarget = True 발생한 element값의 다음 값을 받아옴
                        print(element.text)                                                 #읽어온 텍스트 확인
                        aosSettingInfo = element.text
                        if findText in "버전":
                            if aosSettingInfo in "https:/":
                                continue
                            else:
                                break
                        else:
                            break
                    # if element.text == '듀얼-스트림 재생 우선순위':
                    if element.text == findText:
                        isTarget = True
                        aosfindXpath = elements
                        continue
            except:
                pass
            if isTarget == True:
                break
        time.sleep(1)
    except:
        print('Finding Text FAIL')

    return aosSettingInfo, aosfindXpath

def old_AOS_Setting_Info(driver, findText):
    global aosSettingInfo, aosfindXpath
    time.sleep(1)
    print('finding Text...')
    # elements = driver.find_elements_by_class_name('android.widget.TextView')
    # print(elements)
    try:
        for layoutNum in range(1,30):
            # print('=======')
            isTarget = False
            try:
                for textViewNum in range(1, 3):
                    elements = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[{0}]/android.widget.RelativeLayout/android.widget.TextView[{1}]".format(layoutNum,textViewNum)
                    element = driver.find_element(by=AppiumBy.XPATH, value=elements)
                    # print(textViewNum, element)
                    if isTarget == True:                                                    # isTarget = True 발생한 element값의 다음 값을 받아옴
                        print(element.text)                                                 #읽어온 텍스트 확인
                        print(element.className)
                        aosSettingInfo = element.text
                        break
                    # if element.text == '듀얼-스트림 재생 우선순위':
                    if element.text == findText:
                        isTarget = True
                        aosfindXpath = elements
                        continue
            except:
                pass
            if isTarget == True:
                break
        time.sleep(1)
    except:
        print('Finding Text FAIL')

    return aosSettingInfo, aosfindXpath
#--------Change_FenServer--------
# FEN SERVER 변경

def Change_FenServer(driver, osType, fenServer, delayTime):
    element = "com.idis.android.idismobileplus:id/settingButton"                                                        # 설정(톱니바퀴)버튼
    mobile_click(driver, osType, 'id', element, delayTime)

    if osType == "ios":

        driver.implicitly_wait(5)

        sizeX = driver.get_window_size()["width"]  # 가로길이 display size측정
        sizeY = driver.get_window_size()["height"]  # 세로길이 display size측정
        driver.swipe(start_x=sizeX / 2, start_y=sizeY / 2, end_x=sizeX / 2, end_y=sizeY / 2 + sizeY / 10, duration=100)  # FEN 서버 메뉴 위치 복구
        driver.swipe(start_x=sizeX / 2, start_y=sizeY / 2, end_x=sizeX / 2, end_y=sizeY / 2 + sizeY / 10, duration=100)

        findFenServerEditing = IOS_find(driver, 'XCUIElementTypeStaticText', 'FEN 서버 주소')
        findFenServerEditing.click()
        time.sleep(delayTime)

        element = "dvrnames.net"
        driver.driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=element).click()
        time.sleep(delayTime)

        try:
            changeFenServerTextField = IOS_find(driver, 'XCUIElementTypeTextField', '기타')
            changeFenServerTextField.click()
        except:
            changeFenServerTextField = IOS_find(driver, 'XCUIElementTypeTextField', '기타')
            changeFenServerTextField.clear()
        changeFenServerTextField.send_keys(fenServer)
        time.sleep(delayTime)

        saveChangedFenServer = IOS_find(driver, 'XCUIElementTypeButton', '저장')
        saveChangedFenServer.click()
        time.sleep(delayTime)

    else:
        element = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.view.ViewGroup/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/androidx.recyclerview.widget.RecyclerView/android.widget.LinearLayout[5]/android.widget.RelativeLayout/android.widget.TextView[2]"
        # FEN하단 주소
        mobile_click(driver, osType, 'xpath', element, delayTime)

        element = "/hierarchy/android.widget.FrameLayout/android.widget.LinearLayout/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.FrameLayout/androidx.appcompat.widget.LinearLayoutCompat/android.widget.FrameLayout/android.widget.ListView/android.widget.CheckedTextView[3]"
        # FEN서버 주소 팝업창에서 "직접 입력"버튼
        mobile_click(driver, osType, 'xpath', element, delayTime)

        element = "com.idis.android.idismobileplus:id/dialogInputText"                                                  # FEN서버주소 수동입력란
        mobile_send_clear(driver, osType, 'id', element, delayTime)
        time.sleep(delayTime)

        element = "com.idis.android.idismobileplus:id/dialogInputText"
        mobile_send(driver, osType, fenServer, 'id', element, delayTime)

        element = "android:id/button1"  # FEN서버주소 수동입력팝업창 확인버튼
        mobile_click(driver, osType, 'id', element, delayTime)

#--------Regist_IpAddress--------
# IP 주소로 장치 등록하기

def Regist_IpAddress(driver, osType, deviceIp, deviceId, devicePw, delayTime):                           #IP로 장치 추가 함수

    global registFail

    registFail = 1
    writeLog(logFileName, "장치 등록 시작 (%s)" % (deviceIp))

    element = "com.idis.android.idismobileplus:id/addFloatingButton"    #장치추가 +버튼
    mobile_click(driver, osType, 'id', element, delayTime)

    driver.implicitly_wait(10)

    if osType == "android":                                             #IP로 장치등록 버튼 (And, IOS 분기)
        element = "//android.widget.LinearLayout[@content-desc=\"RID_LIST_BTN_ADDIP\"]/android.widget.ImageView"
        mobile_click(driver, osType, 'xpath', element, delayTime)
    else:
        element = "RID_LIST_BTN_ADDIP"                                          #IP로 장치등록 버튼
        mobile_click(driver, osType, 'id', element, delayTime)

    element = "com.idis.android.idismobileplus:id/siteAddAddressEditText"       #IP입력란
    inputText = "%s" % (deviceIp)
    mobile_send(driver, osType, inputText, 'id', element, delayTime)

    driver.implicitly_wait(10)
    time.sleep(5 * delayTime)

    element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"        #다음 버튼 클릭
    mobile_click(driver, osType, 'id', element, delayTime)

    driver.implicitly_wait(10)
    time.sleep(5 * delayTime)

    element = "com.idis.android.idismobileplus:id/siteAddPasswordEditText"
    mobile_element_displayed(driver, osType, 'id', element)

    time.sleep(5*delayTime)

    if MobileBasicAct.displayedElement == "False":
        writeLog(logFileName, "ID 입력창 발생 안함[%s]" % (deviceIp))
        if osType == "ios":
            element = "확인"                                                                                              # 검색 실패 경고창 확인
            mobile_click(driver, osType, 'id', element, delayTime)
        element = "com.idis.android.idismobileplus:id/commonTopBackButton"  # 뒤로 가기 클릭 (IOS는 취소 버튼)
        #element = "장치 추가_뒤로가기_취소 버튼"
        mobile_click(driver, osType, 'id', element, delayTime)
        registFail = 1
    else:                                                                                                   # IP 입력 후 다음 버튼 생성시 진행
        for x in range(2):                                                                                  #IP입력 후, 대기시간 최대 15초
            element = "com.idis.android.idismobileplus:id/siteAddIdEditText"                                # ID 입력란
            mobile_element_displayed(driver, osType, 'id', element)
            if MobileBasicAct.displayedElement == "True":
                time.sleep(delayTime)
                break
            else:
                time.sleep(delayTime)                                                                          # 최대 15초 대기
                writeLog(logFileName, "IP장치 {0}회 실패" .format(x))
                continue
        try:                                                                                                # IP넣고 다음창으로 이동한지 여부
            element = "com.idis.android.idismobileplus:id/siteAddIdEditText"
            mobile_send(driver, osType, deviceId, 'id', element, delayTime)

        except:                                                                                             # IP로 접속 실패
            element = "com.idis.android.idismobileplus:id/commonTopBackButton"                              # 뒤로 가기 클릭 (IOS는 취소 버튼)
            mobile_click(driver, osType, 'id', element, delayTime)
            writeLog(logFileName, "IP 주소 등록: 장치 접속 불가")

        else:
            element = "com.idis.android.idismobileplus:id/siteAddPasswordEditText"                          # 패스워드 입력
            mobile_click(driver, osType, 'id', element, delayTime)                                          # 패스워드입력란 클릭 (바로 send시 에러뜸)

            element = "com.idis.android.idismobileplus:id/siteAddPasswordEditText"
            mobile_element_displayed(driver, osType, 'id', element)
            if MobileBasicAct.displayedElement == "True":
                mobile_send(driver, osType, devicePw, 'id', element, delayTime)                                         # 패스워드 입력
                element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"                                    # 다음 버튼
                mobile_click(driver, osType, 'id', element, delayTime)

                element = "com.idis.android.idismobileplus:id/siteAddSiteNameEditText"                                     # 장치이름
                mobile_element_displayed(driver, osType, 'id', element)
                if MobileBasicAct.displayedElement == "True":                                                            # 패스워드가 맞을 경우
                    mobile_click(driver, osType, 'id', element, delayTime)
                    element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"
                    mobile_click(driver, osType, 'id', element, delayTime)

                    element = "com.idis.android.idismobileplus:id/addFloatingButton"
                    # driver.find_element_by_id(element)
                    mobile_element_displayed(driver, osType, 'id', element)
                    if MobileBasicAct.displayedElement == "True":
                        registFail = 0
                        writeLog(logFileName, "등록 완료")
                    else:
                        if osType == "ios":
                            element = "확인"  # ios 중복 경고 토스트 "확인" 버튼 클릭
                            mobile_click(driver, osType, 'id', element, delayTime)
                            element = "장치_추가_취소"
                            mobile_click(driver, osType, 'id', element, delayTime)
                        else:
                            element = "com.idis.android.idismobileplus:id/commonTopBackButton"                              # 뒤로 가기 클릭 (IOS는 완료 버튼)
                            mobile_click(driver, osType, 'id', element, delayTime)
                        writeLog(logFileName, "IP 주소 등록: 중복된 장치 추가")
                else:
                    writeLog(logFileName, "장치 비밀번호 일치 안함")
                    if osType == "ios":
                        element = "확인"
                        mobile_click(driver, osType, 'id', element, delayTime)
                        element = "장치_추가_취소"
                        mobile_click(driver, osType, 'id', element, delayTime)
                    else:
                        pass
                    element = "com.idis.android.idismobileplus:id/commonTopBackButton"  # 뒤로 가기 클릭
                    mobile_click(driver, osType, 'id', element, delayTime)
            else:
                pass
    return registFail

#--------Search_DeviceName--------
# 리스트에서 장치 이름 찾기

def List_Search_Deivce(driver, osType, deviceName, delayTime):
    element = "com.idis.android.idismobileplus:id/titleSiteSearchButton"                                        # 검색(돋보기)
    mobile_click(driver, osType, 'id', element, delayTime)

    element = "com.idis.android.idismobileplus:id/listSearchEditText"                                           # 장치 검색 창
    mobile_click(driver, osType, 'id', element, delayTime)
    mobile_send(driver, osType, deviceName, 'id', element, delayTime)

    time.sleep(3)
    sizeX = driver.get_window_size()["width"]  # 가로길이 display size측정
    sizeY = driver.get_window_size()["height"]  # 세로길이 display size측정
    driver.swipe(start_x=sizeX / 2, start_y=sizeY / 2, end_x=sizeX / 2, end_y=sizeY / 2 + sizeY / 10, duration=100)     # 상단으로 이동

    time.sleep(3)

#--------Detail_Connect--------
# 상세 정보 페이지로 접속하기
#connectType    접속 타입: 1) "Live", 2)"Play", 3)"Connect"
#deviceName     접속하고자 하는 장치 이름(리스트 검색)

# ex> Detail_Connect(driver, "ios", "Connect", "10.0.18.111", delayTime)

def Detail_Connect(driver, osType, connectType,deviceName, delayTime):                                                                    ##
    global connectSuccess
    connectSuccess = 0

    List_Search_Deivce(driver, osType, deviceName, delayTime)                                                           # 장치 이름 검색
    time.sleep(middleDelay)

    element = "com.idis.android.idismobileplus:id/siteDetailButton"                                                     # 장치 상세정보 페이지로 이동
    mobile_click(driver, osType, 'id', element, delayTime)

    if connectType == "Connect":
        element = "com.idis.android.idismobileplus:id/detailiNEXConnectButton"                                          # Connect 접속버튼클릭
    elif connectType == "Play":
        element = ""
    else:
        element = "com.idis.android.idismobileplus:id/detailWatchButton"                                                # Live접속버튼클릭

    mobile_click(driver, osType, 'id', element, delayTime)
    time.sleep(longDelay)

    for x in range(2):
        if connectType == "Connect":                                                                                    # ios의 경우 푸시체크 버튼 확인
            if osType == "ios":
                element = "iNEX푸시체크"
            else:
                element = "com.idis.android.idismobileplus:id/inexServiceViewPager"
        else:
            element = "com.idis.android.idismobileplus:id/screenTopBackButton"                                          ## 상단 Live 뒤로 가기 버튼 확인

        mobile_element_displayed(driver, osType, 'id', element)
        time.sleep(longDelay)

        if MobileBasicAct.displayedElement == "True":
            if osType == "android":
                element = "com.idis.android.idismobileplus:id/loadingCancelButton"
                mobile_element_displayed(driver, osType, 'id', element)
                if MobileBasicAct.displayedElement == "False":
                    connectSuccess = 1
                    break
                else:
                    mobile_click(driver, osType, 'id', element, delayTime)
            else:
                connectSuccess = 1
                break
        else:
            time.sleep(delayTime)
    return connectSuccess

#--------Regist_iNEX--------
# iNEX 등록하기

def Regist_iNEX(driver, osType, deviceName, deviceIp, deviceId, devicePw, delayTime):
    global registFail
    registFail = 1
    middleDelay = 3 * delayTime

    element = "com.idis.android.idismobileplus:id/addFloatingButton"                                                    # 장치추가 +버튼
    mobile_click(driver, osType, 'id', element, delayTime)

    element = "com.idis.android.idismobileplus:id/siteAddAddressButtonLayout"                                           # IP로 장치등록 버튼
    mobile_click(driver, osType, 'id', element, delayTime)

    element = "com.idis.android.idismobileplus:id/siteAddAddressEditText"                                               # IP입력란
    mobile_send(driver, osType, deviceIp, 'id', element, delayTime)

    element = "com.idis.android.idismobileplus:id/siteAddiNEXCheckBox"                                                  # iNEX check box
    mobile_click(driver, osType, 'id', element, delayTime)

    element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"                                                # 다음 버튼 클릭
    mobile_click(driver, osType, 'id', element, delayTime)
    time.sleep(middleDelay)
    for x in range(2):                                                                                                  # IP입력 후, 대기시간이 얼마나 걸릴지 몰라서 최대 15초 대기
        try:
            element = "com.idis.android.idismobileplus:id/siteAddIdEditText"                                            # ID넣는 곳
            driver.find_element(by=AppiumBy.ID, value=element)
            time.sleep(delayTime)
            break

        except:
            time.sleep(middleDelay)
            time.sleep(middleDelay)
            # writeLog(logFileName, "iNEX등록 {0}회 실패".format(x))
            continue

    try:                                                                                                                # IP넣고 다음창으로 이동한지 여부
        element = "com.idis.android.idismobileplus:id/siteAddIdEditText"                                                # ID입력
        mobile_send(driver, osType, deviceId, 'id', element, delayTime)

    except:                                                                                                             # iNEX접속 실패
        element = "com.idis.android.idismobileplus:id/commonTopBackButton"                                              # 뒤로 가기 클릭
        mobile_click(driver, osType, 'id', element, delayTime)

    else:
        element = "com.idis.android.idismobileplus:id/siteAddPasswordEditText"                                          # 패스워드 입력
        mobile_click(driver, osType, 'id', element, delayTime)                                                          # 패스워드입력란 클릭안하고 바로 send시 에러뜸

        element = "com.idis.android.idismobileplus:id/siteAddPasswordEditText"                                          # 패스워드 입력
        mobile_send(driver, osType, devicePw, 'id', element, delayTime)
        element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"                                            # 다음 버튼
        mobile_click(driver, osType, 'id', element, delayTime)

        # element = "com.idis.android.idismobileplus:id/siteAddSiteNameEditText"                                          # 장치이름
        # mobile_send(driver, osType, deviceName, 'id', element, delayTime)
        element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"                                            # 다음버튼
        mobile_click(driver, osType, 'id', element, delayTime)

        try:                                                                                                            # 정상등록
            element = "com.idis.android.idismobileplus:id/addFloatingButton"
            mobile_element_displayed(driver, osType, 'id', element)
            if MobileBasicAct.displayedElement == "True":
                registFail = 0
                writeLog(logFileName, "iNEX 등록 완료")
        except:                                                                                                         # 이미 같은 이름의 장치가 있는 경우
            element = "com.idis.android.idismobileplus:id/commonTopBackButton"                                          # 뒤로 가기 클릭
            mobile_click(driver, osType, 'id', element, delayTime)
        time.sleep(middleDelay)

    return registFail

#--------FrontButton_Connect--------
# Front 버튼으로 연결하기
#connectType    접속 타입: 1) "Live", 2)"Search", 3)"Connect"
#deviceName     접속하고자 하는 장치 이름(리스트 검색)

# ex> FrontButton_Connect(driver, "ios", "Live", "10.0.18.111", delayTime)

def FrontButton_Connect(driver, osType, connectType, deviceName, delayTime):
    global connectSuccess
    connectSuccess = 0

    List_Search_Deivce(driver, osType, deviceName, delayTime)  # 장치 이름 검색
    time.sleep(middleDelay)

    if connectType == "Connect":
        element = "com.idis.android.idismobileplus:id/siteiNEXConnectButton"  # Connect 접속버튼클릭
    elif connectType == "Search":
        element = "com.idis.android.idismobileplus:id/sitePlayButton"  # Search 접속버튼클릭
    else:
        element = "com.idis.android.idismobileplus:id/siteLiveButton"  # Live 접속버튼클릭

    mobile_click(driver, osType, 'id', element, delayTime)
    time.sleep(longDelay)

    for x in range(2):                                                                                                  # 확인 가능 ID가 나타날 때까지 최대 10초 대기
        if connectType == "Connect":                                                                                    # iNEX의 경우 "푸시체크" 버튼
            if osType == "ios":
                element = "iNEX푸시체크"
            else:
                element = "com.idis.android.idismobileplus:id/inexServiceViewPager"  # iNEX Page??
        else:
            if osType == "ios":
                element = "뒤로가기_목록"
            else:
                element = "com.idis.android.idismobileplus:id/screenTopBackButton"                                      ## 상단 Live "뒤로 가기 버튼" 확인

        mobile_element_displayed(driver, osType, 'id', element)
        time.sleep(longDelay)

        if MobileBasicAct.displayedElement == "True":
            if osType == "android":
                element = "com.idis.android.idismobileplus:id/loadingCancelButton"
                mobile_element_displayed(driver, osType, 'id', element)
                if MobileBasicAct.displayedElement == "False":
                    connectSuccess = 1
                    break
                else:
                    mobile_click(driver, osType, 'id', element, delayTime)
            else:
                connectSuccess = 1
                break
        else:
            time.sleep(longDelay)
    return connectSuccess


#--------Read_iNEX_Device--------
# iNEX 내 등록장치 리스트 확인
# iNEX 장치 읽어온 후 iNEX ListFile에 쓰기

def Read_iNEX_Device(driver, osType, iNEXListFile, delayTime):
    writeReport(iNEXListFile, "iNEX 등록 장치 리스트")
    writeReport(iNEXListFile, "-----------------")
    if osType == "ios":
        allSettingCells = IOS_find(driver, 'XCUIElementTypeTable', '')
        time.sleep(delayTime)
        print('finding Text...')
        for cell in allSettingCells:
            deviceList = cell.find_element(by=AppiumBy.CLASS_NAME, value='XCUIElementTypeStaticText')
            for title in deviceList:
                print(title.text)
                registDevice = title.text
                writeReport(iNEXListFile, ">>{}".format(registDevice))                                                  # iNEX장치리스트 입력
    else:
        try:
            deviceList = driver.find_element(by=AppiumBy.ID, value="com.idis.android.idismobileplus:id/inexDeviceTitle")               # resource ID로 받아온 컴포넌트를 전부받아옴
            for title in deviceList:
                registDevice = title.text
                writeReport(iNEXListFile, ">>{}".format(registDevice))
        except:
            pass
    writeReport(iNEXListFile, "-----------------")
    time.sleep(delayTime)


#--------Regist_deviceInfo--------
def Regist_deviceInfo(driver, osType, registInfo, deviceId, devicePw, delayTime):

    global registFail
    registFail = 1
    middleDelay = 3 * delayTime

    for loopNum in range(0,2):
        time.sleep(middleDelay)
        for loopIndex in range(0,10):
            element = "com.idis.android.idismobileplus:id/siteAddPasswordEditText"  # PW 입력창이 나타났는지 확인
            mobile_element_displayed(driver, osType, 'id', element)

            time.sleep(middleDelay)
            print("등록대기중...")
            if MobileBasicAct.displayedElement == "False":
                pass
            else:
                break
        if MobileBasicAct.displayedElement == "False":
            time.sleep(middleDelay)
            time.sleep(middleDelay)
            logText = "[warning] PW 입력창 미발생:"
            writeLog(logFileName, logText)
            element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"                                        # 다음 버튼
            mobile_click(driver, osType, 'id', element, delayTime)
        else:
            pass

    if MobileBasicAct.displayedElement == "False":
        writeLog(logFileName, "장치 검색 안됨: 패스워드 입력창 발생 안함")
    else:                                                                                                               # 장치 등록 정보 입력 후 PW창 생성시 진행
        time.sleep(middleDelay)
        element = "com.idis.android.idismobileplus:id/siteAddIdEditText"  # ID 입력란
        mobile_element_displayed(driver, osType, 'id', element)
        if MobileBasicAct.displayedElement == "True":
            time.sleep(delayTime)
        else:
            time.sleep(middleDelay)  # 최대 15초 대기
            # writeLog(logFileName, "장치등록 {0}회 실패".format(x))

            if osType == "ios":
                element = "확인"
                mobile_click(driver, osType, 'id', element, delayTime)
                element = "장치_추가_취소"
                mobile_click(driver, osType, 'id', element, delayTime)
            else:
                pass
            element = "com.idis.android.idismobileplus:id/commonTopBackButton"  # 뒤로 가기 클릭
            mobile_click(driver, osType, 'id', element, delayTime)

        try:  # 장치 등록 정보 입력 후 다음창으로 이동한지 여부
            element = "com.idis.android.idismobileplus:id/siteAddIdEditText"
            mobile_send(driver, osType, deviceId, 'id', element, delayTime)

        except:  # 장치 등록 정보로 접속 실패
            element = "com.idis.android.idismobileplus:id/commonTopBackButton"  # 뒤로 가기 클릭 (IOS는 취소 버튼)
            mobile_click(driver, osType, 'id', element, delayTime)
            writeLog(logFileName, "주소 등록: 장치 접속 불가 [%s]" % (registInfo))

        else:
            element = "com.idis.android.idismobileplus:id/siteAddPasswordEditText"  # 패스워드 입력
            mobile_click(driver, osType, 'id', element, delayTime)  # 패스워드입력란 클릭 (바로 send시 에러뜸)

            element = "com.idis.android.idismobileplus:id/siteAddPasswordEditText"
            mobile_element_displayed(driver, osType, 'id', element)
            if MobileBasicAct.displayedElement == "True":
                mobile_send(driver, osType, devicePw, 'id', element, delayTime)  # 패스워드 입력
                element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"  # 다음 버튼
                mobile_click(driver, osType, 'id', element, delayTime)

                for loopIndex in range(0,10):
                    element = "com.idis.android.idismobileplus:id/siteAddSiteNameEditText"  # 장치이름
                    mobile_element_displayed(driver, osType, 'id', element)
                    if MobileBasicAct.displayedElement == "True":
                        break
                    else:
                        sleep(middleDelay)

                if MobileBasicAct.displayedElement == "True":                                                           # 패스워드가 맞을 경우
                    mobile_click(driver, osType, 'id', element, delayTime)
                    element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"
                    mobile_click(driver, osType, 'id', element, delayTime)

                    element = "com.idis.android.idismobileplus:id/addFloatingButton"
                    # driver.find_element_by_id(element)
                    mobile_element_displayed(driver, osType, 'id', element)
                    if MobileBasicAct.displayedElement == "True":
                        registFail = 0
                        writeLog(logFileName, "등록 완료")
                    else:
                        if osType == "ios":
                            element = "확인"  # 중복 경고 토스트 "확인" 버튼 클릭
                            mobile_click(driver, osType, 'id', element, delayTime)
                            element = "장치_추가_취소"
                            mobile_click(driver, osType, 'id', element, delayTime)
                        else:
                            element = "com.idis.android.idismobileplus:id/commonTopBackButton"  # 뒤로 가기 클릭 (IOS는 완료 버튼)
                            mobile_click(driver, osType, 'id', element, delayTime)
                        writeLog(logFileName, "주소 등록: 중복된 장치 존재 [%s]" % (registInfo))
                else:
                    writeLog(logFileName, "장치 비밀번호 일치 안함")
                    if osType == "ios":
                        element = "확인"
                        mobile_click(driver, osType, 'id', element, delayTime)
                        element = "장치_추가_취소"
                        mobile_click(driver, osType, 'id', element, delayTime)
                    else:
                        pass
                    element = "com.idis.android.idismobileplus:id/commonTopBackButton"  # 뒤로 가기 클릭
                    mobile_click(driver, osType, 'id', element, delayTime)
            else:
                pass
    return registFail

#--------Regist_Fen--------
#Regist_iNEX(driver, osType, deviceName, deviceIp, deviceId, devicePw, delayTime)

def Regist_Fen_Name(driver, osType, fenName, deviceId, devicePw, delayTime):

    global registFail
    registFail = 1
    middleDelay = 3 * delayTime

    element = "com.idis.android.idismobileplus:id/addFloatingButton"                                                    #장치등록 +버튼
    mobile_click(driver, osType, 'id', element, delayTime)

    if osType == "ios":
        element = "RID_LIST_BTN_ADDFEN"                                                                                 #FEN 선택 ID / IOS, Android 일치 필요
        mobile_click(driver, osType, 'id', element, delayTime)
    else:
        element = "//android.widget.LinearLayout[@content-desc=\"RID_LIST_BTN_ADDFEN\"]/android.widget.ImageView"       #FEN선택 Android Xpath 사용
        mobile_click(driver, osType, 'xpath', element, delayTime)

    element = "com.idis.android.idismobileplus:id/siteAddFENEditText"                                                   #FEN name입력란
    mobile_send(driver, osType, fenName, 'id', element, delayTime)

    sleep(middleDelay)
    element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"                                                #다음 버튼
    mobile_click(driver, osType, 'id', element, delayTime)

    registInfo = fenName
    Regist_deviceInfo(driver, osType, registInfo, deviceId, devicePw, delayTime)

#--------Detail_Change_Device_Name--------

def Detail_Change_Device_Name(driver, osType,deviceName, delayTime):

    List_Search_Deivce(driver, osType, deviceName, delayTime)

    element = "com.idis.android.idismobileplus:id/siteDetailButton"                                                     # 장치 상세정보 페이지로 이동
    mobile_click(driver, osType, 'id', element, delayTime)

    element = "com.idis.android.idismobileplus:id/detailETCButton"                                                      # 장치 3개의 점 클릭
    mobile_click(driver, osType, 'id', element, delayTime)

    if osType == "ios":
        element = "이름 수정"
        mobile_click(driver, osType, 'id', element, delayTime)
    else:
        element = "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[1]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView"
    # 이름수정
        mobile_click(driver, osType, 'xpath', element, delayTime)

    element = "장치 수정_이름란"
    mobile_click(driver, osType, 'action', element, delayTime)

    # element = "com.idis.android.idismobileplus:id/dialogInputText"                                                      # 이름 넣는 곳
    # mobile_click(driver, osType, 'id', element, delayTime)


    mobile_send_clear(driver, osType, 'action', element, delayTime)
    inputText = "이름변경test1@"
    mobile_send(driver, osType, inputText, 'action', element, delayTime)

    # element = "android:id/button1"                                                                                      # 확인버튼
    # mobile_click(driver, osType, 'id', element, delayTime)
    #
    # driver.save_screenshot(folderPath + "\\장치이름 변경({0}).png" .format(inputText))
    # writeReport(reportFileName, "장치이름 변경 - 성공[캡쳐]")
    #
    # element = "com.idis.android.idismobileplus:id/commonTopBackButton"                                                  # 상세정보창에서 위쪽 뒤로가기 버튼
    # mobile_click(driver, osType, 'id', element, delayTime)
    # sleep(shortDelay)
    #
    # element = "com.idis.android.idismobileplus:id/listSearchCloseButton"                                                 # 돋보기 닫기 버튼
    # mobile_click(driver, osType, 'id', element, delayTime)


#--------Find_MaxChannel--------
# Live 접속이 된 상태에서 최대 채널 개수 찾기

def Find_MaxChannel(driver, osType, delayTime):
    global maxChannelNum, channelLoop, ChannelFail
    ChannelFail = 0
    channelLoop = 1
    maxChannelNum = 1
    while True:
        sleep(delayTime)
        if channelLoop == 1:                                                                                              # 최초 x값이 1에서 시작
            try:
                # print("채널1 Test")
                if osType == "ios":
                    element = "CameraOsdView0"
                    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=element)
                else:
                    print("AOS 최대 장치 개수 파악")
                    element = "com.idis.android.idismobileplus:id/cameraOSDView01"                                       # 채널 스크린 번호(8ch이하 제품)
                    driver.find_element(by=AppiumBy.ID, value=element)
                channelLoop = channelLoop + 1                                                                              # channelLoop 값 2로 변경
                maxChannelNum = maxChannelNum * 4                                                                          # 1ch다음은 4ch이므로 (1 -> 4 채널 변경)
                continue
            except:
                logText = "[Error] Max 채널 확인: 채널1, 스크린 확인 실패"
                writeLog(logFileName, logText)
                ChannelFail = 1
                break

        elif 2 < maxChannelNum < 10:
            try:
                # print("채널2 테스트")
                if osType == "ios":
                    findNum = maxChannelNum - 1
                    # print("CameraOsdView{0}".format(findNum))
                    element = "CameraOsdView{0}".format(findNum)
                    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=element)
                else:
                    element = "com.idis.android.idismobileplus:id/cameraOSDView0{0}".format(maxChannelNum)                 # 채널 스크린 번호(8ch이하 제품)
                    driver.find_element(by=AppiumBy.ID, value=element)
                channelLoop = channelLoop + 1                                                                                       # X 값 3로 변경
                maxChannelNum = maxChannelNum * 2                                                                                     # 4ch이상 부터는 x2로 채널 증가 (4 -> 8 채널 변경)
                continue

            except:
                maxChannelNum = maxChannelNum / 2                                                                                     # 다음 채널이 없을 경우, ch/2로 하여 현재 채널을 의미하도록
                logText = "Layout {}ch장치".format(maxChannelNum)
                writeLog(logFileName, logText)
                break

        elif maxChannelNum > 10:
            try:
                if osType == "ios":
                    findNum = maxChannelNum - 1
                    element = "CameraOsdView{0}".format(findNum)
                    driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=element)
                else:
                    element = "com.idis.android.idismobileplus:id/cameraOSDView{0}".format(maxChannelNum)  # 채널 스크린 번호(8ch이하 제품)
                    driver.find_element(by=AppiumBy.ID, value=element)
                channelLoop = channelLoop + 1
                maxChannelNum = maxChannelNum * 2
                continue

            except:
                maxChannelNum = maxChannelNum / 2
                logText = "Layout {}ch장치".format(maxChannelNum)
                writeLog(logFileName, logText)
                break
    return maxChannelNum, channelLoop

#--------Move_To_Camera--------
# Live 접속이 된 상태에서 채널 변경
# moveToCamNum = 0
# moveCamStatus = 0
def Move_To_Camera(driver, osType, delayTime):

    global moveToCamNum
    global moveCamStatus
    moveCamStatus = 0
    moveToCamNum = 0
    shortDelay = 3*delayTime
    # Live 접속 상태
    element = "com.idis.android.idismobileplus:id/screenLayoutButton"                                                   # Layout버튼 (1채널로 변경)
    mobile_click(driver, osType, 'id', element, delayTime)

    element = "com.idis.android.idismobileplus:id/screenCameraButton"                                                   # 카메라 이동 버튼
    mobile_click(driver, osType, 'id', element, delayTime)
    time.sleep(delayTime)

    if osType == "ios":
        layout = driver.find_element(by=AppiumBy.CLASS_NAME, value='XCUIElementTypeCell')
    else:
        layout = driver.find_element(by=AppiumBy.CLASS_NAME, value='android.widget.TextView')                                          # className으로 받아온 컴포넌트들 전부를 검사
    noCamStr_list = ['비활성화', '카메라 선택']
    loopNum = 1
    for temp in layout:
        moveToCamNum = temp.text                                                                                        # 비활성화 단어 들어가 있는지 확인
        if noCamStr_list[0] not in moveToCamNum and noCamStr_list[1] not in moveToCamNum:                               # 비활성화 and 카메라선택이 안들어간 문구를 클릭하여 이동(위에서부터 서치)
            if loopNum == 2:
                temp.click()
                sleep(shortDelay)
                moveCamStatus = 1
                break
            else:
                loopNum += 1
        else:
            continue
    time.sleep(shortDelay)
    return moveCamStatus, moveToCamNum

#--------Digital_Zoom--------
# Live 접속이 된 상태에서 디지털 줌

def Digital_Zoom(driver, osType, action, delayTime):

    shortDelay = 3*delayTime
    # Live 접속 상태
    sleep(shortDelay)
    x = driver.get_window_size()["width"]                                                                               # 가로길이 display size측정
    y = driver.get_window_size()["height"]                                                                              # 세로길이 display size측정

    osdId = 'CameraOsdView0'
    if osType == "ios":
        sleep(3*delayTime)
        touchAction1 = TouchAction(driver)
        touchAction2 = TouchAction(driver)
        multiAction = MultiAction(driver)

        fullOsdView = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='OsdView')
        size = fullOsdView.size
        width = size['width']
        height = size['height']

        if action == "ZoomIn":
            print("줌인 동작")
            touchAction1.long_press(fullOsdView, width / 2, height / 2).wait(250).move_to(fullOsdView, width / 2 - 100, height / 2)
            touchAction2.long_press(fullOsdView, width / 2, height / 2).wait(250).move_to(fullOsdView, width / 2 + 100, height / 2)

        else:
            print("줌아웃 동작")
            touchAction1.long_press(fullOsdView, width / 2, height / 2).wait(250).move_to(fullOsdView, width / 4 + 100, height / 2)
            touchAction2.long_press(fullOsdView, width / 2, height / 2).wait(250).move_to(fullOsdView, width / 4 - 100, height / 2)

        multiAction.add(touchAction1)
        multiAction.add(touchAction2)
        multiAction.perform()

        sleep(3*delayTime)

    else:
        if action == "ZoomIn":
            print("줌인 동작")
            leftAction = TouchAction()
            leftAction.press(x=x*0.4, y=y*0.4)                                                                          # 왼손 Zoom-In 초기 터치 부분
            leftAction.move_to(x=x*0.2, y=y*0.35)                                                                       # 왼손 Zoom-In하고자하는 좌표
            leftAction.release()

            rightAction = TouchAction()
            rightAction.press(x=x*0.6, y=y*0.4)                                                                          # 왼손 Zoom-In 초기 터치 부분
            rightAction.move_to(x=x*0.8, y=y*0.45)                                                                       # 왼손 Zoom-In하고자하는 좌표
            rightAction.release()

            zoomIn = MultiAction(driver)
            zoomIn.add(leftAction, rightAction)                                                                             # 왼손, 오른손더함
            zoomIn.perform()                                                                                                # 왼손, 오른손 Zoom-In 실행

        else:
            print("줌아웃 동작")
            leftAction = TouchAction()
            rightAction = TouchAction()

            leftAction.press(x=x * 0.2, y=y * 0.35)                                                                         # 왼손 Zoom-Out 초기 터치 부분
            leftAction.move_to(x=x * 0.4, y=y * 0.4)                                                                        # 왼손 Zoom-Out하고자하는 좌표
            leftAction.release()

            rightAction.press(x=x * 0.9, y=y * 0.45)                                                                        # 오른손 Zoom-Out 초기 터치 부분
            rightAction.move_to(x=x * 0.5, y=y * 0.35)                                                                       # 오른손 Zoom-Out하고자하는 좌표
            rightAction.release()

            zoomOut = MultiAction(driver)
            zoomOut.add(leftAction, rightAction)
            zoomOut.perform()
    sleep(shortDelay)

#-----------------Live Search 상단 메뉴 선택-----------------------

def Select_View_Menu(driver, osType, viewMenuName, delayTime):

    global selectMenuError
    # Live 또는 Search 접속 상태 전제
    # print("Select_View_Menu 동작")
    selectMenuError = 0

    element = "com.idis.android.idismobileplus:id/screenTopETCButton"                                                   # Live 상단 3개의 점
    mobile_click(driver, osType, 'id', element, delayTime)

    sleep(delayTime)
    if osType == "ios":
        element = viewMenuName
        mobile_click(driver, osType, 'id', element, delayTime)
        if MobileBasicAct.clickSearchFail == 1:
            selectMenuError = 1
        else:
            pass
        sleep(shortDelay)
        element = "승인"
        mobile_click(driver, osType, 'id', element, delayTime)
        sleep(shortDelay)
        element = "확인"
        mobile_click(driver, osType, 'id', element, delayTime)
    else:                                                                                                               # AOS 동작
        try:
            for menuCount in range(1, 10):
                element = "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[{}]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView".format(
                    menuCount)
                menuText = driver.find_element(by=AppiumBy.XPATH, value=element).get_attribute('text')                                      # Element의 Text를 받아옴
                if menuText == viewMenuName:
                    mobile_click(driver, osType, 'xpath', element, delayTime)
                    break
                else:
                    pass
        except:
            selectMenuError = 1
    if selectMenuError == 0:
        # print("{} 클릭".format(viewMenuName))
        pass
    else:
        logText = "{} 클릭 Error".format(viewMenuName)
        writeLog(logFileName, logText)
    return selectMenuError

#-----------------find_Single_Screen-----------------------
singleScreen = 0                                                                                                         # 단일 화면 확인 변수
def Find_Single_Screen(driver, osType, delayTime):
    global singleScreen
    viewMenuName = "스마트 필터"
    element = "com.idis.android.idismobileplus:id/screenTopETCButton"  # Live 상단 3개의 점
    mobile_click(driver, osType, 'id', element, delayTime)
    if osType == "ios":
        sleep(3*delayTime)
        mobile_element_displayed(driver, osType, 'id', viewMenuName)
        if MobileBasicAct.displayedElement == "True":
            singleScreen = 1
        else:
            singleScreen = 0
    else:
        try:
            for menuCount in range(1, 10):
                element = "/hierarchy/android.widget.FrameLayout/android.widget.FrameLayout/android.widget.ListView/android.widget.LinearLayout[{}]/android.widget.LinearLayout/android.widget.RelativeLayout/android.widget.TextView".format(
                    menuCount)
                menuText = driver.find_element(by=AppiumBy.XPATH, value=element).get_attribute('text')                                      # Element의 Text를 받아옴
                print(menuText)
                if menuText == viewMenuName:
                    singleScreen = 1
                    break
                else:
                    singleScreen = 0
        except:
            singleScreen = 0

    # if osType == "ios":
    #

    sizeX = driver.get_window_size()["width"]  # 가로길이 display size측정
    sizeY = driver.get_window_size()["height"]  # 세로길이 display size측정
    TouchAction(driver).press(x=sizeX * 0.5, y=sizeY * 0.3).release().perform()

    # else:
    #     element = "com.idis.android.idismobileplus:id/screenTopTitle"
    #     mobile_click(driver, osType, 'id', element, delayTime)
    #
    #     # singleTap = TouchAction(driver)
    #     # topName = "com.idis.android.idismobileplus:id/screenTopTitle"
    #     # singleTap.tap(topName)
    #     # singleTap.perform()

    return singleScreen

def main():

    delayTime = 1
    # osType = "ios"
    # Desired_Cap = {
    #     "deviceName": "RND5의 iPhone",  # 실제 장치 이름
    #     "platformVersion": "12.4.8",  # 실제 장치 OS 버전
    #     "platformName": "ios",  # 실제 장치 플랫폼
    #     "app": "/Users/jungtong/Documents/Appium_ipa/IDIS/IDIS.ipa",  # 실제 장치에서 실행할 앱 파일
    #     # "app": "/Users/jungtong/Documents/Appium_ipa/IDIS/IDIS_1.1.1_98.ipa",
    #     "automationName": "XCUITest",  # 변경 X
    #     "udid": "93ca7786b0827f2bb118f26126a02ee4ab12a379",  # 실제 장치 고유 id
    #     "xcodeOrgId": "26B93MEUCK",  # 개발자 계정 고유 id
    #     "xcodeSigningId": "iPhone Developer",  # 변경 X
    #     "wƒdaBaseUrl": "http://192.168.0.3:8100",  # 실제 장치 ip
    #     "appPushTimeout": 60000,  # 타임아웃 설정 값
    #     "noReset": "true"
    # }
    osType = "android"
    mobileDeviceVersion = "11"
    Desired_Cap = {
        "platformName": "{}".format(osType),
        "platformVersion": "{}".format(mobileDeviceVersion),
        "deviceName": "Gallaxy 10",
        "app": "C:\\MobileAppTest\\workspace\\apk\\app-idisplus-211007.apk",                                            # PC에 저장된 apk경로
        # "app": "C:\\MobileAppTest\\workspace\\apk\\app-idisplus-eum.apk",
        "automationName": "Appium",
        "udid": "R3CM80KQK5T",
        "newCommandTimeout": 60000,
        "appPackage": "com.idis.android.idismobileplus",
        "appActivity": "com.idis.android.rasmobile.splash.activity.SplashActivity",
        "noReset": True                                                                                                 # 앱초기화 안함.
    }

    driver = webdriver.Remote("Http://localhost:4723/wd/hub", Desired_Cap)
    fenNameText = "mobile_exxo"
    FrontButton_Connect(driver, osType, "Live", fenNameText, delayTime)
    # Find_MaxChannel(driver, osType, delayTime)
    for loopNum in range(0, 4):
        Find_Single_Screen(driver, osType, delayTime)                                                     # 단일 화면 찾기
        if singleScreen == 1:
            print("-> 단일 화면 변경 완료")
            break
        else:
            element = "com.idis.android.idismobileplus:id/screenLayoutButton"                                           # Layout 변경
            mobile_click(driver, osType, 'id', element, delayTime)
    # element = "com.idis.android.idismobileplus:id/screenLayoutButton"  # Layout버튼
    # mobile_click(driver, osType, 'id', element, delayTime)

    # viewMenuName = "화면 비율에 맞추기"
    #
    # Select_View_Menu(driver, osType, viewMenuName, delayTime)

    Digital_Zoom(driver, osType, 'ZoomIn', delayTime)
    Digital_Zoom(driver, osType, 'ZoomOut', delayTime)
    sleep(middleDelay)
    pass


if __name__ == "__main__":
    main()
