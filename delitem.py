# -*- coding: utf-8 -*-
import urllib2
import urllib
import cookielib
import csv
from poster.encode import multipart_encode
from poster.streaminghttp import StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler

login_page = "http://10.164.1.100/index.php"
login_data = {"authusername":"Jonathan","authpassword":"1234"}
edititem_page = "http://10.164.1.100/index.php?action=edititem&id=new"
delitem_page = "http://10.164.1.100/index.php?action=edititem&delid="
edituser_page = "http://10.164.1.100/index.php?action=edititem&id=new"
deluser_page = "http://10.164.1.100/index.php?action=edituser&delid="
choice = raw_input("\n!!! Plz type in the the target page number you're going to\n\n1.Items edit page\n2.Users edit page\n3.Quit\n\nSo your choice is:")
if choice == '1':
    selected_page=delitem_page
elif choice == '2':
    selected_page=deluser_page
else:
    exit()
#构造opener
handlers = [StreamingHTTPHandler, StreamingHTTPRedirectHandler, StreamingHTTPSHandler]
opener = urllib2.build_opener(*handlers)
opener.add_handler(urllib2.HTTPCookieProcessor(cookielib.CookieJar()))#带cookie的opener
opener.addheaders = [('User-agent',r'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.65 Safari/537.36')]#伪装成一个正常的浏览器，以防服务器拒绝访问。

urllib2.install_opener(opener)

#登陆及提交表单
opener.open(login_page,urllib.urlencode(login_data))
startnum=int(raw_input("Plz type in the start number of the items you're going to delete:\n"))
endnum=int(raw_input("Plz type in the end number of the items you're going to delete:\n"))+1
for n in range(startnum,endnum):
    opener.open(selected_page+str(n))
    print r"There's %s items last."% (endnum-n)
print u'\nIt has been done!'
exit()