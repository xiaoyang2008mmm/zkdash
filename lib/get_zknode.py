import  zookeeper
zk=zookeeper.init('10.46.162.118:2181')
 
def get_node(node_key):
    data=[]
    if node_key == "/":
        for node in zookeeper.get_children(zk,node_key):
             key =  "/" + node
             if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                  data.append(get_node(key))
                  #get_node(key)
             else:
                  data.append({'name': node})
    else:
        for node in zookeeper.get_children(zk,node_key):
             key =  node_key + "/" + node
             if (zookeeper.get(zk,key)[1])['numChildren'] > 0:
                  data.append(get_node(key))
             else:
		  data.append({'name': node})
        
        
    node_dict = {'name':node_key}
    if not len(data):
        data=['None']
    node_dict['children'] = data
    return node_dict
 
print get_node('/')
 
 
zookeeper.close(zk)
