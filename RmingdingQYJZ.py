# -*- coding: utf-8 -*-
import os
import sys
import requests
import re
import threading #用于触发时间

default_encoding="utf-8"
if(default_encoding!=sys.getdefaultencoding()):
    reload(sys)
    sys.setdefaultencoding(default_encoding)

from email.mime.text import MIMEText

def Page_Info(myPage):
    """"Regex"""
    mypage_Info = re.findall('<span class="tit_em1">【前沿讲座】+.*?</span>', myPage)
    # mypage_Info2 = re.findall('<span class="tit_em1">【素质拓展】+.*?</span>', myPage)
    return mypage_Info
def Spider(url):
    myPage = requests.get(url).content.encode("utf-8")
    myPageResults = Page_Info(myPage) #通过Page_Info（）函数匹配到讲座信息

    readNameFile= open("Speech_Name.txt", "a+")
    SpeechName = readNameFile.readlines()
    readNameFile.close()

    lastNameNum = len(SpeechName)
    lastestSpeechName = SpeechName[lastNameNum-1].strip("\n").lstrip("﻿<")
    pagelastone = myPageResults[0].strip("\n").lstrip("﻿<")
    if  pagelastone!= lastestSpeechName :
        print "出前沿讲座了，并给您发送了3封邮件"
        for i in ["1", "2", "3"]:
            print "Send email " + i
            QQMail()  # 3封邮件通知出新讲座

        myfile = open("Speech_Name.txt", 'a+')
        myfile.write(pagelastone+"\n")
        myfile.close()
def QQMail():
    import smtplib
    # ========================================== # 要发给谁，这里发给4个人 #==========================================
    mailto_list=["384087521@qq.com"]
    # mailto_list=["384087521@qq.com","598611416@qq.com","1632280739@qq.com","841782779@qq.com"]
    #========================================== # 设置服务器，用户名、口令以及邮箱的后缀 #==========================================
    mail_host="smtp.qq.com"
    mail_user="384087521@qq.com"
    mail_pass="tiankong34"
    #qq要求授权码，密码不行，你要在手机发短信具体的上qq邮箱网站上看
    mail_postfix="qq.com"
    #========================================== # 发送邮件 #==========================================
    def send_mail(to_list,sub,content):
        me=mail_user+"<"+mail_user+"@"+mail_postfix+">"
        msg = MIMEText(content)
        msg['Subject'] = sub
        msg['From'] = me
        msg['To'] = ";".join(to_list)
        try:
            s = smtplib.SMTP_SSL(mail_host, 465)
            s.set_debuglevel(1)
            s.login(mail_user,mail_pass)
            s.sendmail(me, to_list, msg.as_string())
            s.close()
            return True
        except:
            return False
    if send_mail(mailto_list, "测试：出 前沿讲座 了！", "大鱼叫你快去报名喽~~~\n http://sem.bjtu.edu.cn/lists-sem_hdyb.html"):
        print ("发送成功")
    else:
        print ("发送失败")

def myMoniter():
    print u"滴答"
    Spider(start_url)
    global mytimer
    mytimer = threading.Timer(10, myMoniter)
    mytimer.start()

if __name__=='__main__':
    "start"
    start_url = "http://sem.bjtu.edu.cn/lists-sem_hdyb.html"
    mytimer = threading.Timer(1,myMoniter)
    mytimer.start()
    # try:
    mytimer.sleep(2)
    # except AttributeError:
    #     print "可能是版本问题，timer.sleep()异常"
    # else:
    #     print "未知异常"

    mytimer.cancel()
    print "end"
