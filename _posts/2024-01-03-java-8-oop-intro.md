---
title: (Java - 8) 객체지향 프로그래밍(OOP)
description: 자바에서의 객체지향 프로그래밍
author: seungki1011
date: 2024-01-03 12:30:00 +0900
categories: [Java]
tags: [java]
math: true
mermaid: true
---

---

## 1) 객체 지향 vs 절차 지향(OOP vs POP)

* 객체 지향 프로그래밍은 OOP(Object-Oriented-Programming)라는 용어로 많이 사용한다



* 객체 지향 프로그래밍은 절차 지향(procedural)과 다르게 데이터와 해당 데이터에 대한 행동(메소드)이 하나의 객체 안에 함께 포함된다
  * 절차 지향적 프로그래밍의 한계의 원인중 하나는 데이터와 기능의 분리 때문 → 관리 포인트(manage point)의 증가

<br>

![POP vs OOP](../post_images/2024-01-03-java-8-oop-intro/popvsoop.jpeg)

<p align='center'>https://simplesnippets.tech/java-introduction-to-object-oriented-programming-oop/</p>

<br>

---

## 2) 인스턴스 메서드(Instance Method)

* 인스턴스 메소드는 인스턴스 생성 후 ```참조변수.methodName();```으로 호출
  * 인스턴스 메소드는 인스턴스 변수 관련된 작업을 할 수 있음
  * 메소드 내에서 인스턴스 변수 사용 가능



* 객체는 자신의 메소드를 통해 자신의 멤버 변수에 접근



* 클래스는 기능 역할을 하는 메소드도 포함한다
  * 속성(데이터) : 멤버 변수 + 기능 : 메소드



* 인스턴스 메소드는 ```static``` 접근 제어자 사용 불가

<br>

```java
public class ControllerData {
    int value;

    void increase() {
        value++;
        System.out.println("Increased value(+1) | value = "+value);
    }
}
```

<br>

```java
public class oop1 {
    public static void main(String[] args) {
        ControllerData controllerData = new ControllerData();
        System.out.println("Current value = "+controllerData.value);
        controllerData.increase();
        controllerData.increase();
        controllerData.increase();
        System.out.println("Current value = "+controllerData.value);
    }
}
```

```
Current value = 0
Increased value(+1) | value = 1
Increased value(+1) | value = 2
Increased value(+1) | value = 3
Current value = 3
```

<br>

---

## 3) Static Method

* 정적 메소드
* 객체(instance) 생성 없이 호출 가능
* 인스턴스 멤버와 관련 없는 작업 함
* 메소드 내에 인스턴스 변수 사용 불가
* [Static](https://seungki1011.github.io/posts/java-12-static/#3-%EC%A0%95%EC%A0%81-%EB%A9%94%EC%84%9C%EB%93%9Cstatic-method)에서 추가 설명

<br>

---

## 4) 캡슐화(Encapsulation)

* 속성과 기능을 묶어서 필요한 기능을 메소드를 통해 외부에 제공하는 것
* 변수에 대한 직접적인 접근을 막고 인스턴스가 제공하 필드와 메서드를 통해서 접근이 가능하도록 한다
* 캡슐화는 접근 제어자를 ```private```으로 설정해서 외 접근을 제한함
* 메소드는 ```public```으로 설정해서 메소드를 통한 간접 접근만 허용
* [접근제어자(Access Modifier)](https://seungki1011.github.io/posts/java-11-access-modifier/#3-%EC%BA%A1%EC%8A%90%ED%99%94encapsulation)에서 더 알아보기

<br>

![encapsulation](../post_images/2024-01-03-java-8-oop-intro/encapsulation.png)

<p align='center'>https://waytoeasylearn.com/learn/encapsulation/</p>

<br>

---

## Further Reading

* [함수형 프로그래밍(Functional Programming)](https://www.geeksforgeeks.org/functional-programming-paradigm/)

---

## Reference

1. [https://www.geeksforgeeks.org/difference-between-oop-and-pop/](https://www.geeksforgeeks.org/difference-between-oop-and-pop/)
1. [https://simplesnippets.tech/java-introduction-to-object-oriented-programming-oop/](https://simplesnippets.tech/java-introduction-to-object-oriented-programming-oop/)
1. [https://waytoeasylearn.com/learn/encapsulation/](https://waytoeasylearn.com/learn/encapsulation/)

