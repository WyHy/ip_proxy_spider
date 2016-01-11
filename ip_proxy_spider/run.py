#-*- coding:utf-8 -*-
import sys
sys.path.append(".")
sys.path.append("..")

from spiders.ip_spider import Spider_kuaidaili, Spider_nianshao, Spider_spys, Spider_xicidaili
from scrapy.crawler import CrawlerProcess, CrawlerRunner
from twisted.internet import reactor, defer
from scrapy.utils.project import get_project_settings

spiders = []

spider_0 = Spider_kuaidaili()
spider_1 = Spider_nianshao()
spider_2 = Spider_spys()
spider_3 = Spider_xicidaili()

spiders.append(spider_0)
spiders.append(spider_1)
spiders.append(spider_2)
spiders.append(spider_3)
    
def run_crawler_by_process():
    process = CrawlerProcess(get_project_settings())
    
    [process.crawl(spider) for spider in spiders]
    process.start()

def run_crawler_by_runner():
    runner = CrawlerRunner(get_project_settings())
    
    [runner.crawl(spider) for spider in spiders]
    d = runner.join()
    d.addBoth(lambda _: reactor.stop())
    reactor.run()
    
def run_crawler_by_runner_and_defer():
    runner = CrawlerRunner(get_project_settings())
    @defer.inlineCallbacks
    def crawl():
        [(yield runner.crawl(spider)) for spider in spiders]        
        reactor.stop()
    
    crawl()
    reactor.run()
    
    
if __name__ == "__main__":
    run_crawler_by_process()
#     run_crawler_by_runner()
#     run_crawler_by_runner_and_defer()
    
