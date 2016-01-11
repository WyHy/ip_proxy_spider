# -*- coding: utf-8 -*-
import random
from spiders.rules import get_ip_proxy
import mysql.connector
import settings
import traceback
import utils

class RandomUserAgent(object):
    """Randomly rotate user agents based on a list of predefined ones"""
    def __init__(self, agents):
        self.agents = agents
        
    @classmethod
    def from_crawler(cls, crawler):
        return cls(crawler.settings.getlist('USER_AGENTS'))
    
    def process_request(self, request, spider):
        #print "**************************" + random.choice(self.agents)
        request.headers.setdefault('User-Agent', random.choice(self.agents))

class ProxyMiddleware(object):
    def process_request(self, request, spider):
        if get_ip_proxy():           
            if request.meta.has_key('tried'):
                request.meta['tried'] = int(request.meta['tried']) + 1
            else:
                proxy = random.choice(get_ip_proxy())
                request.meta['proxy'] = "http://%s:%s" % (proxy['ip'], proxy['port'])
                request.meta['ip'] = proxy['ip']
                request.meta['port'] = proxy['port']
                request.meta['tried'] = 1
                
                print utils.get_time_now(), "use ip: %s proxy: %s, try for %s times" % (request.url, request.meta['proxy'], request.meta['tried'] )

                
#                 encoded_user_pass = base64.encodestring(proxy['user_pass'])
#                 request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass

    def process_response(self, request, response, spider):
        return response
    
    # 当请求失败并重试后会调用此方法    
    def process_exception(self, request, exception, spider):
        #清理失效ip
        
#         print '11111111111111111', request.meta
        
        if request.meta.has_key('ip'):
            utils.disable_ip(request.meta['ip'], request.meta['port'])
        
        #清空meta，请求重试
        request.meta.clear()
        return request