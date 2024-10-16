# Weather Data ETL with Airflow

## 프로젝트 개요
이 프로젝트는 **Airflow**를 이용하여 날씨 데이터를 주기적으로 수집, 변환(ETL), 그리고 PostgreSQL 데이터베이스에 적재하는 파이프라인을 구축하는 실습입니다. **기상청 API**로부터 데이터를 수집하고, 이를 가공하여 데이터베이스에 저장하는 과정을 자동화했습니다.

---

## 프로젝트 구조

### 주요 기능
1. **데이터 수집**: 기상청 API에서 날씨 데이터를 가져옵니다.
2. **데이터 변환**: 온도와 강수량 정보를 추출 및 가공합니다.
3. **데이터 적재**: PostgreSQL 데이터베이스에 데이터를 저장합니다.

---

## 기술 스택
- **Airflow**: 워크플로우 스케줄링 및 파이프라인 관리
- **Python**: 데이터 처리 및 ETL 코드 작성
- **PostgreSQL**: 데이터 저장소
- **Pandas**: 데이터 가공 및 변환
- **Docker** (옵션): Airflow 환경 설정 및 실행
- **기상청 API**: 날씨 데이터 소스

---

## 코드 설명

### `dag.py` 코드 요약
- **`SimpleHttpOperator`**: 기상청 API에서 데이터를 가져옵니다.
- **`PythonOperator`**: 수집된 데이터를 가공하고, 데이터베이스에 저장합니다.
- **`PostgresHook`**: PostgreSQL에 데이터를 적재하기 위한 연결을 수행합니다.
<img width="733" alt="스크린샷 2024-10-16 오후 10 34 14" src="https://github.com/user-attachments/assets/ba8d836b-9995-468a-9fe3-8b8d875e579e">

