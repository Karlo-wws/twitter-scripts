import os, json, requests, urllib, logging
import MySQLdb as mdb
from connection import conn,x

Host = "http://us.battle.net"
logging.basicConfig(filename='/var/log/guildinfo.log', level=logging.WARNING, format='%(asctime)s %(message)s')

sql = "SELECT achid, stamp FROM wwspost.news WHERE posted='0' and type='guildAchievement'"

info = x.execute(sql)
numcheck = int(x.rowcount)
if numcheck > 0:
        data = x.fetchall()
        for row in data:
                achid = str(row[0])
                stamp = str(row[1])
                URL = Host + "/api/wow/achievement/" + achid
                r = requests.get(URL)
                c = r.json()
                achname = c['title']
                POST = "Wiping with Style has completed: %s \n http://www.wowhead.com/achievement=%s #worldofwarcraft #achievement" % (achname,achid)
                print POST
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
