import os, json, requests, urllib, argparse, logging, sys
import MySQLdb as mdb
from connection import conn,x

logging.basicConfig(filename='/var/log/guildinfo.log', level=logging.WARNING, format='%(asctime)s %(message)s')

Host = "http://us.battle.net"
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

URL = Host + "/api/wow/guild/" + Realm + "/" + GuildName + "?fields=members"
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
# print levels
# {'Turku': 90L, 'Meekmillz': 48L, 'Karlo': 90L, 'Skizita': 83L, 'Guinivere': 90L, 'Syvala': 85L, 'Higoodbye': 90L, 'Evoluti\xc3\xb2n': 90L, 'Adenya': 90L, 'Edo': 90L, 'Deaora': 90L, 'Belleya': 3L, 'Jeina': 90L, 'Malynd': 90L, 'Thallsnipe': 90L, 'Trivestom': 41L, 'Xuluu': 90L, 'Bellaphe': 90L, 'Thallheal': 52L, 'Cylonna': 90L, 'Krazyk': 90L, 'Yedo': 90L, 'Fuknark': 90L, 'Becroft': 42L, 'Sayyid': 90L, 'Arlonel': 80L, 'Sybellea': 24L, 'Aileyra': 90L, 'Thallizen': 35L, 'Krimch': 90L, 'Dhorah': 1L, 'Thallakazot': 80L, 'Sheyna': 90L, 'Celthorn': 90L, 'Adaphasha': 14L, 'Thallys': 90L, 'Kyriis': 39L, 'Skcizito': 90L, 'Maeverity': 90L, 'Talyssah': 90L, 'Adanduin': 11L, 'Rhyian': 74L, 'Xulos': 90L, 'Cyndrall': 90L, 'Taylliar': 33L, 'Lorellana': 52L, 'Sevley': 90L, 'Thalladin': 80L, 'Saaid': 90L, 'Daphnee': 90L, 'Ravixwar': 90L, 'Xenuit': 41L, 'Pori': 90L, 'Seanwoo': 90L, 'Garavint': 14L, 'Zimakus': 29L, 'Tasin': 90L, 'Fandrion': 90L, 'Zaroda': 90L, 'Tyrelea': 90L, 'Syyinnia': 90L, 'Thallswipe': 51L, 'Rogitzo': 90L, 'Shamitzo': 90L, 'Xavaver': 90L, 'Lahti': 90L, 'Vavictus': 90L, 'Kalabar': 56L, 'Zumackha': 90L, 'Falrox': 52L, 'Syldria': 17L, 'Crauder': 7L, 'Vyten': 90L}
# print rank
# {'Turku': 6L, 'Meekmillz': 8L, 'Karlo': 0L, 'Skizita': 2L, 'Guinivere': 1L, 'Syvala': 2L, 'Higoodbye': 8L, 'Evoluti\xc3\xb2n': 8L, 'Adenya': 2L, 'Edo': 6L, 'Deaora': 6L, 'Belleya': 1L, 'Jeina': 1L, 'Malynd': 2L, 'Thallsnipe': 2L, 'Trivestom': 6L, 'Xuluu': 3L, 'Bellaphe': 1L, 'Thallheal': 2L, 'Cylonna': 2L, 'Krazyk': 6L, 'Yedo': 6L, 'Fuknark': 6L, 'Becroft': 6L, 'Sayyid': 6L, 'Arlonel': 6L, 'Sybellea': 1L, 'Aileyra': 2L, 'Thallizen': 2L, 'Krimch': 2L, 'Dhorah': 7L, 'Thallakazot': 2L, 'Sheyna': 1L, 'Celthorn': 1L, 'Adaphasha': 1L, 'Thallys': 2L, 'Kyriis': 1L, 'Skcizito': 2L, 'Maeverity': 1L, 'Talyssah': 2L, 'Adanduin': 1L, 'Rhyian': 2L, 'Xulos': 8L, 'Cyndrall': 2L, 'Taylliar': 2L, 'Lorellana': 8L, 'Sevley': 1L, 'Thalladin': 2L, 'Saaid': 6L, 'Daphnee': 1L, 'Ravixwar': 6L, 'Xenuit': 3L, 'Pori': 6L, 'Seanwoo': 6L, 'Garavint': 1L, 'Zimakus': 1L, 'Tasin': 8L, 'Fandrion': 1L, 'Zaroda': 2L, 'Tyrelea': 2L, 'Syyinnia': 8L, 'Thallswipe': 2L, 'Rogitzo': 2L, 'Shamitzo': 2L, 'Xavaver': 8L, 'Lahti': 6L, 'Vavictus': 6L, 'Kalabar': 4L, 'Zumackha': 8L, 'Falrox': 6L, 'Syldria': 6L, 'Crauder': 1L, 'Vyten': 6L}

try:
	status = c['status']
	reason = c['reason']
	logging.warning(reason)
	sys.exit()
except KeyError:
	pass

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
                # Traceback (most recent call last):
                # File "/var/www/wwsguild/twitter-scripts/members.py", line 58, in <module>
                # UnicodeEncodeError: 'ascii' codec can't encode character u'\xf2' in position 57: ordinal not in range(128)
                #
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
