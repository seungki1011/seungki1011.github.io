---
title: (Spring Data JPA - 3) 벌크 수정, @EntityGraph, JPA Hint, Lock
description: 스프링 데이터 JPA의 벌크 수정 쿼리(bulk update), @EntityGraph로 N+1문제 해결, JPA Hint, Lock 기능
author: seungki1011
date: 2024-05-16 12:30:00 +0900
categories: [6. 백엔드(Backend), Spring Data JPA]
tags: [spring data jpa, jpa, spring, n+1, hint]
math: true
mermaid: true
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

















