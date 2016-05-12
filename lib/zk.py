import zookeeper,json
from   get_zknode import get_node
def get_base():
    zk=zookeeper.init('10.46.162.118:2181')
    data = get_node('/')
    zookeeper.close(zk)
    return json.dumps(data)
     


