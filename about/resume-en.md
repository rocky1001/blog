Title: Resume
Date: 2016-10-08 09:53
Category: about
Tags: resume
Summary: My resume in English.
Slug: rocky-resume-in-English

**E-Mail:** [rockychi1001@gmail.com](mailto:rockychi1001@gmail.com "my email")  
**Location:** Xi’an, China

----
##Summary	   
* Worked as Java engineer for 3 years, mainly on J2EE projects.

* Worked as Data analyst for 1 year using Hadoop(MRv1), Hive and Pig.

* Working as Software engineer for 3 years, mainly in Python.
 
#####Highlights	
* Main: Python, Java, SQL, JavaScript, Bash, Lua.

* Others: Linux(CentOS, Ubuntu), MySQL, Redis, Hadoop, OpenResty, TCP, HTTP, SOAP, RESTful.

* English: CET-6(79/100), CET-4(87.5/100), National College English Oral Test(B+).

#####Interested in	
* Coding, making life interesting and easier with programs and applications.

* Raspberry Pi with camera (Hardware, computer vision related stuff).

----
##Experience
2012.10 - Ongoing: **Senior Software Engineer @Hylink digital advertising Co. LTD.**  

#####Real-time OLAP platform
Working as major developer, includes:

* Test and choose the main project(Airbnb Caravel and Apache Kylin).

* Secondary development on Caravel and Kylin, and also it's [opensource](https://github.com/rocky1001/caravel/tree/caravel-kylin "Caravel with Kylin").

* Now huge ad delivery logs data(more than 10GB per day) can do multi-dimension OLAP based on this platform.

#####Mobile application advertising system  
Worked as team leader and major developer in the team, includes:

* Design and build advertising data management platform (B/S arch in Python, Django).

* Build app advertising delivery log analyze system (RESTful interface for inner-system communicate, SFTP interface to collect log automatically, and Hive for log analyzing, all glued in python).

* The system now delivering 2 million ads per day, collecting more than 10GB logs file, which are used to optimizing the advertising delivery strategy.

* Design and build demographic labeling system for mobile users, using the delivery log to label the mobile user, the result data can be used to guide the ad delivery for better effect.

#####Data Management Platform(DMP, user data storage and analysis platform)  
Worked as major developer in the team, includes:

* Analyzing delivery logs data with different dimension combinations (Mainly using Hive, also tried Elastic Search/Apache Kylin for OLAP).

* Design and build cookie mapping server, mapping the cookie data with ad exchangers.

* Implementation of user demographic labeling with machine-learning, includes:

    a. using web spider to get the training data for the classification algorithms.  
    b. collect particular words dictionary for chinese word segmentation.  
    c. using machine-learning algorithms provided by sklearn(a ML toolbox written in Python) for document classification.
  
#####High performance WEB application module
Worked as major developer, includes:

* Research and choose the main framework(OpenResty), web application development(with Lua script).

* Refactoring cookie mapping server with OpenResty, the server now can handle 20K+ QPS in a quad-core PC.

* Implementation of DMP real-time label query interface under the framework.

#####Distribute web spider(crawling URL's content for demographic label analysis)  
Worked as major developer, includes:

* Design and build a multi-processing web spider for URL content extraction(First in Java and refactored to Python later, data stored in HDFS).

* Processing 2 million URLs in 24 hours on a normal quad-core PC with 50Mbit bandwidth.

* Text data crawled used to build the text classification model, which helped us lots on demographic labeling system.

2009.7 - 2012.10: **Java Software Engineer @Datang mobile communication equipment Co. LTD.**

#####HSS(Home Subscriber Server) development for LTE(4G) network  
Worked as major developer in the team(then team leader at early 2012), includes:

* Design and implementation of HSS database web console (under Struts, Spring and Hibernate framework, running on CentOS 5.9). The database(with millions telecom users data stored in) based on Oracle 9i relied on this web console to do all data configuration work.

* Maintenance and refactoring of HSS diameter protocol stack (inner-network communication function, implemented in Java). For example, The stack is based on TCP protocol at the beginning, then I refactored it to SCTP protocol based.

* Customize development of HSS according to requirements of particular industry and enterprises.

* Development and maintenance of the CG (Charging-Gateway) system, which used to do chargings in the LTE network.
 
----
##Education	
2006 - 2009  
M.S in Communication and Information System @[Xi’an Jiaotong University](http://en.xjtu.edu.cn/ "Xi’an Jiaotong University")

2002 - 2006  
B.S. in Information Engineering @[Jinan University](http://welcome.jnu.edu.cn/en2014/ "Jinan University")
