from appium import webdriver                                                    # Webdriver쓰기 위한 라이브러리호출
from time import sleep
from MobileBasicAct import *
import MobileBasicAct
import os


MWL_VERSION = "2022/07/07 02a"

longDelay = 5
middleDelay = 3
shortDelay = 1
delayTime = shortDelay

fenAddress = "qa.idis.co.kr"
deviceIP = "10.0.18.18"
fenName = "0048"
searchTime = "20210727010101"
weblinkPassword = "qwerty0-"



# osType = "android"

osType = "ios"

devicePw = ""
strftime("%y-%m-%d %I:%M:%S", localtime())
strTime = strftime("%y-%m-%d %H-%M-%S", localtime())

logFileName = "test_log.txt"										             # 디버그 로그 파일 이름


oldIpLiveLink = "idis://10.0.127.161:8016/trackID=0&basic_auth=YWRtaW46"
oldFenLiveLink = "idis://dvrnames.net:10088/name=161&trackID=0&encrypt_auth=YWRtaW46RTNCMEM0NDI5OEZDMUMxNDlBRkJGNEM4OTk2RkI5MjQyN0FFNDFFNDY0OUI5MzRDQTQ5NTk5MUI3ODUyQjg1NQ=="
idisIpRegistLink = "idis://10.0.127.161:8016/register?basic_auth=YWRtaW46"
idisFenRegistLink = "idis://dvrnames.net:10088/register?name=161&encrypt_auth=YWRtaW46RTNCMEM0NDI5OEZDMUMxNDlBRkJGNEM4OTk2RkI5MjQyN0FFNDFFNDY0OUI5MzRDQTQ5NTk5MUI3ODUyQjg1NQ=="
idisIpLiveLink = "idis://10.0.127.161:8016/w?basic_auth=YWRtaW46"
idisFenLiveLink = "idis://fen.idisglobal.com:10088/w?name=161&encrypt_auth=YWRtaW46RTNCMEM0NDI5OEZDMUMxNDlBRkJGNEM4OTk2RkI5MjQyN0FFNDFFNDY0OUI5MzRDQTQ5NTk5MUI3ODUyQjg1NQ=="
idisIpSearchLink = "idis://10.0.127.161:8016/s?basic_auth=YWRtaW46"
idisFenSearchLink = "idis://fen.idisglobal.com:10088/s?name=161&encrypt_auth=YWRtaW46RTNCMEM0NDI5OEZDMUMxNDlBRkJGNEM4OTk2RkI5MjQyN0FFNDFFNDY0OUI5MzRDQTQ5NTk5MUI3ODUyQjg1NQ=="
g2IpLiveLink = "g2client://proto/live?address=10.0.127.161&port=8016&chs=0"
g2FenLiveLink = "g2client://proto/live?fen%3DMTYx%26chs%3D0"
# g2IpSearchLink = "g2client://proto/play?address=10.0.127.161&port=8016&chs=0&time=20200630090225&ts=5"
# g2FenSearchLink = "g2client://proto/play?fen%3DMTYx%26port%3D8016%26chs%3D0%26time%3D20200626061459%26ts%3D5"

searchTimeInfo = "20211019090225"
g2IpSearchLink = "g2client://proto/play?address=10.0.127.161&port=8016&chs=0&time={}&ts=5".format(searchTimeInfo)
g2FenSearchLink = "g2client://proto/play?fen%3DMTYx%26port%3D8016%26chs%3D0%26time%3D{}%26ts%3D5".format(searchTimeInfo)

#------------------------------------------------------

def Open_Weblink(driver, osType, linkText, delayTime):
    if "ios" in osType:                                                                                                 # IOS는 우회 접속 (driver.get 작동 안함)
        driver.execute_script('mobile: terminateApp',{'bundleId': 'com.idis.ios.idismobileplus'})                       # App 종료
        sleep(delayTime)
        driver.execute_script('mobile: launchApp', {'bundleId': 'com.apple.mobilesafari'})                              # safari 로 우회 접속
        sleep(delayTime)

        if "iPAD" in osType:
            urlButton1 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='UnifiedTabBar')             # iPAD 주소창 ID로 접속
            urlButton1.click()
            sleep(3*delayTime)
            urlButton2 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='UnifiedTabBar')
            urlButton2.send_keys(Keys.BACK_SPACE + linkText)
        else:
            urlButton1 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='URL')
            urlButton1.click()
            sleep(3*delayTime)
            urlButton2 = driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='URL')
            urlButton2.send_keys(Keys.BACK_SPACE + linkText)

        sleep(delayTime)
        try:
            driver.find_element(by=AppiumBy.ACCESSIBILITY_ID, value='Go').click()
        except:
            pass
        sleep(3*delayTime)
        try:
            driver.find_element(by=AppiumBy.NAME, value='열기').click()
        except:
            pass
        sleep(3*delayTime)
    else:
        driver.get(linkText)

    sleep(10*delayTime)
#------------------------------------------------------

def G2_Weblink_Ip_Live(driver, osType, g2IpLiveLink, delayTime):
    writeLog(logFileName, ">>G2 Weblink Ip Live")
    driver.implicitly_wait(15)                                                                                          #Live창이 뜰 때까지 최대 15초 대기
    # linkText = "g2client://proto/live?address={0}&port=8016&chs=0" .format(deviceIp)
    Open_Weblink(driver, osType, g2IpLiveLink, delayTime)
    sleep(5*delayTime)

def G2_Weblink_Fen_Live(driver, osType, g2FenLiveLink, delayTime):
    writeLog(logFileName, ">>G2 Weblink FEN Live")
    driver.implicitly_wait(15)
    # linkText = "g2client://proto/live?fen%3DMDA0OA%3D%3D%26port%3D8016%26chs%3D0"                                       #Encrypt방식(FEN이름이 고정된 것으로 Test필요할 듯) 현재는 FEN이름이 0048
    Open_Weblink(driver, osType, g2FenLiveLink, delayTime)
    sleep(5*delayTime)

def G2_Weblink_Ip_Search(driver, osType, g2IpSearchLink, delayTime):
    writeLog(logFileName, ">>G2 Weblink Ip Search")
    driver.implicitly_wait(15)
    # linkText = "g2client://proto/play?address={0}&port=8016&chs=0&time={1}" .format(deviceIP, searchTime)               #SearchTime변수에 설정된 시간으로 Search이동
    Open_Weblink(driver, osType, g2IpSearchLink, delayTime)
    sleep(10*delayTime)

def G2_Weblink_Fen_Search(driver, osType, g2IpSearchLink, delayTime):
    writeLog(logFileName, ">>G2 Weblink FEN Search")
    driver.implicitly_wait(15)
    # driver.get("g2client://proto/play?fen%3DMDA0OA%3D%3D%26port%3D8016%26chs%3D0%26time%3D{0}" .format(searchTime))     #SearchTime변수에 설정된 시간으로 Search이동 / (FEN이름이 고정된 것으로 Test필요할 듯) 현재는 FEN이름이 0048
    Open_Weblink(driver, osType, g2IpSearchLink, delayTime)
    sleep(5*delayTime)

def Old_Weblink_Basic_Ip_Live(driver, osType,oldIpLiveLink, delayTime):
    writeLog(logFileName, ">>Old Weblink Ip Live")
    driver.implicitly_wait(15)
    # driver.get("idis://{0}:8016/trackID=0&basic_auth=YWRtaW46cXdlcnR5MC0=" .format(deviceIP))                           #장치 접속 admin / qwerty0- (Base64인코딩방식)
    Open_Weblink(driver, osType, oldIpLiveLink, delayTime)
    sleep(5*delayTime)

def Old_Weblink_Encrypt_Fen_Live(driver, osType, oldFenLiveLink, delayTime):
    writeLog(logFileName, ">>Old Weblink FEN Live")
    driver.implicitly_wait(15)
    # driver.get("idis://{0}:10088/name={1}&trackID=0&encrypt_auth=YWRtaW46RjhEOURFRUMxRjRCQUNCRUUxRTFGNjVCODVCMUNFM0VGQzMxNDZGRjdBMDc5QjlDNjJDOEY5OTU2NUI4N0I5Mg==" .format(fenAddress, fenName))
    #장치 접속 admin / qwerty0- (SHA-256인코딩방식)
    Open_Weblink(driver, osType, oldFenLiveLink, delayTime)
    sleep(5*delayTime)
#-----------------------------------------------------------------------------------------------------------------------

def New_Weblink_IpAdd(driver, osType, devicePw, idisIpRegitLink, delayTime):
    writeLog(logFileName, ">>New Weblink IP 등록")
    driver.implicitly_wait(15)                                                                                          #등록창이 뜰 때까지 최대 15초 대기
    # linkText = "idis://{0}:8016/register?basic_auth=YWRtaW4=".format(deviceIp)
    Open_Weblink(driver, osType, idisIpRegitLink, delayTime)
    sleep(5*delayTime)

    if "ios" in osType:
        element = "//XCUIElementTypeButton[@name=\"취소\"]"  # app실행 시, 장치가져오기 취소 버튼
        mobile_click(driver, osType, 'xpath', element, delayTime)
    else:
        element = "android:id/button2"  # 메세지창 발생
        mobile_click(driver, osType, 'id', element, delayTime)

    element = "com.idis.android.idismobileplus:id/siteAddPasswordEditText"                                              # 패스워드 입력란
    mobile_click(driver, osType, 'id', element, delayTime)                                                              # 패스워드입력란 클릭안하고 바로 send시 에러뜸
    inputText = devicePw
    mobile_send(driver, osType, inputText, 'id', element, delayTime)

    element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"                                                # 다음 버튼
    mobile_click(driver, osType, 'id', element, delayTime)
    driver.implicitly_wait(5*delayTime)

    element = "com.idis.android.idismobileplus:id/siteAddSiteNameEditText"                                              # 장치이름
    mobile_click(driver, osType, 'id', element, delayTime)
    inputText = "WebLink_IP등록"                                                                                         #장치이름 설정
    mobile_send(driver, osType, inputText, 'id', element, delayTime)
    element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"                                                # 다음버튼
    mobile_click(driver, osType, 'id', element, delayTime)

def New_Weblink_FenAdd(driver, osType, devicePw, idisFenRegitLink, delayTime):
    writeLog(logFileName, ">>New Weblink FEN 등록")
    # try:
    driver.implicitly_wait(15)                                                                                          #등록창이 뜰 때까지 최대 10초 대기
    # linkText = "idis://{0}:10088/register?name={1}&basic_auth=YWRtaW4=".format(fenAddress, fenName)
    Open_Weblink(driver, osType, idisFenRegitLink, delayTime)

    # -----------------------------------------------------------------------------------------------------------

    if "ios" in osType:
        element = "확인"  # 검색 실패시 확인
        mobile_click(driver, osType, 'id', element, delayTime)
    else:
        pass
    sleep(5 * delayTime)
    element = "com.idis.android.idismobileplus:id/siteAddFENEditText"  # FEN name입력란

    mobile_element_displayed(driver,osType,'id',element)
    if MobileBasicAct.displayedElement == "True":
        mobile_click(driver, osType, 'id', element, delayTime)
        sleep(3 * delayTime)
        element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"  # 다음 버튼
        mobile_click(driver, osType, 'id', element, delayTime)
    else:
        print("FEN Name 창 확인 불가")
    #-----------------------------------------------------------------------------------------------------------


    element = "com.idis.android.idismobileplus:id/siteAddPasswordEditText"                                              # 패스워드 입력란
    mobile_click(driver, osType, 'id', element, delayTime)                                                              # 패스워드입력란 클릭안하고 바로 send시 에러뜸
    inputText = devicePw
    mobile_send(driver, osType, inputText, 'id', element, delayTime)
    element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"                                                # 다음 버튼
    mobile_click(driver, osType, 'id', element, delayTime)

    driver.implicitly_wait(5*delayTime)

    element = "com.idis.android.idismobileplus:id/siteAddSiteNameEditText"                                              # 장치이름
    mobile_click(driver, osType, 'id', element, delayTime)
    inputText = "WebLink_FEN등록"                                                                                        # 장치이름 설정
    mobile_send(driver, osType, inputText, 'id', element, delayTime)
    element = "com.idis.android.idismobileplus:id/siteAddViewNextButton"                                                # 다음버튼
    mobile_click(driver, osType, 'id', element, delayTime)
    driver.implicitly_wait(5*delayTime)
    # except:
    #     pass

def New_WebLink_Basic_Ip_Live(driver, osType, idisIpLiveLink, delayTime):
    writeLog(logFileName, ">>New Weblink IP Live 접속")
    driver.implicitly_wait(15)
    # linkText = "idis://{0}:8016/w?basic_auth=YWRtaW46".format(deviceIp)                                                 #장치 접속 admin : No PW (Base64인코딩방식)
    Open_Weblink(driver, osType, idisIpLiveLink, delayTime)
    sleep(5 * delayTime)

def New_WebLink_Encrypt_Fen_Live(driver, osType, idisFenLiveLink, delayTime):
    writeLog(logFileName, ">>New Weblink Encrypt FEN Live 접속")
    driver.implicitly_wait(15)
    # linkText = "idis://{0}:10088/w?name={1}&encrypt_auth=YWRtaW46".format(fenAddress, fenName)  #장치 접속 admin / NoPw (SHA-256인코딩방식)
    Open_Weblink(driver, osType, idisFenLiveLink, delayTime)
    sleep(3*delayTime)

def New_WebLink_Encrypt_Ip_Search(driver, osType, idisIpSearchLink, delayTime):
    writeLog(logFileName, ">>New Weblink Encrypt IP Search 접속")
    driver.implicitly_wait(15)
    # linkText = "idis://{0}:8016/s?encrypt_auth=YWRtaW46RjhEOURFRUMxRjRCQUNCRUUxRTFGNjVCODVCMUNFM0VGQzMxNDZGRjdBMDc5QjlDNjJDOEY5OTU2NUI4N0I5Mg==" .format(deviceIp)
    #장치 접속 admin / qwerty0-(SHA-256인코딩방식)
    Open_Weblink(driver, osType, idisIpSearchLink, delayTime)
    sleep(5 * delayTime)

def New_WebLink_Basic_Fen_Search(driver, osType, idisFenSearchLink, delayTime):
    writeLog(logFileName, ">>New Weblink Fen Search 접속")
    driver.implicitly_wait(15)
    # linkText = "idis://{0}:10088/s?name={1}&basic_auth=YWRtaW46cXdlcnR5MC0=" .format(fenAddress, fenName)              #장치 접속 admin / qwerty0-(Base64인코딩방식)
    Open_Weblink(driver, osType, idisFenSearchLink, delayTime)
    sleep(5 * delayTime)

#-----------------------------------------------------------------------------------

def main():

    global mobileDeviceVersion

    # Desired_Cap = {
    #     # "deviceName": "RND5의 iPhone",  # 실제 장치 이름
    #     "deviceName": "Idis iPhoneX",  # 실제 장치 이름
    #     "platformVersion": "{}".format(mobileDeviceVersion),  # 실제 장치 OS 버전
    #     "platformName": "ios",  # 실제 장치 플랫폼
    #     "app": "/Users/jungtong/Documents/Appium_ipa/IDIS/IDIS.ipa",  # 실제 장치에서 실행할 앱 파일
    #     # "app": "/Users/jungtong/Documents/Appium_ipa/IDIS_1.1.1_103/IDIS_1.1.1_103.ipa",
    #     "automationName": "XCUITest",  # 변경 X
    #     # "udid": "93ca7786b0827f2bb118f26126a02ee4ab12a379",  # 실제 장치 고유 id
    #     "udid": "a4ec23762894478028cf84ee452e8a0318e23a1d",
    #     "xcodeOrgId": "26B93MEUCK",  # 개발자 계정 고유 id
    #     "xcodeSigningId": "iPhone Developer",  # 변경 X
    #     "wƒdaBaseUrl": "http://192.168.0.2:8100",  # 실제 장치 ip
    #     "appPushTimeout": 60000,  # 타임아웃 설정 값
    #     "noReset": "true"
    # }

    mobileDeviceVersion = "12.4.8"

    Desired_Cap = {
        "deviceName": "RND5의 iPhone",  # 실제 장치 이름
        "platformVersion": "{}".format(mobileDeviceVersion),  # 실제 장치 OS 버전
        "platformName": "ios",  # 실제 장치 플랫폼
        # "app": "/Users/jungtong/Documents/Appium_ipa/IDIS/IDIS.ipa",  # 실제 장치에서 실행할 앱 파일
        "app": "/Users/jungtong/Documents/Appium_ipa/IDIS_1.1.1_103/IDIS_1.1.1_103.ipa",
        "automationName": "XCUITest",  # 변경 X
        "udid": "93ca7786b0827f2bb118f26126a02ee4ab12a379",  # 실제 장치 고유 id
        "xcodeOrgId": "26B93MEUCK",  # 개발자 계정 고유 id
        "xcodeSigningId": "iPhone Developer",  # 변경 X
        "wƒdaBaseUrl": "http://192.168.0.3:8100",  # 실제 장치 ip
        "appPushTimeout": 60000,  # 타임아웃 설정 값
        "noReset": "true"
    }

    # Desired_Cap = {
    #     "platformName": "Android",
    #     "platformVersion": "11",
    #     "deviceName": "Gallaxy 10",
    #     "app": "C:\\MobileAppTest\\workspace\\apk\\app-idisplus.apk",                                                   # PC에 저장된 apk경로
    #     "automationName": "Appium",
    #     "udid": "R3CM80KQK5T",
    #     "newCommandTimeout": 60000,
    #     "appPackage": "com.idis.android.idismobileplus",
    #     "appActivity": "com.idis.android.rasmobile.splash.activity.SplashActivity",
    #     "noReset": True                                                                                                 # 앱초기화 안함.
    # }

    driver = webdriver.Remote("Http://localhost:4723/wd/hub", Desired_Cap)

    # driver.get('g2client://proto/live?address={0}&port=8016&chs=0' .format(deviceIP))
    print("Start")

    # New_Weblink_IpAdd(driver, osType, devicePw, idisIpRegistLink, delayTime)                                                                            # 신버전 IP로 장치등록
    # New_Weblink_FenAdd(driver, osType, devicePw, idisFenRegistLink, delayTime)                                                                # 신버전 FEN으로 장치등록
    # New_WebLink_Basic_Ip_Live(driver, osType, idisIpLiveLink, delayTime)                                                                                # 신버전  IP로 Live접속
    # New_WebLink_Encrypt_Fen_Live(driver, osType, idisFenLiveLink, delayTime)                                                                               # 신버전 FEN으로 Live접속
    # New_WebLink_Encrypt_Ip_Search(driver, osType, idisIpSearchLink, delayTime)                                                                                # 신버전 Encrypt암호화 IP로 Serch접속
    # New_WebLink_Basic_Fen_Search(driver, osType, idisFenSearchLink, delayTime)                                                                               # 신버전 basic암호화 FEN으로 Search접속
    #
    # G2_Weblink_Ip_Live(driver,osType, g2IpLiveLink, delayTime)                                                                        # G2방식 IP로 Live접속
    # G2_Weblink_Fen_Live(driver, osType, g2FenLiveLink, delayTime)                                                                      # G2방식 FEN으로 Live접속
    # G2_Weblink_Fen_Search(driver, osType, g2FenSearchLink, delayTime)                                                                    # G2방식 FEN으로 Search접

    G2_Weblink_Ip_Search(driver, osType, g2IpSearchLink, delayTime)                                                                     # G2방식 IP로 Search접속
    # Old_Weblink_Basic_Ip_Live(driver, osType, oldIpLiveLink, delayTime)                                                                # 구버전 Basic암호화 IP접속
    # Old_Weblink_Encrypt_Fen_Live(driver, osType, oldFenLiveLink, delayTime)                                                             # 구버전 Encrypt암호화 FEN접속
    print("Finish")
if __name__ == "__main__":
    main()