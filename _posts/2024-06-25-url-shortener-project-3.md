---
title: (Url Shortener - 3) URL 단축 서비스 개발 시작, 발생한 문제들
description: 프로젝트의 개발을 시작하면서 했던 고민과 만났던 문제들.
author: seungki1011
date: 2024-06-25 10:30:00 +0900
categories: [Project, Url-Shortener]
tags: [project, backend, transaction, trouble-shooting, spring]
pin: true
math: true
mermaid: true
---

---

## 엔티티 클래스 작성

원본 URL과 숏코드를 저장할 엔티티 클래스를 작성해보자.

<br>

```java
@Entity
@Getter
@Table(name = "url_mapping")
@NoArgsConstructor(access = AccessLevel.PROTECTED)
public class UrlMapping {

    @Id
    @GeneratedValue(strategy = GenerationType.SEQUENCE)
    private Long id;

    @Column(unique = true)
    private String shortcode;

    private String originalUrl;

    private LocalDateTime createdAt;
    private LocalDateTime viewedAt;
    private int viewCount = 0;

    public UrlMapping(String shortcode, String originalUrl, LocalDateTime createdAt) {
        this.shortcode = shortcode;
        this.originalUrl = originalUrl;
        this.createdAt = createdAt;
    }

    public void incrementViewCount() {
        this.viewCount++;
        this.viewedAt = LocalDateTime.now();
    }

    public void setShortcode(String shortcode) {
        this.shortcode = shortcode;
    }

    /*
      추후 회원 가입 기능을 추가할 때 사용
     */
    // @ManyToOne(fetch = FetchType.LAZY)
    // @JoinColumn(name = "member_id")
    // private Member member;

}
```

* `incrementViewCount()` : 단축 URL을 통해 원본 URL을 조회할 때, 해당 단축 URL의 `viewCount`를 `1` 증가시키고, 조회 시간(`viewedAt`)을 업데이트 한다
* 숏코드를 생성하기 위한 로직도 전부 엔티티 클래스에 작성할지 고민 했으나, 일단은 서비스 계층에서 구현하기로 했다
* 숏코드 생성 알고리즘 자체는 유틸 클래스로 빼서 작성(Base62 인코더, 해시 함수)
* 빌더 클래스는 사용하지는 않기로 함

<br>

이전 포스트에서 대략적으로 정한 설계대로 개발을 시작하면서 만났던 문제들을 살펴보자.

<br>

---

## 이슈 1 : UnexpectedRollbackException

### 이슈 발생 배경

* 동일한 URL로 URL 단축을 위한 `POST` 요청을 보내게 되면 첫 번째 요청은 정상적으로 수행되지만, 두 번째 요청에서`ConstraintViolationException`이 발생한다.
* `ConstraintViolationException`이 발생하는 원인은 동일한 URL에 대해서는 같은 숏코드가 나오고, 중복 숏코드를 처리하는 로직을 구현하지 않았기 때문이다.



* 중복된 숏코드를 처리하기 위해서 다음의 중복 처리 로직을 구현하기로 했다.
  * 만약 `shortenUrl(originalUrl)`을 통해 숏코드를 생성했을 때 `ConstraintViolationException`이 발생한다면, 서비스 계충에서 잡아서 핸들링한다.
  * 핸들링 로직은 원본 URL에 램덤 솔트(salt)를 추가해서 솔트를 추가한 URL로 숏코드를 재생성하는 방법을 사용한다. 물론 원본 URL은 동일하게 저장한다.
  * 예시) `https://abc123.com` + `saltvalue` = `https://abc123.comsaltvalue`



* 문제는 다음과 같다
  * `@Transactional`이 붙은 테스트 코드에서 `shortenUrl`을 같은 `originalUrl`로 호출하는 경우 정상적으로 예외를 핸들링하고 숏코드로 새로운 값으로 재생성하는 것을 확인할 수 있었다
  * **컨트롤러 계층 테스트를 위해서 동일한 URL(`originalUrl`)로 포스트 요청을 두 번하는 경우, 두 번째 요청에서 `UnexpectedRollbackException`이 발생하고, 예상한대로 동작하지 않는다는 문제가 발생한다.**

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/post1.png){: width="972" height="589" }_문제 발생 상황_

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/constraint1.png){: width="972" height="589" }

![clickreq](../post_images/2024-06-25-url-shortener-project-3/constraint2.png){: width="972" height="589" }_ConstraintViolationException 발생_

* 테스트 코드에서는 숏코드가 중복되면 `ConstraintViolationException` 발생하고, 서비스 계층에서 정상적으로 처리하는 것 까지 확인 가능하다
* 내 예상은, 아마 `@Test`에서 동작하는 `@Transactional`의 특수성 때문에 정상적으로 동작하는 것 같지만, 다시 알아볼 예정이다

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/rollbackexception.png){: width="972" height="589" }_동일한 URL POST 요청 두 번_ 

* 반면에 동일한 URL에 대해서 `POST` 요청을 두 번 수행하는 경우, 두 번째 요청에서 `UnexpectedRollbackException` 발생

<br>

---

### 이슈 재현

이슈 상황을 재현해보자.

<br>

`UrlMappingRepository`

```java
public void save(UrlMapping urlMapping) {
        em.persist(urlMapping);
}
```

<br>

`UrlShortenerService`

```java
@Transactional
public String shortenUrl(String originalUrl) {
    String shortcode = generateShortcode(originalUrl);
    UrlMapping urlMapping = new UrlMapping(shortcode, originalUrl, LocalDateTime.now());

    try {
        umr.save(urlMapping);
        em.flush();
        log.info("[No Duplication] shortcode = {}", shortcode);
    } catch (ConstraintViolationException | DataIntegrityViolationException e) {
        log.info("[Exception!] ", e);
        log.info("[Shortcode Duplication] Original shortcode = {}", shortcode);
        shortcode = generateShortcodeWithSalt(originalUrl);
        urlMapping.setShortcode(shortcode);
        umr.save(urlMapping);
        log.info("[Shortcode Duplication] Salted shortcode = {}", shortcode);
    }
    return urlMapping.getShortcode();
}
```

* `generateShortcode()` : 원본 URL을 입력으로 받아서 숏코드를 생성해주는 메서드
* `generateShortcodeWithSalt()` : 원본 URL을 입력으로 받고, 해당 URL에 솔트를 추가해서 숏코드를 생성해주는 메서드
  * 이 메서드는 숏코드가 중복되어 예외가 발생한 경우, 핸들링을 위해서 사용한다

<br>

`UrlShortenerController`

```java
@PostMapping("/shorten")
public String shortenUrl(@RequestParam("url") String originalUrl) {
    String shortcode = uss.shortenUrl(originalUrl);
    return "redirect:/detail/" + shortcode;
}
```

* 단축하고 싶은 URL을 입력해서 `POST` 요청을 보내서 성공적으로 처리되면, 해당 숏코드를 `PathVariable`로 사용해서, `/detail/{shortcode}`로 리다이렉트한다
* 해당 페이지는 결과 단축 URL을 링크로 제공한다

<br>

다음은 테스트 코드이다.

<br>

`TestDuplicateShortcode`

```java
@SpringBootTest
@AutoConfigureMockMvc
public class TestDuplicateShortcode {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UrlShortenerService uss;

    @DisplayName("중복된 URL로 shortenUrl()을 두 번 호출하는 경우 숏코드가 서로 달라야 한다")
    @Transactional
    @Test
    public void test_duplicate_shortcode() {
        String originalUrl = "https://www.inflearn.com/";

        String originalShortcode = uss.shortenUrl(originalUrl);
        String saltUrlShortcode = uss.shortenUrl(originalUrl);

        assertThat(originalShortcode).isNotEqualTo(saltUrlShortcode);
    }
  
    @DisplayName("같은 URL을 이용한 POST 요청은 성공해야 한다")
    @Test
    public void test_post_shortenUrl() throws Exception {
        String originalUrl = "https://www.inflearn.com/";

        mockMvc.perform(post("/shorten")
                        .param("url", originalUrl))
                .andExpect(status().is3xxRedirection())
                .andExpect(redirectedUrl("/detail/naA5WFV"));

        // 같은 URL 두 번째 요청
        mockMvc.perform(post("/shorten")
                        .param("url", originalUrl))
                .andExpect(status().is3xxRedirection());

    }

}
```

* `test_duplicate_shortcode()`
  * 동일한 URL로 `shortenUrl(originalUrl)`을 두 번 호출하면, 두 번째 호출에서는 예외를 처리해서 숏코드를 재생성해야 한다
  * 기존 숏코드와 예외 핸들링 이후의 숏코드를 비교하면 달라야한다
  * 이 테스트의 경우 통과한다
* `test_post_shortenUrl()`
  * 동일한 URL로 `/shorten`으로 `POST` 요청을 두 번 수행하면, 두 번째 요청에서는 변경된 숏코드로 응답을 주어야한다
  * 두 번째 요청에서 `UnexpectedRollbackException`이 발생해서, 의도한 결과가 나오지 않는다

<br>

---

### 원인 파악 

`UnexpectedRollbackException`이기 때문에 트랜잭션 전파와 관련된 문제로 보인다.

<br>

> ```java
> public class UnexpectedRollbackException
> extends TransactionException
> ```
>
> Thrown when an attempt to commit a transaction resulted in an unexpected rollback.
>
> `rollback-only`로 표기된 트랜잭션을 커밋하려고 시도하는 경우 발생한다.
>
> 참고 : [https://docs.oracle.com/middleware/12212/odi/reference-java-api/oracle/odi/core/persistence/transaction/UnexpectedRollbackException.html](https://docs.oracle.com/middleware/12212/odi/reference-java-api/oracle/odi/core/persistence/transaction/UnexpectedRollbackException.html)
{: .prompt-info }


<br>

일단 현재 트랜잭션이 어떻게 수행되고 있는지 파악하기로 했다.

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/issue1rollbackonly.png){: width="972" height="589" }_현재 상황_

위의 그림을 정리하자면 다음과 같다. 두 번째 요청에서 이전과 동일한 URL을 사용해서 같은 숏코드가 생성된 상황이라고 가정하자. 

* 서비스 계층의 `shortenUrl()` 부터 트랜잭션이 시작된다.
* `shortenUrl()`의 내부 로직에서 숏코드를 생성하고, 레포지토리 계층의 `save()`를 호출하게 된다
* 이미 존재하는 숏코드를 DB에 넣으려고 하면 `ConstraintViolationException`이 발생한다
* 예외가 발생했기 때문에 현재의 트랜잭션은 `rollback-only`로 표시된다
* 이 경우에 서비스 계층에서 예외를 받아서 처리해도, 트랜잭션은 이미 `rollback-only`로 표시되어 있기 때문에 `UnexpectedRollbackException`이 발생한다

<br>

그럼 이 문제를 해결하기 위해서는 서비스 계층의 `shortenUrl()`에서 시작된 트랜잭션을 어떻게든 정상적으로 커밋되도록 만들어야한다.

이를 위해서는 트랜잭션 전파의 속성 중에 `REQUIRES_NEW`를 사용해서 해결할 수 있다.

<br>

---

### 트랜잭션 전파(Transaction Propagation)

자세히 들어가기 전에 먼저 트랜잭션의 전파에 대해 복습해보자.

트랜잭션이 이미 진행중인 상황에서 추가로 트랜잭션을 수행하게 되는 경우 어떻게 동작할까? 트랜잭션 중에 새로운 트랜잭션이 수행되는 경우 어떻게 동작할지 결정하는 것을 트랜잭션 전파(Transaction Propogation)라고 한다.

스프링에서 이런 트랜잭션 전파의 속성을 설정할 수 있으며, 기본 옵션은 `REQUIRED`이다. `REQUIRED`의 경우 트랜잭션 전파는 다음과 같이 동작한다.

* 처음 수행되는 트랜잭션을 외부 트랜잭션이라고 한다
* 외부 트랜잭션이 진행 도중에 호출되는 트랜잭션은 내부 트랜잭션이 된다
* 내부 트랜잭션은 외부 트랜잭션에 참여한다고 표현한다
* 스프링은 외부 트랜잭션과 내부 트랜잭션을 하나의 물리 트랜잭션으로 묶는다
  * 물리 트랜잭션 : 실제 데이터베이스에 적용되는 트랜잭션
* 외부 트랜잭션과 내부 트랜잭션은 각각 논리 트랜잭션으로 취급된다

<br>

* 디폴트 옵션인 `REQUIRED`는 다음의 기본 원칙을 가진다
  * 모든 논리 트랜잭션이 커밋되어야 물리 트랜잭션이 커밋된다
  * 하나의 논리 트랜잭션이라도 롤백되면, 전체 트랜잭션도 롤백된다

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/propagation.png){: width="972" height="589" }_기본 전파 옵션 REQUIRED_

정리하자면 `REQUIRED`는 다음 처럼 행동하게 된다.

- 외부/내부 트랜잭션 모두 커밋 되면 물리 트랜잭션도 커밋
- 내부 트랜잭션이 롤백되면 물리 트랜잭션도 롤백
- 외부 트랜잭션이 롤백되면 물리 트랜잭션도 롤백

<br>

여기서 알 수 있는 것은, 만약 나의 서비스 계층과 레포지토리 계층에 전부 `@Transactional`을 설정해서 사용하더라도, 전파 옵션이 `REQUIRED`로 설정되어 있는 한, 하나의 트랜잭셔이라도 `rollback-only`로 표시되어 있으면 전체 트랜잭션도 롤백된다. 

아래 그림은 레포지토리 계층의 `save()`에 `@Transactional`을 적용하는 경우이다.

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/required.png){: width="972" height="589" }_현재 프로젝트의 레포지토리 계층에 @Transactional을 적용하는 경우_

* 이전에 레포지토리 계층의 `save()`에 `@Transactional`을 적용하지 않았던 케이스와 다른 점은
  * 전체 트랜잭션이 `rollback-only`로 표시되는 것이 아니라, 내부 트랜잭션인 `트랜잭션2`가 `rollback-only`로 표시된다.
  * 외부 트랜잭션의 커밋 시점에서 `rollback-only`를 확인해서 `UnexpectedRollbackException`가 발생한다.

<br>

이를 해결하기 위해서 전파 옵션 `REQUIRES_NEW`가 등장한다.

<br>

---

### Propagation.REQUIRES_NEW

전파 옵션인 `Propagation.REQUIRES_NEW`를 사용하게 되면, 항상 새로운 트랜잭션을 만들게 된다. 

쉽게 말해서 외부 트랜잭션과 내부 트랜잭션을 완전히 분리해서 사용할 수 있게 된다. 완전히 분리해서 별도의 물리 트랜잭션으로 사용하기 때문에, 당연히 커밋과 롤백도 각각 별도로 이루어지게 된다. 이렇게 되면 트랜잭션이 `rollback-only`로 표시되어 롤백되어도 다른 트랜잭션에 영향을 주지 않는다.

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/rn.png){: width="972" height="589" }_REQUIRES_NEW를 사용하는 경우_

<br>

결론적으로 `UnexpectedRollbackException`를 해결하기 위해서는 레포지토리 계층 `save()`의 트랜잭션의 전파 속성을 `REQUIRES_NEW`로 사용하면 해결할 수 있을거로 예상이 된다.

<br>

> `REQUIRES_NEW` 사용시 주의점은 새로운 트랜잭션을 위해 커넥션을 추가로 사용하기 때문에 성능에 영향을 줄 수 있다. 현재 프로젝트의 경우, 중복 숏코드 처리가 자주 일어나는 상황이 아니기 때문에 크게 신경쓰지 않아도 될 것 같다.
{: .prompt-warning }

<br>

---

### 문제 해결

코드에 해결 방안을 적용해보자.

<br>

`UrlShortenerService`

```java
@Transactional
public String shortenUrl(String originalUrl) {
    String shortcode = null;
    try {
        shortcode = saveUrlMapping(originalUrl);
        em.flush();
        log.info("[No Duplication] shortcode = {}", shortcode);
    } catch (DataIntegrityViolationException | ConstraintViolationException e) {
        log.info("[Exception!] ", e);
        shortcode = handleShortcodeDuplication(originalUrl);
    }
    return shortcode;
}

public String saveUrlMapping(String originalUrl) {
    String shortcode = generateShortcode(originalUrl);
    UrlMapping urlMapping = new UrlMapping(shortcode, originalUrl, LocalDateTime.now());
    umr.save(urlMapping);
    return shortcode;
}

public String handleShortcodeDuplication(String originalUrl) {
    String newShortcode = generateShortcodeWithSalt(originalUrl);
    log.info("[Shortcode Duplication] Salted shortcode = {}", newShortcode);
    UrlMapping urlMapping = new UrlMapping(newShortcode, originalUrl, LocalDateTime.now());
    umr.save(urlMapping);
    return newShortcode;
}
```

<br>

`UrlMappingRepository`

```java
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void save(UrlMapping urlMapping) {
    em.persist(urlMapping);
}
```

<br>

테스트 코드를 실행해보면 이전과 다르게 전부 통과하는 것을 확인할 수 있다.

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/test.png){: width="640" height="150" }_테스트 코드 실행_



<br>

---

## 이슈 2

















