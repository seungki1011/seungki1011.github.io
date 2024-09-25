---
title: (Url 단축 - 4) URL 단축 서비스 API 개발
description: API 개발, 개선점, 후기
author: seungki1011
date: 2024-07-05 10:30:00 +0900
categories: [Project, Url 단축 API와 서버사이드 페이지]
tags: [project, backend, trouble-shooting, spring, rest-api]
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

## API 설계

API는 다음과 같이 설계했다.

<br>

| 메서드 |          API 경로           | 출력 포맷 |              요청 파라미터               |           요청 본문            |          기능 설명          |
| :----: | :-------------------------: | :-------: | :--------------------------------------: | :----------------------------: | :-------------------------: |
| `POST` |      `api/v1/shorten`       |   JSON    |                                          | `url` : 단축할 원본 URL (JSON) |          URL 단축           |
| `GET`  | `api/v1/detail/{shortcode}` |   JSON    | `shortcode` : 단축 URL 숏코드 (`String`) |                                | 단축한 URL의 상세 정보 조회 |

<br>

---

## API 예외 처리

웹 브라우저로 화면을 제공하는 경우에 에러가 발생하면 단순히 `4xx`, `5xx`와 관련된 오류 화면을 보여주거나, 필요하면 특정 에러 페이지를 만들어서 보여주면 된다. 반면에 API는 상황과 예외에 따라서 응답으로 출력하는 데이터가 달라질 수 있다. 쉽게 말해서 세밀한 제어가 필요하다.

이전 포스트에서 HTML 화면을 제공할 때 `@ControllerAdvice`와 `@ExceptionHandler`를 사용해서 특정 예외 별로 오류 페이지가 나가도록 설정을 했다. 그러나 **보통의 경우 `@RestControllerAdvice`와 `@ExceptionHandler`를 이용한 전역 `ApiExceptionHandler`를 만들어서 API에 대한 예외 핸들링**을 한다.

많은 경우 API 예외를 처리하기 위해서 다음의 클래스를 구성한다.

* 전역으로 API 예외를 처리하기 위한 핸들러 클래스인 `ApiExceptionHandler`
* 예외 케이스를 관리하기 위한 `enum` 클래스인 `ErrorCode` 클래스

<br>

---

## 개섬할 점

- 에러 핸들링을 더 깔끔하게 처리할 방법이 있을 것이다
- **API 개선**
  - URL을 리스트로 여러 개 받아서 단축 URL로 변환 할 수 있도록 구현
  - URL을 단축하는 API의 결과를 상세 정보로 받는 것이 아닌 원본 URL과 단축 URL만 받을 수 있도록 구현
  - 요청 검증을 더 자세히한다(현재 검증이 너무 단순하다. 검증을 해야하는 부분이 훨씬 많을 것이다.)
  - 에러 메세지에 필요 없는 내용은 출력하지 않도록 수정(`trace`를 로그를 통해서 확인하도록 수정. 유저는 굳이 `trace`를 알 필요 없다.)
- **API 응답 클래스를 만들어서 사용하기**
  - 공통의 응답 클래스를 만들어서 API 정상 응답, 예외 응답을 더 일정하게 줄 수 있다
  - 이는 클라이언트 개발자와의 협업에서도 중요하다
  

<br>

---

## 결과

### 서버 사이드 랜더링

<br>

![스크린샷 2024-07-15 오전 10.13.24](../post_images/2024-07-01-url-shortener-project-4/view1.png)_URL 입력 폼_

<br>

![스크린샷 2024-07-15 오전 10.13.41](../post_images/2024-07-01-url-shortener-project-4/view2.png)_단축 결과 상세 페이지_

<br>

![스크린샷 2024-07-15 오전 10.14.27](../post_images/2024-07-01-url-shortener-project-4/view3.png)_URL 검증_

<br>

---

### API

포스트맨(PostMan)을 통해서 확인.

<br>

![스크린샷 2024-07-15 오후 12.51.50](../post_images/2024-07-01-url-shortener-project-4/api1.png)_URL 단축 요청 성공_

<br>

![스크린샷 2024-07-15 오후 12.50.46](../post_images/2024-07-01-url-shortener-project-4/api2.png)_URL 단축 요청 실패_

<br>![스크린샷 2024-07-15 오후 12.52.47](../post_images/2024-07-01-url-shortener-project-4/api3.png)_단축 URL 상세 정보 조회 성공_

<br>

![스크린샷 2024-07-15 오후 12.53.07](../post_images/2024-07-01-url-shortener-project-4/api4.png)_단축 URL 상세 정보 조회 실패_

<br>

---

## 느낀점

멘토 없이 혼자 공부하는게 너무 어렵다. 코드 리뷰가 없으니 내가 정말 똑바로 만들고 있는지 의심이 들어서 참 힘들었다..

~~열심히 구글링하면서, 다른 사람들 깃헙에서 코드 리뷰 받은 것을 최대한 활용하려고 했다~~

<br>

---

## 앞으로 공부할 내용

* TDD와 더불어서 여러 테스트 프레임워크의 사용법 학습
  * 이번 프로젝트에서도 테스트를 하면서 진행하긴 했지만 그냥 남들이 작성한 테스트를 참고하면서 감으로 구현한 것에 불과하다
* Spring Data JPA 학습
  * 스프링 데이터를 학습해서 다음 프로젝트에 적용하기
* AOP 적용
* 더 복잡한 데이터 모델을 사용하는 프로젝트 진행하기
  * 이번 프로젝트는 너무 단순해서 데이터 모델링을 제대로 해볼 기회가 없었다
* API 보안 적용
  * OAuth2
  * JWT
  * 세션
  * 스프링 시큐리티
* 모니터링 적용
  * 스프링 부트 액츄에이터 사용 vs 사용하지 않고 적용
  * Prometheus
  * Grafana
* 캐시 서버 적용
  * Redis

<br>

프로젝트 깃헙 주소: [https://github.com/seungki1011/url-shortener](https://github.com/seungki1011/url-shortener)
