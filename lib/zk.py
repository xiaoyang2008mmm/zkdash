import zookeeper,json
def get_base():
    zk=zookeeper.init('10.46.162.118:2181')
    data = []
    for node in zookeeper.get_children(zk,'/'):
        data.append({'name': "/{0}".format(node),'isParent':True})
    zookeeper.close(zk)
    return json.dumps(data)
