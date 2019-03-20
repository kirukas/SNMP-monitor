import rrdtool


class CreateRRD:
    ret = rrdtool.create("trend.rrd",
                         "--start", 'N',
                         "--step", '10',
                         "DS:CPUload:GAUGE:600:U:U",
                         "RRA:AVERAGE:0.5:1:24")

    if ret:
        print(rrdtool.error())

    ultima_lectura = int(rrdtool.last("trend.rrd"))
    tiempo_final = ultima_lectura
    tiempo_inicial = tiempo_final - 360

    ret = rrdtool.graphv("trend.png",
                         "--start", str(tiempo_inicial),
                         "--end", str(tiempo_final),
                         "--vertical-label=Carga CPU",
                         "--title=Uso de CPU",
                         "--color", "ARROW#009900",
                         '--vertical-label', "Uso de CPU (%)",
                         '--lower-limit', '0',
                         '--upper-limit', '100',
                         "DEF:carga=trend.rrd:CPUload:AVERAGE",
                         "AREA:carga#00FF00:Carga CPU",
                         "LINE1:30",
                         "AREA:5#ff000022:stack",
                         "VDEF:CPUlast=carga,LAST",
                         "VDEF:CPUmin=carga,MINIMUM",
                         "VDEF:CPUavg=carga,AVERAGE",
                         "VDEF:CPUmax=carga,MAXIMUM",

                         "COMMENT:Now          Min             Avg             Max",
                         "GPRINT:CPUlast:%12.0lf%s",
                         "GPRINT:CPUmin:%10.0lf%s",
                         "GPRINT:CPUavg:%13.0lf%s",
                         "GPRINT:CPUmax:%13.0lf%s",
                         "VDEF:m=carga,LSLSLOPE",
                         "VDEF:b=carga,LSLINT",
                         'CDEF:tendencia=carga,POP,m,COUNT,*,b,+',
                         "LINE2:tendencia#FFBB00")

    print(ret)
    print(ret.keys())
    print(ret.items())
