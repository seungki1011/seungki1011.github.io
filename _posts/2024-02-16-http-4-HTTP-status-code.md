---
title: (HTTP - 4) HTTP 상태 코드(Status Code) 
description: HTTP의 상태코드에 대해서
author: seungki1011
date: 2024-02-16 12:30:00 +0900
categories: [1. 컴퓨터 공학(CS), HTTP]
tags: [network, http]
math: true
mermaid: true
---

---

## 1xx, 2xx(Successful)

* **1xx(Informational)**
  * 요청이 수신되어 처리중
  * 거의 사용 안함

<br>

* **2xx(Successful)**

  * **요청을 정상 처리**

  * 200 OK 
    * 요청 성공 

  * 201 Created 
    * 요청 성공해서 새로운 리소스가 생성됨
    * 응답 메세지의 Location 필드에 생성된 리소스의 URI

  * 202 Accepted
    * 요청이 접수되었으나 처리가 완료되지 않음

  * 204 No Content
    * 요청을 성공적으로 수행했지만, 응답 페이로드 본문에 보낼 데이터가 없음
    * 예) 웹 문서 편집기의 save 버튼, save 버튼의 결과로 아무 내용이 없어도 된다

<br>

---

## 3xx(Redirection)

* **3xx(Redirection)**

  * 요청을 완료하기 위해 에이전트의 추가 행동(조치)이 필요하다

  * 웹 브라우저는 3xx 응답 결과에 ```Location```헤더가 있으면, ```Location```에 주어진 URL로 이동한다(Redirect) 

  * 300 Multiple Choices
    * 거의 사용하지 않음
  * **304 Not Modified**
    * **요청된 리소스를 재전송할 필요가 없음을 나타낸다. 캐시된 자원으로의 암묵적인 리다이렉션**
      * 쉽게 말해서 클라이언트에게 리소스가 수정되지 않았음을 알려준다
      * 클라이언트는 로컬 PC에 저장된 캐시를 재사용 (캐시로 리다이렉트)
    * 응답에 메세지 바디를 포함하면 안된다 (로컬 캐시를 사용해야함)
    * 조건부 ```GET, HEAD``` 요청시 사용

<br>

---

### 3xx - Permanent Redirection(영구 리다이렉션)

* **리다이렉션 상태 응답 코드는 요청한 리소스가 [`Location`](https://developer.mozilla.org/en-US/docs/Web/HTTP/Headers/Location) 헤더에 주어진 URI로 완전히 옮겨졌다는 것을 나타낸다**
  * 쉽게 말해서 리소스의 URI가 영구적으로 이동



* 예) ```/event``` → ```/new-event```
* 원래의 URL을 사용하지 않는다
* 검색 엔진에서도 변경을 인지



* **301 Moved Permanently**
  * 브라우저는 ```Location```에서 주어진 URI로 리다이렉트한다
  * 리다이렉트시 요청 메서드가 ```GET```으로 변한고, 본문이 제거될 수 있음



* **308 Permanent Redirect**
  * 301과 기능은 같지만, 리다이렉트시 요청 메서드와 본문을 유지한다
  * 웬만하면 이렇게 사용하지 않음, 그냥 요청을```GET```으로 돌리는 경우가 대부분



* 영구 리다이렉션 보다는 일시적 리다이렉션을 더 많이 사용

<br>

---

### 3xx - Temporary Redirection(일시적 리다이렉션)

* **요청한 리소스가 `Location` 헤더에 주어진 URI로 임시로 옮겨졌다는 것을 나타낸다**
  * 쉽게 말해서 리소스의 URI가 일시적으로 변경됨



* 검색 엔진은 리소스에 대한 링크를 업데이트하지 않는다
  * 쉽게 말해서 검색 엔진 등에서 URL을 변경하면 안됨 



* **302 Found**
  * 요청한 리소스가 `Location` 헤더에 주어진 URI로 임시로 옮겨짐
  * 리다이렉트시 요청 메서드가 ```GET```으로 변하고, 본문이 제거될 수 있다
  * 보통 302를 많이 사용



* **303 See Other**
  * 302와 기능은 같음
  * 리디렉션이 요청한 리소스 자체에 연결되지 않고 다른 페이지에 연결됨을 나타낸다
  * 리다이렉트시 요청 메서드가 ```GET```으로 변경된다



* **307 Temporary Redirect**
  * 302와 기능은 같음
  * 리다이렉트시 요청 메서드와 본문을 유지한다(요청 메서드를 변경하면 안된다)



* **일시적 리다이렉트를 사용하는 상황**
  * POST/REDIRECT/GET (PRG)
  * 문제 : ```POST```로 주문후에 웹 브라우저 새로고침하는 경우 → 새로고침은 다시 요청 → 중복 주문이 발생할 수 있다
  * 해결 : ```POST``` 주문후에 주문 결과를 ```GET``` 메서드로 리다이렉트 하도록 한다 → 새로고침을 해도 결과 화면을 ```GET```으로 조회

<br>

---

## 4xx (Client Error), 5xx (Server Error)

* **4xx (Client Error)**
  * 클라이언트 오류, 잘못된 문법, 등으로 서버가 요청을 수행할 수 없음
  * **오류의 원인은 클라이언트에 있음!**
  * 쉽게 말해서 클라이언트가 이미 잘못된 요청, 데이터를 보내고 있기 때문에, 백날 재시도 해봤자 똑같이 실패함
  * **400 Bad Request**
    * 클라이언트가 잘못된 요청을 해서 서버가 요청을 처리할 수 없음
    * 요청 구문, 메세지 등의 오류
    * **클라이언트는 요청 내용을 재검토하고 보내야한다**
    * 예) 요청 파라미터 잘못, 잘못된 API 스펙
  * **401 Unauthorized**
    * 인증(Authentication)이 없음
    * 응답에 ```WWW-Authenticate```헤더와 함께 인증 방법을 설명
      * Authentication : 본인이 누구인지 확인 (로그인)
      * Authorization : 권한 부여 (ADMIN 권한 처럼 특정 리소스에 접근할 수 있는 권한, 인증이 있어야 인가 가능)
  * **403 Forbidden**
    * 인증 자격은 있지만 접근 권한이 불충분한 경우
    * 예) 사용자 권한으로 로그인 → 어드민 등급 리소스에 접근
  * **404 Not Found**
    * 요청 리소를 찾을 수 없음
    * 권한이 부족한 클라이언트에게 해당 리소스를 숨기고 싶을때 사용하기도 함

<br>

* **5xx (Server Error)**
  * 서버 오류, 서버가 정상 요청을 처리하지 못한다
  * 서버에 문제가 있는 것이기 때문에 재시도하면 성공할 수 도 있음 (서버가 복구되거나 하는 경우)
  * **500 Internal Server Error**
    * 서버내부 문제
    * 서버에 문제가 생겼는데 애매하면 그냥 500 오류 사용
  * **503 Service Unavailable**
    * 서버가 일시적인 과부하 또는 예정된 작업으로 잠시 요청을 처리할 수 없음
    * ```Retry-After``` 헤더 필드에 얼마뒤에 복구되는지 보낼 수 있음
    * 많이 사용 안함
  * 웬만히면 서버 에러를 만들지 말자! → 500대 에러로 모니터링 툴들이 트리거 될 수 있음

---

## Reference

1. [인프런 - 모든 개발자를 위한 HTTP 웹 기본 지식](https://www.inflearn.com/course/http-%EC%9B%B9-%EB%84%A4%ED%8A%B8%EC%9B%8C%ED%81%AC/dashboard)
2. [널널한 개발자 - 네트워크 기초](https://www.youtube.com/watch?v=k1gyh9BlOT8&list=PLXvgR_grOs1BFH-TuqFsfHqbh-gpMbFoy)
3. HTTP 완벽 가이드
4. 네트워크 하향식 접근(Computer Networking a Top-Down Approach)