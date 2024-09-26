from datetime import datetime
from airflow.operators.python import PythonOperator
from airflow.providers.http.operators.http import SimpleHttpOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow import DAG

import json
from pandas import json_normalize

from airflow.models import Variable

def _extract_data(date, **context):
    res = context['ti'].xcom_pull(task_ids='get_op')  # context['ti']는 현재 실행 중인 태스크 인스턴스에 대한 객체

    temperature = res["response"]["body"]["items"]["item"][24]["fcstValue"]
    rain = res["response"]["body"]["items"]["item"][12]["fcstValue"]
    store_rain = ''
    if rain != "강수없음":
        rain = float(rain)
        if rain < 1.0:
            store_rain += "1.0mm 미만"
        elif 1.0 <= rain < 30.0:
            store_rain += "1.0~29.0mm"
        elif 30.0 <= rain < 50.0:
            store_rain += "30.0~50.0mm"
        else:
            store_rain += "50.0mm 이상"
    else:
        store_rain += "강수없음"

    today_weather = json_normalize({
        "weather_date": date,
        "temperature": temperature,
        "precipitation": store_rain
    })

    context["ti"].xcom_push(
        key="weather_data",
        value=today_weather)

def _store_weather(ti):
    weather_data = ti.xcom_pull(
        key="weather_data",
        task_ids="extract_data_op")

    # date = weather_data.get('date')
    # temperature = weather_data.get('temperature')
    # precipitation = weather_data.get('precipitation')

    date = weather_data['weather_date'].values[0]
    temperature = weather_data['temperature'].values[0]
    precipitation = weather_data['precipitation'].values[0]

    hook = PostgresHook(
        postgres_conn_id='my_postgres_connection'
    )

    insert_query = """
            INSERT INTO weather_data (weather_date, temperature, precipitation)
            VALUES (%s, %s, %s)
        """

    hook.run(insert_query, parameters=(date, temperature, precipitation))

with DAG(
    dag_id="weather_dag",
    description="@daily",
    schedule_interval='0 0 * * *',
    start_date=datetime(2024,9,1),
    catchup=False) as dag:

    base_date = datetime.now().strftime("%Y%m%d")  # 발표 일자
    serviceKey = Variable.get("serviceKey")


    task_get_op = SimpleHttpOperator(
        task_id='get_op',
        http_conn_id='my_http_connection',
        method='GET',
        endpoint=f"/getUltraSrtFcst?serviceKey={serviceKey}&numOfRows=60&pageNo=1&dataType=json&base_date=20240926&base_time=0830&nx=101&ny=84",
        response_filter=lambda response: json.loads(response.text),
        log_response=True
    )

    task_extract_data_op = PythonOperator(
        task_id='extract_data_op',
        python_callable=_extract_data,
        op_args=[base_date]
    )

    task_store_op = PythonOperator(
        task_id='store_op',
        python_callable=_store_weather
    )

task_get_op >> task_extract_data_op >> task_store_op