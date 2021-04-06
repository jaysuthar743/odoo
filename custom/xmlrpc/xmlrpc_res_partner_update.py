import xmlrpc.client
import xlrd
import base64

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

print(object_proxy.execute_kw(DB, uid, PASS, 'res.partner', 'search', [[['name', 'ilike', "Wood Corner"]]]))

loc = "res_partner_update.xls"

wb = xlrd.open_workbook(loc)

for sheet in wb.sheets():
    for row in range(1, sheet.nrows):
        res_partner_id = sheet.cell(row, 0).value
        res_partner_phone = sheet.cell(row, 1).value  # product sales price
        id = object_proxy.execute_kw(DB, uid, PASS, 'res.partner', 'write', [[res_partner_id], {
            'phone': int(res_partner_phone)
        }])
        print(id)

