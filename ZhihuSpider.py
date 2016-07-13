#!/usr/bin/env python
#coding=utf-8
import sys
from odo.backends.tests.test_mongo import pymongo
reload(sys)
sys.setdefaultencoding("utf-8")
import requests
import re
import Queue
from collections import deque
from lxml import html


class Spider():
    def __init__(self, url):
        # 初始化
        self.url = url
        self.header={}
        #cookie
        self.header = {}
        self.header["User-Agent"]="Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:35.0) Gecko/20100101 Firefox/35.0"
        self.cookies={'_za':'1083cf47-44ac-4a12-bc38-ab2cf3400518',
        'udid':'"AHCAq-SylAmPTmiLH7XcPGHhiFwko2YTdIU=|1457555183"',
        '_zap':'60e28b6a-8317-4f77-880f-3f29b016485e',
        'd_c0':'"AAAAa3_BogmPTuKqd_cdW17aT-0z4SJNmz0=|1461257374"',
        '_ga':'GA1.2.697870809.1461297740',
        '_xsrf':'fda24504e0f2beb4c65c3f3be7cd6b87',
        'q_c1':'cfbe6a31e95b405abcaab587818cf2ba|1467562681000|1451696127000',
        '__utmt':'1',
        'l_cap_id':'"ZDVmNDAyMjQwZmNhNDY0ZTg0ZjUxZWMxYzE0ZTk2MmU=|1467737987|499ac52a06f3b84a98fe7212ead95a095d8eb074"',
        'cap_id':'"YmY5MjdiYmMwNGIwNDFkODhmYTk2YmUyYzNkZGJmMDQ=|1467737987|8beaecd1b33bf77ed761d439d24314316d5ee0cb"',
        '__utma':'51854390.697870809.1461297740.1467737986.1467737986.1',
        '__utmb':'51854390.2.10.1467737986',
        '__utmc':'51854390',
        '__utmz':'51854390.1467737986.1.1.utmcsr=zhihu.com|utmccn=(referral)|utmcmd=referral|utmcct=/',
        '__utmv':'51854390.000--|3=entry_date=20160101=1',
        'login':'"MzNiZWI3MWI0NGRhNDVmOWEwZTEzNTA1YzFjYjhmM2I=|1467737995|6f1e1c2db806ae38752842d5d871e24cda4bc6c4"',
        'a_t':'"2.0AEBAxmINLwoXAAAAjHSjVwBAQMZiDS8KAAAAa3_BogkXAAAAYQJVTYx0o1cAzZ-mFVtkyagGpe5CAhWdYsggUF1BMUl_vsYN4fs05PTXtnGe8WsRQA=="',
        'z_c0':'Mi4wQUVCQXhtSU5Md29BQUFCcmY4R2lDUmNBQUFCaEFsVk5qSFNqVndETm42WVZXMlRKcUFhbDdrSUNGWjFpeUNCUVhR|1467737996|7c4ea26bac2d6b9f249138504710168887b4e7ab',
        'n_c':'1'}
        
        
    def get_data(self):
        get_html=requests.get(self.url,cookies=self.cookies,headers=self.header,verify=False)
        #get_html.encode = 'utf-8'
        # 生成xpath
        tree = html.fromstring(get_html.text)
        self.user_name=self.get_element(tree.xpath("//a[@class='name']/text()"))
        self.user_bio = self.get_element(tree.xpath("//span[@class='bio']/@title"))
        self.user_location=self.get_element(tree.xpath("//span[@class='location item']/@title"))
        self.user_field = self.get_element(tree.xpath("span[@class='business item']/i/@title"))
        self.user_gender=self.get_element(tree.xpath("//span[@class='item gender']/i/@class"))
        if "female" in self.user_gender and self.user_gender:
            self.user_gender = "female"
        else:
            self.user_gender = "male"
        self.user_employment = self.get_element(tree.xpath("//span[@class='employment item']/@title"))
        self.user_position = self.get_element(tree.xpath("//span[@class='position item']/@title"))
        self.user_education = self.get_element(tree.xpath("//span[@class='education item']/@title"))
        self.user_major = self.get_element(tree.xpath("//span[@class='education-extra item']/@title"))
        self.user_sidebar = tree.xpath("//div[@class='zu-main-sidebar']//strong/text()")
        self.user_following = self.user_sidebar[0]
        self.user_follower = self.user_sidebar[1]
        if len(self.user_sidebar)==5:
            self.user_column = self.user_sidebar[2]
            self.user_column= re.findall('\d*',self.user_column)[0]
            self.user_topic = self.user_sidebar[3]
            self.user_topic = re.findall('\d*',self.user_topic)[0]
            self.user_pageview = self.user_sidebar[4]
        else:
            self.user_column = 0
            self.user_topic = self.user_sidebar[2]
            self.user_topic = re.findall('\d*',self.user_topic)[0]
            self.user_pageview = self.user_sidebar[3]
        self.user_profile_bar = tree.xpath("//div[@class='profile-navbar clearfix']//span[@class='num']/text()")
        self.user_ask = self.user_profile_bar[0]
        self.user_answer = self.user_profile_bar[1]
        self.user_article = self.user_profile_bar[2]
        self.user_collection = self.user_profile_bar[3]
        self.user_edit = self.user_profile_bar[4]
        self.user_agree = self.get_element(tree.xpath("//span[@class='zm-profile-header-user-agree']//strong/text()"))
        self.user_thanks = self.get_element(tree.xpath("//span[@class='zm-profile-header-user-thanks']//strong/text()"))
        #return followee list
        self.user_followees = tree.xpath("//h2[@class='zm-list-content-title']/a/@href")
        self.print_data_out()
        return self.user_followees
    
    def zhihu_dict(self):
        data ={"name":self.user_name,
         "bio":self.user_bio,
         "field":self.user_field,
         "gender":self.user_gender,
         "employment":self.user_employment,
         "position":self.user_position,
         "education":self.user_education,
         "major":self.user_major,
         "following":self.user_following,
         "follower":self.user_follower,
         "column":self.user_column,
         "topic":self.user_topic,
         "pageview":self.user_pageview,
         "ask":self.user_ask,
         "answer":self.user_answer,
         "article":self.user_article,
         "collection":self.user_collection,
         "edit":self.user_edit,
         "agree":self.user_agree,
         "thanks":self.user_thanks}
        return data
        
    def get_element(self,xpath):
        if xpath:
            return xpath[0]
        else:
            return ''

  
    def print_data_out(self):
        print "*" * 60
        print '用户名:%s\n' % self.user_name
        print "用户性别:%s\n" % self.user_gender
        print '用户城市:%s\n' % self.user_location
        print '用户雇主:%s\n' % self.user_employment
        print '用户职位:%s\n' % self.user_position
        print '教育:%s\n' % self.user_education
        print '专业:%s\n' % self.user_major
        print '关注了:%s\n' % self.user_following
        print '被关注:%s\n' % self.user_follower
        print '专栏数:%s\n' % self.user_column
        print '话题数:%s\n' % self.user_topic
        print '页面访问量:%s\n' % self.user_pageview
        print '提问数:%s\n' % self.user_ask
        print '回答数:%s\n' % self.user_answer
        print '文章数:%s\n' % self.user_article
        print '收藏数:%s\n' % self.user_collection
        print '公共编辑:%s\n' % self.user_edit
        print '获得赞同:%s\n' % self.user_agree
        print '获得感谢:%s\n' % self.user_thanks
        print "*" * 60
        
def main():
    m = Spider('https://www.zhihu.com/people/reynolds/followees')
    next_people = m.get_data()
    zhihu_data = m.zhihu_dict()
    # 利用队列实现BFS算法
    url_queue = deque()
    for people in next_people:
        url_queue.append(people)
    #连接mongodb
    client=pymongo.MongoClient("localhost",27017)
    db = client.zhihu2
    collection=db.data_collection
    # insert one item to mongoDB 
    user_name = zhihu_data['name']
    # check duplicates
    if not collection.find_one({"name":user_name}):
            collection.insert(zhihu_data)
    else:
        pass

    # BFS
    try:
        # 限制爬取的最大数量
        count = 1
        while not url_queue and count < 10000:
            m = Spider(url_queue.popleft()+'/followees')
            next_people = m.get_data()
            zhihu_data = m.zhihu_dict()
            user_name = zhihu_data['name']
            for people in next_people:
                url_queue.append(people)
            # checking duplicates    
            if not collection.find_one({"name":user_name}):
                collection.insert(zhihu_data)
            else:
                pass
            count += 1

    except:
        print m.url
        sys.exit()
        
        

        
    
    
    #print next_people
    #for people in next_people:
    #    url = people+'/followees'
    #    n = Spider(url)
    #    next = n.get_data()
        
    
main()



#result = etree.tostring(tree, pretty_print=True,encoding='UTF-8')
#print result