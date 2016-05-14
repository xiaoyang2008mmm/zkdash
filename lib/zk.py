import zookeeper,json
from   get_zknode import get_node
def get_base():
    zk=zookeeper.init('127.0.0.1:2181')
    data = get_node('/')
    zookeeper.close(zk)
    return json.dumps(data)
     


