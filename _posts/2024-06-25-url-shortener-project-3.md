---
title: (Url Shortener - 3)URL 단축 서비스 개발 시작, 발생한 문제들
description: 프로젝트의 개발을 시작하면서 했던 고민과 만났던 문제들.
author: seungki1011
date: 2024-06-25 10:30:00 +0900
categories: [Project, Url-Shortener]
tags: [project, backend]
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
* 빌더 클래스를 작성하지는 않기로 함

<br>

이전 포스트에서 대략적으로 정한 설계대로 개발을 시작하면서 만났던 문제들을 살펴보자.

<br>

---

## `UnexpectedRollbackException`

### 문제 발생 상황

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

* 테스트 코드에서는 숏코드가 중복되면 `ConstraintViolationException` 발생하고, 서비스 계층에서 정상적으로 처리하는 것 까지 확인 가능

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/rollbackexception.png){: width="972" height="589" }_동일한 URL POST 요청 두 번_ 

* 동일한 URL에 대해서 `POST` 요청을 두 번 수행하는 경우, 두 번째 요청에서 `UnexpectedRollbackException` 발생

---

### 문제 재현

문제 상황을 재연해보자.

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

---

### 원인 파악 

`UnexpectedRollbackException`이기 때문에 트랜잭션 전파와 관련된 문제로 보인다.



















