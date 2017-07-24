#!/bin/bash

set -x
DATE=`date +%Y%m%d`
YESTADY=`date -d -1day +%Y%m%d`
echo "__start"
echo $DATE
date
#STARTDATE=`date -d -7day +%Y%m%d`
STARTDATE=`date -d -1day +%Y%m%d`
ENDDATE=`date -d -7day +%y%m%d`

PYTHON="/home/xuyikai/bin/python2.7"
HADOOP="/home/xuyikai/hadoop/bin/hadoop"

day_sum=0
for i in `seq 0 6`
do
	flag=0
	day=-$((7-$i))day
	STARTDATE=`date -d $day +%Y%m%d`
	ENDDATE=$STARTDATE

	log_file=data/log_file.txt."$ENDDATE"
	if [[ ! -s "$log_file" ]];then
		../queryengine-client-2.1.7-online/queryengine/bin/queryengine --hivevar day1=$STARTDATE day2=$ENDDATE -f get_jingxiu_new.sql
		if [ $? -ne 0 ];then
    		echo "get pv failed! try again..."
    		$HADOOP fs -rmr /app/ecom/impl/xuyikai/jingxiu/query/
    		$HADOOP fs -mkdir /app/ecom/impl/xuyikai/jingxiu/query/
    		../queryengine-client-2.1.7-online/queryengine/bin/queryengine --hivevar day1=$STARTDATE day2=$ENDDATE -f get_jingxiu_new.sql
    		if [ $? -ne 0 ];then
        		echo "get log failed again! exit"
        		exit 1
    		fi
		fi
#mv data/pv.txt data/pv.txt."$ENDDATE"
		if [[ -f "$log_file" ]];then
			rm $log_file
		fi
		$HADOOP fs -getmerge /app/ecom/impl/zhengshuai03/jingxiu/newpv/"$STARTDATE"_"$ENDDATE" ./data/log_file.txt."$ENDDATE"
		if [[ ! -s "$log_file" ]];then
    		echo "$log_file is empty"
    		exit
		fi
		flag=1
	fi

	if [ $flag -eq 1 ];then
		let "day_sum = $day_sum + 1"
		cat "$log_file" >> ./data/log_file.txt
	fi
done

echo "processing $day_sum days"
if [ $day_sum -eq 0 ];then
    echo "today's data has already been proceed!"
	exit

fi
echo "__end"
date
