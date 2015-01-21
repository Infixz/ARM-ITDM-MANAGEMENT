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
#待POST的数据结构
formdict = {"itemtypeid":10,
"ispart":0,
"rackmountable":0,
"manufacturerid":7,
"model":'model',
"usize":'',
"sn":'sn',
"sn2":'sn2',
"sn3":'',
"comments":'comments',
"label":'label',
"status":0,
"userid":1,
"locationid":'',
"locareaid":'',
"rackid":'',
"rackposition":'',
"rackposdepth":6,
"function":'',
"maintenanceinfo":'',
"origin":'',
"purchprice":'',
"purchasedate":'',
"warrantymonths":12,
"warrinfo":'',
"hd":'',
"ram":'',
"cpu":'',
"cpuno":1,
"corespercpu":2,
"dnsname":'',
"macs":'',
"ipv4":'',
"ipv6":'',
"remadmip":'',
"panelport":'',
"switchid":'',
"switchport":'',
"ports":0,
"itemsfilter":'Filter',
"invoicefilter":'Filter',
"softfilter":'Filter',
"contrfilter":'Filter',
"action":'edititem'}

#需要更新的数据内容
formlistfixed=["model",
"sn2",
"sn",
"dnsname",
"warrantymonths",
"comments",
"label"]

#csv转化来的n个条目（每个条目一个formdict）&处理
reader = csv.reader(file(r'C:\Users\johwan01\Documents\Johnathon wang\ARM\asset_info.csv', 'rb'))
formlistval=[line for line in reader]  #formlistval毛坯
for i in range(len(formlistval)):#formlistval处理(合并备注，添加标题)
    formlistval[i][1]+='(P/N)'
    formlistval[i][5]='username:'+formlistval[i][5]+"\nDepartment:"+formlistval[i][6]
    formlistval[i].pop(6)
    formlistval[i][6]+='(Asset Id)'
    try:
        formlistval[i][4]=int(formlistval[i][4][5])-2
    except:
        continue

#dict更新函数
def dictupdate(x):#用来n次刷新_需要更新的7个元素的字典
    for i in range(7):  #6=len(formlistfixed)
        formdict[formlistfixed[i]]=formlistval[x][i]

#网络端初始化
login_page = "http://10.164.1.100/index.php"
edit_page = "http://10.164.1.100/index.php?action=edititem&id=new"
login_data = {"authusername":"Jonathan","authpassword":"1234"}

#构造opener
handlers = [StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler]
opener = urllib2.build_opener(*handlers)
opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))#带cookie的opener
opener.addheaders = [('User-agent',r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36')]#伪装成一个正常的浏览器，以防服务器拒绝访问。

urllib2.install_opener(opener)
#</初始化>

#登陆及提交表单
opener.open(login_page,urllib.urlencode(login_data))#登陆；存疑：要request才能算请求页面么；应该没事，记得上次返回页面已经是itemedit页面了
opener.open(edit_page)
for n in range(len(formlistval)):#n次迭代发送完整个csv文件的item
    dictupdate(n)#多少次发送多少次item_dict更新
    datagen, headers = multipart_encode(formdict)
    request = urllib2.Request(edit_page, datagen, headers)
    result = urllib2.urlopen(request)
    print r"There's %s items last."% (len(formlistval)-n)
print u'\nIt has been done!'
exit()