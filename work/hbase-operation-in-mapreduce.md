Title: 在MapReduce中读写HBase数据库
Date: 2015-09-24 16:19
Category: work
Tags: hbase, operation, mapreduce
Summary: 介绍在MapReduce中如何操作(读写)HBase数据库.
Slug: hbase-operation-in-mapreduce

之前有blog介绍过了HBase的rowkey设计和column索引等内容,  
这篇blog主要介绍HBase应用的一个小实例--在MapReduce代码中读写HBase.

##基本数据流程

实例的基本数据流程如下:

1. Mapper从HDFS上面读入文本数据
2. 在HBase中进行相应的查询
3. (有需要的话)新增/更新/删除HBase中的数据  

任务比较简单,没有用到Reducer.

因为涉及到稍微复杂点的HBase操作(包括操作大于一个HBase表),  
也就没有用MR输出直接写入HBase库的方案.

##Main输入参数

使用ToolRunner.run方法执行MR时,可以在命令行中传入任意KV参数供代码使用,

这一特性比原始的写法(一个简单main函数的写法)里面,一个个去解析args参数要简单方便的多.

Main代码示例如下:
````java
public class TestMain extends Configured implements Tool {

    public static void main(String[] args) throws Exception {
        int exitCode = ToolRunner.run(new TestMain(), args);
        System.exit(exitCode);
    }

    @Override
    public int run(String[] args) throws Exception {

        Configuration conf = getConf();

        System.out.println("inputPath=" + conf.get("inputPath"));
        System.out.println("param2=" + conf.get("param2"));
        System.out.println("param3=" + conf.get("param3"));
        System.out.println("param4=" + conf.get("param4"));
        System.out.println("param5=" + conf.get("param5"));

        Job job = new Job(conf, "TestMain");
        job.setJarByClass(TestMain.class);
        job.setMapperClass(TestMapper.class);
        job.setMapOutputKeyClass(NullWritable.class);
        job.setMapOutputValueClass(NullWritable.class);
        job.setInputFormatClass(TextInputFormat.class);
        // OutputFormatClass 必须设置,不然运行时会报错;如果确实没有任何输出,这里设置为NullOutputFormat
        job.setOutputFormatClass(NullOutputFormat.class);

        FileInputFormat.addInputPath(job, new Path(conf.get("inputPath")));

        return (job.waitForCompletion(true) ? 0 : 1);
    }
}
````

此时,命令行执行参数如下:
````
hadoop jar test.jar \
-DinputPath=/tmp/test \
-Dparam2=param2 \
-Dparam3=param3 \
-Dparam4=param4 \
-Dparam5=param5
````

##Mapper的处理

在Mapper的setup方法中建立与HBase的连接(拿到**HBase操作实例**),

在map方法中,完成具体的业务逻辑处理即可.

##HBase的操作

即前面提到的HBase操作实例,是我自己对HBase操作的一个简单封装(异常处理部分还需要优化),  
代码如下:
````java
public class HBaseOpt {
    private static HashMap<String, HBaseOpt> hbaseInsMap = new HashMap<String, HBaseOpt>(2);
    private HTable table = null;

    private HBaseOpt(String zkQuorum, String tableName) {
        Configuration conf = HBaseConfiguration.create();
        conf.set("hbase.zookeeper.quorum", zkQuorum);
        try {
            table = new HTable(conf, tableName);
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public static HBaseOpt getInstance(String zkQuorum, String tableName) {
        if (null == hbaseInsMap.get(tableName)) {
            HBaseOpt hbaseInsTmp = new HBaseOpt(zkQuorum, tableName);
            hbaseInsMap.put(tableName, hbaseInsTmp);
            return hbaseInsTmp;
        } else {
            return hbaseInsMap.get(tableName);
        }

    }

    public void put(String key, String cf, String col, String val) {
        Put put = new Put(key.getBytes());
        put.add(cf.getBytes(), col.getBytes(), val.getBytes());
        try {
            table.put(put);
//            System.out.print("put.toString()=" + put.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    // Cell value
    public String get(String key, String cf, String col) {
        Get get = new Get(key.getBytes());
        get.addColumn(cf.getBytes(), col.getBytes());
        try {
            Result rs = table.get(get);
            byte[] value = rs.getValue(cf.getBytes(), col.getBytes());
            if (null != value) {
//                System.out.print("k:cf:col=" + new String(value));
                return new String(value);
            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return null;
    }

    public void delete(String key) {
        Delete del = new Delete(key.getBytes());
        try {
            table.delete(del);
//            System.out.print("put.toString()=" + put.toString());
        } catch (IOException e) {
            e.printStackTrace();
        }
    }

    public Map<String, String> scan(String startKey, String endKey, String cf, String col) {
        Scan scan = new Scan(startKey.getBytes(), endKey.getBytes());
        scan.addColumn(cf.getBytes(), col.getBytes());
        scan.setCaching(50);
        scan.setBatch(50);
        HashMap<String, String> resultMap = new HashMap<String, String>(50);
        try {
            ResultScanner scanner = table.getScanner(scan);
            for (Result rs = scanner.next(); rs != null; rs = scanner.next()) {
                byte[] key = rs.getRow();
                byte[] value = rs.getValue(cf.getBytes(), col.getBytes());
                if (null != value) {
//                    System.out.print("k:cf:col=" + new String(value));
                    resultMap.put(new String(key), new String(value));
                }

            }
        } catch (IOException e) {
            e.printStackTrace();
        }
        return resultMap;
    }


    // For local test
    public static void main(String[] args) {
        String key = "a";
        String cf = "d";
        String col = "id";
        // 传入HSlave hostname给zookeeper
        HBaseOpt hbase = HBaseOpt.getInstance("A, B, C", "test");
//        hbase.put(key, cf, col, "test_value_for_key_a");
//        System.out.println(hbase.get(key, cf, col));

        // scan by key range
        Map<String, String> resultMap = hbase.scan("321", "321~", cf, col);
        for (String keyTmp : resultMap.keySet()) {
            System.out.println(keyTmp);
            System.out.println(resultMap.get(keyTmp));
            System.out.println("------------");
        }
    }
}
````

##HBase的rowkey模糊查询

HBase本身支持filter查询,但是效率不高.

常见的做法是利用HBase的rowkey设置起始和结束key值, 来达到模糊查询的目的.

不过有个限制是:只能使用key的任意**prefix** value, 而不能从中间截取key进行查询.

举例:假设HBase数据表结构和数据为:

|part1_part2_part3|data  |
|-----------------|----  |
|abc_123_321      |value1|
|abc_321_xyz      |value2|
|abc_987_xyz      |value2|
|abc_abc_xyz      |value2|
|abz_921_xyz      |value3|
|xyz_abc_123      |value4|
|123_abc_xyz      |value5|
|...              |...   |

那么我们只能用part1开头的组合(part1_part2, part1_part2_part3等)进行模糊查询,

而不能直接用part2,或part3去查询.

例如:

输入start key=abc_1, end key=abc_9, 可以查出上表中的如下数据:  

|part1_part2_part3|data  |
|-----------------|----  |
|abc_123_321      |value1|
|abc_321_xyz      |value2|
|abc_987_xyz      |value2|

如果想查出所有以"abc"开头的数据,可以输入:  
start key=abc, end key=abc~

**~** 代表ascII中常用字符的最大值.


##结语

借助HBase操作帮助类, 在Mapper(或是Reducer)中就可以很方便地完成对HBase的所有操作了.