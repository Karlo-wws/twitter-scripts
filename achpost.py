import os, json, requests, urllib, logging
import MySQLdb as mdb
from connection import conn,x
from apikey import key

Host = "https://us.api.battle.net"
logging.basicConfig(filename='/var/log/guildinfo.log', level=logging.WARNING, format='%(asctime)s %(message)s')

sql = "SELECT chrname, achid, stamp FROM wwspost.news WHERE posted='0' and type='playerAchievement'"

info = x.execute(sql)
numcheck = int(x.rowcount)
if numcheck > 0:
        data = x.fetchall()
        for row in data:
                charname = row[0]
                enc = unicode(charname)
                achid = str(row[1])
                stamp = str(row[2])
                URL = Host + "/wow/achievement/" + achid + "?fields=news&locale=en_US&apikey=" + key
                r = requests.get(URL)
                c = r.json()
                achname = c['title']
                POST = "%s completed %s http://www.wowhead.com/achievement=%s #worldofwarcraft #achievement" % (enc,achname,achid)
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

