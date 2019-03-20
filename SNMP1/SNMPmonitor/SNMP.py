from pysnmp.hlapi import *
class SNMP:
    def __makeQuery(self,OIDlist):
        ObjectTypeMIB = []
        for OID in OIDlist:
            ObjectTypeMIB.append(ObjectType(ObjectIdentity(OID)))
        return ObjectTypeMIB
    
    def sendRequest(self,device,OIDlist):
        print("send request to "+device.getIP()+"...")
        errorIndication, errorStatus, errorIndex, varBinds = next(
            getCmd(
                SnmpEngine(),
                CommunityData(device.getCommunity()),
                UdpTransportTarget((device.getIP(),device.getPort())),ContextData(),
                *self.__makeQuery(OIDlist)
            )
        )
        return errorIndication, errorStatus, errorIndex, varBinds
    def setValue(self,device,OID,value):
        wassSuccessful = False
        msgInfo = None 
        errorIndication, errorStatus, errorIndex, varBinds = next(
            setCmd(
                SnmpEngine(),
                CommunityData(device.getCommunity()),
                UdpTransportTarget((device.getIP(), device.getPort())),ContextData(),
                ObjectType(ObjectIdentity(OID),value)
            )   
        )
        if errorIndication:
            info = errorIndication
        elif errorStatus:
            info = ('%s at %s' % (errorStatus.prettyPrint(),
                                errorIndex and varBinds[int(errorIndex) - 1][0] or '?'))
        else:
            for varBind in varBinds:
                info = (' = '.join([x.prettyPrint() for x in varBind]))
            wassSuccessful = True
        return wassSuccessful,info.split()[2]
