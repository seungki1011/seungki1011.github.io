---
title: (ThymeLeaf - 1) 타임리프 맛보기
description: 타임리프를 상품 관리 기능을 만들면서 경험해보기
author: seungki1011
date: 2024-03-18 12:30:00 +0900
categories: [Backend, Spring MVC]
tags: [spring, springmvc, thymeleaf]
math: true
mermaid: true
---

---

## 1. 타임리프(Thymeleaf) 소개

타임리프 공식 문서 : [https://www.thymeleaf.org/documentation.html](https://www.thymeleaf.org/documentation.html)

타임리프의 특징은 다음과 같다.

* [SSR(server-side rendering)](https://seungki1011.github.io/posts/springmvc-1-web/#4-ssrserver-side-rendering-csrclient-side-rendering)
* 스프링 통합 지원
  * 타임리프는 스프링의 다양한 기능을 편리하게 사용할 수 있도록 지원한다

<br>

> Natural Templates
>
> HTML templates written in Thymeleaf still look and work like HTML, letting the actual templates that are run in your application keep working as useful design artifacts.
>
> 쉽게 말해서 타임리프는 순수 HTML을 최대한 유지하는 특징이 있다. 타임리프로 작성한 파일은 HTML을 유지하기 때문에 웹 브라우저에서 파일을 직접 열어도 내용을 확인할 수 있고, 서버를 통해 뷰 템플릿을 거치면 동적으로 변경된 결과를 확인할 수 있다.
{: .prompt-tip }

<br>

타임리프에 대한 기능을 자세히 살펴보기 전에 이번 포스트에서는 타임리프를 간단하게 사용해보는 실습을 진행해보자.

간단한 상품 관리 페이지를 타임리프를 이용해서 만들어보자.

<br>

> * 해당 타임리프 실습은 데이터베이스 연결없이 그냥 메모리 내에서 처리하도록 하자. (JPA, JDBC 사용 X)
> * 스프링 부트 3.2 부터 자바 컴파일러에 `-parameters` 옵션을 추가해야 애노테이션 이름 생략이 가능하다
>   * 문제가 되는 애노테이션 : `@RequestParam`, `@PathVariable`
    {: .prompt-warning }

<br>

---

## 2. 요구 사항 (타임리프 실습 시작)

상품 관리 기능의 요구 사항을 살펴보자.

<br>

* **상품 모델**
  * 상품 ID : `id`
  * 상품명 : `itemName`
  * 가격 : `price`
  * 수량 : `quantity`

* **상품 관리 기능**
  * 상품 목록
  * 상품 상세
  * 상품 등록
  * 상품 수정
  * 상품 삭제

<br>

![viewlogic](img/viewlogic.png)_뷰/컨트롤러 흐름_

<br>

---

## 3. Item 도메인

상품 모델인 `Item`을 만들어보자.

<br>

`Item`

```java
@Getter @Setter
@NoArgsConstructor
public class Item {

    private Long id;
    private String itemName;
    private Integer price;
    private Integer quantity;

    public Item(Long id, String itemName, Integer price, Integer quantity) {
        this.id = id;
        this.itemName = itemName;
        this.price = price;
        this.quantity = quantity;
    }
}
```

* `Integer` 사용은 혹시 `0`이 아니라 `null` 값인 경우를 대비해서 사용

<br>

이번에는 상품 레포지토리를 만들어보자.

<br>

`ItemRepository`

```java
@Repository
public class ItemRepository {

    /**
     * static을 사용해야 메모리에 공통 관리
     * 동시에 여러 스레드에서 접근하는 경우라면 ConcurrentHashMap을 사용해야 함
     */
    private static final Map<Long, Item> itemStore = new HashMap<>();
    private static long sequence = 0L;

    public Item save(Item item) {
        item.setId(sequence++);
        itemStore.put(item.getId(), item);
        return item;
    }

    public Item findById(Long id) {
        return itemStore.get(id);
    }

    public List<Item> findAll() {
        return new ArrayList<>(itemStore.values());
    }

    public void update(Long itemId, Item updateParam) {
        Item item = findById(itemId);
        item.setItemName(updateParam.getItemName());
        item.setPrice(updateParam.getPrice());
        item.setQuantity(updateParam.getQuantity());
    }

    public void delete(Long itemId) {
        itemStore.remove(itemId);
    }

    public void clearItemStore() {
        itemStore.clear();
    }

}
```

<br>

해당 레포지토리를 테스트 해보자.

```java
@SpringBootTest
class ItemRepositoryTest {

    private final ItemRepository itemRepository = new ItemRepository();

    @AfterEach
    void afterEach() {
        itemRepository.clearItemStore();
    }


    @DisplayName("아이템을 저장하면 찾을 수 있어야한다")
    @Test
    public void test_save_findById() {
        Item item = new Item(1L, "Chicken", 22000, 10);

        Item savedItem = itemRepository.save(item);
        Item findItem = itemRepository.findById(item.getId());

        assertThat(savedItem).isEqualTo(findItem);
    }

    @DisplayName("아이템을 한개 저장후, 아이템을 삭제하면 빈 리스트가 반환된다")
    @Test
    public void test_delete() {
        Item item = new Item(1L, "Chicken", 22000, 10);

        Item savedItem = itemRepository.save(item);
        itemRepository.delete(savedItem.getId());
        List<Item> itemList = itemRepository.findAll();

        assertThat(itemList).isEmpty();
    }

}
```

* 확인해보면 정상적으로 테스트가 통과되는 것을 확인할 수 있다

<br>

---

## 4. HTML

### 4.1 사용할 HTML 코드

다음은 타임리프를 사용할 베이스가 될 HTML 코드들이다. 타임리프를 적용하기 위해 수정할 것이다.

<br>

* `/resources/static/css/bootstrap.min.css` : 부트스트랩(Bootstrap) 파일 추가
  * [부트스트랩 5.0 다운로드](https://getbootstrap.com/docs/5.0/getting-started/download/)



* `/resources/static/item/` : 이 경로에 넣어서 정적 리소스로 제공하는 방식을 사용할 것이다
  * `items.html`
  * `item.html`
  * `addForm.html`
  * `editForm.html`

<br>

> `/resources/static` 디렉토리 안에 정적 리소스를 넣으면 전부 공개되기 때문에 주의를 요한다. 현재 사용하는 HTML 파일들은 이후에 타임리프를 사용하기 위해서, 수정 후에 `/resources/templates`에 뷰 템플릿 HTML로 보관할 것이다.
{: .prompt-danger }


<br>

`items.html` : 상품 목록 페이지

```html
<!DOCTYPE HTML>
<html>

<head>
  <meta charset="utf-8">
  <link href="../css/bootstrap.min.css" rel="stylesheet">
</head>

<body>
<div class="container" style="max-width: 600px">
  <div class="py-5 text-center">
    <h2>상품 목록</h2>
  </div>
  <div class="row">
    <div class="col">
      <button class="btn btn-primary float-end"
              onclick="location.href='addForm.html'"
              type="button">상품 등록</button>
    </div>
  </div>
  <hr class="my-4">
  <div>
    
    <table class="table">
      <thead>
      <tr>
        <th>ID</th>
        <th>상품명</th> 
        <th>가격</th> 
        <th>수량</th>
      </tr>
      </thead>
      <tbody>
      <tr>
        <td><a href="item.html">1</a></td>
        <td><a href="item.html">테스트 상품 A</a></td> 
        <td>1000</td>
        <td>10</td>
      </tr> 
      <tr>
        <td><a href="item.html">2</a></td>
        <td><a href="item.html">테스트 상품 B</a></td> 
        <td>10000</td>
        <td>20</td>
      </tr>
      </tbody>
    </table>
    
  </div>
</div> <!-- /container -->
</body>
</html>
```

<br>

`addForm.html` : 상품 등록 페이지

```html
<!DOCTYPE HTML>
<html>
<head>
    <meta charset="utf-8">
    <link href="../css/bootstrap.min.css" rel="stylesheet">
    <style>
        .container {
            max-width: 560px;
        }
    </style>
</head>

<body>
<div class="container">
    <div class="py-5 text-center">
        <h2>상품 등록 폼</h2>
    </div>

    <h4 class="mb-3">상품 입력</h4>

    <form action="item.html" method="post">
        <div>
            <label for="itemName">상품명</label>
            <input type="text" id="itemName" name="itemName" class="form-control"
                   placeholder="이름을 입력해주세요">
        </div>
        <div>
            <label for="price">가격</label>
            <input type="text" id="price" name="price" class="form-control"
                   placeholder="가격을 입력해주세요">
        </div>
        <div>
            <label for="quantity">수량</label>
            <input type="text" id="quantity" name="quantity" class="form-control"
                   placeholder="수량을 입력해주세요">
        </div>

        <hr class="my-4">
        <div class="row">
            <div class="col">
                <button class="w-100 btn btn-primary btn-lg"
                        type="submit">상품 등록</button>
            </div>
            <div class="col">
                <button class="w-100 btn btn-secondary btn-lg"
                        onclick="location.href='items.html'"
                        type="button">취소</button>
            </div>
        </div>
    </form>
</div> <!-- /container -->
</body>
</html>
```

<br>

`item.html`, `editForm.html`을 보여주지 않는 이유는 어차피 기존 HTML들에 타임리프를 사용하기 위해서 수정을 하고 사용하게 될 것이기 때문이다.

지금은 사용할 HTML의 모양이 이렇다 정도만 알고있으면 된다.

<br>

---

### 4.2 화면으로 확인

아래 그림은 각 HTML 페이지들이 랜더링된 모습이다.

<br>

![itemhtml](img/item-html.png)_각 페이지의 모습_

<br>

---

## 5. 컨트롤러 구현, 타임리프 구현 

이제 컨트롤러를 만들고, 제대로 사용하기 위해서 기존의 HTML 파일을 타임리프로 수정해서 `templates` 하위에 넣자.

<br>

### 5.1 상품 목록

먼저 상품 목록을 위한 컨트롤러와 뷰를 만들어보자.

일단 상품 목록(`items.html`)을 위한 컨트롤러를 작성해보자.

```java
@Controller
@RequestMapping("/basic/items") // 공통 경로 설정
@RequiredArgsConstructor
public class BasicItemController {

    private final ItemRepository itemRepository;

    // 테스트 데이터 추가
    @PostConstruct
    public void initDb() {
        itemRepository.save(new Item(1L, "테스트 상품 A", 1000, 10));
        itemRepository.save(new Item(2L, "테스트 상품 B", 10000, 20));
    }

    @GetMapping
    public String items(Model model) {
        List<Item> itemList = itemRepository.findAll();
        model.addAttribute("items", itemList);
        return "basic/items";
    }

}
```

<br>

---

#### 5.1.1 타임리프 선언, 타임리프 속성(th:속성)으로 변경

타임리프를 사용하기 위해서는 현재의 `items.html`을 그대로 사용할 수 없다. 

일단 `items.html`을 복사해서 `resources/templates/basic` 하위에 넣자. 이제 타임리프를 사용하기 위해서 html 파일을 조금 수정해보자.

<br>

`items.html`

```html
<!DOCTYPE HTML>
<html xmlns:th="http://www.thymeleaf.org">

<head>
  <meta charset="utf-8">
  <link href="../css/bootstrap.min.css"
        th:href="@{/css/bootstrap.min.css}" rel="stylesheet">
</head>
```

* `<html xmlns:th="http://www.thymeleaf.org">` : 타임리프의 사용 선언

* ```html
  <link href="../css/bootstrap.min.css"
          th:href="@{/css/bootstrap.min.css}" rel="stylesheet">
  ```

  * HTML을 그대로 보는 경우 기본값인 `href`를 사용한다
  * 타임리프 템플릿을 거치게 되면 `th:href`의 값을 사용한다
  * 계속 `th:xxx`를 보게 될텐데, 간단하게 말해서 타임리프 템플릿을 거치게 되면 원래 값이 `th:xxx`로 변경된다고 생각하면 된다
    * `th:xxx`의 부분이 서버사이드 랜더링 되는 것이다
    * 대부분 HTML 속성은 `th:xxx` 같은 형식으로 변경이 가능하다
  * `@{}` : 타임리프의 URL 링크 표현식

<br>

---

#### 5.1.2 리터럴 대체

등록 버튼을 누르면 그냥 `addForm.html`로 가도록 링크가 설정되어 있다. 이것을 타임리프를 사용해서 고쳐보자.

```html
<button class="btn btn-primary float-end"
              onclick="location.href='addForm.html'"
              th:onclick="|location.href='@{/basic/items/add}'|"
              type="button">상품 등록</button>
```

* `th:onclick="|location.href='@{/basic/items/add}'|"` : `th:onclick`을 추가해서, 클릭시 `|location.href='@{/basic/items/add}'|`로 간다
* 여기서 `||`를 리터럴 대체 문법이라고 한다
  * 타임리프에서는 문자, 표현식, 등은 분리되어 있기 때문에 원래는 `+`로 더해서 사용해야 한다
  * `||`로 감싸서 사용하면 `+`를 사용할 필요없이 편리하게 사용할 수 있다
  * 파이썬의 `fstring`같은 느낌이다  

<br>

---

#### 5.1.3 루프 돌려서 품목 출력(th:each)

기존 상품 목록을 출력하던 부분을 타임리프를 사용해서 동적으로 출력할 수 있도록 변경해보자.

```html
<tr th:each="item : ${items}">
  <td>
    <a href="item.html" 
       th:href="@{/basic/items/{itemId} (itemId=${item.id})}" 
       th:text="${item.id}">회원id</a>   
  </td>
  <td>
    <a href="item.html" 
       th:href="@{|/basic/items/${item.id}|}" 
       th:text="${item.itemName}">상품명</a>
  </td>
  <td th:text="${item.price}">10000</td>
  <td th:text="${item.quantity}">10</td>
</tr>
```

* `<tr th:each="item : ${items}">`
  * `th:each`를 통해서 반복문 사용이 가능하다
  * 모델에 포함된 `items` 컬렉션의 데이터가 하나씩 `item`에 할당되면서, 반복문 안에서 `item`을 사용할 수 있다
  * `item`의 수만큼 동적으로 생성된다
* `${}`
  * 변수 표현식이라고 한다
  * 모델에 포함된 값, 타임리프 변수로 선언된 값을 조회할 수 있다
  * 현재의 경우를 예로 들자면, `item.itemName` 처럼 사용해서 `item`의 이름을 조회할 수 있다
* `th:text`
  * 내용을 변경한다
  * `<td th:text="${item.price}">10000</td>` : 해당 `10000`을 `${item.price}`으로 변경한다

<br>

---

#### 5.1.4 링크 표현식에 경로 변수 표현

바로 이전 케이스에서의 링크 표현식을 자세히 살펴보자. 

살펴보면 링크 표현식에 경로 변수(path variable) 처럼 보이는 것이 존재하는 것을 확인할 수 있다. (`{itemId}`)

이번에는 링크 표현식에 경로 변수를 설정하는 방법을 알아보자.

<br>

```html
<a href="item.html" 
   th:href="@{/basic/items/{itemId}(itemId=${item.id})}" 
   th:text="${item.id}">회원id</a>  
```

* `th:href="@{/basic/items/{itemId} (itemId=${item.id})}"`
  * 상품 ID를 선택할 수 있는 링크이다. (그럼 당연히 ID에 대한 경로 변수를 표현할 수 있어야한다)
  * `{itemId} (itemId=${item.id})` 해당 문법을 사용하면 `itemId`에 `item.id`를 입력할 수 있다



* 경로 변수를 표현하는 것도 가능하지만, 여기에 쿼리 파라미터를 붙여주는 것도 가능하다
  * 예시) `th:href="@{/basic/items/{itemId}(itemId=${item.id}, query='test1')"`
  * 생성되는 링크의 경로 : `/basic/items/1?query=test1`



* 리터럴 대체 문법을 사용해서 뒤의 `(itemId=${item.id})`를 제거해서 사용하는 것도 가능하다
  * 예시) `th:href="@{|/basic/items/${item.id}|}"`

<br>

---

### 5.2 상품 상세

상품 상세 페이지를 위한 컨트롤러와 뷰를 구현해보자.

일단 상품 상세(`item.html`)를 위한 컨트롤러를 작성해보자.

<br>

```java
/**
 * "/basic/items/{itemId}"로 매핑
 * 상품ID로 상품을 조회해서 모델에 담아둔다
 */
@GetMapping("/{itemId}")
public String item(@PathVariable long itemId, Model model) {
    Item item = itemRepository.findById(itemId);
    model.addAttribute(item);
    return "basic/item";
}
```

<br>

---

#### 5.2.1 th:value로 변경

상품 목록과 마찬가지로 `item.html`을 복사해서 `templates/basic`에 넣자.

이전과 마찬가지로 타임리프 사용을 선언하고, CSS 링크를 설정해주자.

<br>

타임리프를 적용하기 전에는 `value` 속성에 미리 설정한 값을 이용해서 상세화면의 정보가 출력되는 것을 확인할 수 있다.

이를 `th:value`를 추가해서 해당 값을 동적으로 읽어올 수 있도록 구현하자. 

<br>

```html
<div>
    <label for="itemId">상품 ID</label>
    <input type="text" id="itemId" name="itemId" class="form-control"
           value="1" th:value="${item.id}" readonly>
</div>
<div>
    <label for="itemName">상품명</label>
    <input type="text" id="itemName" name="itemName" class="form-control"
           value="테스트 상품 A" th:value="${item.itemName}" readonly> </div>
<div>
    <label for="price">가격</label>
    <input type="text" id="price" name="price" class="form-control"
           value="1000" th:value="${item.price}" readonly>
</div>
<div>
    <label for="quantity">수량</label>
    <input type="text" id="quantity" name="quantity" class="form-control"
           value="10" th:value="${item.quantity}" readonly>
</div>
```

* `th:value="${item.id}"`
  * 위와 같은 형식으로 `item` 정보를 획득해서 `value` 값을 대체한다\

<br>

---

#### 5.2.2 버튼에 링크 표현식 추가

상품 수정, 상품 삭제, 목록으로 버튼에 링크 표현식을 추가하자.

<br>

```html
<div class="col">
    <button class="w-100 btn btn-primary btn-lg"
            onclick="location.href='editForm.html'"
            th:onclick="|location.href='@{/basic/items/{itemId}/edit(itemId=${item.id})}'|"
            type="button">상품 수정</button>
</div>
<div class="col">
    <form th:action="@{/basic/items/{itemId}/delete(itemId=${item.id})}" method="post">
            <button class="w-100 btn btn-danger btn-lg" type="submit">상품 삭제</button>
    </form>
</div>
<div class="col">
    <button class="w-100 btn btn-secondary btn-lg"
            onclick="location.href='items.html'"
            th:onclick="|location.href='@{/basic/items}'|"
            type="button">목록으로</button>
</div>
```

* `th:onclick="|location.href='@{/basic/items/{itemId}/edit(itemId=${item.id})}'|"`
  * 상품 수정 링크에 대한 표현식
* `th:onclick="|location.href='@{/basic/items}'|"`
  * 상품 목록으로 가는 표현식

<br>

상품 삭제 버튼과 관련된 내용은 뒤에 이어서 설명하겠다.

<br>

---

### 5.3 상품 삭제(POST 요청 폼)

위의 상품 삭제 버튼과 관련된 내용을 살펴보자.

먼저 상품 삭제를 위한 컨트롤러를 작성하자.

<br>

```java
@PostMapping("/{itemId}/delete")
public String delete(@PathVariable long itemId) {
    itemRepository.delete(itemId);
    return "redirect:/basic/items";
}
```

* 상품 삭제 버튼을 누르면 `/basic/items/{itemId}/delete`의 경로로 `POST` 요청을 하도록 타임리프를 구현해야 한다
* 상품 삭제 버튼을 누르면 해당 상품ID에 해당하는 상품을 삭제하고 `/basic/items`으로 리다이렉트 하도록한다

<br>

> * 리다이렉트를 하는 이유는 새로고침시 중복 요청이 날아가는 문제와 뷰의 데이터를 업데이트 해서 최신 상태로 유지하기 위함이다
> * 이와 관련된 내용은 뒤에서 `PRG(POST/Redirect/GET)` 패턴을 다룰 때 자세히 살펴볼 것이다
{: .prompt-info }

<br>

이제 다시 상품 상세 폼에서 상품 삭제와 관련된 타임리프 HTML을 살펴보자.

```html
<div class="col">
    <form th:action="@{/basic/items/{itemId}/delete(itemId=${item.id})}" method="post">
            <button class="w-100 btn btn-danger btn-lg" type="submit">상품 삭제</button>
    </form>
</div>
```

* `<form th:action="@{/basic/items/{itemId}/delete(itemId=${item.id})}" method="post">`
  * `POST` 방식의 폼에서 `th:action`을 `/basic/items/{itemId}/delete(itemId=${item.id})`으로 설정해서, 설정한 URL로 전송할 수 있도록 한다

<br>

> 폼 태그 안의 버튼 태그에서 `onclick`을 설정하면, 해당 `onclick` 속성이 우선권을 가지게 되어 `GET` 요청이 나가기 때문에 주의를 요한다.
{: .prompt-warning }

<br>

---

### 5.4 상품 등록

상품 등록과 관련된 코드를 구현해보자.

#### 5.4.1 상품 등록 컨트롤러

등록에 대한 경로를 `/add`로 똑같이 사용해서 요청 메서드에 따라 기능을 구분할 것이다.

* 상품 등록 폼 뷰 : `GET` `/basic/items/add`
* 상품 등록 로직 처리 : `POST` `/basic/items/add`

<br>

먼저 상품 등록 폼의 뷰를 호출 컨트롤러를 작성해보자.

```java
@GetMapping("/add")
public String addForm() {
    return "basic/addForm";
}
```

* `@GetMapping`을 사용해서 단순히 상품 등록 폼의 뷰를 호출한다

<br>

이제 상품 등록 자체를 처리하는 컨트롤러를 작성해보자. 뷰를 호출하는 컨트롤러와 기능을 구분하기 위해서 `@PostMapping` 사용

해당 컨트롤러는 다양한 방법으로 작성이 가능하며, 각 방법의 특징을 다음 코드로 살펴보자.

```java
/**
 * 상품 등록 로직 처리
 * 동일하게 "/add"를 사용하지만 메서드로 기능을 구분
 * 등록을 처리하는 방법은 엄청 다양하다
 * ------------------------------------------------
 * 상품 등록 V1 : @RequestParam 사용
 * - @RequestParam를 사용해서 요청 파라미터 데이터를 변수에 담는다
 * - Item 객체를 생성해서 itemRepository를 통해 저장한다
 * - 저장된 객체 item을 모델에 담아서 뷰에 전달한다
 */
// @PostMapping("/add")
public String addItemV1(@RequestParam String itemName,
                        @RequestParam int price,
                        @RequestParam Integer quantity,
                        Model model) {
    Item item = new Item();
    item.setItemName(itemName);
    item.setPrice(price);
    item.setQuantity(quantity);
    itemRepository.save(item);
    model.addAttribute("item", item);
    return "basic/item";
}

/**
 * 상품 등록 V2 : @ModelAttribute 사용
 * - @ModelAttribute는 Item 객체를 생성해서 요청 파라미터를 setItem 형태로 입력해준다
 * - @ModelAttribute는 모델에 지정한 객체를 자동으로 넣어준다
 */
// @PostMapping("/add")
public String addItemV2(@ModelAttribute("item") Item item, Model model) {
    itemRepository.save(item);
    // model.addAttribute("item", item); // 자동으로 넣어준다, 생략 가능
    return "basic/item";
}

/**
 * 상품 등록 V3 : @ModelAttribute의 이름 생략
 * - @ModelAttribute의 이름 ("item") 생략 가능
 * - 생략하는 경우 모델에 저장될때 사용되는 클래스명의 첫 글자를 소문자로 변경해서 등록한다
 * - Item -> item 으로 변경해서 모델에 자동 등록
 */
@PostMapping("/add")
public String addItemV3(@ModelAttribute Item item) {
    itemRepository.save(item);
    return "basic/item";
}

/**
 * 상품 등록 V4 : @ModelAttribute 전체 생략
 * - V3와 동일하지만 @ModelAttribute 자체를 생략해서 사용하는 경우
 */
// @PostMapping("/add")
public String addItemV4(Item item) {
    itemRepository.save(item);
    return "basic/item";
}
```

* `addItemV3`을 사용 예정
* 사실이 등록을 위한 컨트롤러에는 문제가 존재한다. 만약 등록을 완료후에 새로 고침을 누른다면, 등록 요청이 중복으로 계속 이루어지는 것을 확인할 수 있다. 이런 문제를 해결하기 위해서 `PRG` 패턴을 사용한다. 이에 대해서 뒤에서 자세히 다룰 것이다.

<br>

---

#### 5.4.2 상품 등록 폼 뷰

상품 등록의 위한 뷰 템플릿을 만들자.

먼저 기존의 `addForm.html`을 복사해서 `resources/basic`에 넣어준다. 기존에 해왔던 것 처럼 타임리프 선언을 포함한 준비 작업을 다 적용한다.

변경할 부분은 폼 태그 부분이다. 다음과 같이 변경하면 된다.

```html
<form action="item.html" th:action method="post">
    <div>
        <label for="itemName">상품명</label>
        <input type="text" id="itemName" name="itemName" class="form-control"
               placeholder="이름을 입력해주세요">
    </div>
    <div>
        <label for="price">가격</label>
        <input type="text" id="price" name="price" class="form-control"
               placeholder="가격을 입력해주세요">
    </div>
    <div>
        <label for="quantity">수량</label>
        <input type="text" id="quantity" name="quantity" class="form-control"
               placeholder="수량을 입력해주세요">
    </div>

    <hr class="my-4">
    <div class="row">
        <div class="col">
            <button class="w-100 btn btn-primary btn-lg"
                    type="submit">상품 등록</button>
        </div>
        <div class="col">
            <button class="w-100 btn btn-secondary btn-lg"
                    onclick="location.href='items.html'"
                    th:onclick="|location.href='@{/basic/items}'|"
                    type="button">취소</button>
        </div>
    </div>
</form>
```

* `<form action="item.html" th:action method="post">`
  * `th:action`을 비워놓는 것은 현재 URL에 데이터를 전달한다는 뜻
    * 현재 URL 경로 `/basic/items/add`
    * `post` 방식으로 설정되어 있기 때문에 `/add`에 `POST` 요청이 들어간다
* `th:onclick="|location.href='@{/basic/items}'|"`
  * 취소 버튼을 누르면 상품 목록으로 이동한다

<br>

---

### 5.5 상품 수정

상품 수정 기능을 구현하자.

#### 5.5.1 상품 수정 컨트롤러

이전의 상품 등록과 마찬가지로 수정에 대한 경로를 `/{itemId}/edit`을 수정 폼과 로직 처리에 대해 동일하게 사용하고, 메서드를 다르게 해서 구분할 것이다.

* 상품 수정 폼 뷰 : `GET` `/basic/items/{itemId}/edit`
* 상품 수정 로직 : `POST` `/basic/items/{itemId}/edit`

<br>

먼저 상품 수정 폼의 컨트롤러를 만들자.

```java
@GetMapping("/{itemId}/edit")
public String editForm(@PathVariable Long itemId, Model model) {
    Item item = itemRepository.findById(itemId);
    model.addAttribute("item", item);
    return "basic/addForm";
}
```

* 수정에 필요한 정보 조회
* 수정 폼 뷰 호출

<br>

이제 상품 수정 로직을 위한 컨트롤러를 만들자.

```java
@PostMapping("/{itemId}/edit")
public String edit(@PathVariable Long itemId, @ModelAttribute Item item) {
    itemRepository.update(itemId, item);
    return "redirect:/basic/items/{itemId}";
}
```

* 이전의 상품 등록 컨트롤러와 유사하다
* 여기서도 `redirect`를 사용해서 뷰 템플릿을 호출하는 것이 아니라 상품 상세 페이지로 리다이렉트 시킨다

<br>

---

#### 5.5.2 상품 수정 폼 뷰

싱픔 수정 폼의 뷰를 구현하기 위해서 `editForm.html`을 복사해서 `resources/basic`에 넣자.

기존 등록 폼과 유사하다.

```html
<form action="item.html" th:action method="post">
    <div>
        <label for="id">상품 ID</label>
        <input type="text" id="id" name="id" class="form-control"
               value="1" th:value="${item.id}" readonly>
    </div>
    <div>
        <label for="itemName">상품명</label>
        <input type="text" id="itemName" name="itemName" class="form-control"
               value="테스트 상품 A" th:value="${item.itemName}">
    </div>
    <div>
        <label for="price">가격</label>
        <input type="text" id="price" name="price" class="form-control"
               value="1000" th:value="${item.price}">
    </div>
    <div>
        <label for="quantity">수량</label>
        <input type="text" id="quantity" name="quantity" class="form-control"
               value="10" th:value="${item.quantity}">
    </div>

    <hr class="my-4">
    <div class="row">
        <div class="col">
            <button class="w-100 btn btn-primary btn-lg"
                    type="submit">저장</button>
        </div>
        <div class="col">
            <button class="w-100 btn btn-secondary btn-lg"
                    onclick="location.href='item.html'"
                    th:onclick="|location.href='@{/basic/items/{itemId}(itemId=${item.id})}'|"
                    type="button">취소</button>
        </div>
    </div>
</form>
```

* 상품 등록과 마찬가지로 `th:action`을 비워둬서 현재 경로 데이터가 전송이 되도록 설정한다
* 나머지도 유사하다

<br>

---

## 6. PRG(POST/Redirect/GET) 패턴

### 6.1 PRG 패턴 설명

이전의 상품 등록 컨트롤러에서 문제가 있다고 설명한 것을 떠올려보자.

문제의 코드를 살펴보자.

```java
@PostMapping("/add")
public String addItemV3(@ModelAttribute Item item) {
    itemRepository.save(item);
    return "basic/item";
}
```

<br>

위의 컨트롤러 코드를 사용하는 경우, 등록을 완료후에 새로 고침을 누른다면 등록 요청이 중복으로 계속 이루어지는 것을 확인할 수 있다.

이런 문제가 발생하는 이유는 브라우저의 새로 고침은 서버에 마지막으로 전송하는 데이터를 다시 전송하는 기능이기 때문이다.

쉽게 말해서 상품 데이터를 `POST /add`로 서버에 전송하고 새로고침을 한다면 다시 상품 데이터와 `POST /add`를 다시 보내는 것이다. 이렇기 때문에, 새로고침을 계속하면 똑같은 상품 내용으로 등록이 계속 이루어진다.

<br>

이 문제를 해결하는 것이 PRG 패턴을 사용하는 것이다. 우리가 사용하는 상품 등록을 PRG 패턴으로 구현한다면 다음과 같이 동작해야한다.

1. 등록 `POST` 요청
2. `POST` 요청을 후에 상품이 등록되고 해당 상품 상세창으로 `redirect`
3. `redirect`를 통해 온 상품 상세를 `GET` 요청으로 받아온다

<br>

이렇게 구현하면 새로고침을 하더라도 마지막 요청은 `GET` 요청이기 때문에, 아무리 새로고침을 해도 상품 상세창을 `GET` 요청으로 불러오기만 한다.

<br>

---

### 6.2 상품 등록 컨트롤러 PRG 적용

그러면 상품 등록 컨트롤러를 수정해보자.

```java
/**
 * PRG - Post/Redirect/Get
 * RedirectAttributes 사용
 */
@PostMapping("/add")
public String addItem(Item item, RedirectAttributes redirectAttributes) {
    Item savedItem = itemRepository.save(item);
    redirectAttributes.addAttribute("itemId", savedItem.getId());
    redirectAttributes.addAttribute("status", true);
    return "redirect:/basic/items/{itemId}";
}
```

* `status`에 `true`를 추가해서, 뷰 템플릿에 만약 `status`가 `true`로 들어온다면 `저장 완료!`라고 출력되도록 구현할 수 있다
  * 아래에서 뷰템플릿 어떻게 추가하면 되는지 살펴보자
* 상품을 등록해보면 다음과 같은 리다이렉트 결과가 나온다 `http://localhost:8080/basic/items/3?status=true`
* `RedirectAttributes`를 통해서 URL 인코딩, 경로 변수, 쿼리 파라미터 처리까지 할 수 있다

<br>

> 왜 PRG 패턴을 `return "redirect:/basic/items/" + item.getId();` 으로 작성하지 않고 `RedirectAttributes`를 사용하는 것일까?
>
> 몇가지 이유를 찾아보면 다음과 같다.
>
> * `RedirectAttributes`는 `itemId`를 인코딩해줘서 URL에 안전하게 사용할 수 있도록 해준다
> * 제3자가 해당 변수를 통해 특정 보안 위협을 하는 것을 막아줄 수 있다
{: .prompt-info }

<br>

`status`가 `true`로 들어온다면 `저장 완료!`라고 출력되도록 타임리프 구현. `item.html`에 추가한다.

```html
<div class="container">
     <div class="py-5 text-center">
         <h2>상품 상세</h2> 
     </div>
     <!-- 추가 -->
     <h2 th:if="${param.status}" th:text="'저장 완료!'"></h2>
```

* `th:if` : 해당 조건이 참인 경우 실행
* `${param.status}` : 쿼리 파라미터를 조회
* 쿼리 파라미터를 조회해서 `status`가 `true`면 `저장 완료!` 출력

<br>

---

### 6.3 기능 동작 확인

직접 기능을 사용해보면 상품 관리 페이지의 동작을 확인해보자.

<br>

![itemhtml](img/check.png)

<br>

전부 정상적으로 실행되는 것을 확인할 수 있다.

<br>

---

## Reference

1. [스프링 MVC - 백엔드 웹 개발 핵심 기술](https://www.inflearn.com/course/%EC%8A%A4%ED%94%84%EB%A7%81-mvc-1)
2. [Udemy - Spring Boot 3, Spring 6 & Hibernate](https://www.udemy.com/course/spring-hibernate-tutorial/?couponCode=ST8MT40924)
