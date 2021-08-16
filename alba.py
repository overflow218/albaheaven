import os
import csv
import requests
from bs4 import BeautifulSoup

os.system("clear")
alba_url = "http://www.alba.co.kr"


#브랜드 url을 받았을때 몇페이지까지 있는지 구해주는 함수
def get_max_page(url):
	source = requests.get(url)
	soup = BeautifulSoup(source.text, 'html.parser')
	page = soup.find('p', class_='jobCount').find('strong').text
	page = int (page)
	return int(page / 50 + 1)


# 브랜드 별로 정리한 내용을 csv파일로 써주는 함수
def save_csv(result, brand_name):
	file = open(brand_name +".csv", mode = "w")
	writer = csv.writer(file)
	writer.writerow(['place', 'title', 'time', 'pay', 'date'])
	for r in result:
		writer.writerow(r)
	file.close()

source = requests.get(alba_url)
soup = BeautifulSoup(source.text, 'html.parser')
super_brand = soup.find('div', {'id':'MainSuperBrand'}).find_all('li', class_ = 'impact')

#알아보고자 하는 브랜드를 담아준다
brand_list = []
for i in super_brand:
	corp_url = i.find_all('a')[0]['href']
	corp_name = i.find('span', class_= 'company').text.replace(u'/',u' ')
	brand_list.append([corp_name, corp_url])
#각 브랜드별로 정보를 긁어와서 csv파일로 만들어준다.
for brand in brand_list:
	url = brand[1]
	name = brand[0]
	#page = get_max_page(url)
	result = []
	for i in range(1, 2):
		print(f'{name} {i}번째 페이지 추출중...')
		source = requests.get(f'{url}/?page={i}')
		soup = BeautifulSoup(source.text, 'html.parser')
		div = soup.find('div', id='NormalInfo').find_all('tr')

		for d in div:
			place = d.find('td', 'local')
			if(place == None):
				continue
			place = place.text.replace(u'\xa0',u' ')
			title = d.find('td', 'title').find('span', 'company').text
			time = d.find('td', 'data').find('span').text
			tmp_pay = d.find('td', 'pay').find_all('span')
			pay = tmp_pay[0].text + tmp_pay[1].text
			date = d.find('td', 'regDate').text
			tmp_result = [place, title, time, pay, date]
			result.append(tmp_result)

	save_csv(result, name)
