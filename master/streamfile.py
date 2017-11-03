from pyspark import SparkContext,SparkConf
from pyspark.streaming import StreamingContext
from pyspark.sql import SQLContext
import json
import MySQLdb
import re
import datetime
from contextlib import closing
def parse(rdditem):
#	tmpstr = rdditem.map(lambda x: re.sub(r"\s+", "", x, flags=re.UNICODE))
	if rdditem.count()<=0:
		return
	sttime = datetime.datetime.now()
	sttime_begin = sttime
#        print "start at: " + str(sttime)
	rawstr = "".join(str(x).strip() for x in rdditem.collect())
#	print rawstr
	edtime = datetime.datetime.now()
#       print "end at: " + str(edtime)
	diff = edtime - sttime
	print "duration for joining string = " + str(diff)
        sttime = datetime.datetime.now()
	rawstrlst = [rawstr]
	rawstrrdd = sc.parallelize(rawstrlst)
	rcd = sqlContext.read.json(rawstrrdd)
#	df.printSchema()
	edtime = datetime.datetime.now()
#       print "end at: " + str(edtime)
	diff = edtime - sttime
	print "duration for reading json = " + str(diff)
	sttime = datetime.datetime.now()
	fullinfo = rcd.select("id","resourceType","effectiveDateTime","meta","category","valueQuantity","subject","extension","identifier").first()
#	id_rt_edt = rcd.select("id","resourceType","effectiveDateTime").first()
#	resource_id = id_rt_edt[0]
#	resourceType = id_rt_edt[1]
	resource_id = fullinfo["id"]
	resourceType = fullinfo["resourceType"]
	datalake_row_id = None
#	mt_ct_sbj = rcd.select("meta","category","subject").first()
	meta_resource_version = fullinfo["meta"]["versionId"]
	meta_lastupdated = fullinfo["meta"]["lastUpdated"]
	meta_istrusted = None
	edtime = datetime.datetime.now()
#       print "end at: " + str(edtime)
	diff = edtime - sttime
	print "duration for parsing part0 = " + str(diff)
	sttime = datetime.datetime.now()

	for x in fullinfo["meta"]["tag"]:
		if "dataEntryClassification" in x["system"]:
			meta_data_entry_class = x["code"]
		if "isValidated" in x["system"]:
			meta_isvalidated = x["code"]
		if "sourceUpdateFlag" in x["system"]:
			meta_isconsecutive = x["code"]
	edtime = datetime.datetime.now()
#       print "end at: " + str(edtime)
	diff = edtime - sttime
	print "duration for parsing part00 = " + str(diff)
	sttime = datetime.datetime.now()

	eff_ts = fullinfo["effectiveDateTime"]
	category_cd = fullinfo["category"]["coding"][0]["code"]
	category_uri = fullinfo["category"]["coding"][0]["system"]
	category_disp = fullinfo["category"]["coding"][0]["display"]
#	vq = rcd.select("valueQuantity").first()[0]
	remain_dose_count = fullinfo["valueQuantity"]["value"]
	remain_dsgcnt_unit = fullinfo["valueQuantity"]["unit"]
	remain_dsgcnt_sys = fullinfo["valueQuantity"]["system"]
	alert_uri = None
	alert_cd = None
	alert_uom = None
	alert_type = None
	alert_val = None
	alert_ts = None
	alert_device_id = fullinfo["subject"]["reference"]
	observ_uom = None
	edtime = datetime.datetime.now()
#       print "end at: " + str(edtime)
	diff = edtime - sttime
	print "duration for parsing part1 = " + str(diff)
	sttime = datetime.datetime.now()
#	for x in rcd.select("extension").first()[0]:
	for x in fullinfo["extension"]:
		if "lastMessageID" in x["url"]:
			ext_message_id = x["valueString"]
		if "sourceTime_GMT" in x["url"]:
			ext_source_ts_gmt = x["valueDateTime"]
		if "sourceTime_TZ" in x["url"]:
			ext_source_ts_tz = x["valueString"]
		if "UUID" in x["url"]:
			ext_uuid = x["valueString"]
		if "receiveTime_GMT" in x["url"]:
			ext_receive_ts_gmt = x["valueDateTime"]
		if "receiveTime_TZ" in x["url"]:
			ext_receive_ts_tz = x["valueString"]
		if "releaseVersion" in x["url"]:
			ext_release_ver = x["valueString"]
		if "requestID" in x["url"]:
			ext_request_id = x["valueString"]
		if "MQMsgID" in x["url"]:
			ext_mqmsg_id = x["valueString"]
		if "sourceObjectName" in x["url"]:
			ext_srcobj_nm = x["valueString"]
		if "documentStatus" in x["url"]:
			ext_doc_status = x["valueString"]
		if "ptnIdentifier" in x["url"]:
			ext_ptn_identifier = x["valueString"]
		if "appName" in x["url"]:
			ext_app_nm = x["valueString"]
		if "appVersionNumber" in x["url"]:
			ext_app_version = x["valueString"]
		if "studyid" in x["url"]:
			ext_study_id = x["valueString"]
		if "siteid" in x["url"]:
			ext_site_id = x["valueString"]
		if "apiExecutionMode" in x["url"]:
			ext_api_exe_mode = x["valueString"]
		if "serverTimeOffset" in x["url"]:
			ext_ser_time_offset = x["valueString"]
		if "lastConnectionDate" in x["url"]:
			ext_last_connect_ts = x["valueString"]
		if "doseCount" in x["url"]:
			ext_dose_count = x["valueString"]
#	ext_serial_num = rcd.select("identifier").first()[0][0]["type"]["coding"][0]["display"]
	ext_serial_num = fullinfo["identifier"][0]["type"]["coding"][0]["display"]
	isdeleted = "N"
	edtime = datetime.datetime.now()
#       print "end at: " + str(edtime)
	diff = edtime - sttime
	print "duration for parsing part2 = " + str(diff)
	sttime1 = datetime.datetime.now()

#	db = MySQLdb.connect("192.168.109.154","ivanybma","","demo" )
	with closing(db.cursor()) as cursor:
		cursor = db.cursor()
		cursor.execute("update  DIM_MEDICAL_DEVICE_OBSERV set CRN_IND='N', VLD_TO_TS = %s where CRN_IND = 'Y' and RESOURCE_ID = %s",(datetime.datetime.now(),resource_id)) 
		cursor.execute("insert into DIM_MEDICAL_DEVICE_OBSERV values(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(None,resource_id,resourceType,datalake_row_id,meta_resource_version,meta_lastupdated,meta_istrusted,meta_data_entry_class,meta_isvalidated,meta_isconsecutive,eff_ts,category_cd,category_uri,category_disp,remain_dose_count,remain_dsgcnt_unit,remain_dsgcnt_sys,alert_uri,alert_cd,alert_uom,alert_type,alert_val,alert_ts,alert_device_id,observ_uom,ext_message_id,ext_source_ts_gmt,ext_source_ts_tz,ext_uuid,ext_receive_ts_gmt,ext_receive_ts_tz,ext_release_ver,ext_request_id,ext_request_id,ext_mqmsg_id,ext_srcobj_nm,ext_doc_status,ext_ptn_identifier,ext_app_nm,ext_app_version,ext_study_id,ext_site_id,ext_api_exe_mode,ext_ser_time_offset,ext_last_connect_ts,ext_dose_count,ext_serial_num,'Y',datetime.datetime.now(),None))
	edtime1 = datetime.datetime.now()
#       print "end at: " + str(edtime)
	diff = edtime1 - sttime1
	print "duration for db upsert = " + str(diff)

	sttime2 = datetime.datetime.now()
	db.commit()
	edtime2 = datetime.datetime.now()
#	print "end at: " + str(edtime)
	diff = edtime2 - sttime2
	print "duration for db commit = " + str(diff)
	
	diff = edtime2 - sttime_begin
	print "duration for whole processing = " + str(diff)

	
# Create a local StreamingContext with two working threads and a batch interval of 2 seconds
appName = "pipeline"
master = "spark://192-168-109-152:7077"
#conf = SparkConf().setAppName(appName)
sc = SparkContext(master,appName)
#sc = SparkContext(SparkConf())
sqlContext = SQLContext(sc)
ssc = StreamingContext(sc, 2)

# Create a DStream
lines = ssc.textFileStream("/test/stream_file/")
# Split each line into words

# Print each batch
lines.pprint()
lines.foreachRDD(parse)
#print "testing"
db = MySQLdb.connect("192.168.109.154","ivanybma","","demo" )
cursor = db.cursor()
#cursor.execute("select * from DIM_MEDICAL_DEVICE_OBSERV")
#print cursor.fetchone()
ssc.start()             # Start the computation
ssc.awaitTermination()  # Wait for the computation to terminate
