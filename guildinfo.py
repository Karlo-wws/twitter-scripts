import json, requests, urllib, argparse, logging, sys
import MySQLdb as mdb
from connection import conn,x
from apikey import key


logging.basicConfig(filename='/var/log/guildinfo.log', level=logging.DEBUG, format='%(asctime)s %(message)s')

Host = "https://us.api.battle.net"
minilvl = 540

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
URL = Host + "/wow/guild/" + Realm + "/" + GuildName + "?fields=news&locale=en_US&apikey=" + key
logging.debug(URL)
r = requests.get(URL)
c = r.json()
d = json.dumps(c, sort_keys=True, indent=0)
x.execute("SET NAMES 'utf8'")
exql = "SELECT stamp FROM wwspost.news"
existing = x.execute(exql)
data = str(x.fetchall())

try:
	status = c['status']
	reason = c['reason']
	logging.warning(reason)
	sys.exit()
except KeyError:
	pass

for results in c['news']:
        if results['type'] == "playerAchievement":
                member = results['character']
                char = member.encode("utf-8")
                type = results['type']
                achid = results['achievement']['id']
                timestamp = results['timestamp']
                if str(timestamp) not in data:
                        isql = "INSERT INTO wwspost.news(stamp, chrname, type, achid) VALUES(" + str(timestamp) + ", '" + member + "', '" + type + "', " + str(achid) + ")"
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
                member = results['character']
                enc = member.encode("utf-8")
                type = results['type']
                itemid = results['itemId']
                timestamp = results['timestamp']
                if str(timestamp) not in data:
                    URL2 = Host + "/wow/item/" + str(itemid) + "?locale=en_US&apikey=" + key
                    logging.debug(URL2)
                    r = requests.get(URL2)
                    ci = r.json()
                    di = json.dumps(c, sort_keys=True, indent=0)
                    try:
                    	ilvl = ci['itemLevel']
                    except KeyError:
                    	#print ci['availableContexts']
                    	# I dont like this, but until I figure out http://us.battle.net/en/forum/topic/15007381039, it's kind of boned.
                    	ilvl = minilvl - 1
                    	continue
                    if ilvl > minilvl:
                        isql = "INSERT INTO wwspost.news(chrname, stamp, type, itemid) VALUES('%s','%s','%s','%s')" % (member,timestamp,type,itemid)
                    else:
                        isql = "INSERT INTO wwspost.news(chrname, stamp, type, itemid, posted) VALUES('%s','%s','%s','%s','1')" % (member,timestamp,type,itemid)
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
