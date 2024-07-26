---
title: (Spring Data JPA - 2) 스프링 데이터 JPA 쿼리 메서드(Query Method)
description: 스프링 데이터 JPA의 쿼리 메서드 기능, 페이지네이션, 정렬, 등의 기능에 대하여
author: seungki1011
date: 2024-05-14 12:30:00 +0900
categories: [6. 백엔드(Backend), Spring Data JPA]
tags: [spring data jpa, jpa, spring]
math: true
mermaid: true
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

## 3. 조회 결과의 반환 타입

스프링 데이터 JPA에서 조회 결과의 반환 타입은 다양한 옵션을 제공한다. 각 반환 타입은 특정 요구사항에 맞게 사용할 수 있으며, 쿼리 메소드(또는 쿼리)에서 정의된 조건에 따라 다양한 형태로 결과를 받을 수 있다.

주요 반환 타입들을 살펴보자.

<br>

* **단일 엔티티 반환 : 단건 조회하는 경우**

  * ```java
    User findByUsername(String username);
    ```

  * 결과가 없다면 `null` 반환(원래는 `NoResultException`이 발생하지만, 스프링 데이터 JPA는 이 예외 대신 `null`을 반환한다)

  * 결과가 2건 이상인 경우 `NonUniqueResultException` 예외 발생



* **`Collection` 반환 : 쿼리 결과가 여러 개의 엔티티인 경우**

  * ```java
    List<User> findByStatus(String status);
    ```

  * 결과가 없으면 빈 컬렉션을 반환한다



* **`Optional` : 결과가 무조건 있어야하는 경우 `null` 대신 `Optional`을 반환해서 NPE를 방지할 수 있다**

  * ```java
    Optional<User> findById(Long id);
    ```



* **`Page` : 페이지네이션을 사용하여 대량의 데이터셋을 페이지 단위로 처리하여 성능을 최적화한다**

  * ```java
    Page<User> findByStatus(String status, Pageable pageable);
    ```



* **`Slice` : 페이지네이션과 유사하지만, 전체 페이지 개수를 계산하지 않는다**

  * ```java
    Slice<User> findByStatus(String status, Pageable pageable);
    ```



* **DTO : 사용자 정의 객체를 반환하는 것도 가능하다. 위의 [DTO 조회]() 참고.**

  * ```java
    @Query("SELECT new com.example.UserDTO(u.id, u.username) FROM User u WHERE u.status = :status")
    List<UserDTO> findUserDTOByStatus(@Param("status") String status);
    ```



* **원시(primitive)또는 wrapper 타입**

  * ```java
    @Query("SELECT COUNT(u) FROM User u WHERE u.status = :status")
    long countByStatus(@Param("status") String status);
    ```

<br>

이외에도 많은 반환 타입을 지원한다. [공식 문서 참고](https://docs.spring.io/spring-data/jpa/reference/repositories/query-return-types-reference.html#appendix.query.return.types)

<br>

---

## 4. 정렬, 페이지네이션 기능 (Sort, Pagination) 

스프링 데이터 JPA는 대량의 데이터셋을 효율적으로 조회하고 관리하기 위해 페이지네이션(pagination)과 정렬(sorting) 기능을 제공한다. 이 기능들은 `Pageable`과 `Sort` 인터페이스를 통해 쉽게 구현할 수 있다. 

**페이지네이션은 데이터를 일정 크기의 페이지 단위로 나누어 조회하는 방법이고, 정렬은 데이터를 특정 기준에 따라 정렬하는 방법이다.**

<br>

---

### Page 사용하기

페이지네이션을 통해 데이터베이스에서 필요한 양의 데이터만을 가져올 수 있다. 이를 통해 메모리 사용량을 줄이고, 응답 시간을 단축할 수 있다. 다음은 페이지네이션을 사용하기 위한 주요 인터페이스들이다.

* `Pageable`
  * 페이지 요청 정보를 담고 있는 인터페이스
  * 페이지 번호와 페이지 크기, 정렬 기준을 설정할 수 있다
* `Page`
  * 페이지 정보와 함께 **전체 데이터 수와 전체 페이지 수를 포함**한다. 페이지 수를 계산하기 위해 추가적인 쿼리를 수행할 수 있다.
* `Slice`
  * **페이지 정보만을 포함하며, 전체 페이지 수를 계산하지 않는다.**
  * 성능 최적화를 위해 사용할 수 있다(모바일에서 스크롤 방식으로 컨텐츠 확인하는 경우)
  * 추가 `count` 쿼리 없이 다음 페이지만 확인 가능하다(내부적으로 `limit+1` 조회)

<br>

> 임포트할 때 `org.springframework.data.domain.`의 클래스를 임포트 받아야한다.
{: .prompt-warning }

<br>

먼저 `Page`의 사용법을 알아보자. 

```java
public interface MemberRepository extends Repository<Member, Long> {
    Page<Member> findByAge(int age, Pageable pageable);
}
```

* `Pageable` 인터페이스를 파라미터로 받고 있다. 실제 사용할 때는 해당 인터페이스를 구현한 `PageRequest` 객체를 사용한다.

<br>

```java
@SpringBootTest
@Transactional
class MemberRepositoryTest {
    @Autowired
    MemberRepository memberRepository;
    
    // age가 1인 멤버 10명, age가 2인 멤버 20명 생성
    @BeforeEach
    public void setUp() {
        for (int i = 1; i <= 10; i++) {
            memberRepository.save(new Member("member" + i, 1));
        }
        for (int i = 11; i <= 30; i++) {
            memberRepository.save(new Member("member" + i, 2));
        }
    }

    @Test
    public void 페이지_정렬_없이_테스트() {
        int currentPage = 0; // 첫 번째 페이지를 조회
        int limit = 5; // 페이지당 보여줄 데이터는 5건
      
        PageRequest pageRequest = PageRequest.of(currentPage, limit);
        Page<Member> page = memberRepository.findByAge(1, pageRequest);

        List<Member> content = page.getContent(); // 조회된 데이터
        assertThat(content.size()).isEqualTo(5); // 조회된 데이터의 수
        assertThat(page.getTotalElements()).isEqualTo(10); // 전체 데이터의 수
        assertThat(page.getNumber()).isEqualTo(0); // 페이지 번호
        assertThat(page.getTotalPages()).isEqualTo(2); //전체 페이지 번호
    }
    
}
```

* `Page`에서는 `0`번 페이지가 첫 번째 페이지이다

<br>

---

### 정렬 조건 추가하기

정렬 기능을 사용하려면 `PageRequest` 객체를 생성할 때 `Sort` 객체를 함께 사용하면 된다.

바로 사용해보자. 먼저 레포지토리 인터페이스에 다음 메서드를 추가하자.

```java
public interface MemberRepository extends JpaRepository<Member, Long> {
    // 기존 메서드들 ...
    Page<Member> findByAgeBetween(int startAge, int endAge, Pageable pageable);
}
```

* `age`의 범위로 검색하는 메서드를 추가했다

<br>

```java
@SpringBootTest
@Transactional
@Slf4j
public class MemberRepositorySortTest {
    @Autowired
    MemberRepository memberRepository;
    
    /** 
     * (username, age) -> 엔티티가 (member1, 2) ~ (member10, 11)까지 생성되고 저장된다
     */
    @BeforeEach
    public void setUp() {
        for (int i = 1; i <= 10; i++) {
            memberRepository.save(new Member("member" + i, 1 + i));
        }
    }

    @Test
    public void 페이지_이름_정렬_테스트() {
        int currentPage = 0;
        int limit = 5;
        PageRequest pageRequest = PageRequest.of(currentPage, 
                                                 limit, 
                                                 Sort.by("age").ascending());
        /**
         * age가 2~11의 범위로 검색
         * 찾는 페이지는 0번 페이지
         * 한 페이지당 보여주는 데이터는 5건
         */
        Page<Member> page = memberRepository.findByAgeBetween(2, 11, pageRequest);

        List<Member> content = page.getContent(); // 조회된 데이터
        assertThat(content.get(0).getUsername()).isEqualTo("member1");
        assertThat(content.get(4).getUsername()).isEqualTo("member5");
    }
```

* `Sort.by("age").ascending()` : 나이를 기준으로 오름차순 정렬된다
  * `Sort.by(Direction.ASC, "age")` 처럼 사용하는 것도 가능하다
* 현재 나이를 기준으로 정렬했으니 첫 번째 데이터는 나이가 `2`이고 이름이 `member1`인 엔티티가 반환되어야 한다

<br>

> **페이지를 유지하면서 엔티티를 DTO로 변환하기**
>
> ```java
> Page<Member> page = memberRepository.findByAge(10, pageRequest);
> Page<MemberDto> dtoPage = page.map(m -> new MemberDto());
> ```
{: .prompt-tip }

<br>

---

### Slice 사용하기

스프링 데이터 JPA에서 `Slice` 인터페이스는 `Page`와 유사하지만, 전체 페이지 수를 계산하지 않는다. `Slice`를 사용하면 다음 페이지가 존재하는지 여부만 알 수 있으며, 이로 인해 성능상의 이점이 존재할 수 있다.

`Slice`를 한번 사용해보자. 레포지토리 인터페이스에 다음 메서드를 추가하자.

```java
public interface MemberRepository extends JpaRepository<Member, Long> {
    // 기존 메서드들... 
    Slice<Member> findByUsernameContainingAndAgeBetween(String username, 
                                                        int startAge, 
                                                        int endAge, 
                                                        Pageable pageable);
}
```

* 특정 이름으로 검색했을때 나이의 범위도 고려한다

<br>

```java
@SpringBootTest
@Transactional
public class MemberRepositorySliceTest {
    @Autowired
    MemberRepository memberRepository;

    /**
     * 멤버 엔티티 20개 저장
     * 저장 형태 : (member1, 1) ~ (member10, 10), (멤버11, 11) ~ (멤버20, 20)
     */
    @BeforeEach
    public void setUp() {
        for (int i = 1; i <= 20; i++) {
            if (i <= 10) {
                memberRepository.save(new Member("member" + i, i));
            } else {
                memberRepository.save(new Member("멤버" + i, i));
            }
        }
    }

    @Test
    public void 슬라이스_테스트() {
        /**
         * Page 0
         * slice size 10
         * age 기준 오름차순 정렬
         */
        Pageable pageable = PageRequest.of(0, 10, Sort.by("age").ascending());
      
        /**
         * username에 "member"를 포함한 데이터 중에 age의 범위가 5~15 사이 검색
         */
        Slice<Member> slice = memberRepository
          .findByUsernameContainingAndAgeBetween("member", 5, 15, pageable);

        List<Member> content = slice.getContent();

        /**
         * Slice는 getTotalElements(), getTotalPages() 사용 불가
         */
        assertThat(content).isNotEmpty();
        assertThat(content.size()).isEqualTo(6); // 슬라이스의 크기
        assertThat(slice.getNumber()).isEqualTo(0); // 페이지 번호(넘버)
      
        /**
         * hasNext()가 false인 이유는 age 11부터는 "멤버11"로 username이 저장됨
         */
        assertThat(slice.hasNext()).isFalse(); // 다음 페이지가 존재하는지 확인
        assertThat(slice.hasPrevious()).isFalse(); // 이전 페이지가 존재하는지 확인
      
        /**
         * 1 번째 데이터는 age 5 -> member5
         * 6 번째 데이터는 age 10 -> member10
         */
        assertThat(content.get(0).getUsername()).isEqualTo("member5");
        assertThat(content.get(5).getUsername()).isEqualTo("member10");
    }

}
```

* `Pageable pageable = PageRequest.of(0, 10, Sort.by("age").ascending());`
  * 이전에는 `PageRequest`로 받았지만, `Pageable`로 받는 것도 가능하다
* `Slice`는 `limit+1`을 조회해서 다음 페이지의 여부를 확인한다

<br>

> `Page`나 `Slice` 타입으로 받지 않고 그냥 `List`와 같은 컬렉션 타입으로 받는 것이 가능하다. 물론 `Page`, `Slice`의 기능은 사용하지 못하지만, 단순히 쿼리에 `limit`를 걸어서 가져오고 싶은 경우 사용할 수 있다.
{: .prompt-tip }

<br>

> [페이징과 정렬 공식 문서 참고](https://docs.spring.io/spring-data/jpa/reference/repositories/core-extensions.html#core.web.basic.paging-and-sorting)
{: .prompt-tip }


<br>

---

### Count 쿼리 분리하기

스프링 데이터 JPA에서는 페이지네이션을 사용할 때, 기본적으로 전체 결과 수를 계산하는 `count` 쿼리를 자동으로 실행한다. 하지만 이 **`count` 쿼리가 복잡한 조인이나 서브쿼리를 포함하고 있을 경우 성능에 문제가 발생할 수 있다.** 이러한 경우, **`count` 쿼리를 분리해서 최적화할 수 있는 기능을 제공**한다.

사용법을 알아보자.

`count` 쿼리를 분리하려면, `@Query`와 `@Query`의 `countQuery` 속성을 사용하면 된다. 이를 통해 `count` 쿼리와 실제 데이터 조회 쿼리를 별도로 지정할 수 있다.

<br>

```java
public interface MemberRepository extends JpaRepository<Member, Long> {

    @Query(value = "SELECT m FROM Member m WHERE m.name LIKE %:name% AND m.age BETWEEN :startAge AND :endAge",
           countQuery = "SELECT COUNT(m) FROM Member m WHERE m.name LIKE %:name% AND m.age BETWEEN :startAge AND :endAge")
    Page<Member> findByUsernameContainingAndAgeBetween(@Param("name") String username, 
                                                   @Param("startAge") int startAge, 
                                                   @Param("endAge") int endAge, 
                                                   Pageable pageable);
}
```

* `value` : 실제 데이터를 조회하는 쿼리
* `countQuery` : 전체 결과 수를 계산하는 쿼리

<br>

> **하이버네이트 6 `LEFT JOIN` 최적화**
>
> * 스프링 부트 3^ 을 사용하면 하이버네이트 6이 적용된다.
>
> * Hibernate 6부터 도입된 주요 최적화 중 하나는 쓸모없는 `LEFT JOIN`을 제거하는 것이다
> * 기존의 Hibernate에서는 일부 경우에 불필요한 `LEFT JOIN`을 생성하는 경우가 있었다. 이러한 경우 불필요한 `LEFT JOIN`은 성능에 부정적인 영향을 미칠 수 있다. 예를 들어, 실제로 필요하지 않은 테이블을 조인하여 데이터를 가져오므로 쿼리 실행 시간이 길어지고, 데이터베이스의 부하가 증가할 수 있다.
> * Hibernate 6에서는 이러한 불필요한 조인을 자동으로 최적화하여 제거함으로써 쿼리의 성능을 개선한다.
{: .prompt-info }

<br>

---

## Reference

1. [김영한 : 실전 스프링 데이터 JPA!](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-%EB%8D%B0%EC%9D%B4%ED%84%B0-JPA-%EC%8B%A4%EC%A0%84/dashboard)
1. [https://docs.spring.io/spring-data/jpa/reference/repositories/query-keywords-reference.html#appendix.query.method.subject](https://docs.spring.io/spring-data/jpa/reference/repositories/query-keywords-reference.html#appendix.query.method.subject)
1. [https://docs.spring.io/spring-data/jpa/reference/repositories/core-extensions.html#core.web.basic.paging-and-sorting](https://docs.spring.io/spring-data/jpa/reference/repositories/core-extensions.html#core.web.basic.paging-and-sorting)