---
title: (Java - 04) 형변환(Typecasting)
description: 자바에서의 형변환
author: seungki1011
date: 2024-01-02 12:30:00 +0900
categories: [Java]
tags: [java]
math: true
mermaid: true
---

---

## Typecasting

* 형변환
* 자료형을 다른 형태로 변경하는 것

<br>

---

### 자동 형변환(Widening Type Casting)

* 자동 형변환, 묵시적 형변환 등에 해당



* 작은 범위의 값을 큰 범위에 넣는 것은 가능
  * 예시 ```int```의 값을 ```long```또는 ```double```에 넣기



* 큰 범위의 값을 작은 범위에 넣으면 문제 생김
  * 예시 overflow 문제

<br>

```java
public class tc1 {
    public static void main(String[] args) {
      
        int intVal = 5;
        long longVal;
        double doubleVal;

        // 1. int 값을 long 그릇에 넣는 것은 가능
        longVal = intVal;
        System.out.println("longVal is " + longVal);

        // 2. int 값을 double 그릇에 넣는 것도 가능
        doubleVal = intVal;
        System.out.println("doubleVal is " + doubleVal);

        /*
        작은 범위를 큰 범위에 넣는 경우에는 자바가 자동으로 형변환을 해주기 때문에 다음과 같이
        명시적으로 형을 제시하지 않아도 된다.
        doubleVal = (double) intVal;
         */
    }
}
```

```
longVal is 5
doubleVal is 5.0
```

<br>

---

### 명시적 형변환(Narrow Type Casting)

* 명시적 형변환, 강제 형변환 등에 해당
* 큰 범위의 값을 작은 범위의 값에 넣을 경우 명시적으로 형변환을 해야한다



* 명시적 형변환은 주의해서 사용하자
  * 데이터 손실 주의
  * ```float```과 ```int```간의 형변환시 이런 손실 문제로 ```double```사용을 권장
  * 오버플로우 문제 주의

<br>

```java
public class tc2 {
    public static void main(String[] args) {
      
        int intVal;
        long longVal;
        double doubleVal = 10.345;

        // intVal = doubleVal; 명시적 형변환을 하지 않으면 컴파일 에러 발생
        intVal = (int) doubleVal;

        System.out.println("Original doubleVal is " + doubleVal);
        System.out.println("Value after type casting to int is " + intVal);
    }
}
```

```
original doubleVal is 10.345
Value after type casting to int is 10
```

<br>

---

### 1.3 계산시 형변환

* 다른 타입간의 계산은 상위 타입으로 자동 형변환

<br>

```java
public class tc3 {
    public static void main(String[] args) {
      
        double d1;
        d1 = 10 / 4;
        System.out.println("d1 = " + d1);
        d1 = 10.0 / 4.0;
        System.out.println("d1 = " + d1);
        d1 = (double) 10 / 4;
        System.out.println("d1 = " + d1);
        d1 = 10.0 / 4;
        System.out.println("d1 = " + d1);
    }
}
```

```
10/4 is d1 = 2.0
10.0/4.0 is d1 = 2.5
(double) 10/4 is d1 = 2.5
10.0/4 is d1 = 2.5
```

<br>

---

## Reference

1. [https://www.simplilearn.com/tutorials/java-tutorial/type-casting-in-java](https://www.simplilearn.com/tutorials/java-tutorial/type-casting-in-java)
2. [https://www.geeksforgeeks.org/typecasting-in-java/](https://www.geeksforgeeks.org/typecasting-in-java/)