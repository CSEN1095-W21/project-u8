
from airflow.operators.python_operator import PythonOperator
from airflow.operators.bash import BashOperator
from airflow import DAG
from textwrap import dedent
from datetime import datetime, timedelta
import time
import csv
from textblob import TextBlob
import http.client
import json
import urllib.parse
from airflow.models.baseoperator import chain


def get_token():
    conn = http.client.HTTPSConnection("api.twitter.com")
    payload = ''
    headers = {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Authorization': 'Basic dFFWNFV2VDVtUndyUFc0MWxvQXN2RHhYVDo3dEdEaERUZDdiNmNCMW5STURvektKeEphUGdhVlViRk83azZqSWNiQ29Sb3pzbzFUZQ=="',
        'Cookie': 'guest_id=v1%3A164082175190104227; guest_id_ads=v1%3A164082175190104227; guest_id_marketing=v1%3A164082175190104227; personalization_id="v1_A6J9tFHGXiGbx8iw9nEknQ=="'
    }
    conn.request(
        "POST", "/oauth2/token?grant_type=client_credentials", payload, headers)
    res = conn.getresponse()
    data = res.read()
    token = json.loads(data.decode("utf-8"))["access_token"]
    return token


def getTweet(query):
    conn = http.client.HTTPSConnection("api.twitter.com")
    payload = ''
    headers = {
        'Authorization': "Bearer "+get_token()
    }
    conn.request(
        "GET", f"/2/tweets/search/recent?query={query}&tweet.fields=text&user.fields=description,created_at&max_results=20", payload, headers)
    res = conn.getresponse()
    data = res.read()
    print(data.decode("utf-8"))
    return json.loads(data.decode("utf-8"))["data"]


# Python program to get average of a list
def Average(lst):
    return sum(lst) / len(lst)


def sentiment_analysis(tweets):
    result = []
    sentiment_list = []
    for tweet in tweets:
        analysis = TextBlob(tweet["text"])
        sentiment = map_sentiment(analysis.sentiment[0])
        sentiment_list.append(analysis.sentiment[0])
        result.append([tweet["text"], sentiment, analysis.sentiment[0]])
    avg = Average(sentiment_list)
    return {"data": result, "average": [map_sentiment(avg), avg]}


def map_sentiment(sentiment):
    if sentiment > 0:
        return "Positive"
    elif sentiment < 0:
        return 'Negative'
    else:
        return 'Neutral'


def getChinaTweets(**kwargs):
    ti = kwargs['ti']
    first_country = "China"
    first_country_tweets = getTweet(
        urllib.parse.quote(first_country+" #olympics2021"))
    ti.xcom_push('first_country_tweets', first_country_tweets)


def getIndiaTweets(**kwargs):
    ti = kwargs['ti']
    second_country = "India"
    second_country_tweets = getTweet(
        urllib.parse.quote(second_country+" #olympics2021"))
    ti.xcom_push('second_country_tweets', second_country_tweets)


def getChinaTweetsSentiment(**kwargs):
    ti = kwargs['ti']
    first_country_tweets = ti.xcom_pull(
        task_ids='getChinaTweets', key='first_country_tweets')
    first_country_sentiment_data = sentiment_analysis(first_country_tweets)
    ti.xcom_push('first_country_sentiment_data', first_country_sentiment_data)


def getIndiaTweetsSentiment(**kwargs):
    ti = kwargs['ti']
    second_country_tweets = ti.xcom_pull(
        task_ids='getIndiaTweets', key='second_country_tweets')
    second_country_sentiment_data = sentiment_analysis(second_country_tweets)
    ti.xcom_push('second_country_sentiment_data',
                 second_country_sentiment_data)


# using time module


def save_csv(**kwargs):
    ti = kwargs['ti']
    first_country = "China"
    second_country = "India"

    first_country_sentiment_data = ti.xcom_pull(
        task_ids='getChinaTweetsSentiment', key='first_country_sentiment_data')

    second_country_sentiment_data = ti.xcom_pull(
        task_ids='getIndiaTweetsSentiment', key='second_country_sentiment_data')

    print(second_country_sentiment_data)
    print(first_country_sentiment_data)
    data_file_headers = ["Text", "Sentiment", "Value"]
    average_file_headers = ["Country", "Sentiment", "Value"]

    time_stamp = time.time()

    with open(f"{first_country}_data_{time_stamp}.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(data_file_headers)

        # write multiple rows
        writer.writerows(first_country_sentiment_data["data"])

    with open(f"{second_country}_data_{time_stamp}.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(average_file_headers)

        # write multiple rows
        writer.writerows(second_country_sentiment_data["data"])

    with open(f"average_{time_stamp}.csv", "w", encoding="UTF8", newline="") as f:
        writer = csv.writer(f)

        # write the header
        writer.writerow(data_file_headers)
        # write multiple rows
        first_output = [first_country] + \
            first_country_sentiment_data["average"]
        second_output = [second_country] + \
            second_country_sentiment_data["average"]
        writer.writerows([first_output, second_output])


def compare_performance(**kwargs):
    ti = kwargs['ti']

    first_country_sentiment_data = ti.xcom_pull(
        task_ids='getChinaTweetsSentiment', key='first_country_sentiment_data')

    second_country_sentiment_data = ti.xcom_pull(
        task_ids='getIndiaTweetsSentiment', key='second_country_sentiment_data')

    print("China was one of the best performing countries in Tokyo's olypmics 2021, but India performed poorly, so let's compare the average sentiment analysis for both countries' tweets.")
    print("Hypothesis: China will have positive tweets about the Olympics, whereas India will have negative tweets.")
    print("The average sentiment of the 20 tweets in China is:",
          first_country_sentiment_data["average"][1], "which means the sentiment is Positve")
    print("The average sentiment of the 20 tweets in India is:",
          second_country_sentiment_data["average"][1], "which means the sentiment is Negative")
    print("Therefore we can conclude that the hypothesis is TRUE")


# ## Pipeline

# The DAG object; we'll need this to instantiate a DAG
# Operators; we need this to operate!
# These args will get passed on to each operator
# You can override them on a per-task basis during operator initialization
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    # 'queue': 'bash_queue',
    # 'pool': 'backfill',
    # 'priority_weight': 10,
    # 'end_date': datetime(2016, 1, 1),
    # 'wait_for_downstream': False,
    # 'dag': dag,
    # 'sla': timedelta(hours=2),
    # 'execution_timeout': timedelta(seconds=300),
    # 'on_failure_callback': some_function,
    # 'on_success_callback': some_other_function,
    # 'on_retry_callback': another_function,
    # 'sla_miss_callback': yet_another_function,
    # 'trigger_rule': 'all_success'
}
with DAG(
    'tweeets',
    default_args=default_args,
    description='A simple tutorial DAG',
    start_date=datetime.now(),
    end_date="2022-02-01",
    schedule_interval="@daily",
    catchup=False,
    tags=['example'],
) as dag:

    t1 = PythonOperator(
        task_id='getChinaTweets',
        provide_context=True,
        python_callable=getChinaTweets,
        dag=dag)

    t2 = PythonOperator(
        task_id='getIndiaTweets',
        provide_context=True,
        python_callable=getIndiaTweets,
        dag=dag)

    t3 = PythonOperator(
        task_id='getChinaTweetsSentiment',
        provide_context=True,
        python_callable=getChinaTweetsSentiment,
        dag=dag)

    t4 = PythonOperator(
        task_id='getIndiaTweetsSentiment',
        provide_context=True,
        python_callable=getIndiaTweetsSentiment,
        dag=dag)

    t5 = PythonOperator(
        task_id='save_csv',
        provide_context=True,
        python_callable=save_csv,
        dag=dag)

    t6 = PythonOperator(
        task_id='compare_performance',
        provide_context=True,
        python_callable=compare_performance,
        dag=dag)

    t1 >> t3
    t2 >> t4
    [t3, t4] >> t5
    [t3, t4] >> t6
