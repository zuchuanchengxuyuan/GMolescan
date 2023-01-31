import pymysql
import config


db = pymysql.connect(host=config.dbhost,
                     user=config.dbuser,
                      password=config.dbpassword)
                     # database=config.dbname)
cursor=db.cursor()
sql='create database japanurls CHARACTER SET utf8'
cursor.execute(sql)
db.commit()

sql1='CREATE TABLE `japanurls`.`urls` (`id` int(11) NOT NULL AUTO_INCREMENT, `url` varchar(100) NOT NULL,`exploitname` varchar(30)  ,`mark` varchar(2) ,  PRIMARY KEY (`id`),UNIQUE (url)) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8'
cursor.execute(sql1)
db.commit()
sql2='CREATE TABLE `japanurls`.`scanresult` (`id` int(11) NOT NULL AUTO_INCREMENT,`url` varchar(100) NOT NULL,`exploitname` varchar(30)  ,`resp` varchar(2) ,  PRIMARY KEY (`id`),UNIQUE (url)) ENGINE=InnoDB AUTO_INCREMENT=0 DEFAULT CHARSET=utf8'
cursor.execute(sql2)
db.commit()
