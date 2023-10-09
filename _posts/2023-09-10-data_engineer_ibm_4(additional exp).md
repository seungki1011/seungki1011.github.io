---
layout: post
title:  "OLTP/OLAP, ACID, Metadata"
author: seungki
categories: [ Data Engineering ]
tags: [Terminology, ACID]
image: post_images/data-eng-sdxl.png
toc: True
featured: True

---
---
해당 포스트는 이전 포스트에서 정리한 내용에 대한 추가 설명 및 용어 정리입니다.

---

## OLTP & OLAP

### OLTP(Online Transaction Processing)

OLTP 일상적인 우영 데이터와 트랜잭션을  실시간으로 관리하고 처리하도록 설계된 데이터베이스 시스템이다. 주로 짧고 빈번한 간단한 트랜잭션이 많이 포함되는 작업에 사용된다. OLTP 시스템은 일반적으로 다음과 같은 특징을 가지고 있다.

1. ACID 준수
2. 높은 트랜잭션 볼륨(High Transaction Volume)
   * 판매 주문, 재고 업데이트, 금융 거래 등 엄청난 양의 트랜잭션을 처리해야함
   * 이런 트랜잭션들은 일반적으로 크기가 작으며 업데이트, 삽입 및 삭제가 포함 됨
3. 낮은 지연 시간(Low Latency)
   * OLTP 시스템은 낮은 지연 시간(대기 시간)과 빠른 응답 시간에 최적화 되어있어야 함
   * 유저는 OLTP 데이터베이스를 이용하는 애플리케이션과 상호작용 할 때 즉각적인 피드백을 기대함
4. 정규화된 데이터 구조(Normalized Data Structure)
   * 데이터의 중복성을 줄이고 데이터 무결성을 보장하기 위해 고도로 정규화된 형식으로 구성
   * 이는 효율적인 데이터 업데이트 및 일관성에 적합함
5. 동시 액세스(Concurrent Access)
   * Data locking과 같은 기술을 통해 데이터 일관성과 무결성을 유지하면서 동시에 데이터에 액세스하고 수정하는 여러 동시 사용자 또는 애플리케이션을 지원한다
6. Example
   * POS(Point-of-Sale) 시스템
   * 온라인 뱅킹
   * 항공 예약 시스템
   * CRM(고객 관계 관리) 시스템

#### 오라클에서 정의하는 OLTP

> OLTP(온라인 트랜잭션 처리)는 온라인 뱅킹, 쇼핑, 주문 입력 또는 텍스트 메시지 전송 등 동시에 발생하는 다수의 트랜잭션을 실행하는 데이터 처리 유형입니다. 이러한 트랜잭션은 전통적으로 경제 또는 재무 트랜잭션이라고 칭하며, 기업이 회계 또는 보고 목적으로 언제든 정보에 액세스할 수 있도록 기록 및 보호됩니다.
>
> 트랜잭션의 주요 정의(경제 또는 재무)는 여전히 대부분의 OLTP 시스템의 근간으로 남아있습니다. 그래서 온라인 트랜잭션 처리는 보통 데이터 스토어 내의 소규모 데이터 삽입, 업데이트 및/또는 삭제를 통해 해당 트랜잭션을 수집, 관리 및 보호하는 작업을 포함합니다. 일반적으로 웹, 모바일 또는 기업 애플리케이션은 고객, 공급업체 또는 파트너와의 모든 상호 작용 또는 거래를 추적하고, 이를 OLTP 데이터베이스에 업데이트합니다. 데이터베이스에 저장된 이 트랜잭션 데이터는 기업에 핵심적이며, 보고서 작성용으로 사용되고, 데이터 중심의 의사결정에 활용하기 위해 분석됩니다.

### OLAP(Online Analytical Processing)

OLAP는 복잡한 쿼리 및 데이터 분석 작업을 위해 설계된 데이터베이스 시스템이다. OLAP 시스템은 데이터로부터 인사이트를 추출하고 과거 데이터에 대한 다차원 분석을 수행하는데 사용된다. OLAP 시스템은 일반적으로 다음과 같은 특징을 가지고 있다.

1. 복잡한 쿼리(Complex Queries)
   * 집계, 필터링, 그룹화 및 계산을 포함하는 복잡한 분석 쿼리에 최적화 되어야 함
   * 이런 쿼리를 통해서 데이터로 부터 인사이트를 추출하고, BI의 활동을 지원한다
2. 기록 데이터(Historical Data)
   * 과거의 기록 데이터까지 모두 저장하기 때문에 다양한 기간에 걸쳐 어떤 추세를 분석하고 예측하고 비교할 수 있음
3. 비정규화된 데이터 구조(Denormalized Data Structure)
   * 쿼리 성능을 최적화하기 위해서 데이터 큐브 또는 스타 스키마를 포함한 비정규화된 데이터 구조를 사용하는 경우가 많음
   * 이런 구조는 데이터 검색 및 집계를 단순화 시킴
4. 읽기 집약적(Read Intensive)
   * OLAP 시스템은 보고 및 분석 목적으로 사용되는 경우가 많고, 쓰기 작업은 거의 일어나지 않는다
5. Example
   * Data Warehouse
   * BI Tools
   * Reporting System

#### AWS에서 정의하는 OLAP

>온라인 분석 처리(OLAP)는 다양한 관점에서 비즈니스 데이터를 분석하는 데 사용할 수 있는 소프트웨어 기술입니다. 조직은 웹 사이트, 애플리케이션, 스마트 미터 및 내부 시스템과 같은 여러 데이터 소스에서 데이터를 수집하고 저장합니다. OLAP는 이 데이터를 범주로 결합하고 그룹화하여 전략 계획을 위한 실행 가능한 통찰력을 제공합니다. 예를 들어 소매업체는 색상, 크기, 비용, 위치 등 판매하는 모든 제품에 대한 데이터를 저장합니다. 소매업체는 또한 다른 시스템에서 주문한 품목의 이름 및 총 판매액과 같은 고객 구매 데이터를 수집합니다. OLAP는 데이터 세트를 결합하여 어떤 색상 제품이 더 인기가 있는지 또는 제품 배치가 판매에 미치는 영향과 같은 질문에 답합니다.

### 오라클에서 말하는 OLTP vs OLAP

> OLTP가 온라인 데이터 수정 시스템이라면 OLAP는 분석을 목적으로 대량의 데이터를 검색하는 데 사용되는 다차원 온라인 기록 데이터 저장소 시스템입니다. OLAP는 일반적으로 하나 이상의 OLTP 시스템에서 수집한 데이터에 대한 분석을 제공합니다.

<img src="../post_images/2023-08-10-data_engineer_ibm_4(additional exp)/Difference-between-OLAP-and-OLTP-in-DBMS-2.webp" alt="Difference-between-OLAP-and-OLTP-in-DBMS-2" style="zoom:100%;" class='center-image'/>

<p align='center'>출처 - https://www.geeksforgeeks.org/difference-between-olap-and-oltp-in-dbms/</p>

---

## Transaction & ACID

### Transaction(트랜잭션)

위의 OLTP에서 언급한 트랜잭션(Transaction)과 ACID는 정확히 무엇일까? 일단 트랜잭션이 무엇인지 알아보자. 다음은 오라클 공식문서에서 정의하는 트랜잭션이다.

> A **transaction** is a logical, atomic unit of work that contains one or more SQL statements.
>
> A transaction groups SQL statements so that they are either all committed, which means they are applied to the database, or all rolled back, which means they are undone from the database

트랜잭션은 하나 이상의 SQL 문을 포함하는 논리적이고 원자적인 작업 단위라고 한다. 그냥 간단하게 데이터베이스의 상태를 변화시키는 하나의 작업단위로 보며 된다. 트랜잭션은 SQL문을 모두 커밋(데이터베이스에 적용)하거나 모두 롤백(데이터베이스의 적용에 대한 실행 취소)하도록 그룹화한다. 여기서 **ACID**라는 것이 등장한다. ACID는 데이터베이스 트랜잭션의 기본 속성이라고 이해하면 된다. 

### ACID 

ACID가 나타내는 것은 다음과 같다.

1. 원자성(Atomicity)
   * 트랜잭션은 기본적으로 모든 작업이 수행되거나 아무것도 수행되지 않는 All-or-Nothing을 따른다(한 마디로 중간 상태라는 것이 존재하지 않는다)
   * 예를 들자면 100개의 레코드를 업데이트하는 작업 중에 20개만 업데이트가 되고 실패하는 경우, 모든 변경사항을 롤백한다
2. 일곤성(Consistency)
   * 트랜잭션은 데이터베이스를 하나의 일과된 상태에서 다른 일관된 상태로 전환한다
   * 예를 들어, 저축 계좌에서 인출하고 다른 예금 계좌에 입금하는 은행 거래에서 실패로 인해 데이터베이스가 하나의 계좌에만 입금되어 데이터가 일치하지 않게 되면 안된다
3. 격리(Isolation)
   * 트랜잭션의 효과는 트랜잭션이 커밋될 때까지 다른 트랜잭션에 표기되어선 안됨
   * 예를 들어, 온라인 거래에서 재고 물품이나 계좌 잔액에 대한 테이블을 업데이트하는 과정에서 입금이나 재고 차감에 대한 내용을 다른데서 확인이 가능하면 안됨. 
4. 지속성(Durability)
   * 커밋된 트랜잭션으로 인한 변경 사항은 영구적이다
   * 트랜잭션이 완료된 후 데이터베이스는 복구 메커니즘을 통해 트랜잭션의 변경 사항이 손실되지 않도록 한다

---

## Metadata

### 메타데이터란?

메타데이터는 다른 데이터에 대한 정보를 제공하는 데이터를 의미한다. 데이터베이스, 데이터 웨어하우징 및 데이터 저장소의 맥락에서 메타데이터는 여러가지 유형으로 구분 할 수 있다.

1. 기술 메타데이터(Technical Metadata)
   * 데이터의 구조나 기술적인 측면을 중점에 둔다
   * 데이터 웨하우스에 존재하는 기술 메타데이터는 다음과 같은 요소를 포함 할 수 있다
     * 테이블의 이름이나 행, 열에 대한 정보를 기록하는 테이블
     * 데이터 웨어하우스에 존재하는 데이터베이스의 이름을 기록하거나, 각 열이 가지는 데이터 타입을 기록한 데이터 카탈로그(Data Catalog)
   * 시스템 카탈로그 같은 데이터베이스의 특수 테이블에 저장되는 경우가 많다
2. Operational Metadata
   * 시스템의 프로세스를 설명한다
   * 작업의 시작 및 종료 시간, 디스크 사용량, 데이터 이동 및 사용자의 액세스 추적
   * 문제 해결 및 워크플로우 최적화에 유용하다
3. Business Metadata
   * 사용자의 데이터 검색 및 해석을 돕는다
   * 데이터 획득, 데이터간 또는 데이터와 소스간 연결에 대한 정보
   * 데이터 웨어하우스 시스템에 대한 문서 역할을 할 수 있다
4. Metadata Management Tools
   * IBM Infosphere Information Server
   * Oracle Warehouse Builder
   * SAS Data Integration Server
   * 다양한 툴들이 존재한다

메타 데이터에 대한 내용을 찾아보면 메타데이터의 subset에 해당되는 것들이 굉장히 많다. 특히 데이터 웨어하우스의 범위에서 벗어나서 메타데이터에 대한 설명을 찾아보면 메타 데이터에 대한 용어들이 통일 되지 않았다는 느낌을 강하게 받았다. 한번 자료조사를 통해서 정리해보는 것도 나쁘지 않을 것 같다. **Data Warehouse에서의 메타데이터라는 키워드로 검색해보고, 유형을 찾아볼 것**

* [한국어 나무위키 메타데이터 설명](https://namu.wiki/w/%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0)
* [영어 나무위키 메타데이터 설명](https://en.wikipedia.org/wiki/Metadata)
* [https://www.tutorialspoint.com/dwh/dwh_metadata_concepts.htm](https://www.tutorialspoint.com/dwh/dwh_metadata_concepts.htm)



## 참고

---

1. [Coursera - IBM Introduction to Data Engineering](https://www.coursera.org/learn/introduction-to-data-engineering)
1. [https://www.oracle.com/kr/database/what-is-oltp/](https://www.oracle.com/kr/database/what-is-oltp/)
1. [https://www.geeksforgeeks.org/difference-between-olap-and-oltp-in-dbms/](https://www.geeksforgeeks.org/difference-between-olap-and-oltp-in-dbms/)
1. [https://docs.oracle.com/en/database/oracle/oracle-database/19/cncpt/transactions.html#](https://docs.oracle.com/en/database/oracle/oracle-database/19/cncpt/transactions.html#)
1. [https://www.tutorialspoint.com/dwh/dwh_metadata_concepts.htm](https://www.tutorialspoint.com/dwh/dwh_metadata_concepts.htm)
1. [KOR 나무위키 메타데이터 설명](https://namu.wiki/w/%EB%A9%94%ED%83%80%EB%8D%B0%EC%9D%B4%ED%84%B0)
1. [ENG 나무위키 메타데이터 설명](https://en.wikipedia.org/wiki/Metadata)
