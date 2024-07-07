---
title: (JDBC - 2) 순수 자바에서 JDBC 사용하기
description: 자바만으로 JDBC 사용해보기, POJO에 대하여
author: seungki1011
date: 2024-04-13 12:30:00 +0900
categories: [Backend, JDBC]
tags: [spring, jdbc, dao, java, pojo]
math: true
mermaid: true
---

---

## 1. JDBC 사용 - 3(스프링 사용 x)

스프링을 이용하지 않고 JDBC를 사용해보자. 

모든 예제는 편의상 `SQLException`을 굳이 런타임 예외로 변환하지 않고 그대로 사용함.

<br>

### 1.1 프로젝트, DB 세팅

`build.gradle`

```groovy
dependencies {
    compileOnly 'org.projectlombok:lombok:1.18.32'
    annotationProcessor 'org.projectlombok:lombok:1.18.32'

    testCompileOnly 'org.projectlombok:lombok:1.18.32'
    testAnnotationProcessor 'org.projectlombok:lombok:1.18.32'

    implementation 'org.slf4j:slf4j-api:1.7.32'
    implementation 'ch.qos.logback:logback-classic:1.2.6'

    implementation 'mysql:mysql-connector-java:8.0.30'
    testImplementation platform('org.junit:junit-bom:5.9.1')
    testImplementation 'org.junit.jupiter:junit-jupiter'
}
```

<br>

MySQL 컨테이너를 띄워서 사용하자.

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

데이터베이스와 테이블을 생성하자.

```mysql
CREATE SCHEMA jdbc_test;

USE jdbc_test;

CREATE TABLE product (
	  id int unsigned NOT NULL AUTO_INCREMENT,
    name varchar(255) COLLATE utf8mb4_unicode_ci NOT NULL,
    updated_at datetime NOT NULL,
    description varchar(2048) COLLATE utf8mb4_unicode_ci NOT NULL,
    price int NOT NULL,
    PRIMARY KEY (id)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;

INSERT INTO product (name, updated_at, description, price)
VALUES
	('shoe1', '2024-01-01 01:00:00', 'A footwear product', '20000'),
	('shoe2', '2024-01-01 02:30:00', 'A footwear product', '50000'),
	('shoe3', '2024-01-01 03:00:00', 'A footwear product', '35000'),
	('shoe4', '2024-01-01 06:00:00', 'A footwear product', '185000'),
	('cap1', '2024-01-01 05:25:00', 'A product to wear on the head', '50000'),
	('cap2', '2024-01-05 02:30:00', 'A product to wear on the head', '60000'),
	('tshirt1', '2024-01-05 03:30:00', 'A short sleave shirt', '30000'),
	('tshirt2', '2024-02-02 01:00:00', 'A short sleave shirt', '40000'),
	('tshirt3', '2024-02-03 01:00:00', 'A short sleave shirt', '50000'),
	('tshirt4', '2024-03-05 07:00:00', 'A short sleave shirt', '90000'),
	('ak47', '2024-03-13 02:30:00', 'A assault rifle', '990000'),
	('airpod', '2024-04-03 05:00:00', 'A bluetooth earphone', '230000');
```

<br>

`database.properties`에서 설정을 읽어와서 `DriverManager`에 사용할 수 있도록 구현해보자.

* 귀찮아서 `SQLException`을 굳이 런타임 예외로 변환하지 않고 그대로 사용했음

`resources/database.properties`

```properties
jdbc.url=jdbc:mysql://localhost:3306/jdbc_test?serverTimezone=Asia/Seoul
jdbc.username=root
jdbc.password=admin
```

<br>

---

### 1.2 데이터베이스 커넥션 유틸 구현

다음의 두 유틸을 구현해보자.

* `DriverManager`을 이용한 커넥션 생성을 위한 유틸 구현
* 연결 정보를 `database.properties`에서 얻도록 유틸 구현

<br>

`dbutil/JdbcPropertiesLoader`

```java
@Slf4j
public class JdbcPropertiesLoader {
  
    private static final String PROPERTIES_FILE = "database.properties";
    private static Properties properties;

    static {
        properties = new Properties();
        try (InputStream input = JdbcPropertiesLoader.class.getClassLoader().getResourceAsStream(PROPERTIES_FILE)) {
            if (input == null) {
                System.out.println("file not found");
            }

            properties.load(input);
        } catch (IOException e) {
            log.error("JdbcPropertiesLoader error", e);
        }
    }

    public static String getUrl() {
        return properties.getProperty("jdbc.url");
    }

    public static String getUsername() {
        return properties.getProperty("jdbc.username");
    }

    public static String getPassword() {
        return properties.getProperty("jdbc.password");
    }

}
```

* `database.properties`에서 설정 정보를 읽어오도록 한다

<br>

`dbutil/JdbcConnectionUtil`

```java
@Slf4j
public class JdbcConnectionUtil {
  
    public static String URL;
    public static String USERNAME;
    public static String PASSWORD;

    public static Connection getConnection() {
        Connection connection = null;
        try {
            URL = JdbcPropertiesLoader.getUrl();
            USERNAME = JdbcPropertiesLoader.getUsername();
            PASSWORD = JdbcPropertiesLoader.getPassword();

            connection = DriverManager.getConnection(URL, USERNAME, PASSWORD);
            return connection;
        } catch (SQLException e) {
            throw new IllegalStateException(e);
        }
    }

    public static void close(Connection con, Statement stmt, ResultSet rs) {

        if(rs != null) {
            try {
                rs.close();
            } catch (SQLException e) {
                log.error("ResultSet close error", e);
            }
        }

        if(stmt != null) {
            try {
                stmt.close();
            } catch (SQLException e) {
                log.error("Statement close error", e);
            }
        }

        if(con != null) {
            try {
                con.close();
            } catch (SQLException e) {
                log.error("Connection close error", e);
            }
        }
    }
}
```

<br>

`dbutil/ResultSetUtil`

```java
@Slf4j
public class ResultSetUtil {

    public static void printResultSet(ResultSet rs) {
        try {
            while (rs.next()) {
                System.out.println(rs.getInt(1) + " " + rs.getString(2) + " "
                        + rs.getDate(3) + " " + rs.getString(4) + " "
                        + rs.getInt(5));
            }
        } catch (SQLException e) {
            log.error("printResultSet() error", e);
        }
    }
}
```

* 결과(`ResultSet`)를 출력하는 용도



* `getXXX(int columnIndex)` : 현재 커서가 가리키고 있는 튜플의 `columnIndex`에 해당하는 컬럼의 값을 가져온다
* `getXXX(String columnName)` : 현재 커서가 가리키고 있는 튜플의 `columnName`에 해당하는 컬럼의 값을 가져온다
* `getXXX()` 메서드는 다양하게 존재한다
  * `getString()`
  * `getBlob()`
  * `getInt()`
  * `getClob()`



* `next()` : 커서를 현재 위치에서 한 row(튜플) 다음으로 이동
* `previous()` : 커서를 한 row 이전으로 이동
* `first()` : `ResultSet`의 첫 번째 튜플로 커서 이동
* `last()` : 마지막 위치로 커서 이동 

<br>

---

### 1.3 커넥션 생성, DatabaseMetaData 확인 

`DatabaseMetaData` 객체는 사용하는 DB의 메타정보를 제공한다.

커넥션을 생성해보고, 연결한 DB의 메타정보를 확인해보자.

<br>

 ```java
 @Slf4j
 public class ConnectMain {
     public static void main(String[] args) {
 
         Connection con = null;
 
         // 예외 처리는 JdbcConnectionUtil.getConnection()에서 전부 처리
         con = JdbcConnectionUtil.getConnection();
 
         try {
             DatabaseMetaData dbmd = con.getMetaData();
             log.info("getDriverName() = {}, getDriverVersion = {}",
                      dbmd.getDriverName(), dbmd.getDriverVersion());
           
         } catch (SQLException e) {
             log.error("DatabaseMetaData error", e);
         } finally {
             JdbcConnectionUtil.close(con, null, null);
         }
     }
 }
 ```

```
16:11:49.706 [main] INFO ConnectMain - getDriverName() = MySQL Connector/J, getDriverVersion = mysql-connector-java-8.0.30 (Revision: 1de2fe873fe26189564c030a343885011412976a)
```

* `DatabaseMetaData` 객체를 통해서 벤더가 제공하는 DB의 스펙에 대한 설명을 얻을 수 있다.
  * 이런 정보를 이용해서 특정 버전에 따라 코드의 동작이 달라지도록 코드를 구현하는 것도 가능하다

<br>

---

### 1.4 Statement 사용

이제 ``Statement``와 그 주요 메서드들을 사용해보자.

<br>

#### 1.4.1 executeQuery()

```java
@Slf4j
public class ExecuteQueryMain {
    public static void main(String[] args) {

        Connection con = null;
        Statement stmt = null;
        ResultSet rs = null;

        try {
            // Connection 생성
            con = JdbcConnectionUtil.getConnection();

            // 1. Statement 사용
            stmt = con.createStatement(); // Statement 객체 생성
            // executeQuery() 사용
            rs = stmt.executeQuery("select * from product");

            ResultSetUtil.printResultSet(rs);

        } catch (SQLException e) {
            log.error("DB error", e);
        } finally {
            JdbcConnectionUtil.close(con, stmt, rs);
        }
    }

}
```

```
1 shoe1 2024-01-01 A footwear product 20000
2 shoe2 2024-01-01 A footwear product 50000
3 shoe3 2024-01-01 A footwear product 35000
4 shoe4 2024-01-01 A footwear product 185000
5 cap1 2024-01-01 A product to wear on the head 50000
6 cap2 2024-01-05 A product to wear on the head 60000
7 tshirt1 2024-01-05 A short sleave shirt 30000
8 tshirt2 2024-02-02 A short sleave shirt 40000
9 tshirt3 2024-02-03 A short sleave shirt 50000
10 tshirt4 2024-03-05 A short sleave shirt 90000
11 ak47 2024-03-13 A assault rifle 990000
12 airpod 2024-04-03 A bluetooth earphone 230000
13 sunglass1 2024-04-12 A sunglass 120000
```

* `ResultSet executeQuery(String sql)`
  * SQL을 실행 후 결과에 대한 `ResultSet`을 반환한다
  * 조회에 사용한다

* `Statement createStatement()`
  * `Statement` 객체 생성


<br>

---

#### 1.4.2 executeUpdate()

```java
@Slf4j
public class ExecuteUpdateMain {
    public static void main(String[] args) {

        Connection con = null;
        Statement stmt = null;
        ResultSet rs = null;

        try {
            con = JdbcConnectionUtil.getConnection();
            stmt = con.createStatement();

            // executeUpdate() 사용 - 튜플 삽입
            String insertSql = "insert into product(name, updated_at, description, price)" + "values ('sunglass2', '2024-04-13 14:50:00', 'A sunglass', '80000')";
          
            int changedRows = stmt.executeUpdate(insertSql);
            System.out.println("변경된 row 수 = " + changedRows);

            // executeUpdate() - 값 업데이트
            String updateSql = "update product set price = price - 5000 where name like 'tshirt%'";
            changedRows = stmt.executeUpdate(updateSql);
            System.out.println("변경된 row 수 = " + changedRows);

        } catch (SQLException e) {
            log.error("DB error", e);
        } finally {
            JdbcConnectionUtil.close(con, stmt, rs);
        }
    }
}
```

```
변경된 row 수 = 1
변경된 row 수 = 4
```

* `int executeUpdate(String sql)`
  * `insert`, `update`, `delete` 등과 같이 결과를 받아오지 않고 데이터를 수정하는 SQL에 사용
  * 반환값은 변경사항이 적용된 튜플의 수

<br>

변경이 적용된 `product` 테이블

```
+----+-----------+---------------------+-------------------------------+--------+
| id | name      | updated_at          | description                   | price  |
+----+-----------+---------------------+-------------------------------+--------+
|  1 | shoe1     | 2024-01-01 01:00:00 | A footwear product            |  20000 |
|  2 | shoe2     | 2024-01-01 02:30:00 | A footwear product            |  50000 |
|  3 | shoe3     | 2024-01-01 03:00:00 | A footwear product            |  35000 |
|  4 | shoe4     | 2024-01-01 06:00:00 | A footwear product            | 185000 |
|  5 | cap1      | 2024-01-01 05:25:00 | A product to wear on the head |  50000 |
|  6 | cap2      | 2024-01-05 02:30:00 | A product to wear on the head |  60000 |
|  7 | tshirt1   | 2024-01-05 03:30:00 | A short sleave shirt          |  25000 |
|  8 | tshirt2   | 2024-02-02 01:00:00 | A short sleave shirt          |  35000 |
|  9 | tshirt3   | 2024-02-03 01:00:00 | A short sleave shirt          |  45000 |
| 10 | tshirt4   | 2024-03-05 07:00:00 | A short sleave shirt          |  85000 |
| 11 | ak47      | 2024-03-13 02:30:00 | A assault rifle               | 990000 |
| 12 | airpod    | 2024-04-03 05:00:00 | A bluetooth earphone          | 230000 |
| 13 | sunglass1 | 2024-04-12 12:20:00 | A sunglass                    | 120000 |
| 15 | sunglass2 | 2024-04-13 14:50:00 | A sunglass                    |  80000 |
+----+-----------+---------------------+-------------------------------+--------+
```

<br>

---

#### 1.4.3 executeBatch()

`Statement`에 `executeBatch()`를 사용하는 코드를 살펴보자.

<br>

```java
@Slf4j
public class ExecuteBatchMain {
    public static void main(String[] args) {

        Connection con = null;
        Statement stmt = null;
        ResultSet rs = null;

        try {
            con = JdbcConnectionUtil.getConnection();
            stmt = con.createStatement();

            // addBatch()로 SQL 추가
            stmt.addBatch("update product set price = price + 300000 where name = 'ak47'");
            stmt.addBatch("update product set price = price + 7700 where id = 1");
            stmt.addBatch("update product set price = price + 7700 where id = 2");
            stmt.addBatch("update product set price = price + 4400 where id between 7 and 10");

            // executeBatch()로 batch 단위로 쌓인 SQL 실행
            int[] resultCounts = stmt.executeBatch();
            
            for (int resultCount : resultCounts) {
                System.out.println("resultCount = " + resultCount);
            }

        } catch (SQLException e) {
            log.error("DB error", e);
        } finally {
            JdbcConnectionUtil.close(con, stmt, rs);
        }
    }
}
```

```
resultCount = 1
resultCount = 1
resultCount = 1
resultCount = 4
```

* `int[] executeBatch()`
  * `addBatch()`를 이용해서 실행할 SQL을 추가한다(실행은 되지 않는다)
  * `executeBatch()`를 통해서 쌓인 SQL을 배치(batch)로 실행
  * 모든 SQL이 성공하면, 각 SQL에 대해 영향 받은 튜플의 수를 배열로 반환한다



* `PreparedStatement`에 `addBatch()`를 사용하는 것은 `Statement`에 사용하는 방법과 다르다
  * `PreparedStatement`의 파라미터 바인딩을 전부 끝내고, `pstmt.addBatch()`와 같은 형태로 파라미터 바인딩이 완료된 SQL을 추가한다.
  * 이후 재사용을 위해 `pstmt.clearParameters()`을 이용해서 파라미터 값을 비워준다

<br>

변경이 적용된 `product` 테이블

```
+----+-----------+---------------------+-------------------------------+---------+
| id | name      | updated_at          | description                   | price   |
+----+-----------+---------------------+-------------------------------+---------+
|  1 | shoe1     | 2024-01-01 01:00:00 | A footwear product            |   27700 |
|  2 | shoe2     | 2024-01-01 02:30:00 | A footwear product            |   57700 |
|  3 | shoe3     | 2024-01-01 03:00:00 | A footwear product            |   35000 |
|  4 | shoe4     | 2024-01-01 06:00:00 | A footwear product            |  185000 |
|  5 | cap1      | 2024-01-01 05:25:00 | A product to wear on the head |   50000 |
|  6 | cap2      | 2024-01-05 02:30:00 | A product to wear on the head |   60000 |
|  7 | tshirt1   | 2024-01-05 03:30:00 | A short sleave shirt          |   29400 |
|  8 | tshirt2   | 2024-02-02 01:00:00 | A short sleave shirt          |   39400 |
|  9 | tshirt3   | 2024-02-03 01:00:00 | A short sleave shirt          |   49400 |
| 10 | tshirt4   | 2024-03-05 07:00:00 | A short sleave shirt          |   89400 |
| 11 | ak47      | 2024-03-13 02:30:00 | A assault rifle               | 1290000 |
| 12 | airpod    | 2024-04-03 05:00:00 | A bluetooth earphone          |  230000 |
| 13 | sunglass1 | 2024-04-12 12:20:00 | A sunglass                    |  120000 |
| 15 | sunglass2 | 2024-04-13 14:50:00 | A sunglass                    |   80000 |
+----+-----------+---------------------+-------------------------------+---------+
```

<br>

> `execute()`
>
> * `boolean execute(String sql)` 메서드도 존재한다
> * `getResultSet()`로 결과를 얻고, `getUpdateCount()`로 영향 받은 튜플 수를 얻을 수 있다
> * `executeQuery()`, `executeUpdate()` 보다 사용하기 불편하다
{: .prompt-info }

<br>

---

### 1.5 PreparedStatement 사용

`PreparedStatement`에 대해서 알아보자.

* `PreparedStatement`는 `Statement`의 인터페이스를 모두 구현한다

* `PreparedStatement`는 SQL 쿼리안에 파라미터를 사용할 때 사용한다
  * 파라미터 바인딩을 통해 사용한다

* 변수를 사용할 수 있기 때문에 `Statement`보다 활용도가 높다

<br>

```java
@Slf4j
public class PreparedStatementMain {
    public static void main(String[] args) {

        Connection con = null;
        PreparedStatement pstmt = null;
        ResultSet rs = null;
        String sql = "insert into product(name, updated_at, description, price) values(?,?,?,?)";

        try {
            con = JdbcConnectionUtil.getConnection();
            // PreparedStatement 객체 생성
            pstmt = con.prepareStatement(sql);
            // parameter binding
            pstmt.setString(1, "coat1");
            pstmt.setTimestamp(2, Timestamp.valueOf("2024-04-20 14:50:00"));
            pstmt.setString(3, "This is a coat");
            pstmt.setInt(4, 150000);

            pstmt.executeUpdate(); // 지금 튜플 하나 삽입하고 있음
            pstmt.close();

            // PreparedStatement으로 위에서 입력한 튜플 조회해보기
            pstmt = con.prepareStatement("select * from product where name = ?");
            pstmt.setString(1, "coat1");

            rs = pstmt.executeQuery();
            ResultSetUtil.printResultSet(rs);

        } catch (SQLException e) {
            log.error("DB error", e);
        } finally {
            JdbcConnectionUtil.close(con, pstmt, rs);
        }
    }
}
```

```
16 coat1 2024-04-20 This is a coat 150000
```

* 파라미터 바인딩은 `setXXX()` 형태의 메서드를 이용해서 한다
* `?`을 통한 파라미터 바인딩 방식은 활용도도 높으면서, SQL 인젝션을 방지할 수 있다

<br>

---

### 1.6 CallableStatement 사용

`CallableStatement`를 이용해서 `stored procedure`나 `function`을 다룰 수 있다.

* [`stored procedure`, `function` 복습](https://seungki1011.github.io/posts/sql-4-function-procedure-trigger/)

<br>

---

## 2. POJO 클래스 사용

### 2.1 POJO란

`POJO`(Plain Old Java Object)는 특별한 제한 사항에 얽매이지 않는 일반적인 자바 객체를 의미한다. 부가 설명을 하자면 어떠한 프레임워크에도 종속적이지 않고 활용할 수 있는 순수한 자바 객체이다.

전통적인 `POJO` 클래스에는 몇가지 규칙이 존재했다.

* `public` 클래스이어야한다
* `public` 기본 생성자를 가져야한다
* `getter`, `setter`를 가져야한다
* 클래스안의 객체는 어떤한 접근 제어자를 가져도 되지만, 모든 인스턴스 변수는 `private`이어야한다
* 미리 정의된 클래스를 상속하면 안된다
* 미리 정의된 인터페이스를 구현하면 안된다
* 미리 정의된 애노테이션을 포함하면 안된다

<br>

이런 `POJO`에 대한 해석은 시간이 지나면서 유연하게 바뀌어 왔다.

~~보통 `POJO`를 위한 조건을 모두 만족하면서 사용하기 힘들기 때문에 완벽하게 조건을 만족하지 않더라도 `POJO` compliant로 취급하는 것 같다.~~

애플리케이션 레이어간 데이터 전송을 위해 사용되는 `DTO`(Data Transfer Object)도 `POJO`의 일종으로 볼 수 있다.

<br>

---

### 2.2 POJO 클래스에 매핑 후 사용

매번 코드로 쿼리의 결과의 몇 번째 값이 어떤 타입이 데이터인지 명시하는 것은 불편하다. 미리 `ResultSet`의 결과에 해당하는 것을 `POJO`로 만들면 코드를 더 간결하게 만들 수 있다.

<br>

`domain/Product`

```java
@Data
@NoArgsConstructor
public class Product {

    private int id;
    private String name;
    private LocalDateTime updated_at;
    private String description;
    private int price;
		
    public Product(int id, String name, LocalDateTime updated_at, String description, int price) {
        this.id = id;
        this.name = name;
        this.updated_at = updated_at;
        this.description = description;
        this.price = price;
    }
  
    @Override
    public String toString() {
        return "Product{" +
                "id=" + id +
                ", name='" + name + '\'' +
                ", updated_at=" + updated_at +
                ", description='" + description + '\'' +
                ", price=" + price +
                '}';
    }
}
```

* 편의를 위해 `lombok` 사용

<br>

`dbutil/ResultSetUtil`

```java
@Slf4j
public class ResultSetUtil {
    
    public static void printResultSet(ResultSet rs) {
        try {
            while (rs.next()) {
                System.out.println(rs.getInt(1) + " " + rs.getString(2) + " "
                        + rs.getDate(3) + " " + rs.getString(4) + " "
                        + rs.getInt(5));
            }
        } catch (SQLException e) {
            log.error("printResultSet() error", e);
        }
    }
		
  	// resultSetMapper 추가, 결과 ResultSet을 POJO에 매핑
    public static Product resultSetMapper(ResultSet rs) throws SQLException {
        return new Product(rs.getInt(1), rs.getString(2),
                rs.getTimestamp(3).toLocalDateTime(), rs.getString(4),
                rs.getInt(5));
    }
}
```

<br>

한번 사용해보자.

```java
@Slf4j
public class ResultSetMain {
    public static void main(String[] args) {

        Connection con = null;
        Statement stmt = null;
        ResultSet rs = null;
        String sql = "select id, name, updated_at, description, price from product";

        try {
            con = JdbcConnectionUtil.getConnection();
            stmt = con.createStatement();
            rs = stmt.executeQuery(sql);

            while (rs.next()) {
                System.out.println(ResultSetUtil.resultSetMapper(rs));
            }
        } catch (SQLException e) {
            log.error("DB Error", e);
        } finally {
            JdbcConnectionUtil.close(con, stmt, rs);
        }

    }
}
```

```
Product{id=1, name='shoe1', updated_at=2024-01-01T01:00, description='A footwear product', price=27700}
Product{id=2, name='shoe2', updated_at=2024-01-01T02:30, description='A footwear product', price=57700}
Product{id=3, name='shoe3', updated_at=2024-01-01T03:00, description='A footwear product', price=35000}
Product{id=4, name='shoe4', updated_at=2024-01-01T06:00, description='A footwear product', price=185000}
Product{id=5, name='cap1', updated_at=2024-01-01T05:25, description='A product to wear on the head', price=50000}
Product{id=6, name='cap2', updated_at=2024-01-05T02:30, description='A product to wear on the head', price=60000}
Product{id=7, name='tshirt1', updated_at=2024-01-05T03:30, description='A short sleave shirt', price=29400}
Product{id=8, name='tshirt2', updated_at=2024-02-02T01:00, description='A short sleave shirt', price=39400}
Product{id=9, name='tshirt3', updated_at=2024-02-03T01:00, description='A short sleave shirt', price=49400}
Product{id=10, name='tshirt4', updated_at=2024-03-05T07:00, description='A short sleave shirt', price=89400}
Product{id=11, name='ak47', updated_at=2024-03-13T02:30, description='A assault rifle', price=1290000}
Product{id=12, name='airpod', updated_at=2024-04-03T05:00, description='A bluetooth earphone', price=230000}
Product{id=13, name='sunglass1', updated_at=2024-04-12T12:20, description='A sunglass', price=120000}
Product{id=15, name='sunglass2', updated_at=2024-04-13T14:50, description='A sunglass', price=80000}
Product{id=16, name='coat1', updated_at=2024-04-20T14:50, description='This is a coat', price=150000}
```

*  ORM(Object Relational Mapping) 프레임워크들은 보통 이런 일련의 `POJO` 클래스로 매핑하여 사용하는 방식을 추상화해서 제공해준다

<br>

---

## Reference

1. [인프런 - 김영한 : 스프링 완전 정복](https://www.inflearn.com/roadmaps/373)
2. [인프런 - 쉬운코드 데이터베이스](https://www.inflearn.com/course/%EB%B0%B1%EC%97%94%EB%93%9C-%EB%8D%B0%EC%9D%B4%ED%84%B0%EB%B2%A0%EC%9D%B4%EC%8A%A4-%EA%B0%9C%EB%A1%A0)
3. [패스트 캠퍼스 - 한번에 끝내는 데이터 엔지니어링](https://fastcampus.co.kr/data_online_engineering)