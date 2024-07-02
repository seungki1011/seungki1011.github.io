---
title: (Java - 5) 메서드(Method)
description: 자바에서의 메서드
author: seungki1011
date: 2024-01-03 12:30:00 +0900
categories: [Java]
tags: [java]
pin: true
math: true
mermaid: true
---

---

## 1) 메서드(Method)

* 특정 작업을 수행하는 코드의 집합
* 메서드명은 동사로
* 코드의 용이한 모듈화, 재사용성 증가 등으로 유지보수가 쉬워짐
* 메서드는 멤버변수와 더불어서 클래스의 속성 중 하나
* 메서드 호출을 하면 파라미터에 인수(argument) 대입
* 값을 반환 하지 않는 경우 반환 타입 ```void```



* 메소드는 ```return```을 만나면 종료
  * ```void```는 ```return```생략 가능

<br>


```java
접근제어자 리턴타입 메소드이름(parameters) {
  // 구현
}
```

<br>

```java
public class method1 {
    public static void main(String[] args) {
        System.out.println("method result 1: " + avg(1,2));
        System.out.println("method result 2: " + avg(49,78));
        startMsg();
    }

    // 1. 정적(static) 메소드 정의
    public static double avg(int a, int b){ // 선언부
        return (double) (a+b)/2; // 구현부
    }
    // 2. 값을 반환 안하는 경우 void
    public static void startMsg(){
        System.out.println("This is a start message!");
    }
}
```

```
method result 1: 1.5
method result 2: 63.5
This is a start message!
```

* **자바에서는 변수의 값이 복사되어서 대입된다**

<br>

---

## 2) 정적 메서드

* `static` 메서드
* 객체(instance) 생성 없이 호출 가능
* 인스턴스 멤버와 관련 없는 작업 함
* 메소드 내에 인스턴스 변수 사용 불가
* [Static](https://seungki1011.github.io/posts/java-12-static/)에서 추가 설명

<br>

---

## 3) Instance Method

* 객체(instance) 생성 후 ```참조변수.methodName()``` 으로 호출
* [OOP](https://seungki1011.github.io/posts/java-8-oop-intro/#2-instance-method)에서 추가 설명

<br>

---

## 4) 오버로딩(Overloading)

* 한 클래스 안에서 같은 이름의 메서드를 여러개 정의하는 것



* 오버로딩이 성립하기 위해서는
  * 메서드의 이름이 같아야 함
  * 매개변수의 개수 또는 타입이 달라야 함
  * 반환 타입은 영향이 없음



* 메서드는 구분하기 위한 메서드 시그니쳐는 메서드의 이름 & 매개변수 타입, 갯수
* 오버라이딩된 메소드를 호출하는 경우 파리미터 타입에 가장 알맞은 메소드 부터 선택해서 호출

<br>

**성립하는 경우**

```java
long add(int a, long b) {return a+b;}
long add(long a, int b) {return a+b;}
```

* 매개변수의 타입이 다르면 성립

<br>

**성립하지 않는 경우**

```java
int add(int a, int b) {return a+b;}
long add(int a, int b) {return (long)(a+b);}
```

* 반환 타입은 오버로딩의 성립에 영향이 없음

<br>

---

## 5) 오버라이딩(Overriding)

* 조상 클래스로 부터 상속 받 메서드의 내용 상속받는 클래스에 맞게 변경하는 것(덮어쓰는 것)
* [상속(inheritance)](https://seungki1011.github.io/posts/java-14-inheritance/#4-method-overriding)에서 추가 설명