import requests
from bs4 import BeautifulSoup
import json
import datetime
from pymongo import MongoClient

page_url="http://www.lagou.com/zhaopin/Python/?labelWords=label"	
json_url="http://www.lagou.com/jobs/positionAjax.json?city=%E5%8C%97%E4%BA%AC"
header_info = {"Content-Type": "application/x-www-form-urlencoded"}  # 窗体数据被编码为名称/值对。这是标准的编码格式。这个包头很重要，不填写post请求的form_data参数不生效.

MONGO_CONN = MongoClient('localhost', 27017)
json_session = requests.session()
	
def save(data):
	data['_id'] = data['positionId']
	data['updateTime'] = datetime.datetime.now()
	
	MONGO_CONN['lagouDB']['positionsOfPython'].update_one(
		filter={'_id': data['_id']},
		update=('$set': data),
		upsert=True
	)
	
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
		save(result_dict) #save to database
	
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
			save(result_dict) #save to database

	return

post_request(json_url)



