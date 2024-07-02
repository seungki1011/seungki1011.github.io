---
title: (Java - 07) 참조형(Reference Type)
description: 자바의 참조형에 대해서
author: seungki1011
date: 2024-01-03 12:30:00 +0900
categories: [Java]
tags: [java]
math: true
mermaid: true
---

---

## 1) 기본형, 참조형(Primitive vs Reference)

* 기본형은 실제 사용하는 값을 담는다
  * 기본형은 연산이 가능
  * 기본형은 원시형이라고도 부른다
  * 예) `int i = 0` 



* 참조형은 객체의 메모리 주소를 담는다(참조값)
  * ```.```을 통해 멤버 변수에 접근해서 연산에 사용
  * 예) `Student s = new Student();`

<br>

---

## 2) 참조형 대입

* 참조형에 대입하는 경우 변수에 들어가 있는 참조값을 복사해서 대입하는 것이다
* 주소만 복사되는 것이다



* 메소드 호출하는 경우에도 메소드에 참조형 인수를 전달하면 해당 참조값이 복사되어서 전달됨
  * 참조값이라는 것은 결국에 객체에 접근하기 위한 주소
  * 해당 참조값으로 멤버 변수를 변경하면 당연히 호출자의 객체도 변경이 됨

<br>

```java
public class RF1 {
    public static void main(String[] args) {
      
        Unit unit1 = createUnit("Marine", 30, 150);
        Unit unit2 = createUnit("Firebat", 50, 250);

        printUnit(unit1);
        printUnit(unit2);
    }

    static Unit createUnit(String name, int attack, int defense) { // return 타입이 Unit
        
        Unit unit = new Unit();
        unit.name = name;
        unit.attack = attack;
        unit.defense = defense;
        return unit; // 만들어진 인스턴스의 참조값 반환
    }
    static void printUnit(Unit unit){
        System.out.println("Unit name: "+unit.name+"| Attack: "+unit.attack+"| Defense: "+unit.defense);
    }
}
```

```
Unit name: Marine| Attack: 30| Defense: 150
Unit name: Firebat| Attack: 50| Defense: 250
```

<br>

---

## 3) null

* 참조 변수가 참조가 없는 경우(어떠한 객체도 가리키지 않는 경우)
* 참조할 대상을 나중에 입력하기 위해서 비어있는 참조형 변수에 ```null```을 넣어둔다



* 이미 참조값이 있는 참조변수에 ```null```을 넣는 경우 해당 참조값(메모리 주소)을 알아낼 수 있는 방법이 없기 때문에 해당 인스턴스는 메모리만 차지
  * ```c```언어 같은 경우에는 ```malloc```으로 메모리를 allocate하고 ```free```로 메모리를 놔줌
  * ```java```에서는 JVM의 GC(Garbage Collector)가 사용하지 않는 인스턴스를 자동으로 메모리에서 제거

<br>

---

## 4) NullPointerException(NPE)

* ```null```값을 가지는 객체를 호출하는 경우 발생한다
  * ```.```을 통해 ```null```값에 접근하는 경우
  * 예시: ```null```값을 가진 객체에 대해 메소드를 호출하는 경우



* `null safe`하게 코딩하는 것이 중요하다 

---

## Reference

1. [티스토리 Inpa Dev-Java NULL](https://inpa.tistory.com/entry/JAVA-%E2%98%95-%EA%B0%9C%EB%B0%9C%EC%9E%90%EB%93%A4%EC%9D%84-%EA%B4%B4%EB%A1%AD%ED%9E%88%EB%8A%94-NULL-%ED%8C%8C%ED%97%A4%EC%B9%98%EA%B8%B0)