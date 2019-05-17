# EDIT WINDOW

***A window into Wikipedia editing behavior***

I completed this project in 3 weeks as a fellow at Insight Data Engineering in NYC, January 2019.

***

Wikipedia's credibility depends on the edits behind its articles being transparent. But on their website, it's hard to compare edits beyond the scope of one user's or one page's revisions.

My product is an analytics page for analyzing site-wide user behavior. I analyze 500GB of Wikipedia pages in zipped XML format, process them in Spark, and store in TimescaleDB. On my [website](editwindow.wiki) [now decomissioned due to cost], there is a panel of pre-selected top stats, and clicking them allows users to dig deeper into different metrics. Each page request queries the entire 500GB database. Instead of a live website, as of Mar 12, 2019, you can find a video demo of my website [here](https://www.youtube.com/watch?v=L_mPeOaQdbA&feature=youtu.be).

Some interesting things to look at might be:
- How does the number of revisions change during events such as national holidays?
- How do bots compare to real users in terms of edit volume?
- Do users tend to make edits at a steady rate or do they have periods of heavy activity?
 

***

# Pipeline
-----------------
S3 -> Spark -> TimescaleDB (Postgres) -> Dash 
![alt text](https://github.com/thecolorkeo/InsightWiki/blob/dev/Pipeline.png "EditWindow Pipeline")

EditWindow is a batch processing pipeline built to handle fast queries over a large volume of data.

I downloaded revision history from all pages on the English version of Wikipedia to an S3 bucket, which were in the form of zipped XMLs. I used Spark (Databricks Spark XML package) to parse these xmls into a dataframe. I wrote these files out to TimescaleDB, and created an interactive website with Plotly Dash and Flask. I used Airflow to automate downloading and parsing the Wikipedia files from S3.

| Directory                    | Description of Contents
|:---------------------------- |:---------------------------------------- |
| `airflow/sparkflow.py`       | Runs spark job for every partition in S3 |
| `dashapp/*`                  | HTML and CSS that queries DB and builds the UI |
| `spark/databricks-history.py`| Reads from S3, unzips, parses, and writes into TimescaleDB   |
| `spark-up-history.sh`        | Shell script to run spark job            |
| `test`                       | Unit test for NYC's wikipedia page       |

Data Source: https://dumps.wikimedia.org/enwiki/latest/

To access the latest versions of all Wikipedia pages including all revisions, go to this page and download files with the prefix "enwiki-latest-pages-meta-history"[1-27]. Wikipedia publishes the full site in 27 parts. Wikipedia offers other options for accessing their data, see a full description [here](https://en.wikipedia.org/wiki/Wikipedia:Database_download)

### Cluster set up
- (4) m4.2xlarge EC2 nodes with Spark and Hadoop set up
- (1) r4.4xlarge EC2 node for TimescaleDB and Flask, needs at least 600GB of storage volume

### Environment
Install AWS CLI and [Pegasus](https://github.com/InsightDataScience/pegasus), which is Insight's automatic cluster creator. Set the configuration in workers.yml and master.yml (3 workers and 1 master), then use Pegasus commands to spin up the cluster and install Hadoop and Spark. Clone the databricks [XML parsing package](https://github.com/databricks/spark-xml) and follow the setup instructions that they provide. Follow the [instructions on Timescale's website](https://blog.timescale.com/tutorial-installing-timescaledb-on-aws-c8602b767a98/) for how to install Timescale on an EC2 instance on top of Postgres 10.

| Technology     | Version No.
|:-------------- |:----------- |
| Hadoop       | v2.7.6 |
| Spark | v2.7.6 |
| Databricks XML Parser | v0.4.1 |
| Postgres (TimescaleDB) | v10.6 |

### Getting Started
Start Spark and Hadoop on your EC2 cluster.
```
    peg service <cluster-name> hadoop start
    peg service <cluster-name> spark start
```

Download the 27 files off wikipedia's website into an S3 bucket with the name format `"history<#>.xml.<__>.bz2"` and replace # with the respective number between 1 and 27.
 ```
    curl <wikidump link> <s3 bucket loc> ...
 ```

Create a [hypertable](https://docs.timescale.com/v1.0/getting-started/creating-hypertables) in TimescaleDB called `revs`. Then, run `spark-up-history.sh <#>` to populate revs with each of the files in S3.

```
   SELECT create_hypertable('revs', 'time');
```

Run Dashapp on port 80
```
    sudo python app.py
```

The website should be running then! Congrats!

### Testing
Wikipedia offers the option to [download individual pages](https://en.wikipedia.org/wiki/Special:Export) in xml format. The folder `test/` contains a unit test for the Wiki page for New York City.
