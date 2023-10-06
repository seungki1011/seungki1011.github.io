---
# layout: post
# title:  "(Introduction to Data Engineering - 5) Overview of the Data Repositories"
# author: seungki
# categories: [ Data Engineering ]
# tags: [Coursera, DBMS]
# image: post_images/ibm_coursera.png
# toc: True

---

---

해당 포스트는 코세라의 IBM Data Engineering 코스를 한글로 다시 정리한 내용입니다.

---

## Understanding Data Repositories : DB, Data Warehouse, BigData Repository

### 데이터 저장소의 이해 

데이터 저장소는 비즈니스 운영, 보고 및 데이터 분석에 사용되는 체계적이고 격리된 데이터 집합을 의미한다. 보통 하나 이상의 데이터베이스로 구성되며 크기와 구조가 다양할 수 있다. 다음은 데이터베이스, 데이터 웨어하우스, 빅데이터 저장소 등 다양한 데이터 저장소 유형들의 소개이다.

#### 1. 데이터베이스(Database)

* 데이터 입력, 저장, 검색 및 수정을 위해 설계
* DBMS에 의해 관리(데이터베이스와 DBMS는 사전 의미상 다른 것을 의미하지만, 실제로는 상호교환적으로 쓰이는 경우가 많다)
* 쿼리를 사용해서 데이터 추출 및 수정이 가능하다
* 범주에는 관계형(Relational, RDBMS) 그리고 비관계형(Non-relational, NoSQL) 데이터베이스가 존재한다
  * 관계형 데이터베이스(RDBMS)는 잘 정의된 스키마를 사용해서 데이블 형식 구조(Tabular format)로 데이터를 구성하고 쿼리에 SQL을 사용한다
  * 비관계형 데이터베이스(NoSQL)에는 스키마가 느슨하거나 없는 형태로 데이터를 저장할 수 있으며 속도, 유연성 그리고 확장성이 필요하다

<img src="../post_images/2023-08-11-data_engineer_ibm_5/nonrelation vs relation.png" alt="nonrelation vs relation" style="zoom: 50%;" class='center-image'/>

<p align='center'>출처 - https://www.mparticle.com/blog/relational-vs-nonrelational-databases/</p>

#### 2. 데이터 웨어하우스(Data Warehouse)

* 다양한 소스의 데이터를 저장하는 중앙 저장소 같은 느낌
* ETL 프로세스는 분석 및 BI를 위해 데이터를 추출, 변환하고 하나의 포괄적인 데이터베이스로 로드한다
* 기존 데이터 웨어하우스는 관계형인 경우가 많았지만 비관계형 데이터 저장소가 많아지는 추세
* 데이터 웨어하우스와 관련된 내용으로 데이터 레이크(Data Lake)와 데이터 마트(Data Mart)가 있다

#### 3. 빅데이터 스토어(Bigdata Store)

* 분산된 컴퓨팅 및 스토리지 인프라를 사용한다
* 대규모 데이터 세트 저장, 확장 및 처리
* 클라우드 컴퓨팅, IoT, 소멸 미디어 등에서 생성되는 빅데이터를 관리하는데 필수적이다







---

## Further Reading

* [RDBMS vs NoSQL Database](https://www.mongodb.com/compare/relational-vs-non-relational-databases)



## 참고

---

1. [Coursera - IBM Introduction to Data Engineering](https://www.coursera.org/learn/introduction-to-data-engineering)
1. [https://towardsdatascience.com/relational-vs-non-relational-databases-f2ac792482e3](https://towardsdatascience.com/relational-vs-non-relational-databases-f2ac792482e3)
1. [https://www.mparticle.com/blog/relational-vs-nonrelational-databases/](https://www.mparticle.com/blog/relational-vs-nonrelational-databases/)
