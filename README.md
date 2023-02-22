# cc4DEtest
*CC4 Data Engineer Internship Tech Test*

## Table of Contents
* [How To Use](#how-to-use)
* [Summmary](#summary)
* [Architecture Diagram](#architecture-diagram)

## How To Use
1) Install the dependencies in your virtual environment with the required libraries.
```
pip install -r requirements.txt
```

2) Ensure that **_restaurants.json_** and **_Country-Code.csv_** has been downloaded to the same folder.

3) Run the python file to extract the required restaurant data. Outputs will be in the following files: **_restaurants.csv_** and **_restaurant_events.csv_**. Code will also return the threshold for each of the required ratings in the console.

```
python cc4.py
```

## Summary
**Data ingestion:** We can use MongoDB to store the JSON files containing restaurant data received from the client. As the input files given were in the form of JSON files, I chose to store the data in MongoDB as it is a document-based NoSQL database that is well-suited for storing JSON data. MongoDB allows users to store and query JSON documents natively, without having to convert them to another format like XML or CSV. This allows for efficient and flexible storage of the JSON data, as MongoDB supports dynamic schema and can handle unstructured data. 

Additionally, MongoDB's scalability features, such as sharding and replica sets, can help handle large volumes of data and ensure high availability. Furthermore, when performing analysis later on such as filtering restaurants with good user ratings and interesting past events, it can be done efficiently using MongoDB's query capabilities, without having to load all the data into memory.

**Data processing:** We can set up a Lambda function that runs on a daily basis to check for new JSON files. Upon detection, the function invokes an endpoint on the EC2 instance hosting the MongoDB. This triggers a Python script on the EC2 instance to extract and clean the data. This script can be scheduled to run daily using a cron job.

The script applies the requirements in the problem statement to filter out restaurants with good user ratings and interesting past events, with two assumptions made. Firstly, restaurants with good user ratings are defined as having excellent or very good ratings with a user aggregate rating of 4.0 or more and a minimum of 50 user rating votes to ensure credibility. Secondly, interesting past events are those with high or low sentiment scores analyzed through the use of sentiment prediction on event descriptions with NLP models. 

For example, we can use BERT (Bidirectional Encoder Representations from Transformers) to predict the sentiment of a given text. BERT is a transformer-based model that uses attention mechanisms to encode the context of the input text. It is trained on large amounts of text data and can be fine-tuned for specific NLP tasks, including sentiment analysis. The script will generate two CSV files: 'restaurants.csv' and 'restaurant_events.csv'.

**Data storage:** We can use Amazon S3 to store the generated CSV files. The S3 bucket can be set up to provide read access to the website hosting Steven's travel food series.

**Website deployment:** We can deploy the website on Amazon EC2 instances, which can be configured to automatically pull the data from the S3 bucket and display it to the end-users. The website can be developed using a web framework like Django or Flask, and can be deployed using a containerization tool like Docker or Kubernetes.


## Architecture Diagram
![architecture-Reduced architecture (1)](https://user-images.githubusercontent.com/102446759/220672132-dab50c8d-c2d5-4676-abae-04272f8c3fb7.jpg)
