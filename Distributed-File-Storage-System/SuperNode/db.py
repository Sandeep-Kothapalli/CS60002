import redis
import ast

_redis_port = 6379

r = redis.StrictRedis(host='localhost', port=_redis_port, db=0)

#metadata = {"username_filename" : [clusterName, clusterReplica]}
def saveMetaData(username, filename, clusterName, clusterReplica):
    key = username + "_" + filename
    r.set(key,str([clusterName,clusterReplica]))

def parseMetaData(username, filename):
    key = username + "_" + filename
    return ast.literal_eval(r.get(key).decode('utf-8'))

def keyExists(key):
    return r.exists(key)

def deleteEntry(key):
    r.delete(key)

def getUserFiles(username):
    # return r.get(username).decode('utf-8')
    list_of_keys = r.keys(pattern=f"{username}_*")

    if len(list_of_keys) == 0:
        return ""
    
    print("list of keys is ", list_of_keys)
    filenames = [fname[len(username)+1:] for fname in list_of_keys]

    return "\n".join(filenames)

def saveUserFile(username, filename):
    key = username + "_" + filename
    if(keyExists(key)):
        l=ast.literal_eval(r.get(key).decode('utf-8'))
        l.append(filename)
        r.set(key,str(l))
    

