#!/bin/bash
#####################################################################################################
# Script for monitoring IB switches RX,TX on Exalogic machine.
# Usage: bash IBmonitor_Ports.sh
# Author: Daniela Torres Faría
#####################################################################################################

IP=172.23.59.74
HOST=`ssh root@$IP "hostname"`
DATE=`date +"%d/%m/%Y"`
HOUR=`date +"%H:%M"`
PORT1='0A_ETH_1'
PORT2='1A_ETH_1'

#Switch 1

#Puerto 1

RX1_P1=`ssh root@$IP "getportcounters 0A-ETH-1" | awk ' /RX bytes/ { match($0,"[0-9]+",ary) ; print ary[0] }'`
TX1_P1=`ssh root@$IP "getportcounters 0A-ETH-1" | awk ' /TX bytes/ { match($0,"[0-9]+",ary) ; print ary[0] }'`

#Puerto 2

RX1_P2=`ssh root@$IP "getportcounters 1A-ETH-1" | awk ' /RX bytes/ { match($0,"[0-9]+",ary) ; print ary[0] }'`
TX1_P2=`ssh root@$IP "getportcounters 1A-ETH-1" | awk ' /TX bytes/ { match($0,"[0-9]+",ary) ; print ary[0] }'`

#Tiempo de espera 15 min 

sleep 15m
	
#Puerto 1 
RX2_P1=`ssh root@$IP "getportcounters 0A-ETH-1" | awk ' /RX bytes/ { match($0,"[0-9]+",ary) ; print ary[0] }'`
TX2_P1=`ssh root@$IP "getportcounters 0A-ETH-1" | awk ' /TX bytes/ { match($0,"[0-9]+",ary) ; print ary[0] }'`

#Puerto 2
RX2_P2=`ssh root@$IP "getportcounters 1A-ETH-1" | awk ' /RX bytes/ { match($0,"[0-9]+",ary) ; print ary[0] }'`
TX2_P2=`ssh root@$IP "getportcounters 1A-ETH-1" | awk ' /TX bytes/ { match($0,"[0-9]+",ary) ; print ary[0] }'`


#Puerto 1

#Bytes por segundo 

TOTALRX_P1=$( expr \( $RX2_P1 - $RX1_P1 \) / 900 ) 
TOTALTX_P1=$( expr  \( $TX2_P1 - $TX1_P1 \) / 900 )
	
#Megabytes por segundo 

TOTALRXM_P1=$( expr \( $TOTALRX_P1 / 1024 \) / 1024)
TOTALTXM_P1=$( expr \( $TOTALTX_P1 / 1024 \) / 1024)

#Puerto 2

#Bytes por segundo 

TOTALRX_P2=$( expr \( $RX2_P2 - $RX1_P2 \) / 900 ) 
TOTALTX_P2=$( expr  \( $TX2_P2 - $TX1_P2 \) / 900 )

#Megabytes por segundo 

TOTALRXM_P2=$( expr \( $TOTALRX_P2 / 1024 \) / 1024)
TOTALTXM_P2=$( expr \( $TOTALTX_P2 / 1024 \) / 1024)

#echo "$HOST,$DATE,$HOUR,$TOTALRX_P1,$TOTALTX_P1,$TOTALRXM_P1,$TOTALTXM_P1" >> /u01/common/general/CCScripts/IBMonitor_Res/$HOST"_ibmonitor_Port_0A_ETH_1.csv"
#echo "$HOST,$DATE,$HOUR,$TOTALRX_P2,$TOTALTX_P2,$TOTALRXM_P2,$TOTALTXM_P2" >> /u01/common/general/CCScripts/IBMonitor_Res/$HOST"_ibmonitor_Port_1A_ETH_1.csv"
echo "$HOST,$PORT1,$DATE-$HOUR,$TOTALRX_P1,$TOTALTX_P1,$TOTALRXM_P1,$TOTALTXM_P1" >> /u01/common/general/Exalogic_Scripts/Monitoring/IBMonitorData/$HOST"_ibmonitor_Port_0A_ETH_1.csv"
echo "$HOST,$PORT2,$DATE-$HOUR,$TOTALRX_P2,$TOTALTX_P2,$TOTALRXM_P2,$TOTALTXM_P2" >> /u01/common/general/Exalogic_Scripts/Monitoring/IBMonitorData/$HOST"_ibmonitor_Port_1A_ETH_1.csv"
