---
title: (Spring Data JPA - 3) 벌크 수정, @EntityGraph, JPA Hints, Lock
description: 스프링 데이터 JPA의 벌크 수정 쿼리(bulk update), @EntityGraph로 N+1문제 해결, JPA Hints, Lock 기능
author: seungki1011
date: 2024-05-16 12:30:00 +0900
categories: [6. 백엔드(Backend), Spring Data JPA]
tags: [spring data jpa, jpa, spring, n+1, hint]
math: true
mermaid: true
---

---

## 1. 벌크 수정(Bulk Update)

스프링 데이터 JPA에서 **벌크 수정 쿼리를 실행하려면 `@Modifying` 어노테이션과 함께 `@Query`를 사용**해야 한다. **벌크 쿼리는 엔티티 매니저의 1차 캐시를 무시하고 데이터베이스에서 직접 실행되므로, 캐시와 데이터베이스 간의 불일치를 피하기 위해 주의가 필요**하다.

사용법을 알아보자. 다음 메서드를 레포지토리 인터페이스에 추가하자. 이때 `@Query` 위에 `@Modifying`을 추가해야 한다.

```java
public interface MemberRepository extends JpaRepository<Member, Long> {    
    @Modifying
    @Query("update Member m set m.age = m.age + 1 where m.age >= :age")
    int bulkAgePlus(@Param("age") int age);
}
```

* 지정한 `age` 이상이면, 해당 `age`를 전부 `1`씩 증가시키는 벌크 수정 쿼리이다

<br>

```java
@SpringBootTest
@Transactional
public class BulkUpdateQueryTest {
  
    @Autowired MemberRepository memberRepository;
    @Autowired EntityManager em;

    @Test
    public void 벌크_수정_쿼리_테스트() {
        // (member1, 10) ~ (member5, 50) 저장
        for (int i = 1; i <= 5; i++) {
            memberRepository.save(new Member("member" + i, i*10));
        }
        
        // age 30이상인 경우 age 1씩 증가
        int resultCount = memberRepository.bulkAgePlus(30);
        
        // "member3"을 찾는다
        Optional<Member> member3 = memberRepository.findById(3L);
        assertThat(member3).isPresent();
        
        // 영향 받은 데이터 수는 3개 
        assertThat(resultCount).isEqualTo(3);
      
        /**
         * member3의 age는 30, 벌크 수정 쿼리가 적용되었다면 변경된 age는 31이어야 한다
         * 그러나 확인해보면 age는 그대로 30이다
         * 그 이유는 DB에는 반영이 되었으나, 영속성 컨텍스트는 아직 30으로 남아있기 때문이다
         * 벌크 연산은 영속성 컨텍스트를 무시하고 실행하기 때문에, 영속성 컨텍스트에 있는 엔티티의 상태와 DB의 엔티티 상태가 달라질 수 있다
         */
        assertThat(member3.get().getAge()).isEqualTo(30);
    }

}
```

<br>

위에서 확인 했듯이, **벌크 연산은 영속성 컨텍스트를 무시하고 바로 데이터베이스에서 실행**된다. 따라서 **영속성 컨텍스트에 남아있는 엔티티들과 DB의 엔티티들의 상태 불일치를 주의**해야 한다. 

이를 해결하기 위한 두 가지 방법이 있다.

1. 벌크 연산 후 `entityManager.clear()` 사용 : 영속성 컨텍스트를 초기화 해버린다
   * 영속성 컨텍스트를 초기화 하면 엔티티 매니저는 DB에서 값을 다시 조회해서 가져온다. 당연히 수정이 반영된 값을 가져오기 때문에 불일치 문제를 해결할 수 있다.
2. `@Modifying(clearAutomatically = true)` 사용 : 위 방법과 똑같다고 보면 된다

<br>

> **주의!**
>
> 다시 주의를 하지만, 영속성 컨텍스트를 초기화하지 않는 경우, 수정이 일어난 엔티티를 조회하는 경우 영속성 컨텍스트에 과거의 값이 남아있기 때문에 문제가 생길 수 있다.
{: .prompt-danger }

<br>

---

## 2. N+1 문제 해결(@EntityGraph)

`@EntityGraph`는 JPA에서 **엔티티를 로드할 때 [페치 전략(Fetch Strategy)](https://seungki1011.github.io/posts/jpa-10-fetchjoin/#2-%ED%8E%98%EC%B9%98-%EC%A1%B0%EC%9D%B8join-fetch)을 설정하여 성능을 최적화하는 데 사용된다. 주로 연관된 엔티티를 한 번의 쿼리로 함께 로드하고자 할 때 사용**한다. 이를 통해 `N+1 문제`를 해결하거나, 특정 상황에서만 특정 연관 엔티티를 로드하여 성능을 최적화할 수 있다.

보통 연관된 엔티티를 한번에 조회하기 위해서 페치 전략(`fetch`)을 사용한다.

```java
@Query("select m from Member m left join fetch m.team")
```

<br>

그러면 `@EntityGraph`는 왜 사용하는 것일까?

* 스프링 데이터 JPA는 JPA가 제공하는 엔티티 그래프 기능을 편리하게 사용하게 도와준다. 이 기능을 사용하면 JPQL 없이 페치 조인을 사용할 수 있다. 

* 기본적으로 JPA는 연관된 엔티티를 지연(`LAZY`) 로딩으로 설정할 경우, 초기에는 쿼리를 실행하지 않고, 연관된 엔티티에 접근할 때 추가 쿼리를 실행한다. 많은 엔티티가 연관된 경우 `N+1 문제`가 발생할 수 있다. `@EntityGraph`를 사용하면 한 번의 쿼리로 연관된 엔티티를 로드할 수 있다.

<br>

사용법을 알아보자.

```java
// 공통 메서드를 오버라이드하는 경우
@Override
@EntityGraph(attributePaths = {"team"}) 
List<Member> findAll();

// 쿼리 메서드에서 사용하는 경우
@EntityGraph(attributePaths = {"team"})
List<Member> findByUsername(String username)
  
//JPQL + 엔티티 그래프 
@EntityGraph(attributePaths = {"team"}) 
@Query("select m from Member m") 
List<Member> findMemberEntityGraph();
```

<br>

정리하자면 `@EntityGraph`는 페치 전략을 간편하게 사용할 수 있는 방법으로 보면 된다.

<br>

---

## 3. JPA Hints

**JPA 힌트(JPA Hints)는 JPA 쿼리의 성능을 최적화하거나 특정 동작을 제어하기 위해 JPA 구현체에게 전달하는 추가적인 지시사항**이다. 이러한 힌트는 쿼리 실행 시 JPA 구현체에게 특정 설정이나 최적화 방법을 적용하도록 지시할 수 있다. 대표적으로 Hibernate와 같은 구현체에서 이를 통해 다양한 최적화와 동작 제어를 수행할 수 있다.

JPA 힌트를 사용하는 주요 이유는 다음과 같다.

* **성능 최적화**: 캐시 사용, 쿼리 계획 고정, 쿼리 실행 중 특정 전략 사용, 등을 통해 쿼리 성능을 최적화할 수 있다
* **쿼리 동작 제어**: 특정 동작을 제어하여 쿼리 실행 시 필요한 추가 설정을 할 수 있다

<br>

사용 방법을 알아보자.

`@Query` 애노테이션과 함께 힌트를 사용할 수 있다. 힌트를 설정하려면 `@QueryHint` 애노테이션을 사용한다.

```java
public interface MemberRepository extends JpaRepository<Member, Long> {
    @Query("SELECT m FROM Member m WHERE m.age > :age")
    @QueryHints(@QueryHint(name = "org.hibernate.cacheable", value = "true"))
    List<Member> findByAgeGreaterThanWithHints(@Param("age") int age);
}
```

* `org.hibernate.cacheable`
  * **캐시 사용 설정**: 캐시를 활성화하여 쿼리 결과를 캐시에 저장하고 재사용할 수 있다
* `org.hibernate.readOnly`
  * **읽기 전용 설정**: 쿼리를 읽기 전용으로 설정하여 엔티티를 읽기 전용 모드로 로드한다
  * 데이터를 변경하는 쿼리는 전부 실행되지 않는다

<br>

이외에도 다양한 힌트들이 존재한다.

<br>

> **추가로**
>
> * 쿼리 힌트 공식 문서 [참고](https://docs.spring.io/spring-data/jpa/reference/jpa/query-methods.html#jpa.query-hints)
> * 엔티티 매니저를 통해 힌트를 설정하는 것도 가능하다. [참고](https://docs.jboss.org/hibernate/stable/orm/userguide/html_single/Hibernate_User_Guide.html#jpql-query-hints)
{: .prompt-tip }


<br>

> **JPA 힌트 vs SQL 힌트**
>
> * **적용 수준**
>   * **JPA 힌트**: JPA 쿼리나 `EntityManager`를 통해 적용되며, JPA 구현체(Hibernate)에게 특정 설정을 전달한다.
>   * **SQL 힌트**: SQL문 내에 포함되며, 데이터베이스 엔진(MySQL, Oracle, PostgreSQL 등)에게 직접적으로 영향을 준다.
> * **목적**
>   * **JPA 힌트**: JPA 구현체의 동작을 제어하고 최적화한다.
>     * 예시) 엔티티 캐싱, 쿼리 타임아웃, 읽기 전용 모드 설정.
>   * **SQL 힌트**: 데이터베이스 엔진의 쿼리 최적화 전략을 제어한다.
>     * 예시) 인덱스 사용, 조인 방법, 파티셔닝 전략 등.
> * **사용 방법**
>   * **JPA 힌트**: `@QueryHint` 애노테이션이나 `EntityManager`의 `setHint` 메서드를 사용하여 설정한다.
>   * **SQL 힌트**: SQL 문 내에 직접 삽입된다. 예를 들어, `/*+ INDEX(table_name index_name) */`.
    {: .prompt-info }


<br>

---

## 4. JPA Lock(동시성 제어)

**JPA Lock은 데이터베이스의 동시성 문제를 해결하기 위해 사용되는 기능**이다. 이는 여러 트랜잭션이 동시에 동일한 데이터를 수정할 때 발생할 수 있는 문제를 방지하는 데 도움을 준다. JPA는 두 가지 주요 유형의 잠금을 지원한다.

* 낙관적 락(Optimistic Lock)
* 비관적 락(Pessimistic Lock)

<br>

---

### 낙관적 락(Optimistic Lock)

**낙관적 락은 데이터 충돌이 발생할 가능성이 낮다고 가정하고 트랜잭션을 진행한다. 데이터 충돌이 발생할 경우, 트랜잭션이 실패하고 다시 시도하도록 설계**되어 있다.

사용 방법은 다음과 같다.

먼저 낙관적 락은 엔티티에 `@Version` 애노테이션을 사용하여 구현한다. 이 애노테이션은 엔티티의 버전 필드를 지정하며, DB에서 **엔티티가 수정될 때마다 버전 번호가 증가**한다. 트랜잭션이 데이터를 업데이트할 때, 현재 버전과 DB에 저장된 버전이 일치하지 않으면 예외가 발생한다.

```java
@Entity
@Getter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Member {

    @Id @GeneratedValue
    @Column(name = "member_id")
    private Long id;
    private String name;
    
    @Version
    private Long version;  // 버전 필드

    // 나머지 구현
}
```

<br>

`@Version`을 이용한 낙관적 락의 동작 과정은 다음과 같다.

1. **트랜잭션 시작**: 데이터를 읽고, 엔티티의 버전 필드 값을 기록
2. **데이터 수정**: 트랜잭션 내에서 데이터를 수정
3. **트랜잭션 커밋**: 데이터베이스에 업데이트를 시도하면서 버전 필드 값을 체크
4. **버전 충돌 감지**: 데이터베이스에 저장된 버전과 엔티티의 버전이 일치하지 않으면 `OptimisticLockException` 예외 발생

<br>

다음 처럼에 메서드 레벨에서 낙관적 락을 적용하는 것도 가능하다.

```java
// 이 메소드는 낙관적 락을 사용하여 실행된다
@Lock(LockModeType.OPTIMISTIC)
List<Member> findByName(String name);
```

<br>

---

### 비관적 락(Pessimistic Lock)

**비관적 락은 데이터 충돌이 발생할 가능성이 높다고 가정하고, 트랜잭션이 데이터를 수정할 때 다른 트랜잭션이 접근하지 못하도록 락을 설정**한다. 이는 데이터베이스의 잠금을 직접적으로 제어하여 동시성 문제를 방지한다.

비관적 락은 쿼리 메서드에 `@Lock`를 추가해서 사용한다.

```java
// 이 메서드는 비관적 락을 사용해서 실행된다
@Lock(LockModeType.PESSIMISTIC_WRITE)
List<Member> findByName(String name);
```

<br>

> 실시간 트래픽이 많은 경우 비관적 락은 성능 이슈 때문에 사용을 권장하지 않는다.
>
> 실시간 트래픽보다 동시성 이슈가 더 중요한 경우에 도입을 생각해보자.
{: .prompt-danger }

<br>

> 추가 내용
>
> * JPA에서 낙관적 락은 애플리케이션 레벨에서 동작하며, 직접 DB에 락을 걸어서 사용하는 방식은 아니다.
> * 비관적락은 RDBMS의 배타적 락(exclusive)과 공유 락(shared lock)을 사용해서 구현할 수 있다. [참고](https://seungki1011.github.io/posts/rdbms-7-lock/#%EB%9D%BDlock-%EC%86%8C%EA%B0%9C)

<br>


---

## Reference

1. [김영한 : 실전 스프링 데이터 JPA!](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EB%8D%B0%EC%9D%B4%ED%84%B0-JPA-%EC%8B%A4%EC%A0%84/dashboard)
1. 
