import uuid
import MySQLdb
from bidi.algorithm import get_display
import arabic_reshaper


class AppPipeline(object):

    def __init(self):
        self.db = MySQLdb.connect("localhost", "root", "", "press")

    def open_spider(self, spider):
        cursor = self.db.cursor()
        self.db.set_character_set('utf8')
        cursor.execute('SET NAMES utf8;')
        cursor.execute('SET CHARACTER SET utf8;')
        cursor.execute('SET character_set_connection=utf8;')
        cursor.close()
        self.db.commit()

    def process_item(self, item, spider):
        i = dict(item)
        cursor = self.db.cursor()
        cursor.execute("SELECT id FROM article WHERE link='%s'" % (i["link"]))
        results = cursor.rowcount
        # print(results)
        if results == 0:
            id = str(uuid.uuid4())
            title = get_display(arabic_reshaper.reshape(u'' + i["title"]))
            author = get_display(arabic_reshaper.reshape(u'' + i["author"]))
            link = i["link"]
            description = get_display(arabic_reshaper.reshape(u'' + "\n".join(i["description"])))
            cursor.execute("INSERT INTO article(id, title, author, link, descrip) VALUES (%s,%s,%s,%s,%s) ",
                           (id, title, author, link, description))
            self.db.commit()
            comments = i["comments"]
            names = i["names"]
            feedbacks = i["feedbacks"]
            for comment, name, feedback in zip(comments, names, feedbacks):
                try:
                    cursor.execute(
                        "INSERT INTO comments(id_article, comment, name, feedback) VALUES (%s,%s,%s,%s)",
                        (id,
                         get_display(arabic_reshaper.reshape(u'' + comment)),
                         get_display(arabic_reshaper.reshape(u'' + name)),
                         feedback
                         )
                    )
                    self.db.commit()
                except Exception as e:
                    print(e)
        else:
            idup = cursor.fetchone()
            cursor.execute("DELETE FROM comments WHERE id_article = '%s'" % (idup[0],))
            self.db.commit()
            comments = i["comments"]
            names = i["names"]
            feedbacks = i["feedbacks"]
            for comment, name, feedback in zip(comments, names, feedbacks):
                try:
                    cursor.execute(
                        "INSERT INTO comments(id_article, comment, name, feedback) VALUES (%s,%s,%s,%s)",
                        (idup,
                         get_display(arabic_reshaper.reshape(u'' + comment)),
                         get_display(arabic_reshaper.reshape(u'' + name)),
                         feedback
                         )
                    )
                    self.db.commit()
                except Exception as e:
                    print(e)
        cursor.close()
        return item

    def spider_closed(self, spider):
        self.db.close()
