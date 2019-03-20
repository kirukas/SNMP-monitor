from SNMP import *
import time
import threading
import rrdtool
from DataBase import *
import re
from Mail import *
from CreateRRD import *



class Monitoring(threading.Thread):

    def __init__(self, device, UPdate, OIDlist, db):

        threading.Thread.__init__(self)
        self.device = device  # monitor
        self.protocolSNMP = SNMP()  # protocolo de communicacion
        self.upDate = UPdate  ## tiempo de actualizacion de los datos
        self.isConected = False  # estado de conexion con el dsipositivo a conectar
        self.listOIDinfo = ['1.3.6.1.2.1.1.1.0', '1.3.6.1.2.1.1.6.0', '1.3.6.1.2.1.1.4.0',
                            '1.3.6.1.2.1.1.5.0']  # OID de info del dispositivo
        self.monitoringUP = True
        self.OIDlist = OIDlist
        self.db = db
        self.pattern = re.compile("[Ll][Ii][Nn][Uu][Xx]")

    def setComunication(self, listOID):
        errorIndication, errorStatus, errorIndex, varBinds = self.protocolSNMP.sendRequest(self.device, listOID)
        return errorIndication, errorStatus, errorIndex, varBinds

    def statusConnection(self, errorIndication, errorStatus, errorIndex):
        errorInfo = None
        if errorIndication:
            self.isConected = False
            errorInfo = errorIndication
        elif errorStatus:
            self.isConected = False
            errorInfo = str(
                '%s at %s' % (errorStatus.prettyPrint(), errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            self.isConected = True
        return errorInfo

    def getInformation(self, varBinds):
        info = []
        for varBind in varBinds:
            a, b = (' = '.join([x.prettyPrint() for x in varBind])).split('=')
            info.append(b)
        return info

    def getInformationDevice(self, listOID):
        data = None
        errorIndication, errorStatus, errorIndex, varBinds = self.setComunication(listOID)
        errorInfo = self.statusConnection(errorIndication, errorStatus, errorIndex)
        if self.isConected:
            data = self.getInformation(varBinds)
        else:
            print(errorInfo)
        return data

    ## esta es la funcion donde monitorea
    def startMonitoring(self):


        infoSystem = self.getInformationDevice(self.listOIDinfo)
        if infoSystem:
            # print(infoSystem)
            self.upDateInfoDevice(
                infoSystem)  ## actualizacion de la informacion del dispositivo se actualiza la base de datos
        infoOID = self.getInformationDevice(self.OIDlist)  # informacioin de las mib a monitorizar
        if infoSystem:
            print("dato "+str(infoOID))  ## este es la dato que nececitas
###########################################################################

            CPU_info = float(infoOID[0])
            valor = "N:" + str(CPU_info)
            print(valor)
            ret = rrdtool.update('trend.rrd', valor)
            rrdtool.dump('trend.rrd', 'trend.xml')
            time.sleep(1)

        if ret:
            print(rrdtool.error())
            time.sleep(300)

############################################################################

    def run(self):
        while self.isUP():
            self.startMonitoring()
            time.sleep(self.getTimeUpDate())

    def upDateInfoDevice(self, infoSystem):  # funcion que actualiza la info del sistema
        system = self.setSystem(infoSystem[0])
        self.db.upDateDevice(self.device.getIP(), system, infoSystem[1], infoSystem[2], infoSystem[3])

    def setSystem(self, info):
        system = None
        if self.pattern.search(info):
            system = 'Linux'
        else:
            system = 'Windodws'
        return system

    def setTimeUpDate(self, time):
        self.upDate = time

    def getTimeUpDate(self):
        return self.upDate

    def setMonitoringUP(self, e):
        self.monitoringUP = e

    def isUP(self):
        return self.monitoringUP
