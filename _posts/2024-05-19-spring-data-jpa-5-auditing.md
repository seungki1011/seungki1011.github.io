---
title: (Spring Data JPA - 5) Auditing
description: Audit 기능을 사용해서 엔티티의 생성/변경 추적
author: seungki1011
date: 2024-05-19 12:30:00 +0900
categories: [6. 백엔드(Backend), Spring Data JPA]
tags: [spring data jpa, spring, auditing]
math: true
mermaid: true
---

---

## 1. Auditing

### Auditing을 사용하기 위한 BaseEntity 적용하기

스프링 데이터 JPA에서 **Auditing(감사) 기능은 엔티티의 생성, 수정, 삭제 등의 이벤트를 자동으로 기록하는 기능**이다. 이 기능을 사용하면 **엔티티가 생성되거나 수정될 때 자동으로 생성일자, 수정일자, 생성자, 수정자 등을 기록할 수 있다**. 이는 데이터의 변경 이력을 관리하고, 누가 언제 어떤 데이터를 변경했는지 추적하는 데 유용하다.

이제 Auditing 기능을 사용해보자.

먼저 스프링 부트 애플리케이션 클래스에 `@EnableJpaAuditing`를 추가해야 한다.

```java
@SpringBootApplication
@EnableJpaAuditing
public class DatajpaApplication {
  
	public static void main(String[] args) {
		SpringApplication.run(DatajpaApplication.class, args);
	}
}
```

<br>

등록일자/수정일자/등록자/수정자 필드를 엔티티에 추가하기 위해서 `BaseEntity`와 `BaseDateEntity`를 만들자.

`@MappedSuperClass` 애노테이션을 사용해서 `BaseEntity`와 `BaseDateEntity`를 엔티티의 공통 매핑 정보로 사용할 것이다. 

<br>

> `@MappedSuperClass`에 대해 알아보러 [가기](https://seungki1011.github.io/posts/jpa-6-inheritance-mapping/#5-mappedsuperclass)
{: .prompt-tip }

<br>

`BaseDateEntity`

```java
@Getter
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseDateEntity {

    @CreatedDate
    @Column(updatable = false)
    private LocalDateTime createdDate;
    @LastModifiedDate
    private LocalDateTime lastModifiedDate;
  
}
```

* `abstract` : 추상 클래스를 사용해서 해당 클래스의 인스턴스 생성 방지
* `@MappedSuperclass` : 공통 매핑 정보를 제공하는 클래스에 사용하는 애노테이션
* `@EntityListeners(AuditingEntityListener.class)` : Audit 기능을 사용하기 위해서 필수적으로 추가한다 
* `@CreatedDate` : 등록일자 필드에 추가한다
  * `@Column(updatable = false)` : 등록일자의 변경을 막기 위해서 추가한다
* `@LastModifiedDate` : 수정일자 필드에 추가한다 

<br>

`BaseEntity`

```java
@Getter
@MappedSuperclass
@EntityListeners(AuditingEntityListener.class)
public abstract class BaseEntity extends BaseDateEntity {
    
    @CreatedBy
    @Column(updatable = false)
    private String createdBy;
    @LastModifiedBy
    private String lastModifiedBy;

}
```

* `extends BaseDateEntity` : `BaseEntity`는 `BaseDateEntity`의 매핑정보도 사용한다
* `@CreatedBy` : 등록자 필드에 추가한다
  * `@Column(updatable = false)` : 등록자의 변경을 막기 위해 추가한다
* `@LastModifiedBy` : 수정자 필드에 추가한다

<br>

> `BaseEntity`와 `BaseDateEntity`를 분리해서 사용하는 이유는 모든 엔티티가 등록자/수정자를 사용하지 않기 때문이다. 보통은 등록일/수정일은 사용하지만 등록자/수정자까지 사용하는 경우는 많지 않다.(물론 이것은 비즈니스 도메인에 따라 다르다.)
>
> 필요에 따라 등록일/수정일/등록자/수정자 전부 사용하는 `BaseEntity`를 사용하거나, 등록일/수정일만 사용하는 `BaseDateEntity`를 사용하면 된다.
{: .prompt-tip }

<br>

`BaseEntity`를 우리가 사용하는 엔티티에 적용해보자.

```java
@Entity
@Getter @Setter
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class Member extends BaseEntity {

    @Id
    @GeneratedValue
    @Column(name = "member_id")
    private Long id;
    private String username;
    private int age;
    
    // 기존 구현 ...
  
}
```

<br>

---

### 테스트 코드로 등록일, 수정일 확인하기

실제로 테스트 코드를 통해 필드들이 찍히는 것을 확인하자.

```java
@Slf4j
@Transactional
@SpringBootTest
class BaseEntityTest {
  
    @Autowired MemberRepository memberRepository;
    @Autowired TeamRepository teamRepository;
    @Autowired EntityManager entityManager;

    @Test
    public void Audit_기능_테스트() throws Exception {
        Member member = Member.builder()
                .age(20)
                .username("멤버1")
                .build();
        memberRepository.save(member);

        Team teamA = Team.builder()
                .name("팀A")
                .build();
        teamRepository.save(teamA);

        Thread.sleep(100);
        member.setTeam(teamA);

        entityManager.flush();
        entityManager.clear();

        Optional<Member> optionalMember = memberRepository.findById(member.getId());
        Assertions.assertThat(optionalMember).isPresent();
        Member findMember = optionalMember.get();

        log.info("[등록일]findMember.getCreatedDate() = {}", 
                 findMember.getCreatedDate());
        log.info("[수정일]findMember.getLastModifiedDate() = {}", 
                 findMember.getLastModifiedDate());
      
    }
}
```

```
2024-05-19T14:05:43.831+09:00  INFO 84491 --- [    Test worker] de.datajpa.domain.BaseEntityTest         : [등록일]findMember.getCreatedDate() = 2024-05-1914:05:43.630065
2024-05-19T14:05:43.831+09:00  INFO 84491 --- [    Test worker] de.datajpa.domain.BaseEntityTest         : [수정일]findMember.getLastModifiedDate() = 2024-05-19T14:05:43.748737
```

* 등록일과 수정일이 정상적으로 찍히는 것을 확인할 수 있다

<br>

---

### 테스트 코드로 등록자, 수정자 확인하기

등록자와 수정자를 확인하기 위해서는 다음의 코드를 더 추가해야한다.

스프링 부트 애플리케이션 클래스에 다음 코드를 추가하자.

```java
@SpringBootApplication
@EnableJpaAuditing
public class DatajpaApplication {

	public static void main(String[] args) {
		SpringApplication.run(DatajpaApplication.class, args);
	}

	@Bean
	public AuditorAware<String> auditorProvider() {
		return () -> Optional.of(UUID.randomUUID().toString());
	}
	
}
```

* 현재 예시에서는 `UUID`를 생성해서 사용하고 있지만, 실무에서는 보통 세션 정보나 스프링 시큐리티 로그인 정보에서 ID를 받아서 사용한다

<br>

이제 테스트 코드에서 등록자와 수정자를 확인해보자.

```java
log.info("[등록자]findMember.getLastModifiedDate() = {}", findMember.getCreatedBy());
log.info("[수정자]findMember.getLastModifiedDate() = {}", findMember.getLastModifiedBy());
```

```
2024-05-19T15:34:47.459+09:00  INFO 20861 --- [    Test worker] de.datajpa.domain.BaseEntityTest         : [등록자]findMember.getLastModifiedDate() = 79a1407a-c055-48b4-aba2-a2fd18021f75
2024-05-19T15:34:47.460+09:00  INFO 20861 --- [    Test worker] de.datajpa.domain.BaseEntityTest         : [수정자]findMember.getLastModifiedDate() = cabc99e7-d31b-4595-b88b-4ef5ed0483b9
```

* `UUID`를 랜덤으로 생성해서 사용하고 있기 때문에, 결과에서는 등록자, 수정자가 서로 다르게 나온다

<br>


---

## Reference

1. [https://docs.spring.io/spring-data/jpa/reference/auditing.html](https://docs.spring.io/spring-data/jpa/reference/auditing.html)
1. [김영한 : 실전 스프링 데이터 JPA!](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EB%8D%B0%EC%9D%B4%ED%84%B0-JPA-%EC%8B%A4%EC%A0%84/dashboard)