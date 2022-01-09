import requests
from lxml import etree
import re

url = 'https://www.digikey.cn/zh/products'
#UA = str(input())

#获取页面源码
def get_page(url):
    #网络走了代理的需要加上代理服务器的IP
    # proxy = {
    # 'https':'http://isasrv:8080'
    # }
    headers = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.55 Safari/537.36 Edg/96.0.1054.34'
    }
    session = requests.session()
    #session在发起请求是会创建cookies，并在下次发起session请求时包含sookies。
    #page_text = session.get(url = url,headers = headers,proxies=proxy).text
    page_text = session.get(url=url, headers=headers).text
    return page_text

#获取路径下的内容
def get_content(text,path):
    tree = etree.HTML(text)
    content_list = tree.xpath(path)
    return content_list


text = get_page(url)
#print(text)
content_list = get_content(text,'//*[@id="__next"]/main/section/div/div/div[1]/section/div/div/div[2]/a/span/text()')
url1_list = get_content(text,'//*[@id="__next"]/main/section/div/div/div[1]/section/div/div/div[2]/a/@href')
#print(url1_list)
#print(content_list)
i=-1
lei_dict = {}
#将获得的电子元件首批分类的名称与其对应的url放入字典lei_dict中
for content in content_list:
    print(content)
    i=i+1
    url = 'https://www.digikey.cn'+url1_list[i]
    lei_dict.update({content:url})
    
#在所列出的列表名单中选择你所需要查询的电子元件名称    
while 1:
    print("Select the electronic element name that you need to query and input it !")
    electronic_element_name = input(str('The name is:'))
    if electronic_element_name in content_list:
        break
    else:
        print('The name is not available in the list !')
text = get_page(lei_dict[electronic_element_name])
content_list = get_content(text,'//*[@id="__next"]/main/div/div/div/div[4]/section/div[1]/ul/li/a/span/text()')
pcs_list = get_content(text,'//*[@id="__next"]/main/div/div/div/div[4]/section/div[1]/ul/li/span/text()[2]')
#获取详情页url
concrete_url_list = get_content(text,'//*[@id="__next"]/main/div/div/div/div[4]/section/div[1]/ul/li/a/@href')
for n in range(0,len(content_list)):
    print(content_list[n]+pcs_list[n],'种货品')
#存放详情元件的名称与其对应的url
concrete_dict = {}
for i in range(0,len(content_list)):
    concrete_dict.update({content_list[i]:concrete_url_list[i]})
while 1:
    print("Select the electronic element name that you need to query and input it !")
    concrete_element_name = input(str('The name is:'))
    if concrete_element_name in content_list:
        break
    else:
        print('The name is not available in the list !')   


