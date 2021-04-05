import xmlrpc.client

HOST = 'localhost'
PORT = 8069
DB = 'signature'
USER = 'admin'
PASS = 'admin'

url = 'http://%s:%d/xmlrpc/' % (HOST, PORT)

object_proxy = xmlrpc.client.ServerProxy(url+'object')
common_proxy = xmlrpc.client.ServerProxy(url+'common')

uid = common_proxy.login(DB, USER, PASS)
print("Logged in as %s (uid:%d)" % (USER, uid))

print(object_proxy.execute_kw(DB, uid, PASS, 'res.partner', 'search', [[['name', 'ilike', "Deco"]]]))



