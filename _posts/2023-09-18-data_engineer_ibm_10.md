---
layout: post
title:  "(Introduction to Data Engineering - 10) Performance Tuning & Troubleshooting"
author: seungki
categories: [ Data Engineering ]
tags: [Coursera]
image: post_images/coursera_ibm.png
toc: True

---
---
해당 포스트는 코세라의 IBM Data Engineering 코스를 한글로 다시 정리한 내용입니다.

---

## Performance Issues

데이터 엔지니어의 주요 책중 중 하나는 성능과 가용성을 위해 시스템과 데이터 흐름을 모니터링하고 최적화 하는 것이다. 데이터 엔지니어링에서의 성능은 다양한 영역에 해당 될 수 있다. 성능 이슈가 될만한 요소들을 알아보자.

데이터 파이프라인은 다양한 작업을 처리하는 다양한 도구로 구성되어 있다. 데이터 파이프라인의 성능 이슈에 해당하는 것들에 다음이 포함된다.

* 증가하는 데이터 세트와 워크로드(Workload)에 대한 확장성
* 애플리케이션 오류
* 예약 작업이 일정에 따라 실행되지 않거나, 종속성을 기다리고 있거나, 일부 작업이 올바른 순서로 실행되지 않는 문제
* 호환되지 않는 도구들(Tool incompatibility)

그럼 성능에 대한 측정은 어떻게 할까? 일단 성능을 나타내는 지표(metric)가 필요하다. 지표로는 다음이 해당된다.

* 지연시간(Latency) - 서비스가 요청을 이행하는 데 걸리는 시간
* Failures - 서비스가 실패하는 비율
* Resource Utilization, Utilization Pattern
* 트래픽(Traffic) - 특정 시간 동안 수신된 사용자 요청 수

---

## Troubleshooting

데이터 파이프라인의 성능 문제를 해결하는 방법에는 무엇이 있을까? 문제에 따라 다르지만 일반적으로 다음과 같은 단계를 수행할 수 있다. 

1. 일어난 문제에 대해 최대한 많은 정보를 수집한다. 관찰된 이슈가 실제로 문제인지 확인을 해야한다. 이슈는 사용자 경보 시스템이나 유지 관리 점검 중에 표시되었을 수 있다.
2. 올바른 버전의 소프트웨어와 소스 코드로 작업하고 있는지 확인한다.
3. 만약 최근에 배포한 경우라면, 변경 내용을 확인하고 이슈와 연결되었는지 확인한다.
4. 로그와 지표를 확인하여 문제가 인프라, 데이터, 소프트웨어 또는 이들의 조합과 관련된 문제인지 판단해야한다.
   * 로그 오류 메세지
   * 오류 발생 당시의 네트워크 로드
   * 메모리 및 CPU 사용률
5. 로그나 지표로 문제를 분리해내지 못했다면 테스트 환경에서 문제를 재현해야 할 수 있다.

---

## Database Optimization for Performance

성능 튜닝을 위한 또 한가지 영역은 데이터베이스 최적화이다. 데이터베이스를 위한 성능 지표에는 다음이 포함된다.

*  [System outages](https://www.ibm.com/docs/en/db2/11.5?topic=availability-outages)
*  용량 활용도(Capacity utilization)
*  애플리케이션 속도 저하
*  쿼리 성능
*  Conflicting activities와 쿼리를 여러 사용자를 기반으로 실행하는 경우의 성능
   *  Conflicting activity의 뜻을 모르겠다..
   *  Conflicting activities means <span class="spoiler">**any activity by the service provider which contradicts the provisions mentioned in this contract and acting against the interests of the Trust**.</span>

*  리소스 제약을 유발하는 배치 작업

데이터베이스 최적화를 위한 방법에는 무엇이 있을까?

1. 용량 계획(Capacity Planning)
   * 시스템 로드가 계속해서 변동하는 경우에도 성능에 필요한 최적의 하드웨어 및 리소스를 결정하는 프로세스
   * 향후 성장에 대한 사항도 포함된다
2. 데이터베이스 인덱싱(Database Indexing)
   * 데이터베이스의 각 행을 검색하지 않고도 데이터를 빠르게 찾을 수 있다
   * 쿼리가 처리될 때 디스크에 액세스해야 하는 횟수가 최소화 된다
3. 데이터베이스 파티셔닝(Database Partitioning)
   * 큰 테이블을 더 작은 개별 테이블로 나누는 프로세스
   * 더 작은 부분의 데이터에 접근하기 때문에 쿼리 속도가 빨라진다
   * 데이터 관리 효율성도 증가시킨다
4. 데이터베이스 정규화(Database Normalization)
   * 데이터 중복으로 인해 발생하는 불일치와 업데이트, 삭제, 삽입 작업으로 인해 발생하는 이상 현상을 줄이기 위한 설계 기법
   * 쿼리, 데이터 클렌징, 분석 작업에 대한 효율성과 속도에 영향을 미친다

---

## Monitoring Systems

모니터링 및 경고 시스템은 시스템 및 애플리케이션에 대한 정량적 데이터를 실시간으로 수집하는데 도움이 된다. 데이터 엔지니어링의 영역에서 이런 시스템들은 데이터 파이프라인, 플랫폼, 데이터베이스, 도구, 예약 작업 등에 대한 가시성(visibility)을 제공한다.

데이터베이스 모니터링 도구는 다음과 같은 작업을 포함한다.

* 데이터베이스 성능 지표의 스냅샷을 자주 찍는다
  * 스냅샷을 통해서 실제로 발생하기 시작한 시기와 방법을 추적하는 데 도움이 된다
  * 이슈를 분리해내서, 정확한 원인이 무엇인지 효율적으로 파악이 가능하다
* 애플리케이션 성능 관리 도구는 성능을 측정하고 모니터링하는데 도움을 준다
  * 이를 수행하기 위해 요청 응답 시간과 오류 메세지를 추적한다
  * 각 프로세스에 활용되는 리소스의 양을 추적하기 때문에 리소스를 사전에 할당하여 애플리케이션 성능을 향상시키는데 도움이 된다
* 쿼리 성능을 모니터링하는 도구는 더 나은 리소스 계획 및 할당을 위해 쿼리 처리량, 실행 성능, 리소스 활용 패턴 등에 대한 통계를 수집한다
* 데이터 파이프라인은 일반적으로 완료하는데 시간이 오래 걸리는 장기 프로세스들이 존재한다, 이는 프로세스에 오류가 관찰되면 실패 비용도 높다는 뜻이 된다
  * 작업 수준 런타임(Job-level runtime) 모니터링은 작업을 일련의 논리적 단계들로 나누어서 작업 완료에 대한 내용을 모니터링한다
* 처리되는 데이터의 양을 모니터링하면 워크로드(Workload) 크기로 인해 시스템 속도가 느려지는 판단하는데 도움이 된다
* 유지 관리 루틴(Maintenance routines)을 실행하면 문제가 있는 데이터나 프로세스를 식별하는데 사용할 수 있는 데이터를 생성한다
  * Time based - 사전에 약속된 시간 간격으로 활동을 계획
  * Condition based - 특정 문제가 있거나 성능 저하가 확인 될때 수행

---

## 마무리

지금까지 데이터 엔지니어링이 무엇을 하는지에 대해 전반적으로 정리해보았다. 지금까지 다룬 내용은 복잡한 데이터 엔지니어링에 대한 내용을 아주 단순화 시켜서 소개한 것에 불과하다. 다음 포스팅 내용은 필요한 기술에 대한 실습이나 SQL 관련 내용을 다룰 것 같다. 



## 참고

---

1. [Coursera - IBM Introduction to Data Engineering](https://www.coursera.org/learn/introduction-to-data-engineering)
2. [https://www.ibm.com/docs/en/db2/11.5?topic=availability-outages](https://www.ibm.com/docs/en/db2/11.5?topic=availability-outages)
