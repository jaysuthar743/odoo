import xmlrpc.client
import xlrd

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

loc = "products.xls"

wb = xlrd.open_workbook(loc)

for sheet in wb.sheets():
    for row in range(1, sheet.nrows):
        product_name = sheet.cell(row, 0).value
        list_price = sheet.cell(row, 1).value  # product sales price
        id = object_proxy.execute_kw(DB, uid, PASS, 'product.product', 'create', [{
            'name': str(product_name),
            'list_price': int(list_price)
        }])
        print("Newly Created Product Id: ", id)
