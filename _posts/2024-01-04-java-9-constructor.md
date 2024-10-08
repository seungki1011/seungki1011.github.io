---
title: (Java - 09) 생성자(Constructor)
description: 자바의 생성자에 대해서
author: seungki1011
date: 2024-01-04 12:30:00 +0900
categories: [2. 프로그래밍 언어(Programming Language), Java]
tags: [java]
math: true
mermaid: true
---

---

## 1. 생성자(Constructor)

* 인스턴스가 생성될 때마다 호출되는 인스턴스 초기화 메소드
* 기본 생성자는 자동으로 추가되지만 그 외의 생성자는 사용자가 직접 추가한다
* 참조변수를 넘겨서 변수의 초기화를 담당하는 메소드를 이용하는 것보다 객체 지향을 위해 속성(데이터)와 기능(메소드)을 한 곳(클래스 안)에 두는 것이 더 좋다
* 접근 제어자(access modifier)를 명시하지 않으면 생성자는 기본적으로 `package-private`이 된다(같은 패키지 내에서만 접근 가능)

<br>

> **생성자를 사용하는 이유**
>
> * 인스턴스의 초기화를 편리하게 하기 위해서 사용한다
> * 생성자를 이용해 설정한 파라미터를 무조건 넘기도록 하는 제약을 걸 수 있다(더 안전하다)

<br>

---

## 2. this

* **인스턴스 자신을 가리키는 참조변수**
* 인스턴스의 주소가 저장되어 있다

* 모든 인스턴스 메서드에 자역변수로 숨겨져 있는 채로 존재한다
  * 생성자가 아닌 메서드에도 사용할 수 있다

* **지역 변수와 멤버 변수의 구분을 위해 `this`를 사용한다**

<br>

```java
public class ProductInfo {
    String name;
    int price;
    double rating;

    // 멤버변수(인스턴스 변수)와 지역변수 구분을 위해 this 사용
    void product(String name, int price, double rating){
        this.name = name;
        this.price = price;
        this.rating = rating;
    }
}
```

* `this`의 사용이 필수인 것은 아니다

<br>

```java
public class ProductInfo2 {
    String name;
    int price;
    double rating;

    // 1. this의 사용이 강제는 아님
    // 2. 멤버변수라는 것을 나타내기 위해 this를 붙여서 사용해도 동작한다
    void product2(String productName, int productPrice, double productRating){
        name = productName;
        price = productPrice;
        rating = productRating;

        /*
        this.name = productName;
        this.price = productPrice;
        this.rating = productRating;
         */
    }
}
```

```java
public class Con1 {
    public static void main(String[] args) {
        ProductInfo2 p = new ProductInfo2();
        p.product2("Pen",6000,9.0);
        System.out.println("Name: " +p.name+", Price: "+p.price+", Rating: "+p.rating);
    }
}
```

```
Name: Pen, Price: 6000, Rating: 9.0
```

<br>

---

## 3. 생성자 사용 조건

* 생성자의 이름은 클래스의 이름과 같아야 한다
* 생성자는 리턴타입이 없다
  * `void`도 사용하지 않는다

* 생성자는 인스턴스 생성하고 나서 즉시 호출된다
  * 생성자 안에 특정 값을 설정하는 것이 아니라 메서드 호출 등의 작업도 가능하다. 생성자가 호출되면, 당연히 그 작업도 호출된다.
  

<br>


```java
public class ProductInfo3 {
    String name;
    int price;
    double rating;

    // 생성자 이름은 클래스 이름과 동일
    ProductInfo3(String name, int price, double rating){
        this.name = name;
        this.price = price;
        this.rating = rating;
    }
}
```

```java
public class Con2 {
    public static void main(String[] args) {
        // 사용자 정의 생성자가 존재하면 기본 생성자는 자동으로 생성 안됨
      	// 무조건 직접 정의한 생성자를 호출해야 함(제약)
        // ProductInfo3 product1 = new ProductInfo3();
        ProductInfo3 product1 = new ProductInfo3("Chicken", 20000, 8.5);
        System.out.println("Name: " +product1.name+", Price: "+product1.price+", Rating: "+product1.rating);
    }
}
```

```
Name: Chicken, Price: 20000, Rating: 8.5
```

<br>

---

## 4. 기본 생성자(Default Constructor)

기본 생성자의 특징은 다음과 같다.

* 매개변수가 없는 생성자
* 클래스에 생성자가 하나도 없으면 컴파일러가 기본 생성자를 추가해준다
* **만약 생성자가 하나라도 존재한다면 기본 생성자는 제공되지 않는다**

```java
Car car = new Car(); // 기본 생성자 호출
```

<br>

---

## 5. 생성자 오버로딩(Constructor Overloading)

생성자를 추가해서 오버로딩이 가능하다.

<br>

```java
public class ProductInfo4 {
    String name;
    int price;
    double rating;

    // 생성자 오버로딩 (String name, int price)
    ProductInfo4(String name, int price){// rating 입력 없이 생성자 이용시 이 생성자 호출
        this.name = name;
        this.price = price;
        this.rating = 7.0;
    }
  
    // 생성자 오버로딩 (String name, int price, double rating)
    ProductInfo4(String name, int price, double rating){
        this.name = name;
        this.price = price;
        this.rating = rating;
    }
}
```

```java
public class Con3 {
    public static void main(String[] args) {
        // rating의 디폴트값이 7.0인 생성자 호출
        ProductInfo4 p = new ProductInfo4("Laptop", 1000000);
      
        // ProductInfo4 p = new ProductInfo4("Laptop", 1000000, 8.5); // rating까지 포함한 생성자 호출
        System.out.println("Product name: "+p.name+", Price: "+p.price+", Rating: "+p.rating);
    }
}
```

```
Product name: Laptop, Price: 1000000, Rating: 7.0
```

<br>

---

## 6. this()

* 같은 클래스의 다른 생성자를 호출할 때 사용한다
  * 생성자 내부에서 자신의 생성자를 호출한다

* `this()`를 이용한 생성자 호출은 생성자의 첫 문장에서만 가능하다
* 코드의 재사용성 증가를 위해 사용한다(중복 제거)

<br>

```java
public class ProductInfo5 {
    String name;
    int price;
    double rating;

    // this()
    ProductInfo5(String name, int price){
        this(name, price, 7.0); // 생성자 ProductInfo5(String name, int price, double rating) 호출
    }
  
    ProductInfo5(String name, int price, double rating){
        this.name = name;
        this.price = price;
        this.rating = rating;
    }
}
```

<br>

---

## Reference

1. [https://www.geeksforgeeks.org/constructors-in-java/](https://www.geeksforgeeks.org/constructors-in-java/)
1. [이것이 자바다!](https://www.google.co.kr/books/edition/%EC%9D%B4%EA%B2%83%EC%9D%B4_%EC%9E%90%EB%B0%94%EB%8B%A4_%EA%B0%9C%EC%A0%95%ED%8C%90/SLWGEAAAQBAJ?hl=ko&gbpv=0)
3. [김영한: 실전 자바 로드맵](https://www.inflearn.com/roadmaps/744)