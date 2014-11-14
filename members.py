import os, json, requests, urllib, argparse, logging, sys
import MySQLdb as mdb
from connection import conn,x
from apikey import key

logging.basicConfig(filename='/var/log/guildinfo.log', level=logging.WARNING, format='%(asctime)s %(message)s')

Host = "https://us.api.battle.net"
parser = argparse.ArgumentParser()
parser.add_argument('-r','--realm', help="Pass Realm without prompting",type=str)
parser.add_argument('-g','--guild', help="Pass Guild without prompting",type=str)

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

URL = Host + "/wow/guild/" + Realm + "/" + GuildName + "?fields=members&locale=en_US&apikey=" + key
logging.debug(URL)
r = requests.get(URL)
c = r.json()
d = json.dumps(c, sort_keys=True, indent=0)
x.execute("SET NAMES 'utf8'")
levelql = "SELECT name, level FROM wwspost.members"
cur_level = x.execute(levelql)
levels = dict(x.fetchall())
grankql = "SELECT name, g_rank FROM wwspost.members"
cur_rank = x.execute(grankql)
rank = dict(x.fetchall())
classes = {
        1: 'Warrior',
        2: 'Paladin',
        3: 'Hunter',
        4: 'Rogue',
        5: 'Priest',
        6: 'Death Knight',
        7: 'Shaman',
        8: 'Mage',
        9: 'Warlock',
        10: 'Monk',
        11: 'Druid'
}

try:
	status = c['status']
	reason = c['reason']
	logging.warning(reason)
	sys.exit()
except KeyError:
	pass

try:
	for results in c['members']:
	        member = results['character']['name']
	        enc = member.encode("utf-8")
	        level = str(results['character']['level'])
	        grank = str(results['rank'])
	        class_id = results['character']['class']
	        class_name = classes[class_id]
	        if member in levels:
	                old_level = str(levels[member])
	                old_grank = str(rank[member])
	                if level == old_level:
	                        sql = ""
	                        if grank == old_grank:
	                                sql = ""
	                        else:
	                                sql = "UPDATE wwspost.members SET g_rank='%s' WHERE name='%s'" % (grank,enc)
	                else:
	                        sql = "UPDATE wwspost.members SET level='%s' WHERE name='%s'" % (level,enc)
	                numcheck = len(sql)
	                if numcheck > 0:
	                    try:
	                        logging.warning('Running query: %s' % sql)
	                        x.execute(sql)
	                        conn.commit()
	                    except mdb.Error, e:
	                        try:
	                            logging.warning("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
	                        except IndexError:
	                            print "MySQL Error: %s" % str(e)
	                            conn.rollback()
	        else:
	                sql = "INSERT INTO wwspost.members(name,level,g_rank, joined) VALUES('%s','%s','%s',now())" % (enc,level,grank)
	                logging.warning('Running query: %s' % sql)
			tweet = "%s (Level %s %s) has joined the guild." % (enc, level, class_name)
	                os.system('python /var/www/wwsguild/twitter-scripts/posttwit.py -m "%s"' % tweet)
	                try:
	                    x.execute(sql)
	                    conn.commit()
	                except mdb.Error, e:
	                    try:
	                        print "MySQL Error [%d]: %s" % (e.args[0], e.args[1])
	                        logging.warning("MySQL Error [%d]: %s" % (e.args[0], e.args[1]))
	                    except IndexError:
	                        print "MySQL Error: %s" % str(e)
	                        conn.rollback()
except KeyError:
	logging.warning("Problem getting data, information found: %s " % c)
