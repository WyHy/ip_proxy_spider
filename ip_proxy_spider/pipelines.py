# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem
from twisted.enterprise import adbapi
import MySQLdb.cursors
import utils
import socket
import struct
import traceback
import md5

class IpProxySpiderPipeline(object):
	def process_item(self, item, spider):
		return item
	
class DuplicatesPipeline(object):
	def __init__(self):
		self.ids_seen = set()

	def process_item(self, item, spider):
		if item['ip'] in self.ids_seen:
			raise DropItem("Duplicate item found: %s" % item)
		else:
			self.ids_seen.add(item['ip'])
			return item

class MySQLPipeline(object):
	def __init__(self, dbpool):
		self.dbpool = dbpool

	@classmethod
	def from_settings(cls, settings):
		dbargs = dict(
				host = settings['MYSQL_HOST'],
				db = settings['MYSQL_DBNAME'],
				user = settings['MYSQL_USER'],
				passwd = settings['MYSQL_PASSWD'],
				charset = 'utf8',
				cursorclass = MySQLdb.cursors.DictCursor,
				use_unicode = True,
			)

		dbpool = adbapi.ConnectionPool('MySQLdb', **dbargs)
		return cls(dbpool)

	def process_item(self, item, spider):
		d = self.dbpool.runInteraction(self._do_insert, item, spider)
		d.addErrback(self._handle_error, item, spider)
		d.addBoth(lambda _: item)
		return d
	
	def _do_insert(self, conn, item, spider):
		try:
			conn.execute("select * from ip_proxy_info where ip=%s", (item['ip'],))
			ret = conn.fetchone()
			
			if ret:
				print utils.get_time_now(), "do db update, ip ==>", item['ip']
				conn.execute("update ip_proxy_info set port=%s, anonymous=%s, protocol=%s, location=%s, latency=%s, last_verify_time=%s, source=%s  where ip=%s", 
						(item['port'], item['anonymous'], item['http_type'], item['location'], item['latency'], item['last_verify_time'], item['source'], item['ip']))
			else:
				print utils.get_time_now(), "do db insert, ip ==>", item['ip']
				conn.execute("insert into ip_proxy_info (ip, port, anonymous, protocol, location, latency, last_verify_time, source) values (%s, %s, %s, %s, %s, %s, %s, %s)",
					(item['ip'], item['port'], item['anonymous'], item['http_type'], item['location'], item['latency'], item['last_verify_time'], item['source']))
		except:
			utils.get_time_now(), traceback.format_exc()
			print traceback.format_exc()	

	def _get_linkmd5id(self, item):
		#use md5process url to avoid repeat scrap
		return md5(item['ip']).hexdigest()

	def _handle_error(self, failure, item, spider):
		print utils.get_time_now(), "Error ==>", failure

	def ip_address_to_int(self, ip):
		return socket.ntohl(struct.unpack("I", socket.inet_aton(str(ip)))[0])
