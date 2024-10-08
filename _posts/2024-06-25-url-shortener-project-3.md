---
title: (Url 단축 - 3) URL 단축 서비스 개발 시작, 발생한 문제들
description: 프로젝트의 개발을 시작하면서 했던 고민과 만났던 문제와 트러블 슈팅
author: seungki1011
date: 2024-06-25 10:30:00 +0900
categories: [Project, Url 단축 API와 서버사이드 페이지]
tags: [project, backend, transaction, trouble-shooting, spring]
pin: false
math: true
mermaid: true
project_overview: "스프링 부트 연습을 위해 Bitly와 같은 URL 단축기를 만들어보는 토이 프로젝트입니다."
project_start_date: "2024/06/23"
project_end_date: "2024/07/13"
project_topic: "백엔드"
project_tech_stack: "Java17, Lombok, H2 2.2.224, SpringBoot 3.3.1, JPA(Hibernate), JUnit5, Thymeleaf"
project_team_size: 1
project_github: "https://github.com/seungki1011/url-shortener"
---

---

> **주의**
>
> 해당 프로젝트는 자바, 스프링 부트, JPA를 처음 사용해본 사람이 진행한 프로젝트입니다.
{: .prompt-danger }


---

## 1. 이슈 1 : UnexpectedRollbackException

### 이슈 발생 배경

동일한 URL로 URL 단축을 위한 `POST` 요청을 보내게 되면 첫 번째 요청은 정상적으로 수행되지만, 두 번째 요청에서`ConstraintViolationException`이 발생한다. `ConstraintViolationException`이 발생하는 원인은 동일한 URL에 대해서 같은 숏코드가 나오고, **중복 숏코드를 처리하는 로직을 구현하지 않았기 때문**이다.

중복된 숏코드를 처리하기 위해서 다음의 중복 처리 로직을 구현하기로 했다.
* 숏코드를 생성했을 때 `ConstraintViolationException`이 발생한다면, 서비스 계충에서 잡아서 핸들링한다
* 핸들링 로직은 **원본 URL에 랜덤 솔트(salt)를 추가해서 해당 값으로 숏코드를 재생성**한다. 물론 **원본 URL은 동일하게 저장**한다.
* 예시: `https://abc123.com` + `saltvalue` = `https://abc123.comsaltvalue`에 해싱

<br>

진짜 문제는 다음의 상황에서 발생한다.
* `@Transactional`이 붙은 테스트 코드에서 **동일한 숏코드가 생성되도록 이미 한번 사용한 원본 URL을 사용해서 서비스 계층의 테스트를 진행 하는 경우**, 정상적으로 **예외를 핸들링하고 숏코드로 새로운 값으로 재생성하는 것을 확인**할 수 있었다.
* **컨트롤러 계층 테스트를 위해서 동일한 URL로 포스트 요청을 두 번하는 경우, 두 번째 요청에서 `UnexpectedRollbackException`이 발생하고, 예상한대로 동작하지 않는다는 문제가 발생한다.**
* 여기서 예상한대로의 동작은 **두 번째 요청에서 같은 숏코드가 발생하는 경우 숏코드 재생성을 통한 예외 핸들링 동작을 의미**한다

<br>

그림으로 상황을 살펴보자.

![shortcodeissue1](../post_images/2024-06-25-url-shortener-project-3/shortcodeissue1.png)_문제 발생 상황_

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/constraint1.png){: width="972" height="589" }

![clickreq](../post_images/2024-06-25-url-shortener-project-3/constraint2.png){: width="972" height="589" }_ConstraintViolationException 발생_

* 테스트 코드에서 숏코드가 중복되면 `ConstraintViolationException` 발생하고, 서비스 계층에서 정상적으로 처리하는 것 까지 확인할 수 있었다

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/rollbackexception.png){: width="972" height="589" }_동일한 URL POST 요청 두 번_ 

* 반면에 동일한 URL에 대해서 `POST` 요청을 두 번 수행하는 경우, 두 번째 요청에서 `UnexpectedRollbackException`이 발생한다

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

* `generateShortcode()`: 원본 URL을 입력으로 받아서 숏코드를 생성해주는 메서드
* `generateShortcodeWithSalt()`: 원본 URL을 입력으로 받고, 해당 URL에 솔트를 추가해서 숏코드를 생성해주는 메서드
  * 이 메서드는 숏코드가 중복되어 예외가 발생한 경우, 핸들링을 위해서 사용한다

<br>

`UrlShortenerController`

```java
@PostMapping("/shorten")
public String shortenUrl(@RequestParam("url") String originalUrl, RedirectAttributes redirectAttributes) {
    String shortcode = uss.shortenUrl(originalUrl);
    redirectAttributes.addAttribute("shortcode", shortcode);
    return "redirect:/detail/{shortcode}";
}
```

* 단축하고 싶은 URL을 입력해서 `POST` 요청을 보내서 성공적으로 처리되면, 해당 숏코드를 `PathVariable`로 사용해서, `/detail/{shortcode}`로 리다이렉트한다
* 해당 페이지는 결과 단축 URL을 링크로 제공한다

<br>

다음은 테스트 코드이다.

```java
@SpringBootTest
@AutoConfigureMockMvc
public class TestDuplicateShortcode {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UrlShortenerService uss;

    @DisplayName("중복된 URL로 URL 단축을 수행하는 경우 숏코드가 서로 달라야 한다")
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

* **"중복된 URL로 URL 단축을 수행하는 경우 숏코드가 서로 달라야 한다"**
  * 동일한 URL로 `shortenUrl(originalUrl)`을 두 번 호출하면, 두 번째 호출에서는 예외를 처리해서 숏코드를 재생성해야 한다
  * 기존 숏코드와 예외 핸들링 이후의 숏코드를 비교하면 달라야한다
  * **이 테스트는 통과**했다
* **"같은 URL을 이용한 POST 요청은 성공해야 한다"**
  * 동일한 URL로 `/shorten`으로 `POST` 요청을 두 번 수행하면, **두 번째 요청에서는 변경된 숏코드로 응답을 주어야한다**
  * **두 번째 요청에서 `UnexpectedRollbackException`이 발생해서, 기대한 결과가 나오지 않는다**

<br>

---

### 원인 파악 

`UnexpectedRollbackException`이기 때문에 트랜잭션 전파와 관련된 문제로 보인다.

<br>

> **`UnexpectedRollbackException`이란?**
> 
> *Thrown when an attempt to commit a transaction resulted in an unexpected rollback.*
> 
>`rollback-only`로 표기된 트랜잭션을 커밋하려고 시도하는 경우 발생한다.
> 
>참고 : [https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/UnexpectedRollbackException.html](https://docs.spring.io/spring-framework/docs/current/javadoc-api/org/springframework/transaction/UnexpectedRollbackException.html)
{: .prompt-info }

<br>

일단 현재 트랜잭션이 어떻게 수행되고 있는지 파악하기로 했다.

![transactionfail1](../post_images/2024-06-25-url-shortener-project-3/transactionfail1.png)_현재 상황_

두 번째 요청에서 **이전과 동일한 URL을 사용해서 같은 숏코드가 생성된 상황이라고 가정**하자. 

* 서비스 계층의 `shortenUrl()`부터 트랜잭션이 시작된다
* `shortenUrl()`의 내부 로직에서 숏코드를 생성하고, 레포지토리 계층의 `save()`를 호출하게 된다
* 이미 존재하는 숏코드를 DB에 넣으려고 하면 `ConstraintViolationException`이 발생한다
* 예외가 발생했기 때문에 현재의 트랜잭션은 `rollback-only`로 표시된다
* 이 경우에 서비스 계층에서 예외를 받아서 처리해도, 트랜잭션은 이미 `rollback-only`로 표시되어 있기 때문에 `UnexpectedRollbackException`이 발생한다

<br>

이 문제를 해결하기 위해서는 **서비스 계층의 `shortenUrl()`에서 시작된 트랜잭션을 어떻게든 정상적으로 커밋되도록 만들어야한다**.

이를 위해서는 **트랜잭션 전파의 속성 중에 `REQUIRES_NEW`를 사용해서 해결**할 수 있다.

<br>

---

### 트랜잭션 전파(Transaction Propagation)

자세히 들어가기 전에 먼저 트랜잭션의 전파에 대해 복습해보자.

> *트랜잭션이 이미 진행중인 상황에서 추가로 트랜잭션을 수행하게 되는 경우 어떻게 동작할까?*
>
> **트랜잭션 중에 새로운 트랜잭션이 수행되는 경우 어떻게 동작할지 결정하는 것을 트랜잭션 전파(Transaction Propogation)**라고 한다.

<br>

스프링에서 이런 트랜잭션 전파의 속성을 설정할 수 있으며, 기본 옵션은 `REQUIRED`이다. **`REQUIRED`의 트랜잭션 전파는 다음과 같이 동작**한다.

* 처음 수행되는 트랜잭션을 외부 트랜잭션이라고 한다
* 외부 트랜잭션이 진행 도중에 호출되는 트랜잭션은 내부 트랜잭션이 된다
* 내부 트랜잭션은 외부 트랜잭션에 참여한다고 표현한다
* **스프링은 외부 트랜잭션과 내부 트랜잭션을 하나의 물리 트랜잭션으로 묶는다**
  * 물리 트랜잭션: 실제 데이터베이스에 적용되는 트랜잭션
* 외부 트랜잭션과 내부 트랜잭션은 **각각 논리 트랜잭션으로 취급**된다

<br>

디폴트 옵션인 **`REQUIRED`는 다음의 기본 원칙**을 가진다

* **모든 논리 트랜잭션이 커밋되어야 물리 트랜잭션이 커밋**된다
* **하나의 논리 트랜잭션이라도 롤백되면, 전체 트랜잭션도 롤백**된다

<br>

![transactioncase](../post_images/2024-06-25-url-shortener-project-3/transactioncase.png)_기본 전파 옵션 REQUIRED_

정리하자면 `REQUIRED`는 다음 처럼 행동하게 된다.

- 외부/내부 트랜잭션 모두 커밋 되면 물리 트랜잭션도 커밋
- 내부 트랜잭션이 롤백되면 물리 트랜잭션도 롤백
- 외부 트랜잭션이 롤백되면 물리 트랜잭션도 롤백

<br>

여기서 알 수 있는 것은, 만약 나의 서비스 계층과 레포지토리 계층에 전부 `@Transactional`을 설정해서 사용하더라도, **전파 옵션이 `REQUIRED`로 설정되어 있는 한, 하나의 트랜잭셔이라도 `rollback-only`로 표시되어 있으면 전체 트랜잭션도 롤백**된다. 

아래 그림은 레포지토리 계층의 `save()`에 `@Transactional`을 적용하는 경우이다.

![requiredstrat](../post_images/2024-06-25-url-shortener-project-3/requiredstrat.png)

_현재 프로젝트의 레포지토리 계층에 @Transactional을 적용하는 경우_

* 이전에 레포지토리 계층의 `save()`에 `@Transactional`을 적용하지 않았던 케이스와 다른 점은 다음과 같다.
  * 전체 트랜잭션이 `rollback-only`로 표시되는 것이 아니라, 내부 트랜잭션인 `트랜잭션2`가 `rollback-only`로 표시된다.
  * 외부 트랜잭션의 커밋 시점에서 `rollback-only`를 확인해서 `UnexpectedRollbackException`가 발생한다.

<br>

이를 해결하기 위해서 전파 옵션 `REQUIRES_NEW`가 등장한다.

<br>

---

### Propagation.REQUIRES_NEW

전파 옵션인 `Propagation.REQUIRES_NEW`를 사용하게 되면, 항상 새로운 트랜잭션을 만들게 된다. 

쉽게 말해서 **외부 트랜잭션과 내부 트랜잭션을 완전히 분리해서 사용할 수 있게** 된다. 완전히 분리해서 별도의 물리 트랜잭션으로 사용하기 때문에, 당연히 **커밋과 롤백도 각각 별도로 이루어지게 된다**. 이렇게 되면 트랜잭션이 `rollback-only`로 표시되어 롤백되어도 다른 트랜잭션에 영향을 주지 않는다.

<br>

![newsolution](../post_images/2024-06-25-url-shortener-project-3/newsolution.png)_REQUIRES_NEW를 사용하는 경우_

<br>

결론적으로 **`UnexpectedRollbackException`를 해결하기 위해서는 레포지토리 계층 `save()`의 트랜잭션의 전파 속성을 `REQUIRES_NEW`로 사용하면 해결할 수 있을거로 예상**이 된다.

<br>

> **주의**
>
> `REQUIRES_NEW` 사용시 주의점은 **새로운 트랜잭션을 위해 커넥션을 추가로 사용하기 때문에 성능에 영향**을 줄 수 있다. 현재 프로젝트의 경우, 중복 숏코드 처리가 자주 일어나는 상황이 아니기 때문에 크게 신경쓰지 않아도 될 것 같다.
{: .prompt-warning }

<br>

---

### 문제 해결

코드에 해결 방안을 적용해보자.

<br>

```java
@Transactional
public String shortenUrl(String originalUrl) {
    String shortcode = null;
    try {
        shortcode = saveUrlMapping(originalUrl);
        log.info("[중복 없음] shortcode = {}", shortcode);
    } catch (DataIntegrityViolationException | ConstraintViolationException e) {
        log.error("[예외 발생] ", e);
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
    log.info("[숏코드 중복 발생] Salted shortcode = {}", newShortcode);
    UrlMapping urlMapping = new UrlMapping(newShortcode, originalUrl, LocalDateTime.now());
    umr.save(urlMapping);
    em.flush();
    return newShortcode;
}
```

<br>

`UrlMappingRepository`: 레포지토리의 `save()`에 `Propagation.REQUIRES_NEW` 적용

```java
@Transactional(propagation = Propagation.REQUIRES_NEW)
public void save(UrlMapping urlMapping) {
    em.persist(urlMapping);
}
```

<br>

테스트 코드를 실행해보면 전부 통과하는 것을 확인할 수 있다.

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/test.png){: width="640" height="150" }_테스트 코드 실행_

<br>

---

## 2. 이슈 2 : 리다이렉트 실패

### 이슈 발생 배경

원본 URL의 접두사(prefix)에 `http://` 또는 `https://`와 같은 프로토콜을 붙이지 않으면 리다이렉트가 정상적으로 이루어지지 않는다

<br>

---

### 이슈 재현

* 단축할 URL을 `www.google.com`으로 입력한다.
* 단축된 URL에 GET 요청을 보낸다
* 리다이렉트 결과는 `http://localhost:8080/www.google.com`로 나온다.
* 의도한 결과는 `https://www.google.com`으로 리다이렉트 되는 것이다

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/issue2-2.png){: width="640" height="150" }_의도하지 않은 결과가 나왔다_

<br>

---

### 원인 파악

리다이렉트에 대한 스프링의 공식문서를 찾아보기로했다.

<br>

> The special `redirect:` prefix in a view name lets you perform a redirect. The `UrlBasedViewResolver` (and its subclasses) recognize this as an instruction that a redirect is needed. The rest of the view name is the redirect URL.
>
> The net effect is the same as if the controller had returned a `RedirectView`, but now the controller itself can operate in terms of logical view names. A logical view name (such as `redirect:/myapp/some/resource`) redirects relative to the current Servlet context, while a name such as `redirect:https://myhost.com/some/arbitrary/path` redirects to an absolute URL.
>
> 참고 : [https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet/viewresolver.html#mvc-redirecting-redirect-prefix](https://docs.spring.io/spring-framework/reference/web/webmvc/mvc-servlet/viewresolver.html#mvc-redirecting-redirect-prefix)
{: .prompt-warning }

<br>

스프링의 `redirect`는 접두사로 `http://` 또는 `https://`가 붙지 않으면 상대 경로로 취급하는 것 같다. 반면에 프로토콜 접두사를 붙이는 경우 절대 경로로 인식한다.

그러면 해결방법은 간단하다. URL 앞에 `http://` 또는 `https://`가 붙지 않은 경우를 검증해서 해당 프로토콜 URL 앞에 추가해주거나, URL에 프로토콜을 추가하라는 메세지를 보여주는 로직을 구현하면 된다.

<br>

---

### 문제 해결

다음 두 가지 방법을 생각했다. (클라이언트 사이드는 배제)

먼저 정규 표현식으로 **사용자가 입력한 URL을 특정 패턴(프로토콜 여부, ASCII 이외의 문자인지 여부)에 속하는지 검증**한다.

1. **검증에 통과하지 못하면 오류를 발생시키고, 알맞은 URL을 입력하라고 메세지를 보여준다**
   * 패턴 검증
   * 검증 실패시 오류 발생
   * 해당 오류 메세지를 출력
2. 앞에 프로토콜을 붙이지 않는 경우 자동으로 `http://`를 붙여준다

<br>

이 중에서 **1번 방법을 사용**했다. 이유는 다음과 같다.

* 상대적으로 구현하기 쉽다
* 프로토콜이 붙었는지 검증하는 것도 포함해서, URL로 사용하는 것이 어려운 문자(한글, ASCII에 포함되지 않는 문자, 몇몇 특수 문자)가 들어가는 경우까지 한번에 검증할 수 있다
* 2번은 클라이언트 사이드에서 해당 로직을 구현하는 것이 효율적일거라고 생각했다

<br>

먼저 테스트 코드를 작성했다.

```java
@Slf4j
@SpringBootTest
@AutoConfigureMockMvc
public class TestUrlValidation {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private UrlShortenerService uss;

    @DisplayName("앞에 프로토콜을 붙이지 않은 URL을 사용했을때 검증을 통과하지 못하고 에러가 발생한다")
    @Test
    public void test_no_protocol() throws Exception {

        String invalidUrl = "www.google.com";

        ResultActions result = mockMvc.perform(MockMvcRequestBuilders.post("/shorten")
                .param("url", invalidUrl));

        result.andExpect(status().isOk())
                .andExpect(view().name("shortener_form"))
                .andExpect(model().attributeHasFieldErrors("urlShortenRequest", "url"));

    }

    @DisplayName("검증 패턴을 만족하지 못하는 URL을 사용하면 검증을 통과하지 못하고 에러가 발생한다")
    @Test
    public void test_unsafe_url() throws Exception {

        String invalidUrl = "한글이들어간Url.com";

        ResultActions result = mockMvc.perform(MockMvcRequestBuilders.post("/shorten")
                .param("url", invalidUrl));

        result.andExpect(status().isOk())
                .andExpect(view().name("shortener_form"))
                .andExpect(model().attributeHasFieldErrors("urlShortenRequest", "url"));

    }
    
}
```

* URL 앞에 프로토콜(`http://`, `https://`)이 붙지 않는 경우와 URL로 가능한 문자가 들어 있는 경우를 검증하기 위한 테스트를 작성했다
  * URL이 가능한 문자라는 것은 다음의 패턴을 말한다 `[a-zA-Z0-9-._~:/?#@!$&'()*+,;=%]+`
* 검증에 실패해서 에러가 생기는 경우, 기존 입력 폼의 뷰를 반환하도록 기존 컨트롤러를 수정할 것이다
  * 그렇기 때문에 `status().isOk()`를 기대한다
  * 해당 `url` 필드에 대한 에러도 기대한다

<br>

 테스트를 통과 시키기 위해서 `UrlShortenRequest`라는 DTO를 만들어서 두 가지 케이스에 대한 검증을 적용하면 된다.

<br>

`UrlShortenRequest`

```java
@Getter
public class UrlShortenRequest {
    @NotEmpty(message = "URL은 공백을 허용하지 않습니다")
    @Pattern.List({
            @Pattern(
                    regexp = "^(http://|https://).*",
                    message = "URL은 http:// 또는 https://로 시작해야 합니다"
            ),
            @Pattern(
                    regexp = "[a-zA-Z0-9-._~:/?#@!$&'()*+,;=%]+",
                    message = "URL은 영문자, 숫자 그리고 특수 문자(._~:/?#@!$&'()*+,;=%)만 허용합니다"
            )
    })
    private String url;

    public void setUrl(String url) {
        this.url = url;
    }
}
```

<br>

해당 `UrlShortenRequest`를 사용하기 위해서 컨트롤러를 다시 수정해야한다.

```java
@GetMapping({"/", "/shorten"})
public String shortenerForm(Model model) {
    model.addAttribute("urlShortenRequest", new UrlShortenRequest());
    return "shortener_form";
}

@PostMapping("/shorten")
public String shortenUrl(@ModelAttribute("urlShortenRequest") @Validated UrlShortenRequest usr,
                         BindingResult bindingResult,
                         RedirectAttributes redirectAttributes) {
    if (bindingResult.hasErrors()) {
        return "shortener_form";
    }

    String shortcode = uss.shortenUrl(usr.getUrl());
    redirectAttributes.addAttribute("shortcode", shortcode);
    return "redirect:/detail/{shortcode}";
}
```

<br>

해당 컨트롤러에 맞게 에러가 발생할 경우 에러 메세지를 출력할 수 있도록 뷰에 타임리프 코드를 추가한다.

이제 다시 기존 테스트를 돌려보자.

<br>

기존에는 아무런 검증이 적용되어 있지 않았기 때문에 잘못된 형식의 URL을 입력해도 단축 URL로 만들어서 보여줬다. 그러나 검증 적용 후에는 에러를 발생시킨다.

<br>

![clickreq](../post_images/2024-06-25-url-shortener-project-3/validtest.png){: width="640" height="150" }_검증 테스트_

<br>

이제 테스트를 전부 통과한다.

<br>

---

## 3. 중간 점검

중간 점검을 해보자.

* 굳이 `/shorten`을 경로로 매핑할 필요가 없을 것 같다. `/`을 사용하는 것을 고려하자
* 자바의 `UrlConnection` 클래스를 사용하도록 리팩토링을 고려하자
  * URL에 대한 다양한 API를 제공한다
  * 예시: 사용자가 입력한 URL이 정말 존재하는 URL인지 확인하는 로직을 추가할 수 있다
* **중복 숏코드를 처리하는 로직을 반복문을 사용하도록 수정**하자
  * 중복되지 않을 때 까지 계속 검사
* 숏코드 **중복을 미리 검사해서, 중복되면 `ShortcodeDuplicationException` 같은 커스텀 예외를 던지는 방식**을 사용하면 어떨까?
  * 중복 가능성이 낮기 때문에 DB에서 올라오는 예외를 잡는 방식을 사용하고 있는데, 생각해보니 시스템 **안정성을 생각한다면 미리 중복을 검사해서 잡는 것이 더 좋은 방법**일 것 같다
  
* 다수의 스레드에서 **동시에 같은 URL에 대해 단축 URL을 생성하는 상황**이 발생하면 중복이 발생할 수 있다. 또는 동시에 단축 URL에 접근해서, 조회 카운트가 제대로 집계되지 않는 상황이 발생할 수 있다.
  * **낙관적, 비관적 락의 사용을 고려**해보자
* 추가적인 예외 상황을 파악해서 대비한다
  * 숏코드를 통해 상세정보를 확인할때 해당 숏코드가 DB에 존재하지 않는 경우
  * 단축URL을 통한 요청(`GET: /{shortcode}`)에 대해 숏코드가 DB에 존재하지 않는 경우
  * 중복 재생성 로직을 반복 후에도 문제가 발생하는 경우


* 매개 변수가 많으면 빌더 패턴을 사용하는 것을 고려하자
* **DTO 변환을 어느 계층에서 하는 것이 좋은지 찾아보자**.
* 스프링 데이터 JPA를 사용하자
  * 레포지토리 계층의 구현이 더 간단해진다
  * `Audit`과 더불어서 많은 편의 기능을 제공한다
* 테스트 프레임워크에 대한 공부가 필요하다.(~~지금은 눈치껏 감으로 작성하고 있지만, 더 세밀한 테스트를 위해서는 학습이 필요하다~~)

