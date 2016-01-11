# -*- coding: utf-8 -*- 
from sqlalchemy import Column, VARCHAR, DATETIME, INT
from sqlalchemy.ext.declarative.api import declarative_base
from sqlalchemy.engine import create_engine
from sqlalchemy.orm.session import sessionmaker
from ip_proxy_spider.settings import MYSQL_HOST, MYSQL_DBNAME, MYSQL_USER, MYSQL_PASSWD

Base = declarative_base()

class ProxyRule(Base):
    __tablename__ = "rules"
    
    id = Column(INT, primary_key=True)
    name = Column(VARCHAR(20))
    download_delay = Column(INT)
    allowed_domain = Column(VARCHAR(255))
    start_urls = Column(VARCHAR(255))
    sub_link = Column(VARCHAR(255))
    table_xpath = Column(VARCHAR(255))
    trs_xpath = Column(VARCHAR(255))
    ip_xpath = Column(VARCHAR(255))
    port_xpath = Column(VARCHAR(255))
    anonymous_xpath = Column(VARCHAR(255))
    http_type_xpath = Column(VARCHAR(255))
    location_xpath = Column(VARCHAR(255))
    latency_xpath = Column(VARCHAR(255))
    last_verify_time_xpath = Column(VARCHAR(255))
    max_page_num_xpath = Column(VARCHAR(255))
    time_format = Column(VARCHAR(20))
    
class ProxyItem(Base):
    __tablename__ = "ip_proxy_info"
    
    id = Column(INT, primary_key=True)
    ip = Column(VARCHAR(16))
    port = Column(INT)
    anonymous = Column(VARCHAR(20))
    protocal = Column(VARCHAR(10))
    location = Column(VARCHAR(255))
    latency = Column(VARCHAR(11))
    last_verify_time = Column(DATETIME)
    isvalid = Column(INT)
    source = Column(INT)    
    
def get_rules():
    engine = create_engine('mysql+mysqlconnector://' + MYSQL_USER + ':' + MYSQL_PASSWD + '@' + MYSQL_HOST + ':3306/' + MYSQL_DBNAME)
    DBSession = sessionmaker(bind=engine)
      
    session = DBSession()
#     new_user = User(id='4', name='Huangyi')
#     session.add(new_user)
#     session.commit()
    #session.close()
      
    ##进行查询
#     item = session.query(ProxyItem).filter(ProxyItem.id=='4').one()
    item = session.query(ProxyRule)[0]
    print 'type:', type(item)
    print 'object:', item.name + item.start_urls + item.sub_link
    session.close()
    
def add_rules(new_proxy_rule):
    engine = create_engine('mysql+mysqlconnector://' + MYSQL_USER + ':' + MYSQL_PASSWD + '@' + MYSQL_HOST + ':3306/' + MYSQL_DBNAME)
    DBSession = sessionmaker(bind=engine)
      
    session = DBSession()
    session.add(new_proxy_rule)
    session.commit()
    session.close()
    
def get_ip_proxy():
    engine = create_engine('mysql+mysqlconnector://' + MYSQL_USER + ':' + MYSQL_PASSWD + '@' + MYSQL_HOST + ':3306/' + MYSQL_DBNAME)
    DBSession = sessionmaker(bind=engine)
      
    session = DBSession()      
    ##进行查询
#     item = session.query(ProxyItem).filter(ProxyItem.id=='4').one()
    items = session.query(ProxyItem).filter(ProxyItem.isvalid=='1')
    ipList = []
    for item in items:
        ip = {'ip':item.ip, 'port':item.port, 'user_pass':''}
        ipList.append(ip)
    session.close()
    
    return ipList
    
if __name__ == '__main__':
#     get_rules()

    new_proxy_rule = ProxyRule()
    
    new_proxy_rule.name = "nianshao"
    new_proxy_rule.download_delay = "2"
    new_proxy_rule.allowed_domain = "www.nianshao.me"
    new_proxy_rule.start_urls = "http://www.nianshao.me/"
    new_proxy_rule.sub_link = ""
    new_proxy_rule.table_xpath = "//table[@class='table']"
    new_proxy_rule.trs_xpath = "tbody/tr"
    new_proxy_rule.ip_xpath = "td[1]/text()"
    new_proxy_rule.port_xpath = "td[2]/text()"
    new_proxy_rule.anonymous_xpath = "td[4]/text()"
    new_proxy_rule.http_type_xpath = "td[5]/text()"
    new_proxy_rule.location_xpath = "td[3]//text()"
    new_proxy_rule.latency_xpath = "0"
    new_proxy_rule.last_verify_time_xpath = "td[8]/text()"
    new_proxy_rule.max_page_num_xpath = "//div[@id='listnav']/ul/a/text()"
    new_proxy_rule.time_format = "%Y-%m-%d %H:%M:%S"
    
    add_rules(new_proxy_rule)
    
