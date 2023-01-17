#-*- coding:utf-8 -*-

import os
import os.path
from time import sleep
from datetime import *                                                          # 시간 측정 관련 라이브러ㅆ
from MobileBasicAct import *
from MobilePlusAct import *
from MobileWebLink import *
from appium.webdriver.common.touch_action import TouchAction                    # long key쓰기 위한 라이브러리
from appium.webdriver.common.multi_action import MultiAction                    # Pinch IN/OUT을 위한 라이브러리
import MobileBasicAct
import MobilePlusAct
import MobileWebLink
from appium import webdriver
import unittest
from time import localtime, strftime                                        #로컬 시간 받아오기 위한 라이브러리

global osType,bundleId,mobileIndex
global delayTime
global appVersionText,appBuildText,homePageText
global installFail,fenServer
global deviceListPath

###############################################################################################################

TEST_VERSION = "20220705_01"

delayTime = 1
shortDelay = 1

strftime("%y-%m-%d %I:%M:%S", localtime())
strTime = strftime("%y%m%d_%H%M%S", localtime())
originFolderPath = strTime

logFileName = "test_log.txt"										              # 디버그 로그 파일 이름
reportFileName = "result.txt"								                      # 결과 보고서 파일이름

###############################################################################################################
logfile = open(logFileName,'w')											          # 디버그 로그 파일 리셋
logfile = open(reportFileName,'w')										          # 디버그 로그 파일 리셋

installFail = 0

try:
    mobileInfoFile = "debug\MobileInfo.txt"
    exportMobileInfo(mobileInfoFile)
except:
    mobileInfoFile = "./debug/MobileInfo.txt"
    exportMobileInfo(mobileInfoFile)

osType = MobileBasicAct.platformNameInfo
mobileIndex = "{0}_{1}".format(MobileBasicAct.platformNameInfo, MobileBasicAct.deviceNameInfo)                          # OS_DeviceName 으로 구분하는 INDEX

print(mobileIndex)

if osType == "ios":
    homePage = "https://www.idisglobal.com"
    bundleId = "com.idis.ios.idismobileplus"
else:
    homePage = "https://www.idisglobal.com"
    bundleId = "com.idis.android.idismobileplus"

fenServer = "qa.idis.co.kr"

if osType == "ios":
    # folderPath = "./"+originFolderPath+"/'\'" + deviceIP + "_"
    simpleFolderPath = "./"+originFolderPath+"/'\'" + "_"
    debugFolderPath = "./"+"debug"+"/"
    testDebugPath = "./"+originFolderPath+"/'\'" + "debug"+"/"
else:
    # folderPath = originFolderPath+"\\" + deviceIP + "_"
    simpleFolderPath = originFolderPath+"\\" + "_"
    debugFolderPath = "debug" + "\\"
    testDebugPath = originFolderPath+"\\" + "debug" + "\\"

deviceListPath = debugFolderPath + "testDeviceList.txt"

if os.path.isdir('debug') == True:                                                                                      # debug 폴더 관리
    if os.path.isfile(deviceListPath) == True:
        os.remove(deviceListPath)                                                                                       # 기존 디버깅용 deviceList 삭제
        print("debug 장치 리스트 삭제")
        deviceListFile = open(deviceListPath, 'w')
    else:
        pass
else:
    os.mkdir("debug")                                                                                                   # debug 폴더 생성

def Save_Screenshot(driver,osType,deviceInfo,saveImageName):                                                            # ScreenShot 저장 함수: 경로 지정, 장치 정보 입력
    if osType == "ios":
        folderPath = "./" + originFolderPath + "/'\'" + deviceInfo + "_"
        simpleFolderPath = "./" + originFolderPath + "/'\'" + "_"
    else:
        folderPath = originFolderPath + "\\" + deviceInfo + "_"
        simpleFolderPath = originFolderPath + "\\" + "_"

    if deviceInfo == "":
        driver.save_screenshot(simpleFolderPath + saveImageName)
    else:
        driver.save_screenshot(folderPath + saveImageName)

def Debug_Save_Screenshot(driver,testDebugPath,deviceInfo,saveImageName):                                                            # ScreenShot 저장 함수: 경로 지정, 장치 정보 입력

    if os.path.isdir(testDebugPath) == True:
        pass
    else:
        os.mkdir(testDebugPath)                                                                                                 # 개별 테스트 debug 폴더 생성

    if deviceInfo == "":
        driver.save_screenshot(testDebugPath + saveImageName)
    else:
        driver.save_screenshot(testDebugPath + saveImageName)

###############################################################################################################

#--------Test_Start_App--------
# App 실행 테스트

def Test_Start_App(driver):
    global installFail

    MobilePlusAct.Start_App(driver, osType, delayTime)
    element = "com.idis.android.idismobileplus:id/addFloatingButton"  # 장치등록 +버튼이 있으면 실행TC pass   >>??
    mobile_element_displayed(driver, osType, 'id', element)
    # print("displayedElement")
    # print(MobileBasicAct.displayedElement)
    if MobileBasicAct.displayedElement == "True":
        writeReport(reportFileName, "App실행\t\tPASS")
    else:
        writeReport(reportFileName, "App실행\t\t>>FAIL<<")
        writeReport(reportFileName, "App실행      리스트 장치 추가 UI 확인 불가")
        driver.quit()  # 장치등록 +버튼을 못찾으면 실행TC fail
        installFail = 1
    return installFail

#--------Test_Start_App--------
# App 실행 테스트

def Test_Find_Button(driver):

    writeReport(reportFileName, "UI버튼 확인")

    element = ["com.idis.android.idismobileplus:id/addFloatingButton", "com.idis.android.idismobileplus:id/scanButton",
               "com.idis.android.idismobileplus:id/tfaButton", "com.idis.android.idismobileplus:id/pushButton",
               "com.idis.android.idismobileplus:id/settingButton", "com.idis.android.idismobileplus:id/titleSiteArrangementButton",
               "com.idis.android.idismobileplus:id/titleSiteSearchButton", "com.idis.android.idismobileplus:id/siteLiveButton",
               "com.idis.android.idismobileplus:id/sitePlayButton", "com.idis.android.idismobileplus:id/siteFavoriteButton",
               "com.idis.android.idismobileplus:id/siteDetailButton", "com.idis.android.idismobileplus:id/siteiNEXConnectButton"]

    iconName = ["등록", "QR Code", "2FA", "Push", "설정접속", "목록편집", "검색", "장치Live", "장치Search", "즐겨찾기", "상세접속", "iNEX연결"]

    temp = 0
    for elementTemp in element:
        try:
            driver.find_element(by=AppiumBy.ID, value=elementTemp)
            writeReport(reportFileName, "{0}. {1}버튼 - Pass". format(temp+1, iconName[temp]))
            temp = temp + 1

        except:
            writeReport(reportFileName, "{0}. {1}버튼 - Fail". format(temp+1, iconName[temp]))
            temp = temp + 1

#--------Test_GetVersion--------
# App 버전 / 빌드 확인

def Test_GetVersion(driver):
    element = "com.idis.android.idismobileplus:id/settingButton"                                                        #설정(톱니바퀴)버튼
    mobile_click(driver, osType, 'id', element, delayTime)
    if osType == "ios":
        MobilePlusAct.IOS_Setting_Info(driver, '버전')
        appVersionText = MobilePlusAct.iosSettingInfo
        MobilePlusAct.IOS_Setting_Info(driver, '빌드')
        appBuildText = MobilePlusAct.iosSettingInfo
        MobilePlusAct.IOS_Setting_Info(driver, '홈페이지')
        homePageText = MobilePlusAct.iosSettingInfo
        sleep(shortDelay)
        element = '홈페이지'
        for loopNum in range(0,1):
            print("scroll")
            mobile_scroll_for_element(driver, "ios", "id", element,delayTime)
            driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value=element).click()                                                          # 홈페이지 터치 후 대기
            sleep(shortDelay)
            sleep(shortDelay)
        # driver.save_screenshot(simpleFolderPath + "홈페이지 확인.png")                                                        # 공용 테스트 (장치 정보 필요 없음) 스크린샷
        Save_Screenshot(driver, osType, "기본검사", "홈페이지 확인.png")
        # writeReport(reportFileName, "홈페이지 - 완료[캡쳐]")
        sleep(shortDelay)

        #webdriver.Remote("Http://localhost:4723/wd/hub", Desired_Cap)                                                   # 캡쳐 후 어플 디시 열기

    else:
        for loopNum in range(1,10):
            MobilePlusAct.AOS_Setting_Info(driver, '홈페이지')                                                             # 설정 페이지에서 홈페이지 찾기
            homePageText = MobilePlusAct.aosSettingInfo                                                                   # 홈페이지 텍스트 확인
            # print(homePageText)
            if MobilePlusAct.aosfindXpath != '':
                # print(MobilePlusAct.aosfindXpath)
                break
            driver.swipe(start_x=900, start_y=1000, end_x=900, end_y=200, duration=100)                                     #Swipe Down
            sleep(shortDelay)

        sleep(shortDelay)
        print("버전")
        MobilePlusAct.AOS_Setting_Info(driver, '버전')
        appVersionText = MobilePlusAct.aosSettingInfo

        print("빌드")
        MobilePlusAct.AOS_Setting_Info(driver, '빌드')
        appBuildText = MobilePlusAct.aosSettingInfo

        MobilePlusAct.AOS_Setting_Info(driver, '홈페이지')
        Xpath = MobilePlusAct.aosfindXpath
        sleep(shortDelay)
        driver.find_element(by=AppiumBy.XPATH, value=Xpath).click()                                                          # 홈페이지 터치 후 대기
        sleep(shortDelay*2)

        # driver.save_screenshot(simpleFolderPath + "홈페이지 확인.png")                                                        # 공용 테스트 (장치 정보 필요 없음) 스크린샷
        # writeReport(reportFileName, "홈페이지 - 완료[캡쳐]")
        sleep(shortDelay)

        # element = "com.android.chrome:id/url_bar"                                                                           #홈페이지 URL
        # homePageText = driver.find_element_by_id(element).get_attribute('text')

        # driver.save_screenshot(simpleFolderPath + "홈페이지 확인.png")                                                        # 공용 테스트 (장치 정보 필요 없음) 스크린샷
        Save_Screenshot(driver, osType, "기본검사", "홈페이지 확인.png")
        sleep(shortDelay)

    writeReport(reportFileName, "App 버전\t\tPASS\t{}".format(appVersionText))
    writeReport(reportFileName, "App 빌드\t\tPASS\t{}".format(appBuildText))

    if homePageText == homePage:
        writeReport(reportFileName, "홈페이지\t\tPASS")
    else:
        writeReport(reportFileName, "홈페이지\t\t>>FAIL<<\t{0} : {1}" .format(homePage, homePageText))                    #homepateText가 실제 받아오는 주소

#--------Test_Change_FenServer--------
# App 버전 / 빌드 확인

def Test_Change_FenServer(driver):
    MobilePlusAct.Change_FenServer(driver, osType, fenServer, delayTime)
    if osType == "ios":
        allCells = MobilePlusAct.IOS_find(driver, 'XCUIElementTypeCell', '')
        time.sleep(1)
        changeSuccess = 0
        for cell in allCells:
            elements = cell.find_element(by=AppiumBy.CLASS_NAME, value='XCUIElementTypeStaticText')
            isTarget = False
            for element in elements:
                if element.text == 'FEN 서버 주소':
                    isTarget = True
                    continue
                if isTarget == True and element.text == fenServer:
                    print('Success')
                    changeSuccess = 1
                    break
        if changeSuccess == 1:
            writeReport(reportFileName, "FEN 서버 변경\tPASS")
        else:
            writeReport(reportFileName, "FEN 서버 변경\t>FAIL<")
        time.sleep(2)
    else:
        # driver.save_screenshot(simpleFolderPath + "FEN주소 변경.png")                                                      # 공용 테스트 (장치 정보 필요 없음) 스크린샷
        Save_Screenshot(driver, osType, "기본검사", "FEN주소 변경.png")
        sleep(shortDelay)
        element = "com.idis.android.idismobileplus:id/commonTopBackButton"  # 우측 상단 뒤로가기 버튼
        mobile_click(driver, osType, 'id', element, delayTime)
        sleep(middleDelay)

        writeReport(reportFileName, "FEN 서버 변경\tPASS [캡쳐]")

    element = "com.idis.android.idismobileplus:id/commonTopBackButton"  # 우측 상단 뒤로가기 버튼
    mobile_click(driver, osType, 'id', element, delayTime)

#--------Test_Regist_IpAddress--------
#

def Test_Regist_IpAddress(driver):
    lineNum = 1
    listFile = "basicDevice.txt"
    exportDeviceInfo(listFile, lineNum)
    writeReport(reportFileName, "\n-접속 장치:\t\t{0} : {1}".format(MobileBasicAct.deviceNameText,MobileBasicAct.deviceInfo))                               #장치 이름 표시
    writeDeviceList(deviceListPath, MobileBasicAct.deviceNameText, MobileBasicAct.deviceInfo, MobileBasicAct.deviceIdText, MobileBasicAct.devicePwText)
    writeLog(logFileName, "{0}번 장치 정보: {1}".format(lineNum, MobileBasicAct.deviceNameText))

    MobilePlusAct.Regist_IpAddress(driver, osType, MobileBasicAct.ipAddressText, MobileBasicAct.deviceIdText, MobileBasicAct.devicePwText, delayTime)       # IP주소 장치 등록

    # driver.save_screenshot(folderPath + "IP장치 등록.png")
    Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo, "IP장치 등록.png")

    if MobilePlusAct.registFail == 0:
        writeReport(reportFileName, "IP 장치 등록\t\tPASS\t[캡쳐]")
    else:
        writeReport(reportFileName, "IP 장치 등록\t\t>>FAIL<<\t[캡쳐]")


#--------Test_Regist_Multi_Deivce_Ip--------
# App 버전 / 빌드 확인

def Test_Regist_Multi_Deivce_Ip(driver,lineNum,listFile):

    exportDeviceInfo(listFile, lineNum)
    if MobileBasicAct.deviceLineText == "Finish Line":
        pass
    else:
        writeReport(reportFileName, "\n-접속 장치:\t\t{0}".format(MobileBasicAct.deviceNameText))                           # 장치 이름 표시
        writeLog(logFileName, "{0}번 장치 정보: {1}".format(lineNum, MobileBasicAct.deviceNameText))

        MobilePlusAct.Regist_IpAddress(driver, osType, MobileBasicAct.ipAddressText, MobileBasicAct.deviceIdText, MobileBasicAct.devicePwText, delayTime)       # IP주소 장치 등록

        if MobilePlusAct.registFail == 0:
            # writeReport(reportFileName, "{} 등록\t\tPASS".format(MobileBasicAct.deviceInfo))                              # 등록 성공시 표시 안함
            pass
        else:
            writeReport(reportFileName, "{} 등록\t\t>>FAIL<<".format(MobileBasicAct.deviceInfo))

#----------------------------------------------------------------

#--------Test_IpAddress--------
# IP 주소 등록 및 상세 정보-Live 테스트
def Test_Detail_Connect_Live(driver):
    MobilePlusAct.Detail_Connect(driver, osType, "Live", MobileBasicAct.ipAddressText, delayTime)
    sleep(shortDelay)
    Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"상세정보페이지_Live접속.png")
    if MobilePlusAct.connectSuccess == 1:
        writeReport(reportFileName, "상세정보페이지 Live\t\tPASS\t[캡쳐]")
    else:
        writeReport(reportFileName, "상세정보페이지 Live\t\t>>FAIL<<\t[캡쳐]")
    sleep(shortDelay)
    element = "com.idis.android.idismobileplus:id/screenTopBackButton"  # Live창에서 위쪽 뒤로가기 버튼
    mobile_click(driver, osType, 'id', element, delayTime)

    sleep(shortDelay)

    if osType == "ios":
        element = "상세정보_뒤로가기"
    else:
        element = "com.idis.android.idismobileplus:id/commonTopBackButton"  # 상세정보창에서 위쪽 뒤로가기 버튼
    mobile_click(driver, osType, 'id', element, delayTime)
    sleep(shortDelay)

    element = "com.idis.android.idismobileplus:id/listSearchCloseButton"  # 돋보기 닫기 버튼
    mobile_click(driver, osType, 'id', element, delayTime)

#--------Test_Suite_Regist_IpAddress--------
# IP 주소 등록 테스트 스위트

def Test_Suite_Regist_IpAddress(driver):
    Test_Regist_IpAddress(driver)
    if MobilePlusAct.registFail == 0:
        Test_Detail_Connect_Live(driver)
    else:
        writeReport(reportFileName, "상세정보페이지 Live\t\t>>FAIL<<\t[접속 안됨]")
#--------Test_Regist_iNEX--------
# App 버전 / 빌드 확인

def Test_Regist_iNEX(driver):
    lineNum = 2
    listFile = "basicDevice.txt"
    exportDeviceInfo(listFile, lineNum)
    writeReport(reportFileName, "\n-접속 장치:\t\t{0} : {1}".format(MobileBasicAct.deviceNameText, MobileBasicAct.deviceInfo))
    writeDeviceList(deviceListPath, MobileBasicAct.deviceNameText, MobileBasicAct.deviceInfo,MobileBasicAct.deviceIdText, MobileBasicAct.devicePwText)
    writeLog(logFileName, "{0}번 장치 정보: {1}".format(lineNum, MobileBasicAct.deviceNameText))
    MobilePlusAct.Regist_iNEX(driver, osType, MobileBasicAct.deviceNameText, MobileBasicAct.ipAddressText, MobileBasicAct.deviceIdText, MobileBasicAct.devicePwText, delayTime)
    Save_Screenshot(driver, osType, "기본검사_" + MobileBasicAct.deviceInfo,"iNEX 등록.png")
    if MobilePlusAct.registFail == 0:
        writeReport(reportFileName, "iNEX 등록 확인\t\tPASS\t[캡쳐]")
    else:
        writeReport(reportFileName, "iNEX 등록 확인\t\t>>FAIL<<\t[캡쳐]")

#--------Test_Regist_iNEX--------
# App 버전 / 빌드 확인
def Test_Connect_iNEX(driver):
    lineNum = 2
    listFile = "basicDevice.txt"
    exportDeviceInfo(listFile, lineNum)
    writeLog(logFileName, "{0}번 장치 정보: {1}".format(lineNum, MobileBasicAct.ipAddressText))                            # 장치 주소로 검색
    iNEXListFile = reportFileName                                                                                       # iNEX등록 장치 기록 file을 결과 레포트 경로로 설정
    time.sleep(3)
    MobilePlusAct.FrontButton_Connect(driver, osType, "Connect",MobileBasicAct.ipAddressText, delayTime)
    if MobilePlusAct.connectSuccess == 1:
        writeReport(reportFileName, "UI 버튼 - 접속\t\tPASS")
    else:
        writeReport(reportFileName, "UI 버튼 - 접속\t\t>>FAIL<<")

    sleep(middleDelay)

    if osType == "ios":
        element = "뒤로가기01"                                                                                            # iNEX 리스트에서 뒤로가기 버튼
    else:
        element = "com.idis.android.idismobileplus:id/commonTopBackButton"                                              # 뒤로가기 버튼
    mobile_click(driver, osType, 'id', element, delayTime)


    sleep(shortDelay)
    element = "com.idis.android.idismobileplus:id/listSearchCloseButton"                                                # 돋보기 닫기 버튼
    mobile_click(driver, osType, 'id', element, delayTime)

    # 상세 페이지에서 연결 접속

    MobilePlusAct.Detail_Connect(driver, osType, "Connect", MobileBasicAct.ipAddressText, delayTime)          # 상세 페이지로 접속
    if MobilePlusAct.connectSuccess == 1:
        writeReport(reportFileName, "상세 버튼 - 접속\t\tPASS")
        MobilePlusAct.Read_iNEX_Device(driver, osType, iNEXListFile, delayTime)                               # 상세 페이지로 iNEX 연결 후 등록 장치 리스트 불러옴
    else:
        writeReport(reportFileName, "상세 버튼 - 접속\t\t>>FAIL<<")
    sleep(shortDelay)
    sleep(shortDelay)

    if osType == "ios":
        element = "뒤로가기01"                                                                                             # iNEX 리스트에서 뒤로가기 버튼
    else:
        element = "com.idis.android.idismobileplus:id/commonTopBackButton"                                              # Live창에서 위쪽 뒤로가기 버튼
    mobile_click(driver, osType, 'id', element, delayTime)

    if osType == "ios":
        element = "상세정보_뒤로가기"
    else:
        element = "com.idis.android.idismobileplus:id/commonTopBackButton"                                              # 상세정보창에서 위쪽 뒤로가기 버튼
    mobile_click(driver, osType, 'id', element, delayTime)
    sleep(shortDelay)
    element = "com.idis.android.idismobileplus:id/listSearchCloseButton"                                                # 돋보기 닫기 버튼
    mobile_click(driver, osType, 'id', element, delayTime)

#--------Test_Suite_Regist_IpAddress--------
# IP 주소 등록 테스트 스위트

def Test_Suite_Regist_iNEX(driver):
    Test_Regist_iNEX(driver)
    if MobilePlusAct.registFail == 0:
        Test_Connect_iNEX(driver)
    else:
        writeReport(reportFileName, "UI 버튼 - 접속\t>>FAIL<<")
    print("iNex 접속 테스트 완료")
#--------Test_Regist_Fen--------
# App 버전 / 빌드 확인

def Test_Regist_Fen(driver):
    lineNum = 3
    listFile = "basicDevice.txt"
    exportDeviceInfo(listFile, lineNum)
    writeReport(reportFileName, "\n-접속 장치:\t\t{0} : {1}".format(MobileBasicAct.deviceNameText, MobileBasicAct.deviceInfo))
    writeDeviceList(deviceListPath, MobileBasicAct.deviceNameText, MobileBasicAct.deviceInfo, MobileBasicAct.deviceIdText, MobileBasicAct.devicePwText)
    writeLog(logFileName, "{0}번 장치 정보: {1}".format(lineNum, MobileBasicAct.deviceNameText))
    MobilePlusAct.Regist_Fen_Name(driver, osType, MobileBasicAct.fenNameText, MobileBasicAct.deviceIdText, MobileBasicAct.devicePwText, delayTime)       # IP주소 장치 등록
    TouchAction(driver).press(x=202, y=467).move_to(x=200, y=607).release().perform()
    Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"FEN 장치 등록.png")
    if MobilePlusAct.registFail == 0:
        writeReport(reportFileName, "FEN 장치 등록\t\tPASS\t[캡쳐]")
    else:
        writeReport(reportFileName, "FEN 장치 등록\t\t>>FAIL<<\t[캡쳐]")

#----------Test_Live_Fen-------------
# FEN 장치 등록 및 Live 확인

def Test_Live_Fen(driver):
    # Test_Regist_Fen(driver)
    MobilePlusAct.FrontButton_Connect(driver, osType, "Live", MobileBasicAct.fenNameText, delayTime)                    # Live 접속 모듈
    Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"UI 버튼 - 감시.png")
    if MobilePlusAct.connectSuccess == 1:
        writeReport(reportFileName, "UI 버튼 - 감시\t\tPASS\t[캡쳐]")
    else:
        writeReport(reportFileName, "UI 버튼 - 감시\t\t>>FAIL<<\t[캡쳐]")


#----------Test_Live_Layout-------------
# Live 레이아웃 확인

def Test_Live_Layout(driver):
    print("<<live Layout 테스트>>")
    MobilePlusAct.Find_MaxChannel(driver, osType, delayTime)
    for loopIndex in range(1, MobilePlusAct.channelLoop):
        sleep(delayTime)
        element = "com.idis.android.idismobileplus:id/screenLayoutButton"                                               # Layout버튼
        mobile_click(driver, osType, 'id', element, delayTime)
        if loopIndex == 1:
            ch = 1
            try:
                if osType == "ios":
                    channelNum = ch - 1                                                                                 # IOS는 0부터 채널이 시작됨 채널1: CameraOsdView0
                    element = "CameraOsdView{0}".format(channelNum)
                else:
                    element = "com.idis.android.idismobileplus:id/cameraOSDView0{0}".format(ch)                         # 채널 스크린 번호(8ch이하 제품)  # 채널 스크린 번호(1ch 제품)
                driver.find_element(by=AppiumBy.ID, value=element)
                Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"Layout Live {0}x{0}.png".format(loopIndex))
                writeReport(reportFileName, "Layout Live {0}x{0}\t\tPASS\t[캡쳐]".format(loopIndex))
                ch = ch * 4
            except:
                Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"Layout Live {0}x{0}.png".format(loopIndex))
                writeReport(reportFileName, "Layout Live {0}x{0}\t\t>>FAIL<<\t[캡쳐]".format(loopIndex))

        elif 1 < loopIndex < 4:
            try:
                if osType == "ios":
                    channelNum = ch - 1
                    element = "CameraOsdView{0}".format(channelNum)
                else:
                    element = "com.idis.android.idismobileplus:id/cameraOSDView0{0}".format(ch)                         # 채널 스크린 번호(8ch이하 제품)
                driver.find_element(by=AppiumBy.ID, value=element)
                Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"Layout Live {0}x{0}.png".format(loopIndex))
                writeReport(reportFileName, "Layout Live {0}x{0}\t\tPASS\t[캡쳐]".format(loopIndex))
                ch = ch * 2
            except:
                Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"Layout Live {0}x{0}.png".format(loopIndex))
                writeReport(reportFileName, "Layout {0}x{0}\t\t>>FAIL<<\t[캡쳐]".format(loopIndex))

        else:
            try:
                if osType == "ios":
                    channelNum = ch - 1
                    element = "CameraOsdView{0}".format(channelNum)
                else:
                    element = "com.idis.android.idismobileplus:id/cameraOSDView{0}".format(ch)  # 채널 스크린 번호(8ch이하 제품)
                driver.find_element(by=AppiumBy.ID, value=element)
                Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"Layout Live {0}x{0}.png".format(loopIndex))
                writeReport(reportFileName, "Layout Live {0}x{0}\t\tPASS\t[캡쳐]".format(loopIndex))
                ch = ch * 2
            except:
                Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"Layout Live {0}x{0}.png".format(loopIndex))
                writeReport(reportFileName, "Layout Live {0}x{0}\t\t>>FAIL<<\t[캡쳐]".format(loopIndex))

def Test_Move_To_Cam(driver):
    logText = "<<채널 이동 테스트>>"
    writeLog(logFileName, logText)

    for loopNum in range(0, 5):
        MobilePlusAct.Find_Single_Screen(driver, osType, delayTime)                                                     # 단일 화면 찾기
        if MobilePlusAct.singleScreen == 1:
            print("-> 단일 화면 변경 완료")
            break
        else:
            sleep(delayTime)
            element = "com.idis.android.idismobileplus:id/screenLayoutButton"                                           # Layout 변경
            mobile_click(driver, osType, 'id', element, delayTime)

    MobilePlusAct.Move_To_Camera(driver, osType, delayTime)
    if MobilePlusAct.moveCamStatus == 1:
        Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"Live 카메라 이동_{0}.png".format(MobilePlusAct.moveToCamNum))
        writeReport(reportFileName, "Live카메라 이동 {0}\t\tPASS\t[캡쳐]".format(MobilePlusAct.moveToCamNum))
    else:
        Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"Live 카메라 이동_{0}.png".format(MobilePlusAct.moveToCamNum))
        writeReport(reportFileName, "Live카메라 이동 {0}\t\t>>FAIL<<\t[캡쳐]".format(MobilePlusAct.moveToCamNum))

def Test_Digital_Zoom(driver):
    logText = "<<Zoom 테스트>>"
    writeLog(logFileName, logText)

    for loopNum in range(0, 5):
        MobilePlusAct.Find_Single_Screen(driver, osType, delayTime)                                                     # 단일 화면 찾기
        if MobilePlusAct.singleScreen == 1:
            print("-> 단일 화면 변경 완료")
            break
        else:
            sleep(delayTime)
            element = "com.idis.android.idismobileplus:id/screenLayoutButton"                                           # Layout 변경
            mobile_click(driver, osType, 'id', element, delayTime)

    if MobilePlusAct.singleScreen == 1:
        MobilePlusAct.Digital_Zoom(driver, osType, "ZoomIn", delayTime)
        Save_Screenshot(driver, osType, "기본검사", "Live Zoom-In.png")
        writeReport(reportFileName, "Live Zoom-In\t\tPASS\t[캡쳐]")
        time.sleep(shortDelay)
        MobilePlusAct.Digital_Zoom(driver, osType, "ZoomOut", delayTime)
        Save_Screenshot(driver, osType, "기본검사", "Live Zoom-Out.png")
        writeReport(reportFileName, "Live Zoom-Out\t\tPASS\t[캡쳐]")
        time.sleep(shortDelay)
    else:
        writeReport(reportFileName, "Live Zoom-In\t\t>>FAIL<<")
        writeReport(reportFileName, "Live Zoom-Out\t\t>>FAIL<<")
        logText = "[Error] Zoom 테스트: 단일화면 변경 안됨"
        writeLog(logFileName, logText)

def Test_Osd(driver):
    print("<<OSD 테스트>>")
    x = driver.get_window_size()["width"]                                                                               # 가로길이 display size측정
    y = driver.get_window_size()["height"]                                                                              # 세로길이 display size측정

    TouchAction(driver).press(x=x * 0.5, y=y * 0.3).release().perform()
    sleep(shortDelay)
    Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"Live세로모드_OSD제거.png")
    writeReport(reportFileName, "Live세로모드_OSD제거\t\tPASS\t[캡쳐]")
    sleep(shortDelay)

    TouchAction(driver).press(x=x * 0.5, y=y * 0.3).release().perform()
    sleep(shortDelay)
    Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"Live세로모드_OSD생성.png")
    writeReport(reportFileName, "Live세로모드_OSD생성\t\tPASS\t[캡쳐]")

def Test_Change_Ratio(driver):

    viewMenuName = "화면 비율에 맞추기"

    MobilePlusAct.Select_View_Menu(driver, osType, viewMenuName, delayTime)

    sleep(shortDelay)

    Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"Live-화면비율에 맞추기.png")
    if MobilePlusAct.selectMenuError == 0:
        writeReport(reportFileName, "Live-화면 비율에 맞추기\t\tPASS\t[캡쳐]")
    else:
        writeReport(reportFileName, "Live-화면비율에 맞추기\t\t>>FAIL<<\t[캡쳐]")

    sleep(shortDelay)

    viewMenuName = "영상 비율에 맞추기"
    MobilePlusAct.Select_View_Menu(driver, osType, viewMenuName, delayTime)

    Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"Live-영상비율에 맞추기.png")
    if MobilePlusAct.selectMenuError == 0:
        writeReport(reportFileName, "Live-영상비율에 맞추기\t\tPASS\t[캡쳐]")
    else:
        writeReport(reportFileName, "Live-영상비율에 맞추기\t\t>>FAIL<<\t[캡쳐]")

def Test_Capture_Image(driver):

    viewMenuName = "캡쳐"

    MobilePlusAct.Select_View_Menu(driver, osType, viewMenuName, delayTime)

    if MobilePlusAct.selectMenuError == 0:
        writeReport(reportFileName, "캡쳐 Live - OSD포함\t\tPASS\t[갤러리 파일]")
    else:
        writeReport(reportFileName, "캡쳐 Live - OSD포함\t\t>>FAIL<<\t[갤러리 파일]")

    element = "com.idis.android.idismobileplus:id/screenLayoutButton"                                                   # Layout버튼으로 1x1이동
    mobile_click(driver, osType, 'id', element, delayTime)
    sleep(shortDelay)

    x = driver.get_window_size()["width"]  # 가로길이 display size측정
    y = driver.get_window_size()["height"]  # 세로길이 display size측정

    TouchAction(driver).press(x=x * 0.5, y=y * 0.3).release().perform()                                                 # OSD제거
    sleep(shortDelay)

    MobilePlusAct.Select_View_Menu(driver, osType, viewMenuName, delayTime)

    if MobilePlusAct.selectMenuError == 0:
        writeReport(reportFileName, "캡쳐 Live - OSD제거\t\tPASS\t[갤러리 파일]")
    else:
        writeReport(reportFileName, "캡쳐 Live - OSD제거\t\t>>FAIL<<\t[갤러리 파일]")

def Test_Frame_Info(driver):

    viewMenuName = "정보"

    MobilePlusAct.Select_View_Menu(driver, osType, viewMenuName, delayTime)

    sleep(middleDelay)

    Save_Screenshot(driver, osType, "기본검사_"+MobileBasicAct.deviceInfo,"Live 정보 확인.png")

    if MobilePlusAct.selectMenuError == 0:
        writeReport(reportFileName, "Live 정보 확인\t\tPASS\t[캡쳐]")
    else:
        writeReport(reportFileName, "Live 정보 확인\t\t>>FAIL<<\t[캡쳐]")

    x = driver.get_window_size()["width"]                                                                               # 정보창이 사라지지 않을 경우를 대비 다시 한번 정보창 종료 시도
    y = driver.get_window_size()["height"]
    TouchAction(driver).press(x=x * 0.5, y=y * 0.1).release().perform()
    sleep(shortDelay)

def Test_Confirm_UI(driver):
    writeReport(reportFileName, "\n<UI버튼 확인>")
    confirmUiFail = 0
    element = ["com.idis.android.idismobileplus:id/addFloatingButton",
               "com.idis.android.idismobileplus:id/scanButton",
               "com.idis.android.idismobileplus:id/tfaButton", "com.idis.android.idismobileplus:id/pushButton",
               "com.idis.android.idismobileplus:id/settingButton",
               "com.idis.android.idismobileplus:id/titleSiteArrangementButton",
               "com.idis.android.idismobileplus:id/titleSiteSearchButton",
               "com.idis.android.idismobileplus:id/siteLiveButton",
               "com.idis.android.idismobileplus:id/sitePlayButton",
               "com.idis.android.idismobileplus:id/siteFavoriteButton",
               "com.idis.android.idismobileplus:id/siteDetailButton",
               "com.idis.android.idismobileplus:id/siteiNEXConnectButton"]

    iconName = ["등록", "QR Code", "2FA", "Push", "설정접속", "목록편집", "검색", "장치Live", "장치Search", "즐겨찾기", "상세접속",
                "iNEX연결"]
    temp = 0
    for elementTemp in element:
        try:
            if osType == "ios":
                textFile = "element.txt"
                exportMobileId(textFile, osType, elementTemp)
                driver.find_element(by=AppiumBy.ID, value=MobileBasicAct.iosId)
            else:
                driver.find_element(by=AppiumBy.ID, value=elementTemp)
            temp = temp + 1

        except:
            confirmUiFail = confirmUiFail + 1
            if confirmUiFail == 1:
                writeReport(reportFileName, "UI 버튼 확인\t\t>>FAIL<<".format(temp + 1, iconName[temp]))
            writeReport(reportFileName, "{0}. {1}버튼 확인 불가".format(temp + 1, iconName[temp]))
            temp = temp + 1
    if confirmUiFail == 0:
        writeReport(reportFileName, "UI 버튼 확인\t\tPASS")
    else:
        pass

def Test_Suite_Regist_Fen(driver):
    Test_Regist_Fen(driver)
    if MobilePlusAct.registFail != 0:
        print("등록 실패로 동작 안됨")
    else:
        Test_Live_Fen(driver)
        Test_Live_Layout(driver)
        Test_Move_To_Cam(driver)
        Test_Digital_Zoom(driver)
        Test_Osd(driver)
        Test_Change_Ratio(driver)
        Test_Capture_Image(driver)
        Test_Frame_Info(driver)
        sleep(shortDelay)

    element = "com.idis.android.idismobileplus:id/screenTopBackButton"                                                  # Live창에서 위쪽 뒤로가기 버튼
    mobile_click(driver, osType, 'id', element, delayTime)

    element = "com.idis.android.idismobileplus:id/commonTopBackButton"                                                  # Live창에서 위쪽 뒤로가기 버튼
    mobile_click(driver, osType, 'id', element, delayTime)

    sleep(shortDelay)

    element = "com.idis.android.idismobileplus:id/listSearchCloseButton"                                                # 돋보기 닫기 버튼
    mobile_click(driver, osType, 'id', element, delayTime)



#----------Test_Suite_Multi_Device-------------
# Multi Device 호환 테스트

def Test_Suite_Multi_Device(driver):
    lineNum = 1
    deviceCount  = 0
    passDeviceCount = 0
    failDeviceCount = 0
    ctFailDeviceInfo = ""                                                                                                   # 호환 테스트 실패 장치
    while lineNum < 300:
        # MobilePlusAct.Start_App(driver, osType, delayTime)
        appStatus = driver.query_app_state(bundleId)                                                                        # 0: not install, 1: not running, 2: suspended, 3, background, 4, foreground
        if appStatus != 4:
            MobilePlusAct.Start_App(driver, osType, delayTime)
            driver.activate_app(bundleId)
            driver.reset()                                                                                                  # App Reset하기
            MobilePlusAct.Start_App(driver, osType, delayTime)
            # logText = "{}: App 종료 상태".format(MobileBasicAct.ipAddressText)
            # writeLog(logFileName, logText)
            writeReport(reportFileName, "{} 접속시 App Reset\t\t 접속 확인 필요".format(MobileBasicAct.deviceInfo))
        try:
            if osType == "ios":
                Test_Regist_Multi_Deivce_Ip(driver, lineNum, "./debug/multiDevice.txt")  # 장치 등록하기
            else:
                Test_Regist_Multi_Deivce_Ip(driver, lineNum, "debug\multiDevice.txt")                                           # 장치 등록하기
            deviceCount = lineNum - 1
            if MobileBasicAct.deviceLineText == "Finish Line":
                logText = "호환 테스트 종료"
                writeLog(logFileName, logText)
                writeReport(reportFileName, "\n<호환 테스트 실패 장치 ({0}/{1})>\n- 검색 실패 장치 별도 확인 필요\n\n{2}".format(failDeviceCount,deviceCount-1,ctFailDeviceInfo))
                break
            if MobilePlusAct.registFail != 1:                                                                               # 장치 등록 확인후 Live 확인
                MobilePlusAct.FrontButton_Connect(driver, osType, "Live", MobileBasicAct.ipAddressText,delayTime)           # Live 접속 모듈
                Save_Screenshot(driver, osType, MobileBasicAct.deviceInfo, "감시.png")
                if MobilePlusAct.connectSuccess == 1:
                    writeReport(reportFileName, "{} 감시\t\tPASS\t[캡쳐]".format(MobileBasicAct.deviceInfo))
                else:
                    ctFailDeviceInfo = ctFailDeviceInfo + MobileBasicAct.deviceNameText + "\t" + MobileBasicAct.ipAddressText + "\t" + "({0}/{1})".format(MobileBasicAct.deviceIdText,MobileBasicAct.devicePwText)+"\n"
                    failDeviceCount = failDeviceCount + 1
                    writeReport(reportFileName, "{} 감시\t\t>>FAIL<<\t[캡쳐]".format(MobileBasicAct.deviceInfo))
                element = "com.idis.android.idismobileplus:id/screenTopBackButton"                                          # Live창에서 위쪽 뒤로가기 버튼
                mobile_click(driver, osType, 'id', element, delayTime)
                sleep(delayTime)

                element = "com.idis.android.idismobileplus:id/listSearchCloseButton"                                        # 리스트 검색 닫기 버튼
                mobile_click(driver, osType, 'id', element, delayTime)
                sleep(delayTime*2)

                MobilePlusAct.FrontButton_Connect(driver, osType, "Search", MobileBasicAct.ipAddressText, delayTime)        # Search 접속 모듈
                if MobilePlusAct.connectSuccess == 1:
                    Save_Screenshot(driver, osType, MobileBasicAct.deviceInfo, "검색.png")  # Search 성공시 캡쳐
                    writeReport(reportFileName, "{} 검색\t\tPASS\t[캡쳐]".format(MobileBasicAct.deviceInfo))
                else:
                    if osType == "ios":
                        element = "취소"                                                                              # 구앱으로 연동 메세지창 발생
                        mobile_click(driver, osType, 'id', element, delayTime)
                        element = "확인"                                                                              # 지원 안함 메세지창 발생
                        mobile_click(driver, osType, 'id', element, delayTime)
                    else:
                        element = "android:id/button2"                                                                              # 메세지창 발생
                        mobile_click(driver, osType, 'id', element, delayTime)
                        element = "android:id/button1"                                                                              # 메세지창 발생
                        mobile_click(driver, osType, 'id', element, delayTime)
                    writeReport(reportFileName, "{0} 검색\t\t>>FAIL<<\t".format(MobileBasicAct.deviceInfo))  # 검색 결과 FAIL

                element = "com.idis.android.idismobileplus:id/screenTopBackButton"                                          # Search창에서 위쪽 뒤로가기 버튼
                mobile_click(driver, osType, 'id', element, delayTime)
                element ="com.idis.android.idismobileplus:id/listSearchCloseButton"
                mobile_click(driver, osType, 'id', element, delayTime)

            else:
                failDeviceCount = failDeviceCount + 1
                ctFailDeviceInfo = ctFailDeviceInfo + MobileBasicAct.deviceNameText + "\t" + MobileBasicAct.ipAddressText + "\t" + "({0}/{1})".format(MobileBasicAct.deviceIdText,MobileBasicAct.devicePwText)+"\n"
        except:
            ctFailDeviceInfo = ctFailDeviceInfo + MobileBasicAct.deviceNameText + "\t" + MobileBasicAct.ipAddressText + "\t" + "({0}/{1})".format(MobileBasicAct.deviceIdText, MobileBasicAct.devicePwText) + "\n"
            element = "com.idis.android.idismobileplus:id/screenTopBackButton"                                                  # Error발생시 뒤로가기 버튼 클릭
            mobile_click(driver, osType, 'id', element, delayTime)
            writeLog(logFileName, "비정상 동작")
            writeReport(reportFileName, "{0} 동작\t\t앱 비정상 동작\t[Debug 폴더 확인]".format(MobileBasicAct.ipAddressText))  # 검색 결과 FAIL
            Debug_Save_Screenshot(driver, testDebugPath, "", "비정상 동작_{}.png".format(MobileBasicAct.ipAddressText))
            failDeviceCount = failDeviceCount + 1
        lineNum = lineNum + 1

#----------------------------------------------------------------------------------------------------------------------
# Report 생성
#----------------------------------------------------------------------------------------------------------------------

def Make_Report(originFolderPath, mobileDeviceName, osType, mobileDeviceVersion, testDuration):
    if osType == "ios":
        resultFileName = "./" + originFolderPath + "/'\'" + "Result.txt"
    else:
        resultFileName = originFolderPath + "\\" + "Result.txt"

    resultText = open("result.txt",'r')                                                                                 # 기생성된 Result 문서를 복사 저장
    readResult = resultText.read()
    testDeviceList = open(deviceListPath)
    readDeviceList = testDeviceList.read()

    separatorText = "----------------------------------------------------------------"

    reportElement1 = ["[Test Info]","테스트명:\t\t[Automation Test] Mobile Plus 기본검사", separatorText,
                      "[Test Mobile Device]","Mobile 장치 이름: {}".format(mobileDeviceName),"Mobile 타입: {}".format(osType),"Mobile 버전: {}".format(mobileDeviceVersion),separatorText,
                      "[Test Device]", readDeviceList,"호환 테스트 장치: debug/multiDevice.txt 참조",separatorText,
                      "[Detail]",readResult,separatorText,
                      "테스트 시작 시간:{}".format(startTime),"테스트 종료 시간{}".format(endTime),"소요시간: {}".format(testDuration)]

    for textElement in reportElement1:
        reportfile = open(resultFileName, 'a')
        reportfile.write(textElement + "\n")
    reportfile.close()

#----------------------------------------------------------------------------------------------------------------------
# WebLink 테스트
#----------------------------------------------------------------------------------------------------------------------

def Test_Suite_WebLink(driver):

    nowTime = datetime.now()
    searchTimeInfo= nowTime.strftime("%Y%m%d%H%M%S")                                                                    # WebLink 검색 시간 지정
    print("WebLink 검색 시간: " + searchTimeInfo)
    deviceIp = "10.0.127.161"
    webLinkFenAddress = "dvrnames.net"
    # webLinkFenGlobal = "fen.idisglobal.com"
    webLinkFenName = "161"                                                                                          # 연구팀 시료
    deviceInfo = deviceIp
    deviceNameText = "webLink Device"

    devicePw = "qwerty0-"

    basicAuth = "YWRtaW46cXdlcnR5MC0="
    encyptAuth = "YWRtaW46ZjhkOWRlZWMxZjRiYWNiZWUxZTFmNjViODViMWNlM2VmYzMxNDZmZjdhMDc5YjljNjJjOGY5OTU2NWI4N2I5Mg=="

    writeDeviceList(deviceListPath, deviceNameText, deviceInfo, "admin", devicePw)

    # ----------------------------------- Reference Link ---------------------------------- #

    oldIpLiveLink = "idis://{0}:8016/trackID=0&basic_auth={1}".format(deviceIp,basicAuth)
    oldFenLiveLink = "idis://{0}:10088/name={1}&trackID=0&encrypt_auth={2}".format(webLinkFenAddress,webLinkFenName,encyptAuth)
    idisIpRegistLink = "idis://{0}:8016/register?basic_auth={1}".format(deviceIp,basicAuth)
    idisFenRegistLink = "idis://{0}:10088/register?name={1}&encrypt_auth={2}".format(webLinkFenAddress,webLinkFenName,encyptAuth)
    idisIpLiveLink = "idis://{0}:8016/w?basic_auth={1}".format(deviceIp,basicAuth)
    idisFenLiveLink = "idis://{0}:10088/w?name={1}&encrypt_auth={2}".format(webLinkFenAddress,webLinkFenName,encyptAuth)
    idisIpSearchLink = "idis://{0}:8016/s?basic_auth={1}".format(deviceIp,basicAuth)
    idisFenSearchLink = "idis://{0}:10088/s?name={1}&encrypt_auth={2}".format(webLinkFenAddress,webLinkFenName,encyptAuth)
    g2IpLiveLink = "g2client://proto/live?address={0}&port=8016&chs=0".format(deviceIp)
    g2FenLiveLink = "g2client://proto/live?fen%3DMTYx%26chs%3D0"
    g2IpSearchLink = "g2client://proto/play?address={0}&port=8016&chs=0&time={1}&ts=5".format(deviceIp,searchTimeInfo)
    g2FenSearchLink = "g2client://proto/play?fen%3DMTYx%26port%3D8016%26chs%3D0%26time%3D{}%26ts%3D5".format(searchTimeInfo)

    writeReport(reportFileName, "\n<Web Link>")

    New_Weblink_IpAdd(driver, mobileIndex, devicePw, idisIpRegistLink, delayTime)                                       # 신버전 IP로 장치등록 / osType으로 mobileIndex 사용 (iPAD 별도 분기 가능)

    if osType == "ios":
        element = "취소"  # app실행 시, 장치가져오기 취소 버튼
        mobile_click(driver, osType, 'id', element, delayTime)
    else:
        element = "android:id/button2"                                                                              # app실행 시, 장치가져오기 취소 버튼
        mobile_click(driver, osType, 'id', element, delayTime)

    element = "com.idis.android.idismobileplus:id/addFloatingButton"  # 메인리스트로 갔다는 가정
    mobile_element_displayed(driver, osType, 'id', element)
    if MobileBasicAct.displayedElement == "True":
        saveImageName = "New_IP장치등록.png"
        Save_Screenshot(driver, osType, "Weblink_", saveImageName)
        writeReport(reportFileName, "New_IP장치등록\t\tPASS\t[캡쳐]")
    else:
        element = "com.idis.android.idismobileplus:id/commonTopBackButton"                                               # 뒤로 가기 클릭
        mobile_click(driver, osType, 'id', element, delayTime)
        writeReport(reportFileName, "New_IP장치등록\t\t>>FAIL<<")
    element = "android:id/button2"  # 메세지창 발생
    mobile_click(driver, osType, 'id', element, delayTime)

    New_Weblink_FenAdd(driver, mobileIndex, devicePw, idisFenRegistLink, delayTime)                                        # 신버전 FEN으로 장치등록
    element = "com.idis.android.idismobileplus:id/addFloatingButton"  # 메인리스트로 갔다는 가정
    mobile_element_displayed(driver, osType, 'id', element)
    if MobileBasicAct.displayedElement == "True":
        saveImageName = "New_FEN장치등록.png"
        Save_Screenshot(driver, osType, "Weblink_", saveImageName)
        writeReport(reportFileName, "New_FEN장치등록\t\tPASS\t[캡쳐]")
    else:
        element = "com.idis.android.idismobileplus:id/commonTopBackButton"                                               # 뒤로 가기 클릭
        mobile_click(driver, osType, 'id', element, delayTime)
        writeReport(reportFileName, "New_FEN장치등록\t\t>>FAIL<<")
    element = "android:id/button2"  # 메세지창 발생
    mobile_click(driver, osType, 'id', element, delayTime)

    New_WebLink_Basic_Ip_Live(driver, mobileIndex, idisIpLiveLink, delayTime)
    element = "com.idis.android.idismobileplus:id/screenTopETCButton"                                                    # 레이아웃 버튼 확인
    mobile_element_displayed(driver, osType, 'id', element)
    if MobileBasicAct.displayedElement == "True":
        saveImageName = "New_Basic_Live_IP.png"
        Save_Screenshot(driver, osType, "Weblink_", saveImageName)
        writeReport(reportFileName, "New_Basic_Live_IP\t\tPASS\t[캡쳐]")
        element = "com.idis.android.idismobileplus:id/screenTopBackButton"  # 뒤로 가기 버튼
        mobile_click(driver, osType, 'id', element, delayTime)
        sleep(shortDelay)
    else:
        writeReport(reportFileName, "New_Basic_Live_IP\t\t>>FAIL<<")

    New_WebLink_Encrypt_Fen_Live(driver, mobileIndex, idisFenLiveLink, delayTime)
    element = "com.idis.android.idismobileplus:id/screenTopETCButton"                                                   #
    mobile_element_displayed(driver, osType, 'id', element)
    if MobileBasicAct.displayedElement == "True":
        saveImageName = "New_Encrypt_Live_FEN.png"
        Save_Screenshot(driver, osType, "Weblink_", saveImageName)
        writeReport(reportFileName, "New_Encrypt_Live_FEN\t\tPASS\t[캡쳐]")
        element = "com.idis.android.idismobileplus:id/screenTopBackButton"  # 뒤로 가기 버튼
        mobile_click(driver, osType, 'id', element, delayTime)
        sleep(shortDelay)
    else:
        writeReport(reportFileName, "New_Encrypt_Live_FEN\t\t>>FAIL<<")

    New_WebLink_Encrypt_Ip_Search(driver, mobileIndex, idisIpSearchLink, delayTime)
    element = "com.idis.android.idismobileplus:id/screenTopETCButton"                                                    # 레이아웃 버튼 확인
    mobile_element_displayed(driver, osType, 'id', element)
    if MobileBasicAct.displayedElement == "True":
        saveImageName = "New_Encrypt_Search_IP.png"
        Save_Screenshot(driver, osType, "Weblink_", saveImageName)
        writeReport(reportFileName, "New_Encrypt_Search_IP\t\tPASS\t[캡쳐]")
        element = "com.idis.android.idismobileplus:id/screenTopBackButton"  # 뒤로 가기 버튼
        mobile_click(driver, osType, 'id', element, delayTime)
        sleep(shortDelay)
    else:
        writeReport(reportFileName, "New_Encrypt_Search_IP\t\t>>FAIL<<")


    New_WebLink_Basic_Fen_Search(driver, mobileIndex, idisFenSearchLink, delayTime)
    element = "com.idis.android.idismobileplus:id/screenTopETCButton"                                                    # 레이아웃 버튼 확인
    mobile_element_displayed(driver, osType, 'id', element)
    if MobileBasicAct.displayedElement == "True":
        saveImageName = "New_Basic_Search_FEN.png"
        Save_Screenshot(driver, osType, "Weblink_", saveImageName)
        writeReport(reportFileName, "New_Basic_Search_FEN\t\tPASS\t[캡쳐]")
        element = "com.idis.android.idismobileplus:id/screenTopBackButton"  # 뒤로 가기 버튼
        mobile_click(driver, osType, 'id', element, delayTime)
        sleep(shortDelay)
    else:
        writeReport(reportFileName, "New_Basic_Search_FEN\t\t>>FAIL<<")

    #---------------------------------------------------------------------------

    G2_Weblink_Ip_Live(driver, mobileIndex, g2IpLiveLink, delayTime)                                                             # G2방식 IP로 Live접속
    element = "com.idis.android.idismobileplus:id/screenTopETCButton"
    mobile_element_displayed(driver, osType, 'id', element)
    if MobileBasicAct.displayedElement == "True":
        saveImageName = "G2_Live_IP.png"
        Save_Screenshot(driver, osType, "WebLink_", saveImageName)
        writeReport(reportFileName, "G2_Live_IP\t\tPASS\t[캡쳐]")
        element = "com.idis.android.idismobileplus:id/screenTopBackButton"  # 뒤로 가기 버튼
        mobile_click(driver, osType, 'id', element, delayTime)
        sleep(shortDelay)
    else:
        writeReport(reportFileName, "G2_Live_IP\t\t>>FAIL<<")

    # ---------------------------------------------------------------------------
    G2_Weblink_Fen_Live(driver, mobileIndex, g2FenLiveLink, delayTime)
    element = "com.idis.android.idismobileplus:id/screenTopETCButton"
    mobile_element_displayed(driver, osType, 'id', element)
    if MobileBasicAct.displayedElement == "True":
        saveImageName = "G2_Live_FEN.png"
        Save_Screenshot(driver, osType, "WebLink_", saveImageName)
        writeReport(reportFileName, "G2_Live_FEN\t\tPASS\t[캡쳐]")
        element = "com.idis.android.idismobileplus:id/screenTopBackButton"  # 뒤로 가기 버튼
        mobile_click(driver, osType, 'id', element, delayTime)
        sleep(shortDelay)
    else:
        writeReport(reportFileName, "G2_Live_FEN\t\t>>FAIL<<")

    G2_Weblink_Ip_Search(driver, mobileIndex, g2IpSearchLink, delayTime)
    element = "com.idis.android.idismobileplus:id/screenTopETCButton"
    mobile_element_displayed(driver, osType, 'id', element)
    if MobileBasicAct.displayedElement == "True":
        saveImageName = "G2_Search_IP.png"
        Save_Screenshot(driver, osType, "WebLink_", saveImageName)
        writeReport(reportFileName, "G2_Search_IP\t\tPASS\t[캡쳐]")
        element = "com.idis.android.idismobileplus:id/screenTopBackButton"  # 뒤로 가기 버튼
        mobile_click(driver, osType, 'id', element, delayTime)
        sleep(shortDelay)
    else:
        writeReport(reportFileName, "G2_Sarch_IP\t\t>>FAIL<<")

    G2_Weblink_Fen_Search(driver, mobileIndex, g2FenSearchLink, delayTime)                                                                    # G2방식 FEN으로 Search접속
    element = "com.idis.android.idismobileplus:id/screenTopETCButton"
    mobile_element_displayed(driver, osType, 'id', element)
    if MobileBasicAct.displayedElement == "True":
        saveImageName = "G2_Search_FEN.png"
        Save_Screenshot(driver, osType, "WebLink_", saveImageName)
        writeReport(reportFileName, "G2_Search_FEN\t\tPASS\t[캡쳐]")
        element = "com.idis.android.idismobileplus:id/screenTopBackButton"  # 뒤로 가기 버튼
        mobile_click(driver, osType, 'id', element, delayTime)
        sleep(shortDelay)
    else:
        writeReport(reportFileName, "G2_Sarch_FEN\t\t>>FAIL<<")
    # ---------------------------------------------------------------------------

    Old_Weblink_Basic_Ip_Live(driver, mobileIndex, oldIpLiveLink, delayTime)                                                                # 구버전 Basic암호화 IP접속
    element = "com.idis.android.idismobileplus:id/screenTopETCButton"
    mobile_element_displayed(driver, osType, 'id', element)
    if MobileBasicAct.displayedElement == "True":
        saveImageName = "Old_Basic_Live_IP.png"
        Save_Screenshot(driver, osType, "Weblink_", saveImageName)
        writeReport(reportFileName, "Old_Basic_Live_IP\t\tPASS\t[캡쳐]")
        element = "com.idis.android.idismobileplus:id/screenTopBackButton"  # 뒤로 가기 버튼
        mobile_click(driver, osType, 'id', element, delayTime)
        sleep(shortDelay)
    else:
        writeReport(reportFileName, "Old_Basic_Live_IP\t\t>>FAIL<<")

    Old_Weblink_Encrypt_Fen_Live(driver, mobileIndex, oldFenLiveLink, delayTime)                                                             # 구버전 Encrypt암호화 FEN접속
    element = "com.idis.android.idismobileplus:id/screenTopETCButton"
    mobile_element_displayed(driver, osType, 'id', element)
    if MobileBasicAct.displayedElement == "True":
        saveImageName = "Old_Encrypt_Live_Fen.png"
        Save_Screenshot(driver, osType, "Weblink_", saveImageName)
        writeReport(reportFileName, "Old_Encrypt_Live_Fen\t\tPASS\t[캡쳐]")
        element = "com.idis.android.idismobileplus:id/screenTopBackButton"  # 뒤로 가기 버튼
        mobile_click(driver, osType, 'id', element, delayTime)
        sleep(shortDelay)
    else:
        if osType == "ios":
            element = "확인"                                                                                              # 연결 끊어짐 경고창 확인 버튼
            mobile_click(driver, osType, 'iosId', element, delayTime)
        else:
            pass
        writeReport(reportFileName, "Old_Encrypt_Live_Fen\t\t>>FAIL<<")

#----------------------------------------------------------------------------------------------------------------------
# Main 함수
#----------------------------------------------------------------------------------------------------------------------

def main():
    global mobileDeviceVersion

    appInfoFile = "./debug/AppInfo.txt"
    exportAppInfo(appInfoFile)

    mobileDeviceVersion = MobileBasicAct.platformVersionInfo
    if MobileBasicAct.platformNameInfo == "ios":
        automationNameInfo = "XCUITest"
        Desired_Cap = {
            "deviceName": "{}".format(MobileBasicAct.deviceNameInfo),                                                   # 실제 장치 이름
            "platformVersion": "{}".format(MobileBasicAct.platformVersionInfo),                                         # 실제 장치 OS 버전
            "platformName": "{}".format(MobileBasicAct.platformNameInfo),                                               # 실제 장치 플랫폼
            # "app": "/Users/jungtong/Documents/Appium_ipa/IDIS/IDIS_1.1.1_98.ipa",
            "app": "{}".format(MobileBasicAct.appPathInfo),                                                             # App 실행 경로
            "automationName": "{}". format(automationNameInfo),                                                         # XCUITest (변경 X)
            "udid": "{}". format(MobileBasicAct.udidInfo),                                                              # 실제 장치 고유 id
            "xcodeOrgId": "26B93MEUCK",                                                                                 # 개발자 계정 고유 id
            "xcodeSigningId": "iPhone Developer",                                                                       # 변경 X
            "wƒdaBaseUrl": "http://{}:8100".format(MobileBasicAct.wƒdaBaseUrl),  # 실제 장치 ip                                       # 모바일 장치 접속 IP 주소
            "appPushTimeout": 60000,  # 타임아웃 설정 값
            "noReset": "true"

            # "appium:deviceName": "iPhone(2)",
            # "appium:platformVersion": "13.6.1",
            # "platformName": "ios",
            # "appium:app": "/Users/jungtong/Documents/Appium_ipa/IDIS_IPA_20220413/IDIS.ipa",
            # "appium:automationName": "XCUITest",
            # "appium:udid": "a4ec23762894478028cf84ee452e8a0318e23a1d",
            # "appium:xcodeOrgId": "26B93MEUCK",
            # "appium:xcodeSigningId": "iPhone Developer",
            # "appium:wƒdaBaseUrl": "http://192.168.0.6:8100",
            # "appium:appPushTimeout": "60000",
            # "appium:noReset": "true"
        }
    else:
        automationNameInfo = "Appium"
        Desired_Cap = {
            "platformName": "{}".format(MobileBasicAct.platformNameInfo),
            "platformVersion": "{}".format(MobileBasicAct.platformVersionInfo),
            "deviceName": "{}".format(MobileBasicAct.deviceNameInfo),
            "udid": "{}". format(MobileBasicAct.udidInfo),
            "automationName": "{}". format(automationNameInfo),
            "newCommandTimeout": 600000,
            "app": "{}". format(MobileBasicAct.appPathInfo),
            "appPackage": "{}". format(MobileBasicAct.appPackageInfo),
            "appActivity": "{}". format(MobileBasicAct.appActivityInfo),
            "noReset": True                                                                                               # 앱초기화 안함.
        }

    driver = webdriver.Remote("Http://localhost:4723/wd/hub", Desired_Cap)

    if osType == "ios":
        bundleId = "com.idis.ios.idismobileplus"
    else:
        bundleId = "com.idis.android.idismobileplus"

    if(driver.is_app_installed(bundleId)):                                                                              # App 삭제 후 재설치
        writeLog(logFileName, "기존 앱 삭제")
        driver.remove_app(bundleId)
        driver = webdriver.Remote("Http://localhost:4723/wd/hub", Desired_Cap)
        writeLog(logFileName, "앱 설치")
    else:
        pass

    os.mkdir(originFolderPath)                                                                                          # IOS Push 허용 버튼 발생 시 처리
    if osType == "ios":
        element = "허용 안 함"                                                                                            # 푸시 Off
        mobile_click(driver, osType, 'iosId', element, delayTime)
    writeReport(reportFileName, "<공용 테스트>")
    Test_Start_App(driver)                                                                                              # 앱 실행

    if installFail == 0:
        Test_GetVersion(driver)       # 앱 버전 빌드 확인

        driver = webdriver.Remote("Http://localhost:4723/wd/hub", Desired_Cap)                                          # 홈페이지 확인 후 재실행

        if osType == "ios":
            pass
        else:
            for loopNum in range(0, 10):
                try:
                    element = "android:id/button2"  # app실행 시, 장치가져오기 취소 버튼
                    mobile_click(driver, osType, 'id', element, delayTime)

                except:
                    sleep(delayTime)
                    pass

        sleep(longDelay)

        Test_Change_FenServer(driver)                                                                                   # FEN 서버 변경

        # -----------Web Link 테스트---------------
        Test_Suite_WebLink(driver)

        # -----------Basic Device 테스트---------------
        element = "android:id/button2"  # 메세지창 발생
        mobile_click(driver, osType, 'id', element, delayTime)

        writeReport(reportFileName, "\n<개별 장치 테스트>")
        Test_Suite_Regist_IpAddress(driver)                                                                             # IP 주소 등록 테스트

        Test_Suite_Regist_iNEX(driver)                                                                                  # iNEX 관련 테스트

        Test_Suite_Regist_Fen(driver)                                                                                   # FEN 등록 관련 테스트

        Test_Confirm_UI(driver)

    # -----------Multi Device 테스트---------------
    writeReport(reportFileName, "\n<호환 장치 테스트>")
    Test_Suite_Multi_Device(driver)

if __name__ == "__main__":
    startTime = datetime.now()
    print("Basic 라이브러리\t{}".format(MobileBasicAct.MBAL_VERSION))
    print("plus 라이브러리\t{}".format(MobilePlusAct.MPAL_VERSION))
    print("WebLink 라이브러리\t{}".format(MobileWebLink.MWL_VERSION))
    main()
    print("테스트 동작 완료")
    endTime = datetime.now()
    testDuration = endTime - startTime
    print(testDuration)
    Make_Report(originFolderPath, MobileBasicAct.deviceNameInfo, osType, MobileBasicAct.platformVersionInfo, testDuration)
    print("자동화 테스트 종료")