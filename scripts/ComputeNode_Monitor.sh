#!/bin/bash 
#####################################################################################################
# Script for monitoring operating system's resources on Exalogic machine.
# Generates a CSV file with lines in the following format:
# hostname, date, hour, ram%, #conn_established, #conn_timewait, #conn_closewait, #running_procs  
#
# Usage: bash OSmonitor-2.sh
# Author: Daniela Torres Faría 
# Version: 2.0
#
#####################################################################################################

#Variables 

HOST=`hostname`
DATE=`date +"%d/%m/%Y"`
HOUR=`date +"%H:%M"`
CSVFILE=/u01/common/general/Exalogic_Scripts/Monitoring/OSMonitorData/$HOST"_osmonitor.csv"
PROCS=`ps -Led | wc -l`
OPENF=`cat /proc/sys/fs/file-nr | awk {'print $1'}`
CPU=`sar 1 2 | tail -1 | awk {'printf "%s\n",$3'}`
MEMORY=`free -g | awk 'NR==2{printf "%s\n", (($3-($6+$7))*100)/$2}'`
ESTABLISHED=`/usr/sbin/ss -4 -n state established | wc -l`
TIME_WAIT=`/usr/sbin/ss -4 -n state time-wait | wc -l`
CLOSE_WAIT=`/usr/sbin/ss -4 -n state close-wait | wc -l`
FINWAIT1=`/usr/sbin/ss -t -a | grep FIN-WAIT-1 | wc -l`
FINWAIT2=`/usr/sbin/ss -t -a | grep FIN-WAIT-2 | wc -l`
#TIME_WAIT=`netstat -an | grep TIME_WAIT | wc -l` 
#CLOSE_WAIT=`netstat -an | grep CLOSE_WAIT | wc -l` 
#ESTABLISHED=`netstat -an | grep ESTABLISHED | wc -l`


usage(){
cat << EOF
	Uso: $0 opciones

	Este script recolecta informacion sobre el estado del sistema. 
	Coloca la Salida en un archivo ubicado en la ruta $CSVFILE

	OPTIONS:
	   -help   Muestra este mensaje 
EOF
}

###### Main Script

while getopts h:l:help OPTION
do
     case $OPTION in
         help)
             usage
             exit 0
             ;;
         h)
						usage
						exit 0
             ;;
         ?)
             usage
             exit
             ;;
     esac
done

# display usage if the script is not run as root user 
if [[ $USER != "root" ]]; then 
	echo "[ERROR] - Este script debe ser ejecutado como root" 
	exit 1
fi 

echo "$HOSTNAME,$DATE-$HOUR,$MEMORY,$CPU,$ESTABLISHED,$TIME_WAIT,$CLOSE_WAIT,$FINWAIT1,$FINWAIT2,$PROCS,$OPENF" >> $CSVFILE

exit 0
