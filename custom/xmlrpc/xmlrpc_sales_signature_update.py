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

blank_ids = object_proxy.execute_kw(DB, uid, PASS, 'sale.order', 'search', [[['sale_signature', '=', False]]])

print(blank_ids)

loc = "sale_signature_update.xls"

wb = xlrd.open_workbook(loc)

sheet = wb.sheet_by_index(0)
signature = sheet.cell_value(1, 0)

for sheet in wb.sheets():
    for sale_id in blank_ids:
        id = object_proxy.execute_kw(DB, uid, PASS, 'sale.order', 'write', [[sale_id], {
            'sale_signature': signature
        }])
        print(id)

