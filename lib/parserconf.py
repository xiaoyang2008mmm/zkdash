import ConfigParser




def get_mysql_server(file="./conf/mysql.conf"):
    myconf = {}

    cf = ConfigParser.ConfigParser()    
    cf.read(file)   
  
    myconf['user']        = cf.get("mysqld", "mysql_user")    
    myconf['password']    = cf.get("mysqld", "mysql_password")    
    myconf['port']        = int(cf.get("mysqld", "mysql_port"))    
    myconf['host']        = cf.get("mysqld", "mysql_host")    
    myconf['database']    = cf.get("mysqld", "mysql_database")    
    myconf['charset']     = cf.get("mysqld", "mysql_charset")    
    
    return myconf

