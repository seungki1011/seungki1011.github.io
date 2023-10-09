---
layout: post
title:  "(Introduction to Data Engineering - 8) Architecting Data Platforms"
author: seungki
categories: [ Data Engineering ]
tags: [Coursera]
image: post_images/coursera_ibm.png
toc: True

---
---
해당 포스트는 코세라의 IBM Data Engineering 코스를 한글로 다시 정리한 내용입니다.

---

## Data Platform Architecture

### 데이터 플랫폼의 아키텍쳐

데이터 플랫폼 아키텍쳐의 계층에 대해 알아보자. 각 계층은 데이터 플랫폼에서 특정 작업을 수행하는 기능의 구성 요소들을 나타낸다. 우리가 살펴볼 계층에는 데이터 수집 계층, 데이터 저장 및 통합 계층, 데이터 처리 계층, 데이터 분석 및 인터페이스 계층이 있다. 마지막으로 데이터 파이프라인 계층은 여러가지 계층을 덮는 계층이다.

---

#### Data Collection, Ingestion Layer (데이터 수집 계층)

* 데이터 소스 시스템에 연결하고 데이터를 데이터 플랫폼으로 가져오는 역할
* 데이터 소스에 연결 > 스트리밍 또는 배치로 데이터를 데이터 플랫폼으로 전송 > 메타데이터 저장소에 수집된 데이터에 대한 정보를 유지 관리
  * 관리하는 메타 데이터는 배치로 처리된 수집 데이터의 양, 데이터 소스 그리고 기타 설명 정보
* Google Cloud DataFlow, IBM Streams, Amazon Kinesis, Apache Kafka 등이 데이터 수집에 사용된다

---

#### Data Storage and Integration Layer (데이터 저장 및 통합 계층)

* 데이터 수집후 저장 및 통합을 담당하는 계층
* 데이터의 처리 및 장기간 사용을 위해 저장한다
* 추출된 데이터를 논리적으로나 물리적으로 변환하고 병합한다
* 데이터를 스트리밍 처리나 배치 처리 모두에서 처리가 가능하도록 만든다
* 스토리지 계층은 안정적이고 확장 가능하며 고성능이면서 비용 효율적이어야 한다
* IBM DB2, Microsoft SQL server, MySQL, Oracle Database, PostgreSQL 등이 인기 있는 관계형 데이터베이스들이다
  * Google Cloud SQL, SQL Azure, Amazon RDS 등과 같은 클라우드 기반 데이터베이스(Database-as-a-Service)들이 최근 급부상하고 있다
* NoSQL 데이터베이스에는 MongoDB, Cassandra, Neo4J, Redis 등이 있다
* IBM Cloud Pak, Talend Data Fabric 등과 같은 데이터 통합 도구들이 있다
  * 오픈소스 데이터 통합 도구에는 Dell Boomi, SnapLogic 등이 있다
* 클라우드 기반의 데이터 통합 플랫폼(iPaaS)을 제공해주는 벤더들도 몇 곳 존재한다.
  * 예시로는 Adeptia Integration Suite, Google Cloud's Cooperation 534, IBM's Application Integration Suite on Cloud, Informatica's Integration Cloud

---

#### Data Processing Layer (데이터 처리 계층)

* 데이터가 수집, 저장 및 통합 후에 처리가 필요하다
* 데이터의 유효성 검사(data validation), 변환 및 비즈니스 논리 적용은 이 계층에서 수행되는 작업의 일부이다
* 처리 계층은 다음을 수행할 수 있어야 한다
  * 스토리지에서 배치 또는 스트리밍 모드로 데이터를 읽고 변환을 적용한다
  * 널리 사용되는 쿼리 도구와 프로그래밍 언어를 지원한다
  * 증가하는 데이터 세트의 처리 요구 사항을 충족할 수 있도록 확장이 가능해야한다
  * 데이터 분석가나 과학자가 데이터 플랫폼에서 데이터로 작업할 수 있는 방법을 제공한다
* 계층에서 일어나는 변환 작업 중 일부는 다음과 같다
  * 데이터의 형식과 스키마의 변경(필드 순서를 변경하는 간단한 변환 부터 유니온과 조인을 이용해 복잡한 구조로 결합하는 작업까지 포함한다)
  * 중복성과 불일치를 줄이기 위한 정규화(Normalization)
  * 보고 및 분석을 위해 보다 효율적으로 쿼리할 수 있도록 여러 테이블의 데이터를 단일 테이블로 결합하는 비정규화(Denormalization)
  * 데이터의 불규칙성을 수정하여 다운스트림 애플리케이션 및 사용처에 대해 신뢰할 수 있는 데이터를 제공하는 데이터 클리닝(Data Cleaning)
  * 데이터 변환에 사용하는 도구로는 다음이 있다
    * OpenRefine, Google DataPrep, Watson Studio Refinery, Trifacta Wrangler 등
  * Python이나 R 또한 데이터 처리를 여러 라이브러리와 패키지를 제공한다

데이터의 저장과 처리가 항상 어떤 별도의 계층에서 수행되는 것은 아니다. 예를 들어 관계형 데이터베이스에서는 저장과 처리가 동일한 계층에서 이루어질 수 있지만, 빅데이터 시스템에서는 데이터가 먼저 HDFS에 저장된 다음 Spark와 같은 데이터 처리 엔진에서 처리될 수 있다. 데이터 처리 계층은 데이터가 데이터베이스에 로드되거나 저장되기 전에 변환이 적용되는 경우, 데이터 저장 계층의 앞에 존재할 수도 있다.

---

#### Data Analysis and User Interface Layer(데이터 분석 및 유저 인터페이스 계층)

분석 및 유저 인터페이스 계층은 처리된 데이터를 데이터 소비자에게 전달한다. 데이터 소비자에는 다음이 포함 될 수 있다.

* 대시보드 및 분석 보고서와 같은 시각적 표현을 통해 데이터를 사용하는 BI 분석가 및 비즈니스 이해관계자
* 특정 사용 사례에 대해 이 데이터를 추가로 처리하는 데이터 과학자 및 데이터 분석가
* 데이터 사용해야하는 기타 애플리케이션과 서비스 등

분석 및 UI 계층은 다음을 지원해야 한다.

* 쿼리 도구 및 프로그래밍 언어 지원
  * 예를 들자면 관계형 데이터베이스를 쿼리하기 위한 SQL 언어, 유사 SQL 언어 및 도구
  * Python, Java, R 과 같은 프로그래밍 언어
  * 데이터에 대한 보고서를 받을 수 있는 API
  * 다른 애플리케이션 및 서비스에서 사용하기 위해 스토리지의 데이터를 실시간으로 사용할 수 있는 API

대시보드 및 BI 툴의 예시에는 다음이 있다.

* IBM Cognos Analytics, Tableau, Jupyter Notebooks, Python 및 R 라이브러리, Microsoft Power BI

---

#### Data Pipeline Layer

데이터 파이프라인 계층은 데이터 수집, 저장 및 통합, 처리를 전부 포함하는 계층이라고 할 수 있다. 이전 포스트에도 언급했듯이 ETL또는 ELT 프로세스가 여기에 해당한다. 데이터 파이프라인 계층의 역할을 결국 데이터가 지속적으로 흐르는 데이터 파이프라인을 유지 및 관리하는 것이다.

데이터 파이프라인 솔루션 중에서 널리 사용하는 것에는 

* Apache Airflow
* DataFlow
* 여러가지 솔루션들이 존재한다

**지금까지 살펴본 데이터 플랫폼 계층들은 광범위한 작업을 지원하는 복잡한 아키텍쳐를 단순화 시켜서 설명한 것이다.** 각 요소에 대해 더 깊이 알기 위해서 공부하는 것은 필수적이다.

<img src="../post_images/2023-09-16-data_engineer_ibm_8/dataplatform.png" alt="dataplatform" style="zoom:45%;" class='center-image'/>

<p align='center'>출처 - https://www.coursera.org/learn/introduction-to-data-engineering</p>



## 참고

---

1. [Coursera - IBM Introduction to Data Engineering](https://www.coursera.org/learn/introduction-to-data-engineering)
