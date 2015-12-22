import requests
from bs4 import BeautifulSoup
import json
#import io.StringIO

page_url="http://www.lagou.com/zhaopin/Python/?labelWords=label"	
json_url="http://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC"
json_url1="http://www.lagou.com/jobs/companyAjax.json?city=%E5%8C%97%E4%BA%AC"

global header_info

header_info={
'Accept':'application/json, text/javascript, */*; q=0.01',
'Host':'www.lagou.com',
'Origin':'http://www.lagou.com',
'Proxy-Connection':'keep-alive',
'Referer':'http://www.lagou.com/zhaopin/Python/?labelWords=label',
'User-Agent':'Mozilla/5.0 (Windows NT 6.1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.106 Safari/537.36',
'X-Requested-With':'XMLHttpRequest',
}

jsion_session = requests.session()

def get_json_info(url):
	resp = jsion_session.get(url)
	json_data = resp.json()
	info_list = json_data['content']['result']

	for info_dict in info_list:
		print(info_dict['companyName'], info_dict['positionName'])
	return
	
def post_request(url):
	#post_data={'first':False, 'pn':3,'kd':'Python',} #为什么不起作用？
	post_data={}
	post_data['first']=False
	post_data['pn']=3
	post_data['kd']='Python'
	
	print(post_data)
	form_data=json.dumps(post_data)
	print(form_data)
	p = jsion_session.post(url, data=form_data, headers=header_info)
	#print(p.text)
	json_data = p.json()
	info_list = json_data['content']['result']

	for info_dict in info_list:
		print(info_dict['companyName'], info_dict['positionName'])
	return
	
def test_json():
	array = ['d', 'b', 'c', 'a', {'b':100, 'a':'letter a'}]
	encodestr = json.dumps(array)
	org_obj = json.loads(encodestr)
	print(org_obj.text())
	return


	
post_request(json_url)
#get_json_info(json_url)
#post_json_request(page_url,2)
#get_json_info(json_url)

#test_json()