---
title: (Java - 2) 자바 기본 문법
description: 자바에서의 변수, 연산자, 조건문, 반복문, 관례
author: seungki1011
date: 2023-12-29 12:30:00 +0900
categories: [Java]
tags: [java]
math: true
mermaid: true
---

---

## 1) Variables

자바의 변수에 대해서 알아보자

<br>

* 변수
  * 값을 보관해고 재사용하기 위해 데이터를 담을 그릇이
  * 대부분 프로그래밍 언어는 변수(variable)라는 것을 통해 이런 기능을 제공
  * ```[접근제어자] [자료형] [변수명]```



* 상수
  * 상수의 경우 중간에 값이 변할 수 없음
  * 초기값을 끝까지 사용
  * ```final```을 이용해서 선언

<br>

---

### 1.1 Primitive Type(원시형)

* 정수형
  * ```byte``` : -128 ~ 127
  * ```short``` : -32768 ~ 32767 
  * ```int``` : -2147483648 ~ 2147483647
  * ```long``` : - 9223372036854775808 ~ 9223372036854775807



* 실수형
  * ```float``` : single-precision 64-bit IEEE 754 floating point
  * ```double``` : double-precision 64-bit IEEE 754 floating point



* 문자형
  * ```char``` : 단일 문자 표현
  * ```''```사용
  * ```String```은 참조형 자료형이다



* 논리형
  * boolean : ```true```or ```false```

<br>

---

### 1.2 Reference Type

* **기본 자료형이 아닌 모든 자료형은 참조 자료형**
* **자바의 인스턴스(객체, object)를 가리킬 수 있는 자료형**



* 메모리 주소를 저장한다
  * 참조형 변수는 객체의 주소를 저장하는 것을 숙지하자



* 대표적으로 ```String```

<br>

```java
public class VarType {
    public static void main(String[] args) {
      
        // Integer(정수형)
        int a = 99;
        // Long(정수형), Long은 뒤에 대문자 L 이용 권장
        long b = 888L;
        // Double(실수형)
        double c = 999.9d;
        // Boolean(논리형), true or false
        boolean d = true;
        // Character(문자 하나)
        char e = 'A';
        // String(문자열), 쌍따옴표
        String f = "This is a String";

        // 각 변수 출력
        System.out.println("int a : "+a);
        System.out.println("long b : "+c);
        System.out.println("double c : "+b);
        System.out.println("boolean d : "+d);
        System.out.println("char e : "+e);
        System.out.println("String f : "+false);

        // 숫자 자료형의 MinMax 출력
        System.out.println("Min of int : "+Integer.MIN_VALUE);
        System.out.println("Max of int : "+Integer.MAX_VALUE);

        System.out.println("Min of long : "+Long.MIN_VALUE);
        System.out.println("Max of long : "+Long.MAX_VALUE);

        System.out.println("Min of double : "+Double.MIN_VALUE);
        System.out.println("Max of double : "+Double.MAX_VALUE);
    }
}
```

```
> Task :VarType.main()
int a : 99
long b : 999.9
double c : 888
boolean d : true
char e : A
String f : false
Min of int : -2147483648
Max of int : 2147483647
Min of long : -9223372036854775808
Max of long : 9223372036854775807
Min of double : 4.9E-324
Max of double : 1.7976931348623157E308
```

<br>

---

## 2) Java Convention

> Java의 경우 CamelCase를 이용하는 것이 사실상 표준(Defacto)

<br>

* **변수**
  * 첫글자는 소문자, 나머지 의미 구분을 위한 단어 단위의 첫 글자는 대문자
  * 예시 ```camelCase```, ```myAccount```



* **클래스**
  * 첫글자는 대문자
  * 예시 ```Main```, ```OrderDetail```



* **상수**
  * 상수는 모든 글자를 대문자 사용, 단어구분은 언더바 사용
  * 예시 ```PI```, ```ORDER_LIMIT```



* **패키지**
  * 패지키는 모든 글자를 소문자 사용
  * 예시 ```com.de.java```

<br>

---

## 3) 연산자(Operators)

### 3.1 Arithmetic Operators

* 산술 연산자
  * ```+```, ```-```, ```*```, ```/```, ```%```
  * 수학적인 연산 수행
  * 0으로 나눌려고 하는 경우 예외 발생

<br>

```java
public class Op1 {
    public static void main(String[] args) {
      
        int a = 20;
        int b = 10;
        int c = 7;

        // addition
        int add = a + b;
        System.out.println("a + b = " + add);

        // subtraction
        int sub = a - b;
        System.out.println("a - b = " + sub);

        // multiplication
        int mul = a * b;
        System.out.println("a * b = " + mul);

        // division
        int div = a - b;
        System.out.println("a / b = " + div);

        // remainder operation
        // 나머지가 0 인경우
        int rem1 = a % b;
        System.out.println("a % b = " + rem1);

        // 나머지가 0이 아닌 경우
        int rem2 = a % c;
        System.out.println("a % c = " + rem2);
    }
}
```

```
a + b = 30
a - b = 10
a * b = 200
a / b = 10
a % b = 0
a % c = 6
```

<br>

---

### 3.2 Comparison Operators

#### 3.2.1 숫자 비교

* ```==```, ```!=```, ```>```, ```>=```, ```<```, ```<=```
* 비교 연산
* 결과값이 참이면 ```true``` 반환

<br>

```java
public class Op2 {
    public static void main(String[] args) {

        int a = 20;
        int b = 10;
        int c = 20;

        // 숫자 비교
        System.out.println("a = 20, b = 10, c = 20");
        System.out.println("a == b returns " + (a==b));
        System.out.println("a != b returns " + (a!=b));
        System.out.println("a > b returns " + (a>b));
        System.out.println("a >= c returns " + (a>=c));
        System.out.println("a < b returns " + (a<b));
        System.out.println("a <= b returns " + (a<=b));
        
    }
}
```

```
a = 20, b = 10, c = 20
a == b returns false
a != b returns true
a > b returns true
a >= c returns true
a < b returns false
a <= b returns false
```

<br>

---

#### 3.2.2 문자열 비교

> Java는 메모리 최적화를 위해서 string literal에 대한 pool을 관리함(String Constant Pool). 특정 literal을 이용해서 string을 생성할 때 같은 literal이 pool에 존재하는 경우 재사용함. 이 때문에 ==를 사용하는 경우 예상하지 못하는 결과가 나올 수 있음. (생성자 방식을 이용한 String은 권장하지 않음.)

<br>

* ```.equals()``` 메서드 사용
  * content를 비교
  * null safe 함

<br>

* ```==```는 같은 객체를 메모리에서 참조하는지 확인
  * 원시 타입 비교할때 사용 권장

<br>

```java
public class Op3 {
    public static void main(String[] args) {

        String str1 = "Hello World";
        String str2 = "Hello World";
        String str3 = "Bye Bye World";

        // 문자열의 비교
        // .equals() 사용

        System.out.println("str1 : Hello World, str2 : Hello World, str3 : Bye Bye World");
        System.out.println("compare hello world with hello world : " + "hello world".equals("hello world"));
        System.out.println("compare str1 with Hello World : " + str1.equals("Hello World"));
        System.out.println("compare str1 with str2 : " + str1.equals(str2));
        System.out.println("compare str1 with str3 : " + str1.equals(str3));
    }
}
```

```
str1 : Hello World, str2 : Hello World, str3 : Bye Bye World
compare hello world with hello world : true
compare str1 with Hello World : true
compare str1 with str2 : true
compare str1 with str3 : false
```

<br>

---

### 3.3 Logical Operators

* 논리 연산자
* ```&&```, ```||```, ```!```
  * ```&&``` : 두 조건 모두 참일 경우 ```true``` 반환, 아닌 경우 ```false```
    * AND 연산
  * ```||``` : 두 조건 중 하나라도 참이면 ```true``` 반환, 두 조건 모두 거짓인 경우 ```false```
    * OR 연산
  * ```!``` : 피연산자의 논리값에 대한 부정을 반환한다
    * 예시 ```true```를 ```false```로

<br>

---

## 4) 조건문(Conditional)

* 조건문
* 특정 조건(condition)에 따라 특정 코드를 실행하는 것
* ```if```, ```else if```, ```switch```, 삼항연산자

<br>

### 4.1 if, else-if

* ```if```
  * 조건이 ```true```일 경우 특정 코드 블록 실행
  * ```else```는 조건이 참이 아닌 경우 ```else```에 해당하는 코드 블럭 실행



* `else if`
  * ```if```문의 조건이 거짓인 경우 다음 조건을 체크
  * 여러가지 조건 설정하는 경우 여러개의 ```if```문을 사용하는 것 보다 ```else if```를 사용해서 불필요한 조건 검사를 피하는 것이 좋음
  * 조건은 제일 많이 발생하는 조건을 최상단 조건으로 설정하는 것이 좋음

<br>

```java
public class con1 {
    public static void main(String[] args) {

        // 1. if
        int a = 50;
        int b = 37;

        if (a>b) {
            System.out.println("a is bigger than b");
        }
        if (a>20) {
            System.out.println("a is bigger than 20");
        }

        // 2. if - else
        String c = "Hello";
        if (c.equals("Hello World!")) {
            System.out.println("String c equals to Hello World!");
        } else {
            System.out.println("String c is not Hello World!");
        }

        // 3. else if
        int age = 8;
        if (age>19) {
            System.out.println("You are a adult");
        } else if (19>=age && age>12) {
            System.out.println("You are a teenager");
        } else if (12>=age && age>1) {
            System.out.println("You are a child");
        } else {
            System.out.println("You are a infant");
        }
    }
}
```

```
a is bigger than b
a is bigger than 20
String c is not Hello World!
You are a child
```

* ```else if```를 사용하는 것은 서로 연관 조건인 경우에만 사용
* 독립된 조건이라면 그냥 ```if```문을 따로 사용

<br>

---

### 4.2 Switch

* 조건식의 결과 값이 어떤 케이스의 값과 동일하면 해당 케이스의 코드 실행
  * ```if```문 처럼 특정 조건의 참 거짓에 따라 코드를 실행하는 것이 아님
  * ```if```문으로 그냥 다 해결 할 수 있음



* ```break```로 ```switch```문을 빠져나갈 수 있음
  * ```break```문을 넣지 않으면 다음 케이스의 코드까지 실행



* ```default```는 일치하는 케이스의 값이 없는 경우 실행

<br>

```java
public class con2 {
    public static void main(String[] args) {
      
        // switch
        int choice = 2;

        switch (choice) { // choice에 조건식이 들어간다. 케이스의 값과 조건식의 값이 일치해야 해당 케이스의 코드 실행
            case 1:
                System.out.println("You chose option 1!");
                break; // exit switch block with break
            case 2:
                System.out.println("You chose option 2!");
                break;
            case 3:
                System.out.println("You chose option 3!");
                break;
            default:
                System.out.println("Invalid choice");
                break;
        }
        System.out.println("This is the remaining code executed after the switch block");
    }
}
```

```
You chose option 2!
This is the remaining code executed after the switch block
```

* Java 14부터 새로운 ```switch```도 생겼음

<br>

---

### 4.3 삼항 연산자(Ternary Operator)

* 참과 거짓에 따른 특정 값을 구하는 경우 ```?:``` 연산자를 사용해서 ```if```문에 비해 코드를 간결화 시킬 수 있음
* 단순 표현식만 가능

<br>

```java
// condition이 true면 A 실행, false면 B 실행
(condition) ? A:B 
```

<br>

```java
public class con3 {
    public static void main(String[] args) {
        int asset = 40000;
        String status = (asset >= 30000) ? " You can buy it!" : " You can't buy it!";
        System.out.println("With your asset " + asset + "$" + status);
    }
}
```

```
With your asset 40000$ You can buy it!
```

<br>

---

## 5)  반복문(Loop)

* 반복문은 특정 코드를 반복하기 위해 사용



* ```break```로 반복문 탈출하거나, ```continue```로 다시 조건식으로 다시 돌아갈 수 있음
  * ```continue```를 사용하는 경우 뒤에 오는 코드는 무시하고 돌아감



* 중첩 반복문을 통해 이중, 삼중 반복문을 구현 가능 (nested loop)

<br>

---

### 5.1 `while`

* 조건식이 참이면 코드 블럭 실행, 거짓이면 ```while```문 탈출
* 참인 경우 코드 블럭 실행이 끝난후 다시 조건식 검사
* 종료 시점이 명확하지 않은 경우 ```for```문에 비해 유용할 수 있음

<br>

```java
public class loop1 {
    public static void main(String[] args) {
      
        // while문
        int cnt = 0;
        while (cnt < 5) {
            cnt++; // cnt 1 증가
            // cnt += 1;
            System.out.println("Current cnt is : " + cnt);
        }
    }
}
```

```
Current cnt is : 1
Current cnt is : 2
Current cnt is : 3
Current cnt is : 4
Current cnt is : 5
```

<br>

---

### 5.2 `do`-`while`

* ```do```안의 코드를 먼저 한번 실행 후 조건 검사 (최초 한번은 무조건 실행)

<br>

```java
public class loop2 {
    public static void main(String[] args) {
      
        // 1. do-while 1
        int cnt = 0;
        do {
            cnt++;
            System.out.println("cnt is " + cnt);
        } while(cnt < 3);

        // 2. do-while 2
        int i = 3;
        do {
            System.out.println("do will execute first");
        } while(i < 2);
    }
}
```

```
cnt is 1
cnt is 2
cnt is 3
do will execute first
```

<br>

---

### 5.3 `for`

* 반복 횟수가 정해져 있을때 주로 사용
* 초기값, 조건식, 증감식과 같이 반복에 대한 규칙이 한줄에 모두 들어있어서 가독성이 더 좋음
* 복잡한 조건이 필요한 경우 ```while```문이 더 적합할 수 있음

<br>

```java
for(초기값; 조건식; 증감식) {
  실행 코드 블럭
}
```

<br>

```java
public class loop3 {
    public static void main(String[] args) {
        for (int i=0; i <= 5; i++){
            System.out.println("current i is " + i);
        }
    }
}
```

```
current i is 0
current i is 1
current i is 2
current i is 3
current i is 4
current i is 5
```

<br>

---

### 5.4 for-each

* 인덱스를 접근하기는 ```for```문이 더 쉬움
  * ```for-each```는 인덱스를 사용하기 어려움



* 배열이나 컬렉션 등에 사용 가능
* 인텔리제이에서 ```iter```으로 간단히 생성 가능

<br>

```java
public class loop4 {
    public static void main(String[] args) {
      
        // 1. for-each 1
        int[] numbers = {1, 2, 3};
        for (int number : numbers) {
            System.out.println(number);
        }

        // 2. for-each 2
        String[] studentNames = {"Bob", "Mike", "Shawn", "Merry"};
        for (String name : studentNames) {
            System.out.println(name);
        }
    }
}
```

```
1
2
3
Bob
Mike
Shawn
Merry
```

<br>

---

## P.S.

* 정수는 ```int```, ```long```
  * 20억이 넘어가는 경우 ```long``` 사용



* 실수는 ```double```
  * ```float```는 정밀도가 너무 낮음



* 문자는 ```String``` 이용하자


---

## Reference

1. [https://www.geeksforgeeks.org/strings-in-java/](https://www.geeksforgeeks.org/strings-in-java/)
1. [https://www.baeldung.com/java-foreach-counter](https://www.baeldung.com/java-foreach-counter)