#!/usr/bin/python
# -*- coding: utf-8 -*-

import MySQLdb as db
import sys

#Examples: http://zetcode.com/db/mysqlpython/

# Database
# create database greensdn;
# use greensdn;
# grant all on greensdn.* to 'mininet'@'localhost';

class DBManager(object):

	def FetchOneAssoc(self,cursor) :
	    	data = cursor.fetchone()
		if data == None :
			return None
		desc = cursor.description

		dict = {}

		for (name, value) in zip(desc, data) :
			dict[name[0]] = value

		return dict

	def create_tables(self, cur):

		cur.execute("SET FOREIGN_KEY_CHECKS=0")
		cur.execute("drop table if exists hosts")
	    	cur.execute("CREATE TABLE hosts(macaddr VARCHAR(20) PRIMARY KEY, \
				ipaddr VARCHAR(10), \
				dpid INT, \
				port INT)")

		# User
		cur.execute("SET FOREIGN_KEY_CHECKS=0")
		cur.execute("DROP TABLE IF EXISTS User")
	    	cur.execute("CREATE TABLE User(id INT PRIMARY KEY AUTO_INCREMENT,\
				greenplan VARCHAR(10),\
				dpid INT, \
				port INT, \
				mac VARCHAR(20),\
				network_tokens INT, \
				compute_tokens INT, \
				bandwidth INT, \
				delay INT, \
				jitter INT, \
				loss INT, \
				vcpu INT)")

		cur.execute("DROP TABLE IF EXISTS energy_values")
		cur.execute("CREATE TABLE energy_values(id INT PRIMARY KEY AUTO_INCREMENT,\
				user INT,\
				FOREIGN KEY (user) REFERENCES User(id),\
				network_energy FLOAT(10,4), \
				compute_energy FLOAT(10,4))")
		cur.execute("SET FOREIGN_KEY_CHECKS=1")

	def populate_tables(self, cur):

		cur.execute("INSERT INTO User(id, greenplan, dpid,port,mac,network_tokens, compute_tokens, bandwidth, delay, jitter, loss, vcpu) \
			VALUES(1,'Brown',21,5,'00:00:00:00:00:01', 10, 10, 15, 100, 50, 1, 70)")
		cur.execute("INSERT INTO User(id, greenplan, dpid,port,mac,network_tokens, compute_tokens, bandwidth, delay, jitter, loss, vcpu) \
			VALUES(2,'Green 1',21,6,'00:00:00:00:00:02', 8, 8, 9, 100, 50, 1, 50)")
	  	cur.execute("INSERT INTO User(id, greenplan, dpid,port,mac,network_tokens, compute_tokens, bandwidth, delay, jitter, loss, vcpu) \
			VALUES(3,'Green 2',21,7,'00:00:00:00:00:03', 4, 4, 3, 100, 50, 1, 50)")
		cur.execute("INSERT INTO User(id, greenplan, dpid,port,mac,network_tokens, compute_tokens, bandwidth, delay, jitter, loss, vcpu) \
			VALUES(4,'Green 2',21,8,'00:00:00:00:00:04', 4, 4, 3, 100, 50, 1, 50)")

	def __init__(self):
		try:
			con = db.connect('localhost', 'mininet', '', 'greensdn')

			with con:
				cur = con.cursor(db.cursors.DictCursor)

				# Check if the table of Users is created

				try:
					#self.create_tables(cur)
					cur.execute("select count(*) as count from User")
					cur.execute("select count(*) as count from GreenPlans")
				except:
					self.create_tables(cur)

				#self.populate_tables(cur)


		except db.Error, e:
			print "Error %d: %s" % (e.args[0], e.args[1])
    			sys.exit(1)
		finally:
			if con: con.close()

def createDB():
	obj = DBManager()
	return obj

