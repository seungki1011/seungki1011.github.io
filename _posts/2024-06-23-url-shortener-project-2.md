---
title: (Url Shortener - 2)URL 단축 서비스의 요구 사항 및 설계
description: 프로젝트의 요구 사항을 정리해보고, 설계하기.
author: seungki1011
date: 2024-06-23 10:30:00 +0900
categories: [Project, Url-Shortener]
tags: [project, backend]
pin: true
math: true
mermaid: true
---

---

## 요구 사항

요구 사항을 정해보자.

필수적인 요구사항과 옵션인 요구사항을 구분해서 정리해보자.

* 필수
  * 메인 페이지에서 바로 URL을 입력할 수 있는 폼
  * 입력한 URL에 대한 단축 URL을 제공
  * HTTP API로도 제공
  * 동일한 URL에 대해서도 다른 숏코드가 존재할 수 있다



* 옵션
  * 단축 URL에 비밀번호를 설정하는 기능
  * 단축 URL에 유효기간(expiration date) 설정

<br>

이제 도입할지 말지 고민 중인 회원가입과 관련된 요구 사항을 정리해보자.

- 회원 가입
  - OAuth를 통한 로그인
  - 회원(멤버) 전용 페이지
    - 단축 URL에 대한 클릭수 추적
    - 지금까지 단축한 URL에 대한 히스토리

---

## 기술 스택

다음의 기술 스택을 사용할 예정이다.

<br>

**Language**

* Java `17`

<br>

**Framework & Library**

* Spring Boot `3.3.1`
* Hibernate
* QueryDSL

* Junit5

* Thymeleaf

* Lombok

<br>

**Database**

* MySQL `8.0` (프로덕션)
* H2 `2.2.224` (테스트)

<br>

`build.gradle`

```java
plugins {
	id 'java'
	id 'org.springframework.boot' version '3.3.1'
	id 'io.spring.dependency-management' version '1.1.5'
}

group = 'com.seungki'
version = '0.0.1-SNAPSHOT'

java {
	toolchain {
		languageVersion = JavaLanguageVersion.of(17)
	}
}

configurations {
	compileOnly {
		extendsFrom annotationProcessor
	}
}

repositories {
	mavenCentral()
}

dependencies {
	implementation 'org.springframework.boot:spring-boot-starter-data-jpa'
	implementation 'org.springframework.boot:spring-boot-starter-thymeleaf'
	implementation 'org.springframework.boot:spring-boot-starter-web'
	compileOnly 'org.projectlombok:lombok'
	runtimeOnly 'com.h2database:h2'
	runtimeOnly 'com.mysql:mysql-connector-j'
	annotationProcessor 'org.projectlombok:lombok'
	testImplementation 'org.springframework.boot:spring-boot-starter-test'
	testRuntimeOnly 'org.junit.platform:junit-platform-launcher'

	implementation 'org.springframework.boot:spring-boot-devtools'

	implementation 'org.springframework.boot:spring-boot-starter-validation'

	implementation 'com.querydsl:querydsl-jpa:5.0.0:jakarta'
	annotationProcessor "com.querydsl:querydsl-apt:" +
			"${dependencyManagement.importedProperties['querydsl.version']}:jakarta"
	annotationProcessor "jakarta.annotation:jakarta.annotation-api"
	annotationProcessor "jakarta.persistence:jakarta.persistence-api"

	implementation 'com.github.gavlyukovskiy:p6spy-spring-boot-starter:1.9.0'
}

tasks.named('test') {
	useJUnitPlatform()
}

clean {
	delete file('src/main/generated')
}
```

---

## 도메인 설계



































