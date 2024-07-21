---
title: (MongoDB - 1) NoSQL, MongoDB 소개
description: NoSQL의 등장 배경과 MongoDB 소개, 실습 환경 준비
author: seungki1011
date: 2024-05-05 12:30:00 +0900
categories: [3. 데이터베이스(DB), MongoDB]
tags: [nosql, mongodb]
math: true
mermaid: true
---

---

### 1.2 NoSQL 등장 배경

소셜 미디어 플랫폼들이 등장하면서 데이터베이스들은 높은 처리량(high-throughput)과 낮은 지연시간(low-latency), 등이 요구되었다. 

또한 기존의 정형 데이터가 아닌 비정형, 반정형 데이터가 많아지면서, 관계형 데이터베이스(SQL Database)가 다루지 못하는 영역까지 다룰 수 있는 NoSQL(Not only SQL) 데이터베이스가 등장하게 된다.

정리해서 이야기 하자면 다양항 데이터 유형의 등장, 빅데이터, 대용량 트래픽을 다루는 웹 및 모바일 애플리케이션의 등장에 맞춰서 NoSQL은 확장성, 성능, 사용 편의성으로 인해 인기를 얻기 시작했다. NoSQL은 기존의 정형화된 데이터베이스 구조를 따르지 않으며, 데이터 쿼리에 SQL만을 사용하지 않는다.

<br>

---

### 1.3 NoSQL 분류 및 특징

NoSQL 데이터베이스의 종류는 굉장히 많고, 특징에 따라 다음과 같이 분류할 수 있다.

<br>

1. **Key-Value Based**
   - 키는 데이터의 속성을 나타내며 고유 식별자 역할을 한다
   - 키-값 모두 간단한 정수부터 복잡한 JSON 까지 될 수 있다
   - 사용자 세션 데이터, 선호도, 실시간 추천, 캐싱 등에 적합한 Key-Value 쌍으로 저장
   - 예) Redis, Memchached, DynamoDB 등
   - Redis의 경우 in-memory 캐시 DB로 많이 사용한다

2. **Document-Based**
   - 레코드 및 관련 데이터가 하나의 문서 내에 저장되어 유연한 인덱싱 및 임시 쿼리가 가능하다
   - 실제 use-case로는 이커머스, 의료 기록, CRM 등이 있다
   - 예) MongoDB, DocumentDM, CouchDB 등

3. **Column-Based**
   - 데이터는 행이 아닌 열로 구성되어 있어 많은 쓰기 요청이 필요한 시계열 데이터, 날씨 데이터, IoT 데이터 등에 적합하다
   - 예) Cassandra, HBase 등

4. **Graph-Based**
   - 그래프 모델을 활용하여 데이터를 표현하고 저장하기 때문에 데이터간 연결 및 관계를 시각화하기 적합하다
   - 실제 use-case에는 소셜 네트워크, 추천, 네트워크 다이어그램, 액세스 관리 등에 사용한다
   - 예) Neo4j, CosmosDB 등

<br>

![nosql2](../post_images/2024-05-05-mongo-1-nosql-intro/nosql2.png)

<p align="center">https://learn.microsoft.com/ko-kr/dotnet/architecture/cloud-native/relational-vs-nosql-data </p>

<p align="center">remade by seungki1011</p>

* NoSQL 데이터베이스는 대용량의 데이터를 처리할 수 있는 능력, 분산 처리 시스템 지원, 확장의 용이성, 유연한 스키마 등의 특징이 있다
  * NoSQL의 경우 ACID를 일부 포기하고 그 대신 높은 처리량과 낮은 지연성을 추구한다
  * NoSQL에서는 보통 중복을 허용해서 데이터를 `JOIN` 없이 조회할 수 있도록 한다
  * 필요한 데이터를 그냥 중복이 있어도 전부 저장해놓는 특징 때문에 스케일 아웃도 용이하다



* 이런 NoSQL 데이터베이스의 특징은 에자일한 개발에 유용하다
* 반면 관계형 데이터베이스와 대조되는 강점을 가짐에도 불구하고, NoSQL 데이터베이스는 상대적으로 ACID 준수성이 부족하고 정형 데이터를 다루는 경우 관계형 데이터베이스에 비해서 기능이 부족할 수 있다
  * 그렇게 때문에 Transaction이나 데이터 정합성과 같은 ACID가 정말 중요한 금융 시스템과 같은 경우 NoSQL 데이터베이스를 사용하지 않고 관계형 데이터베이스를 사용한다

<br>

---

## 2. MongoDB 소개

### 2.1 MongoDB의 특징

몽고DB(MongoDB)는 도큐먼트 지향(Document-oriented) 데이터베이스이다. NoSQL 데이터베이스로 분류되는 몽고DB는 동적 스키마형 JSON 도큐먼트에 데이터를 입력한다. 몽고DB는 BSON(Binary JSON)이라는 포맷을 사용해서 저장한다.

BSON은 쉽게 생각해서 JSON 도큐먼트를 바이너리(Binary)로 인코딩한 포맷이라고 생각하면 편하다.

공식 문서 참고 : [https://www.mongodb.com/json-and-bson](https://www.mongodb.com/json-and-bson)

<br>

그럼 몽고DB의 특징을 살펴보자.

![nosql2](../post_images/2024-05-05-mongo-1-nosql-intro/mongodb1.png)

<p align="center">RDBMS vs MongoDB</p>

* 몽고DB에서는 테이블이 아니라 컬렉션(Collection)이라는 명칭을 사용한다
  * 컬렉션은 도큐먼트(Document)의 모음
    * 도큐먼트를 저장하기 위한 논리적인 묶음이라고 보면 된다
    * RDBMS의 테이블을 생각하면 된다
  * 몽고DB는 기본적으로 도큐먼트의 스키마에 제약이 없지만, 컬렉션 단위에서 도큐먼트들이 같은 필드, 데이터 타입을 이용하도록 제약(validator)을 걸 수 있다 
  * Schema Validation을 사용하지 않더라고 애플리케이션 레벨에서 스키마 규칙을 프로그래밍적 모델로 가지고 있는 것이 좋다
  * `db.createCollection("user")` 같은 형태로 컬렉션 생성이 가능, 도큐먼트를 생성하는 과정에서도 컬렉션이 존재하지 않았다면 몽고DB에서 자동으로 생성해준다



* 몽고 DB는 기본적으로 도큐먼트 단위로 데이터를 입력하고 조회한다
  * 데이터는 컬럼에 해당하는 필드(field, key)와 해당하는 값(value)을 입력하면 된다
    * 쉽게 말해서 `JSON` 형태로 데이터를 입력하면 된다
  * 몽고DB는 기존의 관계형 데이터베이스와 다르게 스키마가 아무것도 정해지지 않았기 때문에 자유롭게 필드를 정해서 값을 입력해도 된다
  * `db.user.insertOne({ 필드:값 })` 같은 형태로 하나의 도큐먼트를 입력할 수 있다



* 도큐먼트는 고유한 `_id`를 할당받는다
  * `_id`를 할당받는 시점은 데이터 삽입 시점
  * 자동 할당을 받는 경우 `ObjectId` 형식의 데이터로 `_id`가 생성된다
  * `ObjectId`의 경우 `ObjectId.getTimestamp()`를 이용해서 생성 시점을 가져올 수 있음
  * `_id`를 직접 지정하는 것도 가능



* 전체 도큐먼트를 조회하고 싶으면 `db.user.find({})` 같은 형태로 조회할 수 있다
* 몽고DB는 개발자들이 애플리케이션 레벨에서 스키마 관리를 한다

<br>

![nosql2](../post_images/2024-05-05-mongo-1-nosql-intro/mongodb4.png)

<p align="center">MongoDB는 데이터 중복 허용</p>

* 기존의 RDBMS는 `Product`, `User`, `Order` 테이블을 쪼개서 중복이 없도록 설계하고, 이후 `JOIN`을 통해서 필요한 데이터를 조회한다
* 반면 NoSQL 데이터베이스인 몽고DB에서는 중복된 데이터를 저장해도 괜찮다는 철학을 가진다
  * 한 번 읽을 때 필요한 모든 데이터를 다 저장해놓기 때문에, 굳이 `JOIN`을 사용하지 않아도 된다
  * `JOIN`을 사용하지 않기 때문에 과도한 `JOIN` 수행으로 인한 성능 오버헤드를 방지할 수 있다



* 데이터 중복 허용을 통한 `JOIN` 필요성을 제거하는 대신, 애플리케이션 레벨에서 데이터들이 모두 최신 상태를 유지할 수 있도록 관리해야한다
* 도큐먼트에서 필드 안의 필드 같은 중첩(nested)된 형태로 데이터를 저장하는 것이 가능하다. 그러나 이 경우 데이터 저장, 검색, 집계 과정에서 속도가 느려질 가능성이 있다. 물론 데이터가 적을때는 큰 차이가 없지만, 데이터가 많아지면 성능이 떨어질 수 있기 때문에 유의해서 스키마를 설계하자



* 물론 유연한 스키마를 사용할 수 있지만, RDBMS 데이터베이스 처럼 컬렉션을 참조해서 마치 `JOIN`을 하는 것 처럼 사용이 가능하다

<br>

---

### 2.1 MondoDB 설치

MongoDB를 사용하기 위한 초기 셋팅을 해보자.

로컬에 몽고DB를 설치하지 않고 도커 컴포즈를 사용해서 몽고DB 컨테이너를 이용하자.

다음 두 개의 컨테이너를 올려서 사용할 것이다.

* MondoDB
* MongoExpress(GUI 툴)

<br>

몽고DB와 CLI로 상호작용하기 위해서 `Mongosh`를 설치할 것이다.

`Mongosh` 설치 : [https://www.mongodb.com/docs/mongodb-shell/install/](https://www.mongodb.com/docs/mongodb-shell/install/)

<br>

`JSON` 파일에 존재하는 데이터를 몽고DB의 데이터베이스로 불러오기 위해 사용하는 `mongoimport`를 설치하자.

`mongodb-database-tools` 설치 : [https://www.mongodb.com/docs/database-tools/installation/installation-macos/#installation](https://www.mongodb.com/docs/database-tools/installation/installation-macos/#installation)

<br>

그럼 이제 `compose.yaml` 파일을 다음과 같이 작성하자.

```yaml
services:
  mongodb:
    image: mongo:latest
    container_name: mongodb-container
    restart: always
    ports:
      - "27017:27017"
    environment:
      MONGO_INITDB_ROOT_USERNAME: root
      MONGO_INITDB_ROOT_PASSWORD: admin
    volumes:
      - /Users/{사용자이름}/Desktop/mongodb-data:/data/db

  mongo-express:
    image: mongo-express
    container_name: mongo-express-container
    restart: always
    ports:
      - "8081:8081"
    environment:
      ME_CONFIG_MONGODB_SERVER: mongodb-container
      ME_CONFIG_MONGODB_ADMINUSERNAME: root
      ME_CONFIG_MONGODB_ADMINPASSWORD: admin

networks:
  default:
    name: mongodb-network
```

* `27017`은 몽고DB 기본 포트
* `mongodb-network`라는 도커 네트워크를 정의하고, `mongodb`와 `mongo-express` 컨테이너가 이 네트워크를 통해 통신할 수 있도록 한다
* `MongoExpress`를 사용하기 위해서는 [http://localhost:8081/](http://localhost:8081/)에 접속하면 된다

<br>

`compose.yaml`을 작성한 디렉토리로 가서 `docker compose up -d` 또는 `docker compose -f {컴포즈 파일명} -d`를 이용해서 컨테이너와 네트워크를 생성하자.

생성이 완료되었으면 `mongodb-container`, `mongo-express-container`라는 두개의 컨테이너와 `mongodb-network`라는 네트워크가 만들어져야한다.

<br>

![nosql2](../post_images/2024-05-05-mongo-1-nosql-intro/mongo3.png)

<br>

`docker network inspect mongodb-network`를 통해서 `mongodb-network`에 두 컨테이너 모두 포함되어 있는지 확인해보자.

![nosql2](../post_images/2024-05-05-mongo-1-nosql-intro/network2.png)

<br>

이제 `mongosh`를 이용해서 몽고DB에 접속해보자.

`mongosh --host 127.0.0.1 --port 27017 --username root --password admin`

또는

`mongosh "mongodb://root:admin@127.0.0.1:27017"`

* `--authenticationDatabase {DB명}` 옵션을 이용하면 해당 `user`가 권한을 가지는 데이터베이스로 접속할 수 있다
* `127.0.0.1` 대신 `localhost` 가능

<br>

 ![nosql2](../post_images/2024-05-05-mongo-1-nosql-intro/mongosh.png)

* 연결을 끊기 위해서는 `.exit`, `exit`, `exit()`, `quit`, `quit()` 등을 사용할 수 있다
* `cls`를 이용해서 몽고쉘의 콘솔을 비울수 있다

<br>

---

## Reference

1. [https://www.mongodb.com/docs/manual/core/document/](https://www.mongodb.com/docs/manual/core/document/)
2. [쉬운코드 : NoSQL 설명](https://www.youtube.com/watch?v=sqVByJ5tbNA&t=754s)
3. [AmigosCode : MongoDB Tutorial](https://www.youtube.com/watch?v=Www6cTUymCY)
4. [https://www.mongodb.com/json-and-bson](https://www.mongodb.com/json-and-bson)
5. [https://www.mongodb.com/docs/mongodb-shell/install/](https://www.mongodb.com/docs/mongodb-shell/install/)
6. [https://www.mongodb.com/docs/database-tools/installation/installation-macos/#installation](https://www.mongodb.com/docs/database-tools/installation/installation-macos/#installation)