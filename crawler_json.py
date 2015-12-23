import requests
from bs4 import BeautifulSoup
import json
from urllib import request, parse
#import io.StringIO

page_url="http://www.lagou.com/zhaopin/Python/?labelWords=label"	
json_url="http://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC"
json_url1="http://www.lagou.com/jobs/companyAjax.json?city=%E5%8C%97%E4%BA%AC"

global header_info

header_info = {"Content-Type": "application/x-www-form-urlencoded"}  #这个包头很重要，不填写post请受的form_data不生效

header_info2={
'Accept':'application/json, text/javascript, */*; q=0.01',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.8',
'Content-Length':26,
'Content-Type':'application/x-www-form-urlencoded; charset=UTF-8',
'Cookie':'LGMOID=20151221135835-8C43FC2DFBCED03237B2EFDECB6D0CFA; user_trace_token=20151221135838-e110a8d7-a7a7-11e5-8983-5254005c3644; LGUID=20151221135838-e110aca9-a7a7-11e5-8983-5254005c3644; hideOnekeyBanner=1; index_location_city=%E5%8C%97%E4%BA%AC; JSESSIONID=C45569A8B76DB3A061AB3DD3128B2D52; _gat=1; PRE_UTM=; PRE_HOST=; PRE_SITE=; PRE_LAND=http%3A%2F%2Fwww.lagou.com%2F; SEARCH_ID=8fb2101ffc7149f18ed8b81102e61b79; _ga=GA1.2.876400213.1450677518; Hm_lvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1450677518,1450753792,1450839877; Hm_lpvt_4233e74dff0ae5bd0a3d81c6ccf756e6=1450839899; LGSID=20151223110436-e65ee31f-a921-11e5-8832-525400f775ce; LGRID=20151223110458-f3537bd6-a921-11e5-8832-525400f775ce',
'Host':'www.lagou.com',
'Origin':'http://www.lagou.com',
'Proxy-Connection':'keep-alive',
'Referer':'http://www.lagou.com/zhaopin/Python/?labelWords=label',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
'X-Requested-With':'XMLHttpRequest',
}#这个header传入并未起到作用

json_session = requests.session()
	
def post_request(url):
	page_num = 1 #从第一页开始抓数据
	positionCounts = 0
	
	post_data={}
	post_data['first']='false'
	post_data['pn']= page_num
	post_data['kd']='Python'
	
	#首次抓取并获得hasNetPage值
	p = json_session.post(url, data=post_data, headers=header_info) #直接传入dict即可，post函数会自行转换为str
	json_data = p.json()
	info_list = json_data['content']['result']

	for result_dict in info_list:
		positionCounts = positionCounts+1
		print('%03d' % positionCounts, result_dict['companyName'], result_dict['positionName'])
	
	#根据hasNextPage值，循环抓取相关数据
	while json_data['content']['hasNextPage']:
		page_num = page_num+1
		post_data['pn'] = page_num
		p = json_session.post(url, data=post_data, headers=header_info) #直接传入dict即可，post函数会自行转换为str
		json_data = p.json()
		info_list = json_data['content']['result']
		
		for result_dict in info_list:
			positionCounts = positionCounts+1
			print('%03d' % positionCounts , result_dict['companyName'], result_dict['positionName'])
			
	return
	
def test_json():
	array = ['d', 'b', 'c', 'a', {'b':100, 'a':'letter a'}]
	encodestr = json.dumps(array)
	org_obj = json.loads(encodestr)
	print(org_obj.text())
	return

post_request(json_url)



