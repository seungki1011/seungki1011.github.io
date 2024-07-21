---
title: (JDBC - 3) JdbcTemplate 소개, 기본 사용법
description: JdbcTemplate의 기본 사용법 알아보기
author: seungki1011
date: 2024-04-19 12:30:00 +0900
categories: [6. 백엔드(Backend), JDBC]
tags: [spring, jdbc, dao]
math: true
mermaid: true
---

---

## 1. JdbcTemplate 실습 준비

상품 관리 프로젝트를 기반으로 단순 메모리에 상품을 저장했다가, JdbcTemplate을 적용할것이다.

프로젝트의 구조부터 살펴보자.

<br>

`build.gradle`

```groovy
dependencies {
	  implementation 'org.springframework.boot:spring-boot-starter-thymeleaf'
	  implementation 'org.springframework.boot:spring-boot-starter-web'
	  compileOnly 'org.projectlombok:lombok'
	  annotationProcessor 'org.projectlombok:lombok'
	  testImplementation 'org.springframework.boot:spring-boot-starter-test'
	  testRuntimeOnly 'org.junit.platform:junit-platform-launcher'

	  testCompileOnly 'org.projectlombok:lombok'
	  testAnnotationProcessor 'org.projectlombok:lombok'
}
```

<br>

---

### 1.1 도메인

`Item` : 상품을 나타내는 객체

```Java
@Data
public class Item {

    private Long id;
    private String itemName;
    private Integer price;
    private Integer quantity;

    public Item() {
    }

    public Item(String itemName, Integer price, Integer quantity) {
        this.itemName = itemName;
        this.price = price;
        this.quantity = quantity;
    }
}
```

<br>

---

### 1.2 레포지토리

`ItemRepository`

```java
public interface ItemRepository {

    Item save(Item item);

    void update(Long itemId, ItemUpdateDto updateParam);

    Optional<Item> findById(Long id);

    List<Item> findAll(ItemSearchCond cond);

}
```

* 이후 `JdbcTemplate`이나 `JPA`를 사용할 때 구현체를 쉽게 변경하기 위해서 인터페이스를 도입한다
<br>

`ItemSearchCond` : 검색 조건으로 사용한다

```java
@Data
public class ItemSearchCond {

    private String itemName;
    private Integer maxPrice;

    public ItemSearchCond() {
    }

    public ItemSearchCond(String itemName, Integer maxPrice) {
        this.itemName = itemName;
        this.maxPrice = maxPrice;
    }
}
```

* 상품명, 최대 가격
* 상품명의 일부만 포함되어도 검색이 가능해야 함(`like` 검색)

<br>

`ItemUpdateDto` : 상품을 수정할 때 사용하는 객체

```java
@Data
public class ItemUpdateDto {
    private String itemName;
    private Integer price;
    private Integer quantity;

    public ItemUpdateDto() {
    }

    public ItemUpdateDto(String itemName, Integer price, Integer quantity) {
        this.itemName = itemName;
        this.price = price;
        this.quantity = quantity;
    }
}
```

<br>

> DTO(Data Transfer Object)란?
>
> * 데이터 전송을 위한 객체
> * 기능은 없고 데이터를 전달하는 용도로 사용되면 DTO
>   * 기능이 무조건 없어야하는 것은 아니다
>   * 주 목적이 데이터 전송이면 DTO라고 할 수 있음
> * 예시 프로젝트의 `ItemSearchCond`도 일종의 DTO로 볼 수 있음
>   * 네이밍은 상황에 따라서 적절히 붙여주면 됨
> * DTO를 붙이면 이 객체가 데이터 전송을 위한 객체라는 것을 한눈에 알아볼 수 있어서 좋음
{: .prompt-info }


<br>

`MemoryItemRepository`

* `ItemRepository`를 구현한 메모리 저장소
* 메모리 기반이기 때문에 서버를 종료하고 다시 실행하면 데이터가 전부 사라짐

<br>

---

### 1.3 스프링 부트 설정

`MemoryConfig`

```java
@Configuration
public class MemoryConfig {

    @Bean
    public ItemService itemService() {
        return new ItemServiceV1(itemRepository());
    }

    @Bean
    public ItemRepository itemRepository() {
        return new MemoryItemRepository();
    }

}
```

* 사용하는 서비스, 레포지토리를 스프링 빈으로 등록하고 생성자를 통한 의존성 주입을 위한 설정 클래스
* 컨트롤러는 컴포넌트 스캔

<br>

`TestDataInit`

```java
@Slf4j
@RequiredArgsConstructor
public class TestDataInit {
    private final ItemRepository itemRepository;
  
    /**
     * 확인용 초기 데이터 추가 
     */
    @EventListener(ApplicationReadyEvent.class)
    public void initData() {
        log.info("test data init");
        itemRepository.save(new Item("itemA", 10000, 10));
        itemRepository.save(new Item("itemB", 20000, 20));
    } 
}
```

* `@EventListener(ApplicationReadyEvent.class)` : 스프링 컨테이너가 완전히 초기화를 다 끝내고, 실행 준비가 외었을 때 발생하는 이벤트
  * 프로젝트에서는 이를 통해 `initData()` 메서드를 호출해서 초기 데이터를 생성해준다

<br>

`ItemServiceApplication`

```java
@Import(MemoryConfig.class)
@SpringBootApplication(scanBasePackages = "hello.itemservice.web")
public class ItemServiceApplication {

	public static void main(String[] args) {
		SpringApplication.run(ItemServiceApplication.class, args);
	}

	@Bean
	@Profile("local")
	public TestDataInit testDataInit(ItemRepository itemRepository) {
		return new TestDataInit(itemRepository);
	}

}
```

* `@Import(MemoryConfig.class)`
  * 앞서 설정한 `MemoryConfig` 를 설정 파일로 사용한다




* `@SpringBootApplication(scanBasePackages = "hello.itemservice.web")`
  * 프로젝트에서는 컨트롤러만 컴포넌트 스캔을 사용하고 나머지는 수동 등록한다
  * 컴포넌트 스캔 경로를 `hello.itemservice.web` 하위로 지정한다



* `@Profile("local")`
  * 특정 프로필의 경우에만 해당 스프링 빈을 등록한다
  * 이 경우 `local`이라는 프로필이 사용되는 경우만 `testDataInit`이라는 스프링 빈을 등록

<br>

> 프로필(`@Profile`)
>
> 스프링은 로딩 시점에 `application.properties`의 `spring.profiles.active` 속성을 읽어서 프로필로 사용한다.
>
> 이런 프로필을 사용하는 이유는 개발 환경(로컬), 운영 환경(프로덕션), 테스트 실행 등 다양한 환경에 따라 다른 설정을 사용하기 위해서다.
>
> 예를 들면, 로컬 환경에서는 로컬에 설치된 DB에만 접근해야 하고, 운영 환경은 운영 DB에 접근해야 한다. 이를 위해서 프로필마다 설정 정보를 다르게 설정해서 이용하도록 하면 편하다.
{: .prompt-info }

<br>

---

## 2. 데이터베이스 준비

### 2.1 DB 세팅

데이터베이스를 사용하기 위해서 도커를 이용해서 MySQL 컨테이너를 띄우고 사용하자.

그냥 H2 데이터베이스를 사용해도 무관하다.

<br>

`docker-compose.yaml`

```yaml
services:
  mysql:
    image: mysql:8.1
    container_name: mysql-container
    restart: always
    ports:
      - "3306:3306"
    environment:
      MYSQL_ROOT_PASSWORD: admin
      MYSQL_DATABASE: test_database
      MYSQL_USER: my_username
      MYSQL_PASSWORD: my_password
    volumes:
      - /Users/{사용자이름}/Desktop/mysql-volume:/var/lib/mysql
```

<br>

`schema.sql`

```sql
DROP TABLE IF EXISTS item;
CREATE TABLE item
(
    id BIGINT AUTO_INCREMENT,
    item_name VARCHAR(10),
    price INT,
    quantity INT,
    PRIMARY KEY (id)
);
```

* 위의 쿼리로 테이블 생성하자

<br>

정상적으로 작동하는지 확인 해보자. 다음 쿼리를 실행해서 조회 결과를 살펴보자.

```sql
insert into item(item_name, price, quantity) values ('ItemTest', 10000, 10)
select * from item;
```

<br>

---

### 2.2 권장하는 기본키

데이터베이스의 기본키는 다음의 조건을 만족해야한다.

* `null`값을 허용하지 않는다
* 유일해야 한다(unique)
* 변해선 안된다(immutable)

<br>

테이블의 기본 키를 선택은 다음의 두 종류를 사용할 수 있다.

* 자연 키(natural key)
  * 비즈니스에 의미가 있는 키
  * 이메일, 주민등록번호, 전화번호



* 대리 키(surrogate key)
  * 비즈니스와 관련이 없는 임의로 만들어진 키(대체 키)
  * `auto_increment`, 키 생성 테이블의 키, 오라클 시퀀스

<br>

보통의 경우 자연 키 보다 대리 키를 권장한다. 이유는 다음과 같다.

* 이메일, 주민번호, 전화번호는 언뜻 보면 변하지 않을것 같지만 언젠가는 변할 수 있다
* 어떤 외부적인 요인(정책, 법)에 의해 쉽게 변하지 않을 키를 위해서 자연 키 사용을 피하자

<br>

---

## 3. JdbcTemplate 소개

JdbcTemplate에 대해서 알아보자.

우리가 이전에 학습한 JDBC와 JdbcTemplate의 차이점은 무엇일까? 일단 간단히 소개하자면 JdbcTemplate은 JDBC를 매우 편리하게 사용할 수 있도록 해준다. 

JdbcTemplate은 다음과 같은 장점을 가진다.

* 설정이 편리하다
  * JdbcTemplate은 `spring-jdbc` 라이브러리에 포함되어 있고, 별도의 복잡한 설정 없이 바로 사용할 수 있다



* 반복적인 보일러 플레이트 코드 제거
  * JdbcTemplate은 템플릿 콜백 패턴을 사용해서 많은 반복 작업을 처리해준다
  * 처리해주는 반복 작업에는 다음이 있다
    * 커넥션 획득
    * `statement` 준비, 실행
    * 결과 루프
    * 커넥션, `statement`, `resultset` 종료
    * 트랜잭션을 위한 커넥션 동기화
    * 예외 변환기 실행
  * 개발자는 SQL 작성, 파라미터 정의, 응답값 매핑만 처리해주면 된다

<br>

JdbcTemplate에도 문제는 존재한다. JdbcTemplate은 동적 SQL을 해결하기 어렵다는 단점이 있다.

<br>

---

## 4. JdbcTemplate 설정

`build.gradle`에 다음을 추가하자

```groovy
implementation 'org.springframework.boot:spring-boot-starter-jdbc'
runtimeOnly 'com.mysql:mysql-connector-j'
```

* `spring-boot-starter-jdbc` 라이브러리만 추가하면 된다

<br>

`application.properties`에 `DataSource`의 연결 정보를 추가하자.

```properties
# spring.sql.init.mode=always
spring.datasource.driver-class-name=com.mysql.cj.jdbc.Driver
spring.datasource.url=jdbc:mysql://localhost:3306/test_database?serverTimezone=Asia/Seoul
spring.datasource.username=root
spring.datasource.password=admin
```

<br>

---

## 5. JdbcTemplate 적용

### 5.1 `ItemRepository` 구현체 만들기

`ItemRepository` 인터페이스를 기반으로 구현체인 `JdbcTemplateItemRepository`를 만들어보자.

<br>

`JdbcTemplateItemRepositoryV1`

```java
/**
 * JdbcTemplate
 */
@Slf4j
@Repository
public class JdbcTemplateItemRepositoryV1 implements ItemRepository{

    private final JdbcTemplate template;

    // DataSource 필요
    public JdbcTemplateItemRepositoryV1(DataSource dataSource) {
        this.template = new JdbcTemplate(dataSource);
    }

    @Override
    public Item save(Item item) {
        String sql = "insert into item(item_name, price, quantity) values (?,?,?)";
        KeyHolder keyHolder = new GeneratedKeyHolder();
      
        template.update(con -> {
            // 자동 증가 키
            PreparedStatement ps = con.prepareStatement(sql, new String[]{"id"});
            ps.setString(1, item.getItemName());
            ps.setInt(2, item.getPrice());
            ps.setInt(3, item.getQuantity());
            return ps;
        }, keyHolder);

        long key = keyHolder.getKey().longValue();
        item.setId(key);

        return item;
    }

    @Override
    public void update(Long itemId, ItemUpdateDto updateParam) {
        String sql = "update item set item_name=?, price=?, quantity=? where id=?";
        template.update(sql,
                updateParam.getItemName(),
                updateParam.getPrice(),
                updateParam.getQuantity(),
                itemId);
    }

    @Override
    public Optional<Item> findById(Long id) {
        String sql = "select id, item_name, price, quantity from item where id = ?";
        // 결과(resultset)을 Item으로 바꾸는 코드 필요
        try {
            Item item = template.queryForObject(sql, itemRowMapper(), id);
            return Optional.of(item);
        } catch (EmptyResultDataAccessException e) {
            return Optional.empty();
        }
    }

    private RowMapper<Item> itemRowMapper() {
        return ((rs, rowNum) -> {
            Item item = new Item();
            item.setId(rs.getLong("id"));
            item.setItemName(rs.getString("item_name"));
            item.setPrice(rs.getInt("price"));
            item.setQuantity(rs.getInt("quantity"));
            return item;
        });
    }

    @Override
    public List<Item> findAll(ItemSearchCond cond) {
        String itemName = cond.getItemName();
        Integer maxPrice = cond.getMaxPrice();

        String sql = "select id, item_name, price, quantity from item";

        // 동적 쿼리 작성
        if (StringUtils.hasText(itemName) || maxPrice != null) {
            sql += " where";
        }

        boolean andFlag = false;
        List<Object> param = new ArrayList<>();

        if (StringUtils.hasText(itemName)) {
            sql += " item_name like concat('%',?,'%')";
            param.add(itemName);
            andFlag = true;
        }

        if (maxPrice != null) {
            if (andFlag) {
                sql += " and";
            }
            sql += " price <= ?";
            param.add(maxPrice);
        }

        log.info("sql={}", sql);
        return template.query(sql, itemRowMapper(), param.toArray());
    }
}
```

* `JdbcTemplate`은 `DataSource`가 필요하다
  * `DataSource`를 의존성 주입받고, 생성자 내부에서 `JdbcTemplate`를 생성한다
  * `JdbcTemplate`을 스프링 빈으로 직접 등록하고 주입받는 방법도 있다



* `save(Item item)`
  * 데이터를 저장한다
  * 데이터 변경을 위해 `update()`을 사용한다
  * 데이터를 저장할 때 PK 생성에 `auto increment` 방식을 사용하기 때문에, PK인 ID값을 개발자가 직접 지정하는 것이 아니라 비워두고 저장해야 한다. 데이터베이스가 PK인 ID를 대신 생성해준다.
  * 데이터베이스가 대신 생성해주는 PK ID 값은 데이터베이스에 `INSERT`가 완료 되어야 생성된 PK ID 값을 확인할 수 있다
  * `KeyHolder`와 `con.prepareStatement(sql, new String[]{"id"})`를 사용해서 `id`를 지정해주면 `INSERT` 쿼리 실행 이후에 데이터베이스에서 생성된 ID 값을 조회할 수 있다
  * 뒤에서 다룰 `SimpleJdbcInsert`라는 기능으로 훨씬 편리하게 구현할 수 있다



* `update()`
  * 데이터 업데이트
  * 데이터 변경을 위해 `update()` 사용
  * JDBC에서 사용한 파라미터 바인딩과 비슷하게 사용하면 된다



* `findById()`
  * 데이터를 하나 조회한다
  * `template.queryForObject()`
    * 결과 로우가 하나일 때 사용
    * `RowMapper`는 `ResultSet`을 객체인 `Item`으로 변환해줌
    * 결과가 없으면 `EmptyResultDataAccessException` 발생
    * 둘 이상이면 `IncorrectResultSizeDataAccessException` 발생
  * `Optional`을 반환해야 함. 결과가 없으면 예외를 잡아서 `Optional.empty()`를 반환



* `findAll()`
  * 데이터를 리스트로 조회
  * 검색 조건으로 적절한 데이터를 찾는다
  * `template.query()`
    * 결과가 하나 이상일 때 사용
    * 결과가 없으면 빈 컬렉션 반환
    * 동적 쿼리 사용

<br>

이전에도 언급했지만, JdbcTemplate에서 동적 쿼리의 작성은 매우 어렵다. 이런 동적 쿼리에 대한 문제를 바로 뒤에서 알아보자.

<br>

---

### 5.2 동적 쿼리

`findAll()`의 문제점은 검색하는 조건에 따라 실행하는 SQL이 동적으로 변해야한다. 어떤식으로 SQL이 달라져야 하는지 확인해보자.

<br>

* 검색 조건이 없음

   * ```sql
     select id, item_name, price, quantity from item;
     ```



* `item_name`으로 검색

   * ```SQL
     select id, item_name, price, quantity from item
     where item_name like concat('%',?,'%');
     ```



* `maxPrice`로 검색

   * ```sql
     select id, item_name, price, quantity from item
     where price <= ?
     ```



* `item_name`, `maxPrice` 둘다 검색

   * ```sql
     select id, item_name, price, quantity from item from item
     where item_name like concat('%',?,'%')
     and price <= ?
     ```

<br>

위의 4가지 상황에 따라 SQL이 동적으로 생성되어야 한다. 언뜻 보기에는 쉬워보이지만, 이것을 코드로 구현하려고 하면 생각보다 어렵다. 또한 실무로 들어가면 이보다 조건이 훨씬 복잡하다.

JdbcTemplate의 단점은 이런 동적 쿼리를 처리하기 쉽지 않다는 것이다. 이런 문제를 해결하기 위해서는 MyBatis, QueryDSL 등의 기술을 사용한다.

<br>

---

### 5.3 구성하고 실행해보기

지금까지 구현한 `JdbcTemplateItemRepositoryV1`를 프로젝트에 적용하고 실행해보자.

먼저 `JdbcTemplateV1Config`를 만들자.

<br>

```java
@Configuration
@RequiredArgsConstructor
public class JdbcTemplateV1Config {

    private final DataSource dataSource;

    @Bean
    public ItemService itemService() {
        return new ItemServiceV1(itemRepository());
    }

    @Bean
    public ItemRepository itemRepository() {
        return new JdbcTemplateItemRepositoryV1(dataSource); // 구현체로 JdbcTemplateItemRepositoryV1 사용
    }
} 
```

<br>

`ItemServiceApplication`위에 `JdbcTemplateV1Config.class`를 사용하도록 변경한다.

```java
@Import(JdbcTemplateV1Config.class)
// @Import(MemoryConfig.class)
```

<br>

이제 프로젝트를 실행해보면 MySQL을 저장소로 사용하는 것을 확인할 수 있다.

<br>

---

## 6. `NamedParameterJdbcTemplate`

이름 지정 파라미터에 대해 알아보자.

기존에 파라미터를 바인딩 할 때 다음과 같이 사용했다. 

<br>

```java
String sql = "update item set item_name=?, price=?, quantity=? where id=?";
template.update(sql,
         itemName,
         price,
         quantity,
         itemId);
```

<br>

여기서의 문제는 `item_name`, `quantity`, `price` 등의 순서를 바꾸면 파라미터가 잘못 바인딩 된다는 것이다. 예를 들면, `price`와 `quantity`의 순서를 바꾸면 `quantity=price`, `price=quantity`로 잘못 바인딩되는 대참사가 벌어진다.

이런 문제는 파라미터를 순서대로 바인딩하는 과정에 속에 생기는 모호함 때문에 발생한다. JdbcTemplate은 이 문제를 해결하기 위해서 `NamedParameterJdbcTemplate`라는 기능을 제공한다.

<br>

이제 이름 지정 파라미터(`NamedParameterJdbcTemplate`)를 사용하도록 변경해보자.

<br>

`JdbcTemplateItemRepositoryV2`

```java
/**
 * NamedParameterJdbcTemplate
 */
@Slf4j
@Repository
public class JdbcTemplateItemRepositoryV2 implements ItemRepository{

    /**
     * NamedParameterJdbcTemplate를 사용하도록 변경
     * NamedParameterJdbcTemplate도 내부에 dataSource 필요
     * DI로 dataSource를 받고 내부에서 NamedParameterJdbcTemplate을 생성해서 가진다
     * JdbcTemplate을 사용할 때 관례상 이 방법을 많이 사용
     */
    private final NamedParameterJdbcTemplate template;

    public JdbcTemplateItemRepositoryV2(DataSource dataSource) {
        this.template = new NamedParameterJdbcTemplate(dataSource);
    }

    /**
     * 1. BeanPropertySqlParameterSource
     * 자바빈 프로퍼티 규약을 통해서 자동으로 파라미터 객체 생성
     * 예) getXxx() -> xxx
     * 예) getItemName() -> itemName
     * BeanPropertySqlParameterSource가 많은 것을 자동화 해줘서 좋아보이지만, 모든 상황에서 사용할 수 있는 것은 아님
     * 한계를 아래의 update()에서 설명
     */
    @Override
    public Item save(Item item) {
        /**
         * SQL에서 ? 대신 :itemName 처럼 :파라미터이름 형식으로 받고 있음
         */
        String sql = "insert into item(item_name, price, quantity) " +
                "values (:itemName, :price, :quantity)";

        // 방법1 : BeanPropertySqlParameterSource 사용
        BeanPropertySqlParameterSource param = new BeanPropertySqlParameterSource(item);

        KeyHolder keyHolder = new GeneratedKeyHolder();
        template.update(sql, param, keyHolder);

        long key = keyHolder.getKey().longValue();
        item.setId(key);

        return item;
    }

    /**
     * 2. MapSqlParameterSource
     * Map과 유사
     * SQL 타입을 지정할 수 있는 등, SQL에 특화된 기능 제공
     * 메서드 체이닝 제공
     * update()에서 SQL에 :id를 바인딩 해야 하는데, ItemUpdateDto에는 itemId가 없다
     * 따라서 MapSqlParameterSource을 사용해야 함
     */
    @Override
    public void update(Long itemId, ItemUpdateDto updateParam) {
        String sql = "update item " +
                "set item_name=:itemName, price=:price, quantity=:quantity " +
                "where id=:id";

        // 방법 2 : MapSqlParameterSource 사용
        MapSqlParameterSource param = new MapSqlParameterSource()
                .addValue("itemValue", updateParam.getItemName())
                .addValue("price", updateParam.getPrice())
                .addValue("quantity", updateParam.getQuantity())
                .addValue("id", itemId);

        template.update(sql, param);
    }

    /**
     * 3. Map
     * 단순히 Map을 사용한다
     */
    @Override
    public Optional<Item> findById(Long id) {
        String sql = "select id, item_name, price, quantity from item where id = :id";

        try {
            // 방법 3 : Map 사용
            Map<String, Object> param = Map.of("id", id);
            Item item = template.queryForObject(sql, param, itemRowMapper());

            return Optional.of(item);
        } catch (EmptyResultDataAccessException e) {
            return Optional.empty();
        }
    }

    /**
     * BeanPropertyRowMapper는 ResultSet의 결과를 받아서 자바빈 규약에 맞추어 데이터를 변환해줌
     * 예) select id, price를 통해 조회하면 다음과 같은 코드를 리플렉션을 통해 작성해줌
     * 예) Item item = new Item();
     *    item.setId(rs.getLong("id"));
     *    item.setPrice(rs.getInt("price"));
     * 
     * 만약 select item_name 이면 setItem_name()이 없기 때문에 이 경우에는 다음과 같이 고치면 된다
     * select item_name as itemName
     * as를 통해서 별칭을 사용하면 됨
     */
    private RowMapper<Item> itemRowMapper() {
        return BeanPropertyRowMapper.newInstance(Item.class);
    }

    @Override
    public List<Item> findAll(ItemSearchCond cond) {
        String itemName = cond.getItemName();
        Integer maxPrice = cond.getMaxPrice();

        SqlParameterSource param = new BeanPropertySqlParameterSource(cond);

        String sql = "select id, item_name, price, quantity from item";

        // 동적 쿼리 작성
        if (StringUtils.hasText(itemName) || maxPrice != null) {
            sql += " where";
        }

        boolean andFlag = false;

        if (StringUtils.hasText(itemName)) {
            sql += " item_name like concat('%',:itemName,'%')";
            andFlag = true;
        }

        if (maxPrice != null) {
            if (andFlag) {
                sql += " and";
            }
            sql += " price <= :maxPrice";
        }

        log.info("sql={}", sql);
        return template.query(sql, param, itemRowMapper());
    }
}
```

* 자바 관례와 데이터베이스 관례의 불일치가 존재한다
  * 자바는 `camelCase`를 사용하는 반면, 관계형 데이터베이스에서는 보통 `snake_case`를 사용한다
  * 이런 문제를 `BeanPropertyRowMapper`는 언터스코어 표기법을 카멜로 표기법으로 자동 변환해준다
  * `select item_name`으로 조회해도 `setItemName()`에 문제 없이 들어간다
  * 컬럼 이름과 객체 이름이 완전히 다른 경우는 조회 SQL에서 별칭(`as`)를 사용하자

<br>

---

## 7. `SimpleJdbcInsert`

`INSERT` 쿼리를 직접 작성하지 않아도 되는 `SimpleJdbcInsert`에 대해서 알아보자.

코드로 먼저 `SimpleJdbcInsert`를 적용해보자.

<br>

`JdbcTemplateItemRepositoryV3`

```java
/**
 * SimpleJdbcInsert
 */
@Slf4j
@Repository
public class JdbcTemplateItemRepositoryV3 implements ItemRepository{


    private final NamedParameterJdbcTemplate template;
    // SimpleJdbcInsert 추가
    private final SimpleJdbcInsert jdbcInsert;

    public JdbcTemplateItemRepositoryV3(DataSource dataSource) {
        this.template = new NamedParameterJdbcTemplate(dataSource);
        /**
         * SimpleJdbcInsert가 dataSource를 통해 DB에서 메타데이터를 읽어서 자동으로 인지한다
         */
        this.jdbcInsert = new SimpleJdbcInsert(dataSource)
                .withTableName("item")
                .usingGeneratedKeyColumns("id");
                // .usingColumns("item_name", "price", "quantity"); // 생략 가능
    }

    /**
     * 기존 INSERT 관련 코드를 지우기 다음과 같이 간단하게 작성해서 사용가능
     * 나머지 코드는 안바뀜.SimpleJdbcInsert는 INSERT에서 도움이 되는 기능임.
     */
    @Override
    public Item save(Item item) {
        BeanPropertySqlParameterSource param = new BeanPropertySqlParameterSource(item);
        Number key = jdbcInsert.executeAndReturnKey(param);
        item.setId(key.longValue());
        return item;
    }
  
  // 기존 코드
  
}
```

* `withTableName()` : 데이터를 저장할 테이블명 명시
* `usingGeneratedKeyColumns()` : `key`를 생성하는 PK 컬럼명 명시
* `usingColumns()` : INSERT 쿼리에 사용할 컬럼 지정
  * 생략 가능
  * 특정 컬럼만을 지정해서 저장하고 싶을때 사용하면 됨

<br>

> 참고로 JdbcTemplate 지금까지 설명한 기능 외에도 `SimpleJdbcCall` 처럼 스토어드 프로시져를 호출할 수 있는 기능과 더불어서, 다양한 기능을 제공한다.
>
> 공식 매뉴얼 참고 : [https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#jdbc-JdbcTemplate](https://docs.spring.io/spring-framework/docs/current/reference/html/data-access.html#jdbc-JdbcTemplate)
{: .prompt-tip }

---

## Reference

1. [인프런 - 김영한 : 스프링 완전 정복](https://www.inflearn.com/roadmaps/373)
