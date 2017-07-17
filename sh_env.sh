#!/bin/bash
set -x
HADOOP_CMD="/home/xuyikai/hadoop-client/hadoop/bin/hadoop"
DATE=`date -d -1day +%Y%m%d`
PYTHON="/home/xuyikai/bin/python"
get_time () {
	nowtime=`date +"%Y/%m/%d %H:%M:%S"`
	echo -e $nowtime
}
writelog () {
	if (( $? != 0 ));then
		echo -e "ERROR:\t *[$1] failed!"
		exit -1
	fi
	get_time
	echo -e "SUCCESS:\t *[$1] done!"
}
