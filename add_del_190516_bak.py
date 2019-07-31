#!/usr/bin/python

import pymysql
import subprocess
import sys
import string
import re
import os

con_db = ''
con_sql_usr = ''
go_main = ''
go_prev = ''
vhostconf = "/usr/local/apache/conf"
apachelog = "/usr/local/apache/logs"

def extraction(argv):
        try:
                tmp=subprocess.check_output("%s" %argv, shell=True)
                result = tmp.strip()
                return result
        except subprocess.CalledProcessError:
                return " ."

def Go_prev(mention):
    global go_prev
    while True:
		yn=raw_input("%s (y/n) : " %mention)
		if yn == "y": break;
		elif yn == "n": go_prev = "yes"; break;
		else : anykey=raw_input("Wrong answer!");

class Add_del:
    def __init__ (self, argv1 ):
        self.what = argv1

    def Menu(self):
            global num
            subprocess.call("clear")
            if self.what == "main":
                    print("""######Main_menu
1) User
2) Virtual host
3) mySQL
4) Exit""")
            elif self.what == "usr":
                    print("""######User
1) View user infomation
2) Add user
3) Delete user
4) Return to main menu""")
            elif self.what == "domain":
                    print("""######Virtual_host
1) View virtualhost infomation
2) Add virtualhost
3) Delete virtualhost
4) Return to main menu""")
            elif self.what == "mysql":
                    print("""######mySQL
1) Database
2) mySQL User
3) Return to main menu""")
            elif self.what == "db":
                    print("""######mySQL_Database
1) View databases
2) Creat database
3) Drop database
4) Return to previous menu
5) Return to main menu""")
            elif self.what == "sql_usr":
                    print("""######mySQL_User
1) View mySQL user
2) Add mySQL user
3) Delete mySQL user
4) Return to previous menu
5) Return to main menu""")
            num=raw_input("insert number : ")
            
    def Info(self, mention):
            if self.what == "usr":
                if mention: 
                    print("######User_info")
                    if re.match( 'please', mention ):
                        subprocess.call('egrep "/bin/bash" /etc/passwd | egrep -vw "1002|root" | awk -f /root/Userinfo.awk', shell=True)
                    elif re.match( 'complete', mention ):
                        subprocess.call("cat /etc/passwd | egrep -w \"%s\"  | awk -f /root/Userinfo.awk" %usr, shell=True)
                elif not mention: subprocess.call('egrep "/bin/bash" /etc/passwd | egrep -vw "1002|root" | awk -f /root/Userinfo.awk', shell=True);
                if mention: anykey = raw_input("%s" %mention);
            elif self.what == "domain":
                if mention: 
                    print("######Vhost_info")
                    if re.match( 'please', mention ):
                        subprocess.call ('cat /root/Vhostinfo.txt | awk -f /root/Vhostinfo.awk', shell=True)
                    elif re.match( 'complete', mention ):
                        subprocess.call ('cat /root/Vhostinfo.txt | egrep -w "%s" | awk -f /root/Vhostinfo.awk' %domain, shell=True)
                elif not mention: subprocess.call ('cat /root/Vhostinfo.txt | awk -f /root/Vhostinfo.awk', shell=True);
                if mention: anykey = raw_input("%s" %mention);
            elif self.what == "db":
                if mention: 
                    print("######Database_info")
                    if re.match( 'please', mention ):
                        Add_del.query("show databases", "db_info")
                    elif re.match( 'complete', mention ):
                        Add_del.query("show databases like %s" %db, "db_info")
                elif not mention: Add_del.query("show databases", "db_info");
                if mention: anykey = raw_input("%s" %mention);
            elif self.what == "sql_usr":
                if mention: 
                    print("######mySQL_user_info")
                    if re.match( 'please', mention ):
                        Add_del.query("select distinct host, user, db from db", "sql_usr_info")
                    elif re.match( 'complete', mention ):
                        Add_del.query("select distinct host, user, db from db where user='%s'" %sql_usr, "sql_usr_info")
                elif not mention: Add_del.query("select distinct host, user, db from db", "sql_usr_info");
                if mention: anykey = raw_input("%s" %mention);

    def Head_Insert_Confirm(self, do):
            global usr,con_usr,domain,con_domain,domain_check,db,con_db,sql_usr, con_sql_usr, hostip, con_hostip
            if self.what == "usr":
                    if do == "add":
                            subprocess.call("clear")
                            print("######Add_user")
                    elif do == "del":
                            subprocess.call("clear")
                            print("######Delete_user")
                            User.Info(None)
                    elif do == "nohead": None;
                    usr=raw_input("insert username : ")
                    User.Check_blank(do,usr)
                    con_usr=extraction('cat /etc/passwd | awk -F: \'{print $1}\' | egrep -w "%s"' % usr)
            elif self.what == "domain":
                    if do == "add":
                            subprocess.call("clear")
                            print("######Add_Virtualhost")
                    elif do == "del":
                            subprocess.call("clear")
                            print("######Delete_Virtualhost")
                            Vhost.Info(None)
                    elif do == "nohead": None;
                    domain=raw_input("insert domain : ")
                    Vhost.Check_blank(do,domain)
                    con_domain=extraction("echo %s | sed 's/\./_/g'" % domain)
                    domain_check = os.path.exists("%s/vhost/Vhost_%s" %(vhostconf,con_domain))
            elif self.what == "db":
                    if do == "add":
                            subprocess.call("clear")
                            print("######Create_Database")
                    elif do == "del":
                            subprocess.call("clear")
                            print("######Drop_Database")
                            DB.Info(None)
                    elif do == "nohead": None;
                    db=raw_input("insert database name : ")
                    DB.Check_blank(do,db)
                    Add_del.query("show databases like '%s'" %db, "db_confirm")
            elif self.what == "sql_usr":
                    if do == "add":
                            subprocess.call("clear")
                            print("######Add_mySQL_user")
                    elif do == "del":
                            subprocess.call("clear")
                            print("######Delete_mySQL_user")
                            SQL_User.Info(None)
                    elif do == "nohead": None;
                    sql_usr=raw_input("insert mySQL user name : ")
                    SQL_User.Check_blank( do, sql_usr )
                    Add_del.query("select distinct user from user where user='%s'" %sql_usr, "sql_usr_confirm")
            elif self.what == "hostip":
                    hostip=raw_input("insert host IP ( ex: localhost, 192.168.xxx.xxx) : ")
                    if do == "del":
                            Add_del.query("select distinct user from user where host='%s' and user='%s'" %(hostip,sql_usr), "sql_usr_confirm")

    def Check_blank(self, do, param):
        what = self.what
        def recursive():
            if what == "usr": User.Head_Insert_Confirm(do);
            elif what == "domain": Vhost.Head_Insert_Confirm(do);
            elif what == "db": DB.Head_Insert_Confirm(do);
            elif what == "sql_usr": SQL_User.Head_Insert_Confirm(do);
            
        p = re.compile("\s+")
        m = p.search("%s" %param)
        p2 = re.compile("[^A-Z^a-z^0-9^_^-^.]+")
        m2 = p2.search("%s" %param)
        if m:
            anykey=raw_input("it's not permitted that include blank...")
            recursive()
        elif not param :
            anykey=raw_input("you was not entered anything...")
            recursive()
        elif m2 :
            anykey=raw_input("it's not permitted that include special character...")
            recursive()

    def Check_duplication(self, do):
            global usr,con_usr,domain,con_domain,domain_check,db,con_db,sql_usr, con_sql_usr
            if self.what == "usr":
                    if do == "add":
                            while usr == con_usr:
                                    anykey=raw_input("already exist user name...")
                                    Go_prev("try again?")
                                    if go_prev == "yes": break;
                                    User.Head_Insert_Confirm(do)
                    elif do == "del" or do == "nohead" :
                            while usr != con_usr:
                                    anykey=raw_input("please check this user name...")
                                    Go_prev("try again?")
                                    if go_prev == "yes": break;
                                    User.Head_Insert_Confirm(do)
            elif self.what == "domain":
                    if do == "add":
                            while   domain_check == True :
                                    anykey=raw_input("already exist domain...")
                                    Go_prev("try again?")
                                    if go_prev == "yes": break;
                                    Vhost.Head_Insert_Confirm(do)
                    elif do == "del":
                            while   domain_check == False:
                                    anykey=raw_input("please check this domain...")
                                    Go_prev("try again?")
                                    if go_prev == "yes": break;
                                    Vhost.Head_Insert_Confirm(do)
            elif self.what == "db":
                    if do == "add":
                            while db == con_db:
                                    anykey=raw_input("already exist database...")
                                    Go_prev("try again?")
                                    if go_prev == "yes": break;
                                    DB.Head_Insert_Confirm(do)
                    elif do == "del" or do == "nohead" :
                            while db != con_db:
                                    anykey=raw_input("please check this database name...")
                                    Go_prev("try again?")
                                    if go_prev == "yes": break;
                                    DB.Head_Insert_Confirm(do)
            elif self.what == "sql_usr" or self.what == "hostip" :
                    if do == "add":
                            while sql_usr == con_sql_usr:
                                    anykey=raw_input("already exist mySQL username...")
                                    Go_prev("try again?")
                                    if go_prev == "yes": break;
                                    SQL_User.Head_Insert_Confirm(do)
                    elif do == "del":
                            while sql_usr != con_sql_usr:
                                    if self.what == "sql_usr": anykey=raw_input("please check this mySQL username...");
                                    elif self.what == "hostip": anykey=raw_input("please check this host ip...");
                                    Go_prev("try again?")
                                    if go_prev == "yes": break;
                                    if self.what == "sql_usr": SQL_User.Head_Insert_Confirm(do);
                                    elif self.what == "hostip": Hostip.Head_Insert_Confirm(do);

    def Confirm_password(self):
            global usr_pw, con_pw, anykey
            def input_password():
                    global usr_pw, con_pw, anykey
                    os.system("stty -echo")
                    usr_pw=raw_input("insert password : "); print("");
                    con_pw=raw_input("retype password : "); print("");
                    os.system("stty echo")
            input_password()
            while usr_pw != con_pw :
                    anykey=raw_input("Sorry, password do not match...")
                    input_password()

    def Excute(self, do):
            if self.what == "usr" and do == "add":
                    subprocess.call("useradd -d /home/user/%s %s > /dev/null" %(usr,usr),shell=True)
                    subprocess.call("echo %s | passwd --stdin %s > /dev/null" %(usr_pw,usr),shell=True)
            elif self.what   == "usr" and do == "del":
                    subprocess.call("userdel -r  %s > /dev/null" %usr, shell=True)
                    anykey=raw_input("complete deleting user!")
            elif self.what   == "domain" and do == "add":
                    conf = open("%s/vhost/Vhost_%s" %(vhostconf,con_domain),'w')
                    conf.write("""<Virtualhost 192.168.30.137>
    ServerName %s
    DocumentRoot /home/user/%s/www
    CustomLog %s/%s.log combined
    </Virtualhost>\n""" %(domain,usr,apachelog,con_domain))
                    conf.close()
                    subprocess.call("cat %s/vhost/* > %s/Virtualhost_conf" %(vhostconf,vhostconf), shell=True)
                    v_info = open("/root/Vhostinfo.txt",'a')
                    v_info.write("%s:%s:/home/user/%s/www\n" %(domain,usr,usr))
                    v_info.close()
                    subprocess.call("/usr/local/apache/bin/httpd -t 2> /dev/null", shell=True)
                    subprocess.call("/etc/init.d/httpd restart", shell=True)
            elif self.what   == "domain" and do == "del":
                    subprocess.call("rm -f %s/vhost/Vhost_%s > /dev/null" %(vhostconf,con_domain), shell=True)
                    subprocess.call("cat %s/vhost/* > %s/Virtualhost_conf" %(vhostconf,vhostconf), shell=True)
                    subprocess.call("cat /root/Vhostinfo.txt | egrep -vw \"%s\" > /root/Vhostinfo.tmp" %domain, shell=True)
                    subprocess.call("cat /root/Vhostinfo.tmp > /root/Vhostinfo.txt", shell=True)
                    subprocess.call("/usr/local/apache/bin/httpd -t 2> /dev/null", shell=True)
                    subprocess.call("/etc/init.d/httpd restart", shell=True)
                    anykey=raw_input("complete deleting virtual host!")
            elif self.what   == "db" and do == "add":
                    Add_del.query("create database %s" %db, "excute")
            elif self.what   == "db" and do == "del":
                    Add_del.query("drop database %s" %db, "excute")
                    anykey=raw_input("complete dropping database")
            elif self.what   == "sql_usr" and do == "add":
                    Add_del.query("grant all privileges on %s.* to '%s'@'%s' identified by '%s'" %(db,sql_usr,hostip,usr_pw), "excute")
            elif self.what   == "sql_usr" and do == "del":
                    Add_del.query("drop user '%s'@'%s'" %(sql_usr,hostip), "excute")
                    anykey=raw_input("complete deleting mySQL user!")

    @classmethod
    def query(cls, query, use):
            global query_result, db, con_db, con_sql_usr
            mysql_db = pymysql.connect(host='localhost', port=3306, user='root', passwd='jcjeon', db='mysql', charset='utf8')
            cursor = mysql_db.cursor()
            cursor.execute(query)
            if use == "db_info":
                    query_result = cursor.fetchall()
                    print("+-------------------------+")
                    print("|%-25s|" %"DataBase")
                    print("+-------------------------+")
                    for row_data in query_result:
                            if "%s" %row_data   == "information_schema" : None;
                            elif "%s" %row_data == "mysql" : None;
                            elif "%s" %row_data == "performance_schema" : None;
                            else:
                                    print("|%-25s|" %row_data)
                    print("+-------------------------+")
            elif use == "sql_usr_info":
                    query_result = cursor.fetchall()
                    print("+-----------+--------------+-----------+")
                    print("|%-11s|%-14s|%-11s|" %("host","user","db"))
                    print("+-----------+--------------+-----------+")
                    for row_data in query_result:
                            print("|%-11s|%-14s|%-11s|" %row_data)
                    print("+-----------+--------------+-----------+")
            elif use == "db_confirm":
                    query_result = cursor.fetchone()
                    if query_result is None:
                            con_db = " "
                    else :
                            con_db = query_result[0]
            elif use == "sql_usr_confirm":
                    query_result = cursor.fetchone()
                    if query_result is None:
                            con_sql_usr = " "
                    else :
                            con_sql_usr = query_result[0]
            elif use == "excute": None;
            mysql_db.commit()
            mysql_db.close()
#===========================================================
#                          ±¸µ¿ºÎ
#===========================================================
while True:
	Main = Add_del("main")
	User = Add_del("usr")
	Vhost = Add_del("domain")
	mySQL = Add_del("mysql")
	DB = Add_del("db")
	SQL_User = Add_del("sql_usr")
	Hostip = Add_del("hostip")
	Main.Menu()
	if num == "1":
		while True:
			User.Menu()
			if num == "1":
				subprocess.call("clear")
				User.Info("please insert anykey...")
			elif num == "2":
				User.Head_Insert_Confirm("add")
				User.Check_duplication("add")
				if go_prev == "yes" : go_prev = ''; continue;
				User.Confirm_password()
				User.Excute("add")
				User.Info("complete adding user!")
			elif num == "3":
				User.Head_Insert_Confirm("del")
				User.Check_duplication("del")
				if go_prev == "yes" : go_prev = ''; continue;
				Go_prev("are you sure?")
				if go_prev == "yes" : go_prev = ''; continue;
				User.Excute("del")
			elif num == "4": break;
			else : anykey=raw_input("wrong answer!");   
	elif num == "2":
		while True:
			Vhost.Menu()
			if num == "1":
				subprocess.call("clear")
				Vhost.Info("please insert anykey...")
			elif num == "2":
				Vhost.Head_Insert_Confirm("add")
				Vhost.Check_duplication("add")
				if go_prev == "yes" : go_prev = ''; continue;
				User.Head_Insert_Confirm("nohead")
				User.Check_duplication("nohead")
				if go_prev == "yes" : go_prev = ''; continue;
				Vhost.Excute("add")
				Vhost.Info("complete adding virtual host!")
			elif num == "3": 
				Vhost.Head_Insert_Confirm("del")
				Vhost.Check_duplication("del")
				if go_prev == "yes" : go_prev = ''; continue;
				Go_prev("are you sure?")
				if go_prev == "yes" : go_prev = ''; continue;
				Vhost.Excute("del")
			elif num == "4": break;
			else : anykey=raw_input("wrong answer!");
	elif num == "3":
		while True:
			if go_main == "main": go_main=''; break;
			mySQL.Menu()
			if num == "1":
				while True:
					DB.Menu()
					if num=="1":
						subprocess.call("clear")
						DB.Info("please insert anykey...")
					elif num =="2":
						DB.Head_Insert_Confirm("add")
						DB.Check_duplication("add")
						if go_prev == "yes" : go_prev = ''; continue;
						DB.Excute("add")
						DB.Info("complete creating databases!")
					elif num =="3":
						DB.Head_Insert_Confirm("del")
						DB.Check_duplication("del")
						if go_prev == "yes" : go_prev = ''; continue;
						Go_prev("are you sure?")
						if go_prev == "yes" : go_prev = ''; continue;
						DB.Excute("del")
					elif num =="4": break;
					elif num =="5": go_main="main"; break;
			elif num == "2":
				while True:
					SQL_User.Menu()
					if num== "1":
						subprocess.call("clear")
						SQL_User.Info("please insert anykey...")
					elif num == "2":
						SQL_User.Head_Insert_Confirm("add")
						SQL_User.Check_duplication("add")
						if go_prev == "yes" : go_prev = ''; continue;
						print("######Database_info");
						DB.Info(None)
						DB.Head_Insert_Confirm("nohead")
						DB.Check_duplication("nohead")
						if go_prev == "yes" : go_prev = ''; continue;
						Hostip.Head_Insert_Confirm(None)
						SQL_User.Confirm_password()
						SQL_User.Excute("add")
						SQL_User.Info("complete adding mysql user!")
					elif num == "3":
						SQL_User.Head_Insert_Confirm("del")
						SQL_User.Check_duplication("del")
						if go_prev == "yes" : go_prev = ''; continue;
						Hostip.Head_Insert_Confirm("del")
						Hostip.Check_duplication("del")
						if go_prev == "yes" : go_prev = ''; continue;
						Go_prev("are you sure?")
						if go_prev == "yes" : go_prev = ''; continue;
						SQL_User.Excute("del")
					elif num =="4": break;
					elif num =="5": go_main="main"; break;
			elif num == "3": break;
	elif num == "4": break;