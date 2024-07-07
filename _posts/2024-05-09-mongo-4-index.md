---
title: (MongoDB - 4) 몽고DB의 인덱스
description: 몽고DB에서의 인덱스에 대하여, 사용한 쿼리의 소요 시간 알기
author: seungki1011
date: 2024-05-09 12:30:00 +0900
categories: [DB, MongoDB]
tags: [nosql, mongodb]
math: true
mermaid: true
---

---

## 1. 몽고DB 인덱스(Index) 소개

몽고DB도 다른 RDBMS 데이터베이스와 마찬가지로 인덱스(Index)를 제공한다.

만약 인덱스를 사용하지 않는다면 쿼리 결과를 얻기 위해서 항상 전체 컬렉션을 커렉션-스캔(collection-scan)해서 결과를 얻어야 한다. (RDBMS로 치면 테이블에 대해 풀스캔 한다고 생각하면 편하다)

같은 필드에 대해서 쿼리를 자주 사용한다면 인덱스를 생성하는 것을 고려해보자.

<br>

> 추가로
>
> * 몽고DB는 인덱스를 `B-tree`로 구현한다.
> * `_id` 필드에는 기본적으로 고유 인덱스([`unique index`](https://www.mongodb.com/docs/manual/core/index-unique/#std-label-index-type-unique))가 생성되어 있다
{: .prompt-info }

<br>

참고 : [RDBMS에서의 인덱스](https://seungki1011.github.io/posts/sql-5-index/)

<br>

---

## 2. 인덱스 생성

인덱스에도 다양한 종류가 존재한다. 인덱스를 생성하는 방법에 대해서 알아보자.

공식 문서 참고 : [https://www.mongodb.com/docs/manual/core/indexes/create-index/](https://www.mongodb.com/docs/manual/core/indexes/create-index/)

<br>

> `syntax`
>
> ```javascript
> db.collection.createIndex( <key and index type specification>, <options> )
> ```
{: .prompt-info }

<br>

인덱스의 종류는 다양하다. 공식 문서 : [https://www.mongodb.com/docs/manual/core/indexes/index-types/](https://www.mongodb.com/docs/manual/core/indexes/index-types/)

* Single Field Index
* Compound Index
* Multikey Index
* Geospatial Index
* Text Index
* Hashed Index

<br>

상황에 맞게 알맞은 인덱스를 생성해서 사용하자. 예시로는 `Single Field Index`를 생성해보자.

<br>

`예시`

```js
db.books.createIndex({pageCount : 1})
```

* `Single Field Index`의 경우 몽고DB는 양방향 탐색이 가능하기 때문에 오름차순과 내림차순에 차이는 없다
* 예시의 경우 `pageCount` 필드에 대해서 인덱스를 생성하였다
  * `1`은 오름차순 탐색이며, `-1`은 내림차순이다

* `Compound Field Index`(복합 필드 인덱스)는 위의 예시에서 필드를 더 추가하기만 하면 된다
* `unique`과 같은 옵션들도 존재한다

<br>

특정 컬렉션에서 생성한 인덱스를 조회하기 위해서는 다음 명령어를 사용한다.

```js
db.collection.getIndexes()
```

<br>

하나의 인덱스를 제거하기 위해서는 다음 명령어를 사용한다

```js
db.collection.dropIndex("<indexName>")
```

<br>

여러개의 인덱스를 제거하기 위해서는 다음 명령어를 사용한다.

```js
db.collection.dropIndexes(["<index1>", "<index2>", ...])
```

* `_id` 인덱스를 모든 인덱스를 제거하기 위해서는 `db.collection.dropIndexes()`

<br>

---

## 3. 쿼리 소요 시간 확인

사용한 쿼리에 대한 소요 시간과 같은 여러 메트릭(metric)을 확인할 수 있는 명령어는 다음과 같다.

<br>

`예시`

```js 
db.books.find({pageCount: {$get: 400}}).explain("executionStats")
```

* `explain("executionStats")`를 사용하면 된다

<br>

---

## Reference

1. https://www.mongodb.com/docs/manual/core/index-unique/#std-label-index-type-unique
2. [https://www.mongodb.com/docs/manual/core/indexes/create-index/](https://www.mongodb.com/docs/manual/core/indexes/create-index/)
3. [https://www.mongodb.com/docs/manual/core/indexes/index-types/](https://www.mongodb.com/docs/manual/core/indexes/index-types/)
4. [https://seungki1011.github.io/posts/sql-5-index/](https://seungki1011.github.io/posts/sql-5-index/)