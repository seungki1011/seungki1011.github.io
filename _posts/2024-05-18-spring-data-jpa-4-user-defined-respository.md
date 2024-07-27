---
title: (Spring Data JPA - 4) 사용자 정의 레포지토리(Custom Repository)
description: 스프링 데이터 JPA의 사용자 정의 레포지토리 기능
author: seungki1011
date: 2024-05-18 12:30:00 +0900
categories: [6. 백엔드(Backend), Spring Data JPA]
tags: [spring data jpa, jpa, spring]
math: true
mermaid: true
---

---

## 1. 사용자 정의 레포지토리(Custom Repository Implementations) 소개

스프링 데이터 JPA는 기본적으로 `JpaRepository`, `CrudRepository`, `PagingAndSortingRepository` 등 여러 가지 기본 레포지토리 인터페이스를 제공한다. 이들 인터페이스는 일반적인 CRUD 작업과 페이지네이션, 정렬 등의 기본적인 기능을 제공한다.

하지만 복잡한 쿼리나 특정 비즈니스 로직이 필요한 경우, 이러한 기본 레포지토리 인터페이스만으로는 충분하지 않을 수 있다. 

예를 들어서 다음의 경우 직접 메서드를 구현해서 사용해야 한다.

* JPA(`EntityManager`) 직접 사용하기
* JDBC Template 사용하기
* QueryDSL 사용하기
* DB 커넥션을 직접 사용하기
* 기타

<br>

그렇다고 직접 `JpaRepository` 인터페이스를 구현하기 위해서는 기존의 수많은 메서드들을 오버라이드해서 구현해야 한다.

스프링 데이터 JPA는 편하게 **기존 레포지토리 인터페이스의 기능을 그대로 사용하면서 사용자 정의 레포지토리를 만들어 필요한 메소드를 정의할 수 있는 기능을 제공**한다.

<br>

사용법을 알아보자.

먼저 사용자 정의 인터페이스를 하나 만든다.

```java
public interface MemberRepositoryCustom {
     List<Member> findMemberCustom();
}
```

<br>

그 다음, 레포지토리 인터페이스에서 사용자 정의 인터페이스를 상속해야 한다.

```java
public interface MemberRepository
          extends JpaRepository<Member, Long>, MemberRepositoryCustom {
}
```

<br>

마지막으로 사용자 정의 인터페이스를 구현하는 클래스를 만든다. 이때 구현체명은 `레포지토리 인터페이스명 + Impl` 형식으로 이름을 붙여야한다. 

> 스프링 데이터 2.x 부터는 `사용자 정의 인터페이스명 + Impl`을 구현 클래스의 이름으로 사용할 수 있다.
>
> 예) `MemberRepositoryImpl` 대신 `MemberRepositoryCustomImpl` 사용 가능
{: .prompt-info }


<br>

```java
@RequiredArgsConstructor
public class MemberRepositoryImpl implements MemberRepositoryCustom {
   
    private final EntityManager em;
   
    @Override
    public List<Member> findMemberCustom() {
        return em.createQuery("select m from Member m")
                .getResultList();
    } 
}
```

<br>

이제 해당 클래스에 필요한 메서드들을 구현해서 사용하면 된다.

<br>

> **스프링 데이터 JPA에 억지로 맞출 필요가 없다**
>
> 이게 무슨 말이냐면, 굳이 스프링 데이터 JPA의 레포지토리 인터페이스 기능을 사용하지 않고 기존에 사용했듯이, `@Repository` 애노테이션을 붙여서 레포지토리 계층을 구현해도 된다. 물론 이 경우에는 레포지토리 인터페이스의 기능을 사용하지 못한다. 상황에 맞춰서 유연하게 사용하자.
{: .prompt-tip }

<br>

---


## Reference

1. [https://docs.spring.io/spring-data/jpa/reference/repositories/custom-implementations.html#repositories.customize-base-repository](https://docs.spring.io/spring-data/jpa/reference/repositories/custom-implementations.html#repositories.customize-base-repository)
2. [김영한 : 실전 스프링 데이터 JPA!](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EB%8D%B0%EC%9D%B4%ED%84%B0-JPA-%EC%8B%A4%EC%A0%84/dashboard)