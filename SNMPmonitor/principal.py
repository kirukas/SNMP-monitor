from Monitoring import *
from device import *
from DataBase import *
from SNMP import*
#import sys
#from PyQt5.QtCore import pyqtSlot
#from GUI import *
if __name__ == "__main__":
     # app =QtWidgets.QApplication(sys.argv)
     # ex = Ui_MainWindow()
     # ex.show()
     # sys.exit(app.exec_())
    
     IP = '192.168.1.71'
     Port ='161'
     Community = 'SNMPcom'
     OIDlist = ['1.3.6.1.2.1.1.4.0'] # lista de oid a monitorear
     listDevices = []
     user = 'root'## usuario de mysql
     password = 'terrys'## la contraseña de msql
     database = 'devices'# nombre de la base de datos
     timeUPdate = 10 # tiempo de actualizaion en que pedira informacioin del cpu segundos
     db = connectorDB(user,password,database)    
    
     # snmp = SNMP()
     # wassSuccessful,info = snmp.setValue(d,'1.3.6.1.2.1.1.4.0','enriqueherme@gmail.com')
     # print(info)
     
     #db.addDevice(IP,Port,Community,None,None,None,None) # agrega un dispositivo ala base de datos
     # devices = db.getDevices() ## obtiene todos los dispositivo de la base
     # for device in devices:
     #      listDevices.append(Monitoring(Device(device[0],device[1],device[2]),timeUPdate,OIDlist,db))
     # for d in listDevices:
     #      d.start()
          
  
   
