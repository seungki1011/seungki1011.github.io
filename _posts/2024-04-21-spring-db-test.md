---
title: (JDBC - 4) 스프링에서의 데이터베이스 테스트
description: JDBC, JdbcTemplate, JPA 등의 데이터 접근 기술을 사용할 때 데이터베이스와 관련된 테스트에 대하여
author: seungki1011
date: 2024-04-21 12:30:00 +0900
categories: [6. 백엔드(Backend), JDBC]
tags: [spring, jdbc, test]
math: true
mermaid: true
---

---

>  JDBC, JdbcTemplate, MyBatis, JPA 등의 데이터 접근 기술을 사용할 때 데이터베이스와 관련된 테스트에 대해 알아보자.

---

## 1. 데이터베이스 연동

JDBC, JdbcTemplate, MyBatis, JPA 등의 데이터 접근 기술을 사용할 때, 실제 데이터베이스에 접근해서 데이터를 잘 저장하고 조회하는지 테스트를 할 수 있어야한다.

<br>

테스트를 진행하기 전 `test/resources/application.properties`를 수정해야한다.

```properties
spring.profiles.active=test

# spring.sql.init.mode=always
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

spring.datasource.url=jdbc:mysql://localhost:3306/real_test_database?serverTimezone=Asia/Seoul
spring.datasource.username=root
spring.datasource.password=admin

logging.level.org.springframework.jdbc=debug
```

<br>

다음의 테스트 코드로 테스트를 실행해보자.

<br>

`ItemRepositoryTest`

```java
@SpringBootTest
class ItemRepositoryTest {

    @Autowired
    ItemRepository itemRepository;

    @AfterEach
    void afterEach() {
        // MemoryItemRepository의 경우 제한적으로 사용
        if (itemRepository instanceof MemoryItemRepository) {
            ((MemoryItemRepository) itemRepository).clearStore();
        }
    }

    @Test
    void save() {
        // given
        Item item = new Item("itemA", 10000, 10);

        // when
        Item savedItem = itemRepository.save(item);

        // then
        Item findItem = itemRepository.findById(item.getId()).get();
        assertThat(findItem).isEqualTo(savedItem);
    }

    @Test
    void updateItem() {
        // given
        Item item = new Item("item1", 10000, 10);
        Item savedItem = itemRepository.save(item);
        Long itemId = savedItem.getId();

        // when
        ItemUpdateDto updateParam = new ItemUpdateDto("item2", 20000, 30);
        itemRepository.update(itemId, updateParam);

        // then
        Item findItem = itemRepository.findById(itemId).get();
        assertThat(findItem.getItemName()).isEqualTo(updateParam.getItemName());
        assertThat(findItem.getPrice()).isEqualTo(updateParam.getPrice());
        assertThat(findItem.getQuantity()).isEqualTo(updateParam.getQuantity());
    }
    
    /**
     * 테스트 실패!
     * 원인은 이전 데이터베이스를 사용하면서 남았던 데이터 때문
     * 테스트를 할 때 기본적으로 격리된 데이터베이스에서 수행해야함
     * 지금의 상황은 마치 프로덕션이나 개발환경 DB를 테스트용으로 사용한것과 마찬가지
     */
    @Test
    void findItems() {
        //given
        Item item1 = new Item("itemA-1", 10000, 10);
        Item item2 = new Item("itemA-2", 20000, 20);
        Item item3 = new Item("itemB-1", 30000, 30);

        itemRepository.save(item1);
        itemRepository.save(item2);
        itemRepository.save(item3);

        // 둘 다 없음 검증
        test(null, null, item1, item2, item3);
        test("", null, item1, item2, item3);

        // itemName 검증
        test("itemA", null, item1, item2);
        test("temA", null, item1, item2);
        test("itemB", null, item3);

        // maxPrice 검증
        test(null, 10000, item1);

        // 둘 다 있음 검증
        test("itemA", 10000, item1);
    }

    void test(String itemName, Integer maxPrice, Item... items) {
        List<Item> result = itemRepository.findAll(new ItemSearchCond(itemName, maxPrice));
        assertThat(result).containsExactly(items);
    }
}
```

* 테스트를 실행해보면, `updateItem()`과 `save()`는 정상적으로 테스트를 통과하지만 `findItems()`는 실패한다
* `findItems()`의 실패 원인은 과거에 서버를 실행하면서 저장했던 데이터가 데이터베이스에 보관되어 있기 때문이다
* 외부에 영향 받지 않는 격리된 환경에서 테스트하는 것이 중요!
  * 지금의 테스트는 기존 DB를 사용하는 것이기 때문에 문제 발생

<br>

데이터베이스의 분리를 통해 문제를 해결해보자.

<br>

---

## 2. 데이터베이스 분리

이전 테스트에서의 문제를 해결하기 위해서 테스트 전용으로 데이터베이스를 분리해보자.

<br>

`test/resources/application.properties`에서의 DB 엔드포인트 설정을 수정하자.

```properties
spring.datasource.url=jdbc:mysql://localhost:3306/testcode_database?serverTimezone=Asia/Seoul
```

* 가장 간단한 방법은 테스트 전용 데이터베이스를 별도로 운영하는 것
* 기존 MySQL 컨테이너에서 `create database testcode_database;`로 테스트코드용 DB를 생성하자
* 기존의 `jdbc:mysql://localhost:3306/test_database`에서 `test_database` → `testcode_database`로 수정

<br>

이제 다시 한번 `findItems()` 테스트를 실행해보자. 이번에는 통과하는 것을 확인할 수 있다. 그러나 다시 한번 `findItems()`를 실행하면 다시 실패하는 것을 볼 수 있다.

실패하는 이유는 테스트를 실행할 때 입력한 데이터가 데이터베이스에 누적되고 있기 때문이다. 우리가 제일 처음 겪었던 문제가 이전 개발 환경에서 사용한 데이터베이스의 기존에 존재했던 데이터 때문이라면, 이번에는 테스트를 실행하면서 생긴 데이터 때문에 반복 테스트가 실패한 것이다. 이를 해결하기 위해서는 테스트 후에 데이터베이스를 초기화 하거나 지우는 작업이 필요하다.

<br>

롤백(rollback)을 통해 문제를 해결해보자.

<br>

---

## 3. Rollback

롤백을 이용해서 테스트 후 데이터가 누적되는 문제를 해결해보자. 

테스트가 끝나고 트랜잭션을 강제로 롤백하면 데이터를 깔끔하게 제거할 수 있다. 데스트 중에 데이터를 이미 저장했는데, 중간에 테스트가 실패해서 롤백을 호출하지 못해도, 트랜잭션을 커밋하지 않았기 때문에 데이터베이스에 해당 데이터가 반영되지 않는다.

<br>

코드를 통해 알아보자.

<br>

`ItemRepositoryTest`

```java
@SpringBootTest
class ItemRepositoryTest {

    @Autowired
    ItemRepository itemRepository;

    /**
     * DataSource와 마찬가지로 스프링에서 자동으로 빈 등록해줌
     */
    @Autowired
    PlatformTransactionManager transactionManager;
    TransactionStatus status;

    @BeforeEach
    void beforeEach() {
        // 트랜잭션 시작
        status = transactionManager.getTransaction(new DefaultTransactionDefinition());
    }

    @AfterEach
    void afterEach() {
        // MemoryItemRepository 의 경우 제한적으로 사용
        if (itemRepository instanceof MemoryItemRepository) {
            ((MemoryItemRepository) itemRepository).clearStore();
        }
        // 트랜잭션 롤백
        transactionManager.rollback(status);
    }
 
  // 기존 코드
}
```

* 다시 전체 테스트를 돌려보면 전부 통과하는 것을 확인할 수 있다(데이터베이스에 데이터가 없어야 함)



* 트랜잭션 관리자는 `PlatformTransactionManager`를 주입받아서 사용
  * 스프링이 자동으로 빈 등록 해줌



* `@BeforeEach`
  * 각각의 테스트 케이스 실행전에 호출된다
  * 여기에서 트랜잭션을 시작하도록 한다
  * 각 테스트를 트랜잭션 범위 안에서 실행할 수 있게 된다



* `@AfterEach`
  * 각 테스트 케이스 실행 완료 후에 호출된다
  * 여기에서 트랜잭션을 롤백한다
  * 롤백 후 트랜잭션 실행 전 상태로 복구된다

<br>

지금까지 구현한 트랜잭션과 롤백에 대한 기능을 편리하게 사용할 수 있도록 해주는 `@Transactional`이 존재한다.

<br>

---

## 4. 테스트에서의 @Transactional

트랜잭션의 롤백을 편리하게할 수 있는 `@Transactional`에 대해 알아보자.

트랜잭션에 사용하던 `@Transactional`을 테스트에서 사용하면 조금 다르게 동작한다.

코드를 통해 알아보자.

<br>

기존 테스트를 복사해서 `ItemRepositoryTestV2`로 만들고. 위에 `@Transactional`을 붙이자.

```java
@Transactional
@SpringBootTest
class ItemRepositoryTestV2 {
  /**
   * 기존 PlatformTransactionManager, @BeforeEach, @AfterEach 삭제
   * 이전의 트랜잭션 관련 코드 전부 제거해도 됨
   */
}
```

* 이전의 트랜잭션을 적용한 코드와 마찬가지로 정상적으로 동작한다

<br>

기존 `@Transactional` 애노테이션은 로직이 성공적으로 수행되면 커밋하도록 동작한다. 그러나 `@Transactional`을 테스트에서 사용하면 다음과 같이 동작한다.

테스트에서 `@Transactional`을 사용하는 경우, 스프링은 테스트를 트랜잭션 안에서 실행하고, 테스트가 끝나면 트랜잭션을 자동으로 롤백시킨다.

<br>

참고로 데이터베이스에 정말로 데이터가 잘 보관되는지 눈으로 확인해보고 싶은 경우라면, 다음과 같이 `@Commit`을 붙이면 테스트 종류후 롤백 대신 커밋이 된다.

```java
@Commit
// @Rollback(value = false)
@Transactional
@SpringBootTest
class ItemRepositoryTest {}
```

* `@Rollback(value = false)`도 `@Commit`과 똑같은 기능을 한다 

<br>

---

## 5. 임베디드 모드(Embedded Mode)

임베디드 모드를 사용하기 위해서는 먼저 H2 데이터베이스를 라이브러리에 추가하자.

<br>

`build.gradle`

```groovy
dependencies {
    //...
    // 추가
    runtimeOnly 'com.h2database:h2'
}
```

<br>

`test/resources/application.properties`의 `datasource`관련 설정을 주석 처리 하자.

```properties
spring.profiles.active=test

# spring.sql.init.mode=always
# spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver

# spring.datasource.url=jdbc:mysql://localhost:3306/real_test_database?serverTimezone=Asia/Seoul
# spring.datasource.username=root
# spring.datasource.password=admin

logging.level.org.springframework.jdbc=debug
```

<br>

별다른 정보를 제공하지 않으면 스프링 부트는 임베디드 모드로 접근하는 `DataSource`를 만들어서 제공한다.

<br>

---

## Reference

1. [인프런 - 김영한 : 스프링 완전 정복](https://www.inflearn.com/roadmaps/373)

