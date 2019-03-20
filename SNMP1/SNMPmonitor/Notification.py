import smtplib
import rrdtool

COMMASPACE = ', '

tiempo_final = int(rrdtool.last("trend.rrd"))
tiempo_inicial = tiempo_final - 360


class Notification1:
    #def run(self):
        ret = rrdtool.graphv("deteccion.png",
                             "--start", str(tiempo_inicial),
                             "--end", str(tiempo_final),
                             "--title", "Carga de CPU",
                             "--vertical-label=Uso de CPU (%)",
                             '--lower-limit', '0',
                             '--upper-limit', '100',
                             "DEF:carga=trend.rrd:CPUload:AVERAGE",
                             "CDEF:umbral80=carga,80,LT,0,carga,IF",
                             "VDEF:cargaMAX=carga,MAXIMUM",
                             "VDEF:cargaMIN=carga,MINIMUM",
                             "VDEF:cargaSTDEV=carga,STDEV",
                             "VDEF:cargaLAST=carga,LAST",
                             "AREA:carga#00FF00:Carga del CPU",
                             "AREA:umbral80#FF9F00:Tráfico de carga mayor que 80",
                             "AREA:umbral80#FF9F00:Tráfico de carga mayor que 25",
                             "HRULE:80#FF0000:Umbral 1 - 80%",
                             "PRINT:cargaMAX:%6.2lf %S",
                             "GPRINT:cargaMIN:%6.2lf %SMIN",
                             "GPRINT:cargaSTDEV:%6.2lf %SSTDEV",
                             "GPRINT:cargaLAST:%6.2lf %SLAST")

        print (ret)
        print(ret.keys())
        print(ret.items())

        ultimo_valor = float(ret['print[0]'])

        if ultimo_valor > 23:
            print("Sobrepasa Umbral línea base")
