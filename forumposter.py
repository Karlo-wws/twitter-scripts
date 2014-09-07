import os, logging
import MySQLdb as mdb
from connection import conn,x

logging.basicConfig(filename='/var/log/guildinfo.log', level=logging.WARNING)

sql = "SELECT a.post_id, a.post_text,a.topic_id, b.username FROM wip1310308551954.phpbb_posts a INNER JOIN wip1310308551954.phpbb_users b on a.poster_id = b.user_id WHERE a.forum_id=19 AND a.post_tweeted=0 and a.post_subject not like 'Re:%'"

get_data = x.execute(sql)
numcheck = int(x.rowcount)
if numcheck > 0:
        data = x.fetchall()
        for row in data:
                post_id = row[0]
                topic_id = row[2]
                post_text = row[1]
                poster = row[3]
                name_size = len ( poster )
                allowed_size = ( 135 - name_size )
                text = post_text[:allowed_size]
                tweet = post_text + " - " + poster

                try:
                        os.system('python /var/www/wwsguild/twitter-scripts/posttwit.py -m "%s"' % tweet)
                        addql = "INSERT INTO wip1310308551954.phpbb_posts (topic_id,forum_id,post_text,poster_id,poster_ip,post_username,post_subject,post_checksum,bbcode_bitfield,bbcode_uid,post_edit_reason,post_time,post_tweeted) VALUES ('%s',19,'Tweeted','111','127.0.0.1','','Reply','5d782974d96f25a7f333f51b81c550ca','','pqm87p0d','',UNIX_TIMESTAMP(NOW()),1)" % topic_id
                        upql = "UPDATE wip1310308551954.phpbb_posts SET post_tweeted=1 WHERE post_id=%s" % post_id
                        try:
                                x.execute(addql)
                                x.execute(upql)
                                conn.commit()
                        except IndexError:
                                print "MySQL Error: %s" % str(e)
                                conn.rollback()
                except:
                        raise
