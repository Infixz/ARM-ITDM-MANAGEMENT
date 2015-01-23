# -*- coding: utf-8 -*-
import csv
reader = csv.reader(file(r'D:\pylab\ARM-ITDM-MANAGEMENT-master\userlist.csv', 'rb'))
usernamedict={}
for line in reader:  #formlistval毛坯
    usernamedict[line[1]]=line[0]
print usernamedict