from MySQLdb import connections
from superdatagenerator import Super2000Data
import pandas as pd
import cx_Oracle
import super_betcontent

Super2000Data().saleSwitch(1, 'N')


def ch1(num):
    s = []

    for i in range(4):
        s.append(str(int(num %256)))
        num /= 256

    return '.'.join(s[::-1])

ip_int = 168627238
ip_4v = ch1(ip_int)


print(ip_4v)

ch3 = lambda x:sum([256**j*int(i) for j,i in enumerate(x.split('.')[::-1])])
print(ch3('10.13.12.38'))

