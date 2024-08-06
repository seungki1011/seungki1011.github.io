---
title: 빌더 패턴(Builder Pattern)
description: 빌더 패턴에 대하여
author: seungki1011
date: 2024-04-11 12:30:00 +0900
categories: [2. 프로그래밍 언어(Programming Language), Java]
tags: [java, builder]
math: true
mermaid: true
---

## 1. 빌더 패턴(Builder Pattern)

빌더 패턴(Builder Pattern)은 객체 생성 패턴 중 하나이다.

**"생성자가 있는데 웬 생성 패턴?"**이라고 생각할 수 있지만, **빌더는 생성자와 다르게 복잡한 객체를 단계별로 생성할 수 있게 도와준다. 빌더 패턴을 통해서 다양한 표현의 객체를 용이하게 만들어 낼 수 있다.** 

<br>

![builder1](../post_images/2024-02-11-java-builder-pattern/builder1.png)_https://refactoring.guru/ko/design-patterns/builder_

<br>

예시를 통해 살펴보자.

<br>

---

## 2. 생성자 사용의 단점

먼저 `Person`이라는 클래스가 다음 처럼 생성자를 이용한다고 해보자.

```java
@Getter @Setter
public class Person {
    // 필수 매개변수
    private String firstName;
    private String lastName;

    // 선택 매개변수
    private int age;
    private String phone;
    private String address;

    public Person(String firstName, String lastName, int age, String phone, String address) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.age = age;
        this.phone = phone;
        this.address = address;
    }
  
    @Override
    public String toString() {
        return "Person [firstName=" + firstName + ", lastName=" + lastName + ", age=" + age 
          + ", phone=" + phone + ", address=" + address + "]";
    }
}
```

<br>

생성자를 사용하는 `Person` 객체를 생성하고 값을 확인해보자.

```java
@Slf4j
class PersonTest {

    @Test
    public void 생성자_Person_테스트() {
        Person person1 = new Person("리오넬",
                "메시",
                37,
                "010-1234-5678",
                "미국 플로리다");
        Person person2 = new Person("크리스티아누 호날두",
                "산토스 아베이로",
                39,
                null,
                null);

        log.info("person1 = {}", person1);
        log.info("person2 = {}", person2);
    }
}
```

<br>

**"빌더 패턴을 사용하지 말고 그냥 위 처럼 생성자로 사용해도 문제가 없는 것 아닌가?"**라고 생각할 수 있다. 사실 그냥 생성자를 사용해도 치명적인 문제가 생기거나 하는 것은 아니다. 그래도 생성자를 사용하는 경우 생기는 몇 가지 단점을 짚고 넘어가자.

* **객체 생성시 가독성이 좋지 않다**
  * 지금 처럼 필드가 5개인 상태에서도 어느 순서로 필드에 대한 값을 입력해야하는지 파악하기 어렵다. 만약 필드가 6개, 7개로 늘어난다면 더 어려워진다. (~~물론 요즘 IDE들이 좋아져서 옆에 표기해주지만 이는 IDE에 의존하게 되는 것이다.~~)
  * 필수 입력 필드가 아니라 선택 입력 필드를 비우고 싶으면 `null`또는 사용하지 않는다는 것을 나타낼 수 있는 값으로 채워야 한다. 만약 `null`로 채우지 않을거라면, 해당 선택 필드를 제외한 여러개의 생성자를 다시 만들어야한다.

* **`@Setter`의 사용은 권장되지 않는다**
  * `Setter`를 열어두면 어디서든 접근해서 객체의 값을 변경할 수 있기 때문에 불변성(immutability)을 보장할 수 없다. 쉽게 말해서 객체가 일관되지 못한 상태에 놓일 확률이 높아진다.
  * 실무에서도 `@Setter`를 사용하거나 `Setter` 메서드를 함부로 만들지 않고, 정말 필요한 필드에 한해서만 `changeXXX()` 같은 형태로 메서드를 만들어서 사용한다

<br>

빌더를 사용하는 방법을 알아보고, 위의 단점을 해결해보자.

<br>

---

## 3. 빌더(Builder) 사용하기

빌더를 사용해보자.

<br>

기존의 `Person`을 수정해보자.

```java
@Getter
public class Person {
    // 필수 매개변수
    private final String firstName;
    private final String lastName;

    // 선택 매개변수
    private final int age;
    private final String phone;
    private final String address;

    // private 생성자
    private Person(Builder builder) {
        this.firstName = builder.firstName;
        this.lastName = builder.lastName;
        this.age = builder.age;
        this.phone = builder.phone;
        this.address = builder.address;
    }

    // Builder 클래스
    public static class Builder {
        // 필수 매개변수
        private final String firstName;
        private final String lastName;

        // 선택 매개변수
        private int age = 0;
        private String phone = "";
        private String address = "";
        
        // 필수 필드는 빌더의 생성자로 받게해서 무조건 입력을 하도록 구현
        public Builder(String firstName, String lastName) {
            this.firstName = firstName;
            this.lastName = lastName;
        }

        public Builder age(int age) {
            this.age = age;
            return this;
        }

        public Builder phone(String phone) {
            this.phone = phone;
            return this;
        }

        public Builder address(String address) {
            this.address = address;
            return this;
        }

        public Person build() {
            return new Person(this);
        }

    }

    @Override
    public String toString() {
        return "Person [firstName=" + firstName + ", lastName=" + lastName + ", age=" + age 
          + ", phone=" + phone + ", address=" + address + "]";
    }
}
```

* `Builder` 클래스는 **정적 내부(static inner) 클래스**로 구현했다
  * `PersonBuilder`라는 외부 클래스로 따로 만들어서 구현하는 것도 가능하나, 어차피 해당 빌더(`PersonBuilder`)는 해당 클래스(`Person`)만 사용하기 때문에 빌더를 클래스 안에 위치시키는 것이 의미적으로도, 유지 보수성에도 좋다
  * [중첩 클래스에 대해 알아보기](https://seungki1011.github.io/posts/java-20-nested-class/)
  * 내부 클래스를 `static`으로 설정하지 않으면 메모리 누수 문제가 발생할 수 있다. [참고](https://inpa.tistory.com/entry/JAVA-%E2%98%95-%EC%9E%90%EB%B0%94%EC%9D%98-%EB%82%B4%EB%B6%80-%ED%81%B4%EB%9E%98%EC%8A%A4%EB%8A%94-static-%EC%9C%BC%EB%A1%9C-%EC%84%A0%EC%96%B8%ED%95%98%EC%9E%90)

<br>

빌더를 사용해보자.

```java
@Test
public void WithBuilderPerson() {
    Person person1 = new Person.Builder("리오넬", "메시") // 필수 필드
            .age(37)
            .phone("010-1234-5678")
            .address("미국 플로리다")
            .build();

    Person person2 = new Person.Builder("크리스티아누 호날두", "산토스 아베이로")
            .age(39)
            .build();

    log.info("person1 = {}", person1);
    log.info("person2 = {}", person2);
}
```

```
11:35:51.552 [Test worker] INFO de.datajpa.etc.PersonTest -- person1 = Person [firstName=리오넬, lastName=메시, age=37, phone=010-1234-5678, address=미국 플로리다]
11:35:51.558 [Test worker] INFO de.datajpa.etc.PersonTest -- person2 = Person [firstName=크리스티아누 호날두, lastName=산토스 아베이로, age=39, phone=, address=]
```

<br>

빌더를 사용해서 다음과 같은 효과를 얻을 수 있다.

* **`final`을 사용해서 불변으로 만들 수 있다 ([불변에 대해 알아보기](https://seungki1011.github.io/posts/java-16-immutable/))**
  * 사이드 이펙트를 줄일 수 있다
* **매개변수에 대한 기본값을 생성자 방식보다 편하게 사용할 수 있다**
  * 기존 생성자 방식에서는 초기값이 세팅된 필드를 제외한 생성자를 구현하는 방식으로 사용했어야 한다
* **가독성이 좋아진다**
  * 메서드 체이닝 방식으로 값을 설정할 수 있어서 굳이 다시 클래스로 돌아가서 확인할 필요 없이 값을 입력할 수 있다
  * 순서를 신경쓰지 않아도 되서 실수를 방지할 수 있다
  * 선택 필드는 `null`이나 빈 값을 입력해줄 필요 없다
* **필수 매개변수와 선택 매개변수를 구분해서, 필수 매개변수는 무조건 입력하도록 구현하는 것도 가능하다**

<br>

---

## 4. lombok의 @Builder

롬복(lombok)은 개발자가 빌더 패턴을 쉽게 구현할 수 있도록 `@Builder`라는 애노테이션을 지원한다. 빌더 클래스를 따로 구현할 필요 없이 클래스 또는 생성자에 `@Builder`를 붙이면 빌더를 사용할 수 있다.

<br>

### 클래스 레벨에 @Builder 사용하기

클래스 레벨에 `@Builder`를 사용하면 필드 전체에 대해 빌더를 사용할 수 있다. 예시를 통해 알아보자.

<br>

```java
@Getter
@Builder // 빌더를 사용할 클래스 위에 추가
@AllArgsConstructor(access = AccessLevel.PRIVATE) // 외부에서 생성자를 통한 객체 생성을 막는다
public class Person {
    // 필수
    private final String firstName;
    private final String lastName;
    // 선택
    private final int age;
    @Builder.Default
    private final String phone = "";
    @Builder.Default
    private final String address = "";

    @Override
    public String toString() {
        return "Person [firstName=" + firstName + ", lastName=" + lastName + ", age=" + age 
          + ", phone=" + phone + ", address=" + address + "]";
    }
}
```

* `@Builder.Default`를 사용하면 필드에 대한 기본값을 사용할 수 있다

<br>

`@Builder`를 적용한 클래스를 사용해서 객체를 출력해보자.

```java
@Test
public void LombokBuilderOnClass() {
    Person person1 = Person.builder()
            .firstName("리오넬")
            .lastName("메시")
            .age(37)
            .phone("010-1234-5678")
            .address("미국 플로리다")
            .build();
    Person person2 = Person.builder()
            .firstName("크리스티아누 호날두")
            .lastName("산토스 아베이로")
            .age(39)
            .build();

    log.info("person1 = {}", person1);
    log.info("person2 = {}", person2);
}
```

```
14:09:14.960 [Test worker] INFO de.datajpa.etc.PersonTest -- person1 = Person [firstName=리오넬, lastName=메시, age=37, phone=010-1234-5678, address=미국 플로리다]
14:09:14.964 [Test worker] INFO de.datajpa.etc.PersonTest -- person2 = Person [firstName=크리스티아누 호날두, lastName=산토스 아베이로, age=39, phone=, address=]
```

<br>

---

### @Builder 사용시 필수 파라미터 지정

`@Builder`를 사용하는 경우, 기존 빌더의 생성자를 통해 필수 파라미터를 입력하도록 강제하는 방법은 불가능하다.

이 경우에는 필수 필드에 롬복의 `@NonNull` 애노테이션을 추가해서 해당 필드에 `null`을 허용하지 않도록하는 방식을 사용할 수 있다.

<br>

```java
@Getter
@Builder
@AllArgsConstructor(access = AccessLevel.PRIVATE)
public class Person {
    // 필수
    @NonNull
    private final String firstName;
    @NonNull
    private final String lastName;
    
    // 선택
    private final int age;
    @Builder.Default
    private final String phone = "";
    @Builder.Default
    private final String address = "";
}
```

* `@NonNull` 사용시, 빌더를 통해 객체를 생성할 때 필수 파라미터를 제공하지 않으면 컴파일 시점에 오류가 생긴다

<br>

물론 `@NonNull`을 사용하는 방법 외에도 다양한 방법으로 필수 파라미터를 지정할 수 있다.

* [필수 파라미터 빌더 구현하기](https://inpa.tistory.com/entry/GOF-%F0%9F%92%A0-%EB%B9%8C%EB%8D%94Builder-%ED%8C%A8%ED%84%B4-%EB%81%9D%ED%8C%90%EC%99%95-%EC%A0%95%EB%A6%AC#%ED%95%84%EC%88%98_%ED%8C%8C%EB%9D%BC%EB%AF%B8%ED%84%B0_%EB%B9%8C%EB%8D%94_%EA%B5%AC%ED%98%84%ED%95%98%EA%B8%B0)
* [기존 빌더를 재정의해서 필수 필드 입력 받기](https://hothoony.tistory.com/1295)

<br>

---

### 특정 생성자에 @Builder 사용하기

특정 생성자에만 `@Builder`를 적용할 수 있다.

<br>

```java
@Getter
public class Person {
    private String firstName;
    private String lastName;

    private int age;
    private String phone;
    private String address;

    @Builder
    public Person(String firstName, String lastName) {
        this.firstName = firstName;
        this.lastName = lastName;
    }

    public Person(String firstName, String lastName, int age, String phone, String address) {
        this.firstName = firstName;
        this.lastName = lastName;
        this.age = age;
        this.phone = phone;
        this.address = address;
    }

}
```

<br>

다음과 같이 사용할 수 있다.

```java
@Test
public void LombokBuilderOnConstructor() {
    Person person1 = Person.builder()
            .firstName("A")
            .lastName("B")
            .build();

    log.info("person1 = {}", person1);
}
```

* `firstName`과 `lastName`에 대해서만 빌더를 사용할 수 있다

<br>

---

## 5. 빌더의 단점

빌더 패턴의 단점을 알아보자.

* 코드가 복잡하다
  * 빌더 클래스를 정의해야 한다
  * 메소드 체이닝 방식의 객체 생성은 코드가 다소 장황해 보인다
* 직접 객체를 생성하는 생성자 방식에 비해 성능 오버헤드가 발생할 수 있다
  * 객체를 생성하기 위해 여러 메서드의 호출이 성능에 영향을 끼칠 수 있다

<br>

> 이펙티브 자바(Effective Java)에서도 필드의 개수가 4개 이상인 경우에 빌더 패턴의 사용을 권장하고 있다.
>
> 만약 필드수가 많지 않다면 그냥 생성자 방식을 사용하는 것이 효율적일 수 있다.
{: .prompt-tip }

<br>

---

## Reference

1. [https://inpa.tistory.com/entry/JAVA-%E2%98%95-%EC%9E%90%EB%B0%94%EC%9D%98-%EB%82%B4%EB%B6%80-%ED%81%B4%EB%9E%98%EC%8A%A4%EB%8A%94-static-%EC%9C%BC%EB%A1%9C-%EC%84%A0%EC%96%B8%ED%95%98%EC%9E%90](https://inpa.tistory.com/entry/JAVA-%E2%98%95-%EC%9E%90%EB%B0%94%EC%9D%98-%EB%82%B4%EB%B6%80-%ED%81%B4%EB%9E%98%EC%8A%A4%EB%8A%94-static-%EC%9C%BC%EB%A1%9C-%EC%84%A0%EC%96%B8%ED%95%98%EC%9E%90)
2. [https://refactoring.guru/ko/design-patterns/builder](https://refactoring.guru/ko/design-patterns/builder)

