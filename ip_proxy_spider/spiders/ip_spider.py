# -*- coding: utf-8 -*- 
import sys
sys.path.append("..")

import scrapy
from scrapy.http import Request, FormRequest
from ip_proxy_spider.items import IPItem
from ip_proxy_spider.settings import DEFAULT_VALID_DELTA, MAX_PAGE_INDEX_NS, MAX_PAGE_INDEX_KDL
from ip_proxy_spider import utils
import datetime
import PyV8

class Item:
    def __init__(self, ip, port, anonymous, http_type, location, latency, last_verify_time):
        self.ip = ip
        self.port = port
        self.anonymous = anonymous
        self.http_type = http_type
        self.location = location
        self.latency = self.time_to_int(latency)
        self.last_verify_time = last_verify_time
        
    def time_to_int(self, timeStr):
        timeStr = timeStr.replace(u'秒', '')
        timeStr = timeStr.replace(u's', '')
        return int(float(timeStr) * 1000)
    
    def to_string(self):
        return {'ip':self.ip, 'port':self.port, 'anonymous':self.anonymous, 'http_type':self.http_type, 'location':self.location, 'latency':self.latency, 'last_verify_time':self.last_verify_time}
 
class Spider_test(scrapy.Spider):
    name = 'test'
    allowed_domains = ["http://ip.filefab.com/index.php"]
    start_urls = [
                  "http://ip.filefab.com/index.php"
                ]
    
    def parse(self, response):
        print response.status
        print response.xpath("//h1[@id='ipd']/span/text()").extract()        
        
class Spider_xicidaili(scrapy.Spider):
    name = "xicidaili"
    allowed_domains = ["xicidaili.com"]
    start_urls = [
        "http://www.xicidaili.com/nn/",
        "http://www.xicidaili.com/nt/",
        "http://www.xicidaili.com/wn/",
        "http://www.xicidaili.com/wt/"
    ]

    def parse(self, response):
        for val in self.start_urls:
            yield Request(url=val + str(1), callback=self.parse_item, meta={'page': 1, 'url':val}) 
        
    def parse_item(self, response):
        page = response.meta['page']
        url = response.meta['url']
        print utils.get_time_now(), "Target ==> " + (response.url)
        
#         if page > MAX_PAGE_INDEX_KDL:
#             return 
        
        #是否停止爬行
        isBreak = False
        
        itemList = []
        trs = response.xpath("//table[@id='ip_list']/tr")[1:]
        if trs:
            for sel in trs:
                item = Item(sel.xpath('td[3]/text()').extract()[0], sel.xpath('td[4]/text()').extract()[0], sel.xpath('td[6]/text()').extract()[0], 
                            sel.xpath('td[7]/text()').extract()[0], 
                            "".join(sel.xpath('td[5]//a/text()').extract() + sel.xpath('td[5]/text()').extract()).strip(), 
                            sel.xpath('td[9]/div/@title').extract()[0], 
                            sel.xpath('td[10]/text()').extract()[0])
                
#                 print item.to_string()
                itemList.append(item)
                
            #排序
            try: 
                import operator
            except ImportError: 
                cmpfun= lambda x: x.count # use a lambda if no operator module
            else: 
                cmpfun= operator.attrgetter("last_verify_time") # use operator since it's faster than lambda
               
            itemList.sort(key=cmpfun, reverse=True)
              
            for item in itemList:
                if not self.daysDelta(item.last_verify_time):
                    isBreak = True
                    break
                else:    
                    item_ = IPItem()
                    item_['ip'] = item.ip
                    item_['port'] = item.port
                    item_['anonymous'] = item.anonymous
                    item_['http_type'] = item.http_type
                    item_['location'] = item.location
                    item_['latency'] = item.latency
                    item_['last_verify_time'] = datetime.datetime.strptime(item.last_verify_time, '%y-%m-%d %H:%M')
                    item_['source'] = url
       
                    yield item_
        else:
            isBreak = True
                  
        if not isBreak:
            yield Request(url + str(page+1), callback=self.parse_item, meta={'page': page+1, 'url':url})
                
    def daysDelta(self, verify_time):
        #2014-07-30 19:15:25
        d1 = datetime.datetime.strptime(verify_time, '%y-%m-%d %H:%M')
        d2 = datetime.datetime.now()
        delta = d2 - d1
        #Ĭ��ʱ���Ϊ3��
        if delta.days <= DEFAULT_VALID_DELTA:
            return True
        else:
            return False
                
class Spider_kuaidaili(scrapy.Spider):
    name = "kuaidaili"
    allowed_domains = ["kuaidaili.com"]
    start_urls = [
        "http://www.kuaidaili.com/free/inha/",
        "http://www.kuaidaili.com/free/intr/",
        "http://www.kuaidaili.com/free/outha/",
        "http://www.kuaidaili.com/free/outtr/"
    ]

    def parse(self, response):
        for val in self.start_urls:
            yield Request(url=val + str(1), callback=self.parse_item, meta={'page': 1, 'url':val}) 
        
    def parse_item(self, response):
        page = response.meta['page']
        url = response.meta['url']
        
        print utils.get_time_now(), "Target ==> " + (response.url)
        
        if page > MAX_PAGE_INDEX_KDL:
            return 
        
        #是否停止爬行
        isBreak = False
        
        itemList = []
        trs = response.xpath('//tbody/tr')
        if trs:
            for sel in trs:
                item = Item(sel.xpath('td[1]/text()').extract()[0], sel.xpath('td[2]/text()').extract()[0], sel.xpath('td[3]/text()').extract()[0], 
                            sel.xpath('td[4]/text()').extract()[0], 
                            "".join(sel.xpath('td[5]//a/text()').extract()), 
                            sel.xpath('td[6]/text()').extract()[0], 
                            sel.xpath('td[7]/text()').extract()[0])
                
                itemList.append(item)
                
            #排序
            try: 
                import operator
            except ImportError: 
                cmpfun= lambda x: x.count # use a lambda if no operator module
            else: 
                cmpfun= operator.attrgetter("last_verify_time") # use operator since it's faster than lambda
             
            itemList.sort(key=cmpfun, reverse=True)
            
            for item in itemList:
                if not self.daysDelta(item.last_verify_time):
                    isBreak = True
                    break
                else:    
                    item_ = IPItem()
                    item_['ip'] = item.ip
                    item_['port'] = item.port
                    item_['anonymous'] = item.anonymous
                    item_['http_type'] = item.http_type
                    item_['location'] = item.location
                    item_['latency'] = item.latency
                    item_['last_verify_time'] = item.last_verify_time
                    item_['source'] = url
     
                    yield item_
        else:
            isBreak = True
                
        if not isBreak:
            yield Request(url + str(page+1), callback=self.parse_item, meta={'page': page+1, 'url':url})
                
    def daysDelta(self, verify_time):
        #2014-07-30 19:15:25
        d1 = datetime.datetime.strptime(verify_time, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.datetime.now()
        delta = d2 - d1
        #Ĭ��ʱ���Ϊ3��
        if delta.days <= DEFAULT_VALID_DELTA:
            return True
        else:
            return False

class Spider_nianshao(scrapy.Spider):           
    name = "nianshao"
    allowed_domains = ["www.nianshao.me" ]
    start_urls = [
            "http://www.nianshao.me/"
        ]

    def parse(self, response):
        yield Request(url=self.start_urls[0] + '?page=' + str(1), callback=self.parse_item, meta={'page': 1})  
        
    def parse_item(self, response):
        page = response.meta['page']
        
        print utils.get_time_now(), "Target ==> " + (response.url)
        
        if page > MAX_PAGE_INDEX_NS:
            return 
        
        #是否停止爬行
        isBreak = False
        
        itemList = []
        trs = response.xpath("//table[@class='table']/tbody/tr")       
        if trs: 
            for sel in trs:
                item = Item(sel.xpath('td[1]/text()').extract()[0], sel.xpath('td[2]/text()').extract()[0], sel.xpath('td[4]/text()').extract()[0], 
                            sel.xpath('td[5]/text()').extract()[0], sel.xpath('td[3]//text()').extract()[0], '0', 
                            sel.xpath('td[8]/text()').extract()[0])
                 
                itemList.append(item)
            #排序
            try: 
                import operator
            except ImportError: 
                cmpfun= lambda x: x.count # use a lambda if no operator module
            else: 
                cmpfun= operator.attrgetter("last_verify_time") # use operator since it's faster than lambda
             
            itemList.sort(key=cmpfun, reverse=True)
            
            for item in itemList:
                if not self.daysDelta(item.last_verify_time):
                    isBreak = True
                    break
                else:    
                    item_ = IPItem()
                    item_['ip'] = item.ip
                    item_['port'] = item.port
                    item_['anonymous'] = item.anonymous
                    item_['http_type'] = item.http_type
                    item_['location'] = item.location
                    item_['latency'] = item.latency
                    item_['last_verify_time'] = item.last_verify_time
                    item_['source'] = self.allowed_domains[0]
      
                    yield item_
        else:
            isBreak = True
                
        if not isBreak:
            yield Request(self.start_urls[0] + '?page=' + str(page+1), callback=self.parse_item, meta={'page': page+1})        
            
    def daysDelta(self, verify_time):
        #2015-12-23 8:34:51
        d1 = datetime.datetime.strptime(verify_time, '%Y-%m-%d %H:%M:%S')
        d2 = datetime.datetime.now()
        delta = d2 - d1
        #Ĭ��ʱ���Ϊ3��
        if delta.days <= DEFAULT_VALID_DELTA:
            return True
        else:
            return False

class Spider_spys(scrapy.Spider):
        name = "spys"
        allowed_domains = ["spys.ru"]
        start_urls = [
                "http://spys.ru/free-proxy-list/CN/"
        ]

        def parse(self, response):
            yield FormRequest.from_response(
                    response,
                    callback=self.parse_item,
                    method="POST",
                    formdata = {'xf1':'0','xf2': '2','xf3': '0','xf4':'0','xpp':'3'}
                   )

            
        def parse_item(self, response):
            print utils.get_time_now(), "Target ==> " + (response.url)
            js = PyV8.JSContext()
            js.enter()
            
            main_js = response.xpath("//body/script[1]/text()").extract()
            js.eval(main_js[0])
            
            itemList = []
            trs = response.xpath("//table[2]/tr[4]/td/table/tr") 
            
            if trs: 
                for tr in trs[4:-1]:
                    ip_port = tr.xpath("td[1]/font[2]")
                    ip = ip_port.xpath("text()").extract()
                    port = ip_port.xpath("script/text()").extract()[0]
                    port = port.split('<\/font>"+')[1]
                     
                    port_list = port[:-1].split("+")
                    port = ""
                    for val in port_list:
                        port = port + str(js.eval(val))
                 
                    item = Item(ip[0], port, tr.xpath("td[3]/font/text()").extract()[0], 
                                "".join(tr.xpath("td[2]/a/font[@class='spy1']/text()").extract() + tr.xpath("td[2]/a/font[@class='spy14']/text()").extract()), 
                                "".join(tr.xpath("td[4]/font/text()").extract() + tr.xpath("td[4]/font/font/text()").extract()), 
                                tr.xpath("td[6]/font/text()").extract()[0], tr.xpath("td[9]/font/font[@class='spy14']/text()").extract()[0] + tr.xpath("td[9]/font/text()").extract()[0])
                     
                    itemList.append(item)
                #排序
                try: 
                    import operator
                except ImportError: 
                    cmpfun= lambda x: x.count # use a lambda if no operator module
                else: 
                    cmpfun= operator.attrgetter("last_verify_time") # use operator since it's faster than lambda
                  
                itemList.sort(key=cmpfun, reverse=True)
                 
                for item in itemList:
                    if not self.daysDelta(str(item.last_verify_time)):
                        break
                    else:    
                        item_ = IPItem()
                        item_['ip'] = item.ip
                        item_['port'] = item.port
                        item_['anonymous'] = item.anonymous
                        item_['http_type'] = item.http_type
                        item_['location'] = item.location
                        item_['latency'] = item.latency
                        item_['last_verify_time'] = datetime.datetime.strptime(item.last_verify_time[:-1] + ':00', '%d-%b-%Y %H:%M:%S')
                        item_['source'] = self.allowed_domains[0]
                        
                        yield item_ 
            

        def daysDelta(self, verify_time):
            #23-dec-2015
            d1 = datetime.datetime.strptime(verify_time, '%d-%b-%Y %H:%M ')
            d2 = datetime.datetime.now()
            
            delta = d2 - d1
            #Ĭ��ʱ���Ϊ3��
            if delta.days <= DEFAULT_VALID_DELTA:
                return True
            else:
                return False