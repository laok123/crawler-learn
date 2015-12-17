# -*- coding: utf-8 -*-
import requests

URL = 'http://finance.sina.com.cn/stock/t/20150413/010021937376.shtml'
data = requests.get(URL).content.decode('gb2312','ignore').encode('utf-8')
with open('decode', 'wb') as f:
	f.write(data)

#with codecs.open('decode', 'wb', encoding='utf-8') as fp:
#	fp.write(data)

