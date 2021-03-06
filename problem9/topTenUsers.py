from pyspark.sql.functions import *
from pyspark.sql import SQLContext
sqlctx = SQLContext(sc)
df  = sqlctx.jsonFile("/user/training/problem8/output/chatlogs/*")
df.registerTempTable("df")
df1 = sqlctx.sql("SELECT agentName From df where category='Device'")
topten = df1.map(lambda x: (x.agentName, 1)) \
	.reduceByKey(lambda x, y: x+y) \
	.sortBy(lambda x: x[1], ascending=False) \
	.map(lambda (x, y): x +"\t"+str(y)).take(10)

sc.parallelize(sqlctx.createDataFrame(topten).select(col("_1").alias("agentName"),col("_2").alias("count")).toJSON().take(10)) \
.saveAsTextFile("/user/training/problem9/output")




