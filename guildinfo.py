import json, requests, urllib, argparse, logging
import MySQLdb as mdb
from connection import conn,x


logging.basicConfig(filename='/var/log/guildinfo.log', level=logging.WARNING)

Host = "http://us.battle.net"
parser = argparse.ArgumentParser()
parser.add_argument('-r','--realm', help="Pass Realm without prompting",type=str)
parser.add_argument('-g','--guild', help="Pass Guild without prompting",type=str)
parser.add_argument('-m','--members', help="List Guild members",
        action="store_true")
args = parser.parse_args()
if (args.realm):
        Realm = args.realm
else:
        Realm = raw_input('Realm:')

if (args.guild):
        Guild = args.guild
else:
        Guild = raw_input('Guild Name:')
GuildName = urllib.quote(Guild)
URL = Host + "/api/wow/guild/" + Realm + "/" + GuildName + "?fields=news"
logging.debug(URL)
r = requests.get(URL)
c = r.json()
d = json.dumps(c, sort_keys=True, indent=0)
exql = "SELECT stamp FROM wwspost.news"
existing = x.execute(exql)
data = str(x.fetchall())

for results in c['news']:
        if results['type'] == "playerAchievement":
                char = results['character']
                type = results['type']
                achid = results['achievement']['id']
                timestamp = results['timestamp']
                if str(timestamp) not in data:
                        isql = "INSERT INTO wwspost.news(stamp, chrname, type, achid) VALUES(" + str(timestamp) + ", '" + char + "', '" + type + "', " + str(achid) + ")"
                        try:
                                x.execute(isql)
                                conn.commit()
                                logging.warning('Running query: %s' % isql)
                        except mdb.Error, e:
                                try:
                                        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                                        logging.warning("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                                except IndexError:
                                        print "MySQL Error: %s" % str(e)
                                        conn.rollback()
        elif results['type'] == "guildAchievement":
                type = results['type']
                achid = results['achievement']['id']
                timestamp = results['timestamp']
                if str(timestamp) not in data:
                        isql = "INSERT INTO wwspost.news(stamp, type, achid) VALUES(" + str(timestamp) + ", '" + type + "', " + str(achid) + ")"
                        try:
                                x.execute(isql)
                                conn.commit()
                                logging.warning('Running query: %s' % isql)
                        except mdb.Error, e:
                                try:
                                        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                                        logging.warning("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                                except IndexError:
                                        print "MySQL Error: %s" % str(e)
                                        conn.rollback()
        else:
                char = results['character']
                type = results['type']
                itemid = results['itemId']
                timestamp = results['timestamp']
                if str(timestamp) not in data:
                        isql = "INSERT INTO wwspost.news(stamp, chrname, type, itemid) VALUES(" + str(timestamp) + ", '" + char + "', '" + type + "', " + str(itemid) + ")"
                        try:
                                x.execute(isql)
                                conn.commit()
                                logging.warning('Running query: %s' % isql)
                        except mdb.Error, e:
                                try:
                                        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
                                        logging.warning("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
                                except IndexError:
                                        print "MySQL Error: %s" % str(e)
                                        conn.rollback()

lastrun = "UPDATE wwspost.last_run SET time = now()"
try:
        x.execute(lastrun)
        logging.debug('Updating last_run')
        conn.commit()
except mdb.Error, e:
        try:
                print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
        except IndexError:
                print "MySQL Error: %s" % str(e)
                conn.rollback()
conn.close()
