---
title: TDD(테스트 주도 개발) 소개
description: TDD(Test Driven Development), BDD 등에 대한 소개
author: seungki1011
date: 2024-07-07 10:30:00 +0900
categories: [4. 소프트웨어 엔지니어링(SWE), Test]
tags: [test, tdd, bdd, aaa, gwt]
math: true
mermaid: true
---

## 1. TDD(Test Driven Development) 소개

**TDD(Test Driven Development)**, 한글로 번역하면 **테스트 주도 개발**이 무엇인지 알아보자.

먼저 TDD라는 것은 **프로덕션 코드보다 테스트 코드를 먼저 작성해서 테스트가 코드의 구현 과정을 주도**하도록 하는 개발 방법론이다.

<br>

> **TDD의 등장배경**
>
> * 80 ~ 90년대에 반복적 점진적 개발(Iterative and Incremental Development)이 인기를 얻으면서 관련 개발 방법론들이 대두된다.
> * 특히 90년대 후반에 들어서면서 Kent Back의 **Extreme Programming(익스트림 프로그래밍, XP)**과 더불어서 여러 에자일(Agile) 방법론들이 등장한다.
> * **TDD는 XP의 일부로 처음 제안되면서 알려졌다**
> * 이후 2001년의 [에자일 선언문(Agile Manifesto)](https://agilemanifesto.org/iso/ko/manifesto.html), 2002년에 출간된 [Kent Back : Test Driven Development](https://www.amazon.com/Test-Driven-Development-Kent-Beck/dp/0321146530), 등에 의해 점점 인기를 얻기 시작했다
{: .prompt-info }

<br>

> **Extreme Programming(익스트림 프로그래밍, XP)**
>
> * Kent Back이 제안한 소프트웨어 개발 방법론
>* 12개 정도의 구체적인 실천 방법(practice)을 정의하고 있다
> * 소프트웨어의 품질을 올리고, 지속적으로 변하는 고객 요구 사항에 대응하기 위해서 짧은 주기로 프로토타입을 완성하는 애자일(Agile) 방법론 중 하나이다.
{: .prompt-info }

<br>

TDD로 다시 돌아와서, **테스트 코드를 먼저 작성해서 테스트가 코드의 구현 과정을 주도**한다는 것이 무엇인지 그 과정을 구체적으로 살펴보자.

TDD는 보통 다음의 3 단계를 하나의 사이클로 운영한다. 

<br>

![tdd2](../post_images/2024-07-07-testing-2-tdd/tdd2.png)_TDD cycle_

* **RED**
  * 제일 먼저 실패하는 테스트 코드를 작성한다
  * 이때 테스트 코드는 컴파일 조차 안돼도 괜찮다
* **GREEN**
  * 테스트를 통과하도록 위해 실제(프로덕션) 코드를 작성한다
  * 이때 작성하는 코드는 테스트를 통과할 정도로만 최소한의 코드를 작성하도록 한다
* **BLUE**
  * 코드를 리팩토링한다
  * 설계나 구현을 개선한다
  * 이때 테스트의 통과 상태는 유지되어야 한다

<br>

예시를 통해 알아보자.

<br>

---

## 2. TDD 예시

`ShoppingCart`와 `Item`이 존재한다고 해보자.

<br>

```java
public class ShoppingCart {

    private List<Item> items;

    public ShoppingCart() {
        this.items = new ArrayList<>();
    }
    
    public void addItem(Item item) {
        items.add(item);
    }

    public void removeItem(String name) {
        items.removeIf(item -> item.getName().equals(name));
    }
}
```

* 장바구니에 아이템을 추가하고 삭제하는 기능은 이미 구현되어 있는 상황이다

<br>

```java
@Getter
@AllArgsConstructor
public class Item {
    private String name;
    private int price;
    private int quantity;

    @Override
    public String toString() {
        return "Item{" +
                "name='" + name + '\'' +
                ", price=" + price +
                ", quantity=" + quantity +
                '}';
    }
}
```

<br>

이제 `ShoppingCart`에 담긴 아이템의 **총 가격을 계산하는 기능**을 TDD로 구현한다고 해보자.



<br>

























## Reference

1. [https://tech.kakaopay.com/post/implementing-tdd-in-practical-applications/](https://tech.kakaopay.com/post/implementing-tdd-in-practical-applications/)
2. [인프런 : 실용적인 테스트 가이드](https://www.inflearn.com/course/practical-testing-%EC%8B%A4%EC%9A%A9%EC%A0%81%EC%9D%B8-%ED%85%8C%EC%8A%A4%ED%8A%B8-%EA%B0%80%EC%9D%B4%EB%93%9C/dashboard)
3. [https://developer.ibm.com/articles/5-steps-of-test-driven-development/](https://developer.ibm.com/articles/5-steps-of-test-driven-development/)