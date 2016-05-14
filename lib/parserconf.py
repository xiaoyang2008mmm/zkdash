import ConfigParser,string,os,sys    
def get_zk_server(file="./conf/zookeeper.conf"):

    cf = ConfigParser.ConfigParser()    
    cf.read(file)   
  
    zk_server = cf.get("zk", "server")    
    return zk_server
