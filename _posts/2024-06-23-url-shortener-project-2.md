---
title: (Url Shortener - 2) URL 단축 서비스의 요구 사항 및 설계
description: 프로젝트의 요구 사항을 정리해보고, 설계하기.
author: seungki1011
date: 2024-06-23 10:30:00 +0900
categories: [Project, Url-Shortener]
tags: [project, backend]
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

## 1. 요구 사항

요구 사항을 정해보자.

* SSR(타임 리프로 구현)
  * 메인 페이지에서 바로 URL을 입력할 수 있는 폼
  * 단축 URL에 대한 상세 정보를 볼 수 있는 페이지
    * 예: 생성된 날짜, 단축 URL 사용 횟수, 원본 URL 
* HTTP API도 제공한다
* 원본 URL에 대한 단축 URL을 제공한다
* 단축 URL에 대한 상세 정보를 제공한다
* 동일한 URL에 대해서도 다른 숏코드가 존재할 수 있다
* 단축 URL 사용 횟수 기록

<br>

---

## 2. 기술 스택

다음의 기술 스택을 사용할 예정이다.

* Java `17`

* Spring Boot `3.3.1`
* JPA(Hibernate)
* Junit5
* Thymeleaf
* Lombok
* H2 `2.2.224`

<br>

---

## 3. 서비스 제공의 흐름

사용하기로 구현 방법을 다시 살펴보자.

* 프로젝트에서는 해시값을 Base62 인코딩해서 앞 7자를 잘라서 사용하는 방식으로 구현할 것이다.
* 중복 숏코드를 처리하는 로직은 해시 충돌 때문에 중복이 되든, 같은 원본 URL이 이미 존재해서 중복이 되든 그냥 숏코드를 다시 생성하는 방식으로 처리할 것이다.

<br>

![clickreq](../post_images/2024-06-23-url-shortener-project-2/improve.png){: width="972" height="589" }

<br>

![clickreq](../post_images/2024-06-23-url-shortener-project-2/design1.png){: width="972" height="589" }_로직의 흐름에 대해 컨트롤러, 서비스, 레포지토리 계층을 표현한 그림_

<br>

---

## 4. 고민

경험이 없으니 이것이 제대로 된 설계인지 아직 감이 안잡힌다.

* 숏코드로 변환시키거나, 뷰카운트(조회수)를 증가시키는 로직을 서비스 계층이 아니라 엔티티 클래스에 같이 넣어야할지 고민된다.
* 단순히 값만 조회하는 로직은 서비스 계층 없이 그냥 바로 레포지토리 계층에서 호출해도 될지 고민된다.

<br>

일단 개발을 시작하고, 차차 바꿔나갈 생각이다.

다음 포스트에서는 개발 도중 생겨난 이슈의 트러블슈팅을 다룰 예정이다.
