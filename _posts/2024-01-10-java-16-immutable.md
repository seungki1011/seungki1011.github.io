---
title: (Java - 16) 불변(Immutable)
description: Side-Effect와 불변의 중요성에 대해
author: seungki1011
date: 2024-01-10 12:30:00 +0900
categories: [Java]
tags: [java]
math: true
mermaid: true
---

---

## 1) 공유

### 1.1 기본형과 참조형의 공유

들어가기에 앞서 기본형과 참조형을 다시 짚고 가자.

* 기본형(Primitive Type)

  * 기본형은 실제 사용하는 값을 담는다

  * **하나의 값을 여러 변수에서 절대로 공유하지 않는다**

  * ```java
    int a = 5;
    int b = a; // b는 a와 같은 5라는 값이지만 a의 5와 b의 5가 같은 메모리 주소에 위치하는 것은 아니다
    ```



* 참조형(Reference Type)
  * 참조형은 객체의 메모리 주소를 담는다(참조값)
  * **하나의 객체를 참조값을 통해 여러 변수에서 공유할 수 있다**
  * 서로 같은 참조값을 통해 같은 인스턴스를 참조하는 경우, 한쪽에서 변경을 가하면 다른 쪽에서도 변경이 된다 (**서로 같은 인스턴스를 공유하기 때문**이다)

<br>

---

### 1.2 사이드 이펙트(Side-effect)

사이드 이펙트라는 것은 프로그래밍에서 목표하는 작업외에 추가적인 부수 효과를 일이키는 것을 말한다. 대부분의 경우 사이드 이펙트는 부정적인 의미로 사용한다. 사이드 이펙트는 프로그램의 특정 부분에서 발생한 변경이 의도치 않게 다른 부분에 영향을 미치는 경우를 말한다.

코드로 알아보자.

```java
public class Item {
  
    private String value = "";

    public Item(String value) {
        this.value = value;
    }

    public void setValue(String value) {
        this.value = value;
    }

    @Override
    public String toString() {
        return "Item{" +
                "value='" + value + '\'' +
                '}';
    }
}
```

```java
public class ImmutableTest2 {
    public static void main(String[] args) {
      
        Item item1 = new Item("치킨");
        Item item2 = item1;

        System.out.println("item1 : "+item1);
        System.out.println("item2 : "+item2);

        System.out.println("item2.setValue(\"피자\");");
        item2.setValue("피자");
        System.out.println("item1 : "+item1); // 사이드 이펙트 발생, A -> B
        System.out.println("item2 : "+item2);
    }
}
```

```
item1 : Item{value='치킨'}
item2 : Item{value='치킨'}
item2.setValue("피자");
item1 : Item{value='피자'}
item2 : Item{value='피자'}
```

* `item2`의 값을 `A`에서 `B`로 변경하는 것이 목표
* `item1`과 `item2`는 같은 인스턴스를 참조하기 때문에, 사이드 이펙트로 `item1`의 값도 `B`로 변경 됨

<br>

이를 해결하는 것은 쉽다. 그냥 처음 부터 다른 인스턴스를 참조하도록 하면 된다.

```java
Item item1 = new Item("A");
Item item2 = new Item("B");
```

* 이제 같은 객체를 공유하지 않는다
* 그러나 이것이 객체의 공유를 막는다는 것은 아니다(단지 공유만 하지 않을 뿐)

<br>

사실 **참조값의 공유를 막는 것은 불가능하다. 그러나 공유된 객체의 변경을 막기 위해 사용하는 것이 불변(immutable) 객체**이다.

<br>

---

## 2) 불변 객체(Immutable Object)

### 2.1 불변 객체 소개

사이드 이펙트의 근본적인 원인은 공유 그 자체에서 발생하는 것이 아니다. 공유한 객체의 값을 변경하는 경우에 발생한다. 

이런 공유한 객체의 값을 변경하는 것을 방지하기 위해 불변 객체(immutable object)를 도입힌다.

불변 객체란, 객체의 상태(객체의 필드, 멤버 변수)가 변하지 않는 객체를 말한다.

코드로 살펴보자.

<br>

```java
public class ImmutableItem {
  
    private final String value; // final : 한번 생성하고 값을 변경하는 것 불가
    // 사실 final을 사용하지 않아도 setValue가 없으면 값을 변경하는 것은 불가

    public ImmutableItem(String value) {
        this.value = value;
    }

    @Override
    public String toString() {
        return "Item{" +
                "value='" + value + '\'' +
                '}';
    }
}
```

```java
public class ImmutableTest3 {
    public static void main(String[] args) {
      
        ImmutableItem item1 = new ImmutableItem("치킨");
        ImmutableItem item2 = item1; // 참조값 대입을 막을 방법은 없다

        System.out.println("item1 : "+item1);
        System.out.println("item2 : "+item2);

        System.out.println("item2 = new ImmutableItem(\"피자\");");
        // item2.setValue("B");
        item2 = new ImmutableItem("피자");
        System.out.println("item1 : "+item1); // 사이드 이펙트 발생, A -> B
        System.out.println("item2 : "+item2);
    }
}
```

```
item1 : Item{value='치킨'}
item2 : Item{value='치킨'}
item2 = new ImmutableItem("피자");
item1 : Item{value='치킨'}
item2 : Item{value='피자'}
```

* 불변 클래스를 만드는 방법은, 어떻게든 필드 값을 변경하지 못하게 설계하면 된다
* `Item` 클래스를 `ImmutableItem` 클래스로 만드는 과정에서 `setValue()`를 제거, 필드에는 `final` 추가
* 결론적으로 불변 객체의 도입으로 인해, 원하는 값을 설정하기 위해서 개발자는 무조건 새로운 인스턴스를 생성해서 사용해야 한다

<br>

---

### 2.2 불변 객체에서 값 변경

그럼 기존 불변 객체의 값을 변경하고 싶은 로직이 필요할 수도 있다. 이 때 어떻게 구현하는지 코드로 알아보자.

<br>

```java
public class ImmutableObj {
  
    private final int value;

    public ImmutableObj(int value) {
        this.value = value;
    }

    public int getValue() {
        return value;
    }

    public ImmutableObj add(int addValue) {
        int result = value + addValue;
        return new ImmutableObj(result); // 객체를 새로 만들어서 계산 결과를 넣고 반환
    }
}
```

```java
public class ImmutableTest4 {
    public static void main(String[] args) {
      
        ImmutableObj obj1 = new ImmutableObj(20);
        ImmutableObj obj2 = obj1.add(30);

        System.out.println("obj1.getValue() = " + obj1.getValue());
        System.out.println("obj2.getValue() = " + obj2.getValue());
    }
}
```

```
obj1.getValue() = 20
obj2.getValue() = 50
```

* `add()`에서 그냥 새로운 객체를 만들고 계산 결과를 넣고 반환해서, 불변성도 유지하면서 값 변경을 위한 메서드를 구현할 수 있다 
* 불변 객체의 값 변경이라고는 하지만 실제로 불변 객체의 값을 변경하는 것은 아니다
* 기존 `set`을 `new ImmutableObj()` 같은 형식으로 구현할 수 있다
  * 이 때 `setValue()`가 아닌 `withValue()`로 네이밍하는 것이 관례

<br>

---

### 2.3 불변이 중요한 이유

자바에서 여러가지 불변 클래스들이 존재한다. 대표적으로 `String`, `Integer`, `LocalDate` 등 수많은 클래스들이 불변으로 설계되어 있다. 모든 클래스를 불변으로 만드는 것은 아니다. 보통은 객체를 공유하고, 공유한 값을 변경하는 것이 필요한 경우가 많다. 이런 일반적인 경우에 가변 클래스를 사용한다.

<br>

* 불변은 객체를 항상 새로 생성해야하기 때문에 성능상 가변 클래스보다 불리한 경우들이 생길 수 있다
  * 값이 변경이 자주 일어나면 가변 클래스 고려

* 불변 클래스는 값을 변경하면 안되는 경우에 만들어서 사용하면 된다
* 특정 경우에는 같은 기능을 하는 클래스를 가변 클래스, 불변 클래스 모두 만들어서 사용하는 경우도 존재한다

<br>

클래스를 불변으로 설계하는 이유는 다양하다.

* 캐시 안정성
* 멀티 스레드 안정성 
* 엔티티의 값 타입
* 기타 여러 이유