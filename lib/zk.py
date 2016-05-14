import zookeeper,json
from   get_zknode import get_node
from parserconf import get_zk_server
def get_base():

    zk=zookeeper.init(get_zk_server())
    data = get_node('/')
    zookeeper.close(zk)
    return json.dumps(data)
     


