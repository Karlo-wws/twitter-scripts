import os, json, requests, urllib, logging
import MySQLdb as mdb
from connection import conn,x
from apikey import key

Host = "https://us.api.battle.net"
logging.basicConfig(filename='/var/log/guildinfo.log', level=logging.WARNING, format='%(asctime)s %(message)s')
x.execute("SET NAMES 'utf8'")
sql = "SELECT chrname, itemid, stamp FROM wwspost.news WHERE posted='0' and type in ('itemPurchase','itemLoot','itemCraft')"

info = x.execute(sql)
numcheck = int(x.rowcount)
if numcheck > 0:
        data = x.fetchall()
        for row in data:
                charname = row[0]
                enc = unicode(charname)
                itemid = str(row[1])
                stamp = str(row[2])
                URL = Host + "/wow/item/" + str(itemid) + "?locale=en_US&apikey=" + key
                r = requests.get(URL)
                c = r.json()
                itemname = c['name']
                POST = '%s acquired %s http://www.wowhead.com/item=%s #WoW #Warcraft' % (enc,itemname,itemid)
                logging.warning('Posting: %s' % POST)
                try:
                        os.system('python /var/www/wwsguild/twitter-scripts/posttwit.py -m "%s"' % POST.encode("utf-8"))
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
