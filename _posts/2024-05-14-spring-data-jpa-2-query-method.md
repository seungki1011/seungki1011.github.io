---
title: (Spring Data JPA - 2) 스프링 데이터 JPA 쿼리 메서드(Query Method)
description: 스프링 데이터 JPA의 쿼리 메서드 기능에 대하여
author: seungki1011
date: 2024-05-14 12:30:00 +0900
categories: [6. 백엔드(Backend), Spring Data JPA]
tags: [spring data jpa, jpa, spring]
math: true
mermaid: true
---

---

## 1. 쿼리 메서드(Query Method)

스프링 데이터 JPA의 쿼리 메서드 기능은 **복잡한 쿼리를 작성하지 않고도 메소드 이름만으로 원하는 쿼리를 정의할 수 있는 편리한 기능**이다. 

간단한 예시를 한번 보자. 이름과 나이를 기준으로 회원을 조회한다고 가정해보자. 쿼리 메서드 기능을 사용하면 메서드 이름을 다음 처럼 작성하면 된다.

<br>

```java
public interface MemberRepository extends JpaRepository<Member, Long> {
     List<Member> findByUsernameAndAgeGreaterThan(String username, int age);
}
```

* 스프링 데이터는 메서드 이름인 `findByUsernameAndAgeGreaterThan`을 분석해서 맞는 JPQL을 생성해준다
* 메서드 이름에 포함된 변수는 쿼리 파라미터로 사용된다
  * 예) `Username` → `username`, `Age` → `age`

* 이름을 분석해보자
  * `findBy` : 스프링 데이터 JPA에서 엔티티를 검색하기 위한 접두사로, 이는 "주어진 조건에 맞는 데이터를 찾아라"는 의미이다 (조회)
  * `Username` : 검색 조건의 첫 번째 필드인 `username`을 나타낸다. `username` 필드가 주어진 값과 일치하는 데이터를 찾는다.
  * `And` : `AND` 연산으로 두 조건을 연결한다
  * `AgeGreaterThan` : 검색 조건의 두 번째 필드인 `age`를 나타내고, `age` 필드가 주어진 값보다 큰 데이터를 찾는다

<br>

쿼리 메서드에 사용되는 몇 가지 키워드를 살펴보자.

* `find...By`, `get...By`, `read...By`, `query...By` : 조회
  * 보통 엔티티의 타입 반환
* `deleteBy`, `removeBy` : 삭제
* `countBy` : `COUNT` 결과
  * `long` 반환
* `existsBy` : `EXISTS` 결과
  * `boolean` 반환
* `First<n>`, `Top<n>`, 등... : 결과의 갯수를 앞에서 부터 제한
  * `find...By`에서 `...`의 자리에 들어가서 적용할 수 있다
* `Distinct` : 유일한(unique) 결과만 반환 받고 싶을 때 사용한다
  * `find...By`에서 `...`의 자리에 들어가서 적용할 수 있다

<br>

> 자세한 규칙을 살펴보고 싶다면 다음 공식 문서를 참고하자.
>
> * [쿼리 메서드](https://docs.spring.io/spring-data/jpa/reference/repositories/query-methods-details.html#repositories.query-methods.query-creation)
> * [쿼리 메서드 명명 규칙](https://docs.spring.io/spring-data/jpa/reference/repositories/query-keywords-reference.html#appendix.query.method.subject)
{: .prompt-tip }

<br>

> **주의!**
>
> 만약 엔티티의 필드명이 변경된다면, 인터페이스에 정의한 메서드 이름도 같이 변경해줘야 한다. 그렇지 않으면 오류가 발생한다.
{: .prompt-danger }

<br>

---

## 2. 레포지토리에 직접 쿼리 작성(@Query)

### 기존 쿼리 메서드의 한계

쿼리 메서드 기능은 굉장히 편리하지만 단점이 존재한다. 이는 쿼리가 굉장히 복잡해지는 경우 메서드의 이름이 장황하게(~~더럽게~~) 변한다는 것이다. 

예를 들어서 `User` 엔티티에서 `username` 필드가 주어진 값과 일치하고, `age` 필드가 주어진 값보다 크며, `status` 필드가 주어진 값과 일치하고, `joinedDate` 필드가 주어진 날짜 범위 내에 있는 모든 엔티티를 검색하는 쿼리를 사용하고 싶다고 가정해보자. 이를 쿼리 메서드로 작성하면 다음과 같다.

```java
List<User> findByUsernameAndAgeGreaterThanAndStatusAndJoinedDateBetween(String username, int age, String status, Date startDate, Date endDate);
```

<br>

위의 예시에서 알 수 있듯이 **복잡한 쿼리에 대해 메서드 쿼리를 사용하면 메서드 이름에 대한 가독성이 떨어진다.** 또한, 굉장히 복잡한 조인이나 서브쿼리를 사용하는 경우에는 메서드 쿼리만으로 표현하는데 한계가 존재한다.

스프링 데이터 JPA는 이 문제를 해결하기 위해서 레포지토리의 메서드에 JPQL을 직접 작성할 수 있는 `@Query` 기능을 제공한다.

<br>

---

### @Query 사용하기

`@Query`를 사용해서 레포지토리 메서드에 직접 JPQL을 작성하는 방법은 다음과 같다.

<br>

```java
public interface MemberRepository extends JpaRepository<Member, Long> {
    @Query("select m from Member m where m.username= :username and m.age = :age")
    List<Member> findUser(@Param("username") String username, @Param("age") int age);
}
```

* 메서드 바로 위에 `@Query(<JPQL>)`를 사용한다
* **파라미터 바인딩을 위해서 `@Param(<parameter_name>)`을 사용한다**
  * 순서 기반 파라미터 바인딩도 가능하지만 유지보수를 위해 권장하지 않는다

* `@Query`를 적용한 메서드는 메서드 쿼리보다 높은 우선순위를 가진다
  * 쉽게 말해서 쿼리 메서드 명명 규칙을 사용한 메서드 이름을 사용했어도, `@Query`가 붙었으면 `@Query`에 작성한 JPQL이 사용된다

<br>

`@Query`를 사용하면 복잡한 쿼리에 대해서 직접 JPQL을 작성해서 사용할 수 있다. **또 하나의 장점이 있다면, 애플리케이션 실행 시점에 JPQL의 문법 오류를 찾아낼 수 있다**는 것이다. 스프링 애플리케이션 컨텍스트가 초기화되는 동안 `@Query` 어노테이션에 정의된 JPQL 쿼리의 구문이 검증된다. 이때 검증 오류가 발견되면 예외가 발생한다.

<br>

> `@NamedQuery`
>
> `@NamedQuery`라는 애노테이션을 엔티티 클래스 위에 사용해서 Named 쿼리를 정의할 수 있다. Named 쿼리는 이름 그대로, 쿼리에 이름을 붙여서 사용하는 것이다. `@Query`의 기능이 이미 강력하기 때문에, `@NamedQuery`는 잘 사용되지 않는다.
>
> [사용법 참고](https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html#jpa.query-methods.named-queries)
{: .prompt-info }

<br>

---

### DTO로 조회하기

DTO로 조회하기 위해서는 `new` 명령어를 사용해야 한다. 당연한 이야기겠지만, 맞는 DTO도 필요하다.

DTO로 조회하는 방법은 다음과 같다.

먼저 다음과 같은 DTO가 존재한다고 가정해보자.

<br>

`MemberDTO`

```java
@Getter @Setter
@AllArgsConstructor
public class MemberDto {
     private Long id;
     private String username;
     private String teamName;
}
```

<br>

DTO로 조회하기 위한 JPQL은 다음과 같다.

```java
@Query("select new study.datajpa.dto.MemberDto(m.id, m.username, t.name) " +
         "from Member m join m.team t")
List<MemberDto> findMemberDto();
```

* `new study.datajpa.dto.MemberDto(m.id, m.username, t.name)`로 DTO로 조회한다
  * 패키지명까지 명시해야 한다
* 리스트의 요소들을 `MemberDTO` 타입으로 받고 있는 것을 확인할 수 있다

<br>


---

## Reference

1. [김영한 : 실전 스프링 데이터 JPA!](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EB%8D%B0%EC%9D%B4%ED%84%B0-JPA-%EC%8B%A4%EC%A0%84/dashboard)
1. [https://docs.spring.io/spring-data/jpa/reference/repositories/query-keywords-reference.html#appendix.query.method.subject](https://docs.spring.io/spring-data/jpa/reference/repositories/query-keywords-reference.html#appendix.query.method.subject)
