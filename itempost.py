import os, json, requests, urllib, logging
import MySQLdb as mdb
from connection import conn,x

Host = "http://us.battle.net"
logging.basicConfig(filename='/var/log/guildinfo.log', level=logging.WARNING)

sql = "SELECT chrname, itemid, stamp FROM wwspost.news WHERE posted='0' and type in ('itemPurchase','itemLoot','itemCraft')"

info = x.execute(sql)
numcheck = int(x.rowcount)
if numcheck > 0:
        data = x.fetchall()
        for row in data:
                charname = unicode(row[0])
                itemid = str(row[1])
                stamp = str(row[2])
                URL = Host + "/api/wow/item/" + itemid
                r = requests.get(URL)
                c = r.json()
                itemname = c['name']
                POST = '%s acquired %s http://www.wowhead.com/item=%s #loot #worldofwarcraft' % (charname,itemname,itemid)
                logging.warning('Posting: %s' % POST)
                try:
                        os.system('python /var/www/wwsguild/twitter-scripts/posttwit.py -m "%s"' % POST)
                except:
                        print "Error"
                        raise
                fixql = "UPDATE wwspost.news SET posted='1' WHERE stamp =" + stamp
                try:
                        x.execute(fixql)
                        logging.warning('Updating: %s' % fixql)
                        conn.commit()
                except mdb.Error, e:
                        try:
                                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                        except IndexError:
                                print "MySQL Error: %s" % str(e)
                                conn.rollback()
conn.close()
