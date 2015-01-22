# -*- coding: utf-8 -*-
"""
Created on Wed Jan 14 14:28:30 2015

@author: johwan01
"""
import urllib2
import urllib
import cookielib
import csv
from poster.encode import multipart_encode
from poster.streaminghttp import StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler

#main

#<初始化>
#csv转化来的n个条目（每个条目一个formdict）&处理
reader = csv.reader(file(r'C:\Users\johwan01\Documents\Johnathon wang\ARM\userbook.csv', 'rb'))
formlistval=[line for line in reader]  #formlistval毛坯

#网络端初始化
login_page = "http://10.164.1.100/index.php"
login_data = {"authusername":"Jonathan","authpassword":"1234"}
itemsedit_page = "http://10.164.1.100/index.php?action=edititem&id=new"
usersedit_page = "http://10.164.1.100/index.php?action=edituser&id=new"
#构造opener
handlers = [StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler]
opener = urllib2.build_opener(*handlers)
opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))#带cookie的opener
opener.addheaders = [('User-agent',r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36')]#伪装成一个正常的浏览器，以防服务器拒绝访问。
urllib2.install_opener(opener)
#</初始化>

#登陆及提交表单
opener.open(login_page,urllib.urlencode(login_data))#登陆
opener.open(usersedit_page)
for i in range(len(formlistval)):#n次迭代发送完整个csv文件的user
    formlistval[i].pop(0)
    formlistval[i].pop(0)
    username = formlistval[i][0]
    department = formlistval[i][1]
    userdict=[("id","new"),("username",username),("usertype",1),("userdesc",department),("pass",""),("id","new"),("action","edituser")]
    datagen, headers = multipart_encode(userdict)
    request = urllib2.Request(usersedit_page, datagen, headers)
    result = urllib2.urlopen(request)
    print r"There's %s items last."% (len(formlistval)-i)
print u'\nIt has been done!'
exit()