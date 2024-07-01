---
title: (Java - 18) 래퍼(Wrapper) 클래스
description: 자바에서 사용하는 래퍼 클래스에 대해서
author: seungki1011
date: 2024-01-13 12:30:00 +0900
categories: [Java]
tags: [java]
pin: true
math: true
mermaid: true
---


## 1) 기본형(Primitive Type)의 한계

`int`, `double`, `float`와 같은 기본향(Primitive Type)는 객체가 아니다. 이런 기본형들은 다음과 같은 한계를 지닌다.

* 객체가 아니기 때문에, 메서드 제공이 불가능하다

  * 객체 참조가 필요한 컬레션 프레임워크를 사용하거나, 제네릭스도 사용 불가능하다

  

* `null` 값을 가질 수 없다

  * 데이터가 `없다`라는 상태를 표현할 수 없다

<br>

코드로 알아보자.

```java
public class PrimitiveLimit {
    public static void main(String[] args) {
      
        int value = 10;
      
        int i1 = compareTo(value, 5);
        int i2 = compareTo(value, 10);
        int i3 = compareTo(value, 20);
      
        System.out.println("i1 = " + i1);
        System.out.println("i2 = " + i2);
        System.out.println("i3 = " + i3);
      
    }
  	
    // compareTo()라는 외부 메서드
    public static int compareTo(int value, int target) {
      
        if (value < target) {
            return -1;
        } else if (value > target) {
            return 1;
        } else {
            return 0; }
    }
}
```

```
i1 = 1
i2 = 0
i3 = -1
```

* 기본형 `int`인 `value`는 항상  `compareTo()`라는 외부 메서드를 사용해서 비교한다
* 자기 자신인 `value`와 다른 값을 연산하는 것이기 때문에 항상 자기 자신의 값인 `value`가 사용된다
* 만약 객체를 사용했다면, 자기 자신만의 메서드를 가지도록 설계해서 `value.compareTo(int target)` 같은 형태로 사용 가능
  * 쉽게 말해서 객체 자기 자신의 값을 가지고 외부 값과 비교

<br>

```java
public class PrimitiveLimitNull {
    public static void main(String[] args) {

        int[] intArr = {-1, 0, 1, 2, 3};

        System.out.println(findValue(intArr, -1)); //-1
        System.out.println(findValue(intArr, 0));
        System.out.println(findValue(intArr, 1));
        System.out.println(findValue(intArr, 100)); //-1
    }

    private static int findValue(int[] intArr, int target) {
        // 배열에 찾는 값이 존재하면 1 반환, 없으면 -1 반환
        for (int value : intArr) {
            if (value == target) {
                return value;
            }
        }
        return -1;
    }
}
```

```
-1
0
1
-1
```

* `findValue()` 는 배열에 찾는 값이 있으면 해당 값을 반환하고, 찾는 값이 없으면 `-1`을 반환한다



* `findValue()` 는 결과로 `int` 를 반환한다, 그러나 `int` 와 같은 기본형은 항상 값이 있어야 한다
  * 반환할 값을 찾지 못한다면 보통  `-1` 또는 `0` 을 사용해서 반환한다
  * 숫자를 반환할 때의 문제는 `-1` 또는 `0`이 있어서 반환한 것인지, 찾지 못해서 반환한 것인지 명확하지가 않다
  * 객체를 사용할 경우 데이터가 없다는 것을 표현하기 위해 `null`이라는 명확한 값이 존재한다
    * 물론 `NPE`의 발생을 주의하면서 사용해야 한다

<br>

---

## 2) 자바 래퍼 클래스(Wrapper Class)

### 2.1 래퍼 클래스 소개

자바는 기본형을 객체로 사용할 수 있도록 해당 기본형에 대응하는 래퍼 클래스를 제공해준다.

* `byte` → `Byte`
* `short` → `Short`
* `int` → `Int`
* `long` → `Long`
* `float` → `Float`
* `double` → `Double`
* `boolean` → `Boolean`
* `char` → `Character`

<br>

기본 래퍼 클래스들은 불변(immutable)이며, `equals()`로 비교를 해야 한다.

<br>

코드로 알아보자.

```java
public class WrapperTest1 {
    public static void main(String[] args) {
        // Boxing(박싱)
        Integer newInteger = new Integer(10); // deprecated, valueOf() 사용
        Integer integerObj = Integer.valueOf(10); // -128 ~ 127 캐싱

        Long longObj = Long.valueOf(100);
        Double doubleObj = Double.valueOf(0.5);

        System.out.println("newInteger = " + newInteger);
        System.out.println("integerObj = " + integerObj);
        System.out.println("longObj = " + longObj);
        System.out.println("doubleObj = " + doubleObj);

        System.out.println("--내부 값 읽기--");
        int intValue = integerObj.intValue();
        System.out.println("intValue = " + intValue);
        long longValue = longObj.longValue();
        System.out.println("longValue = " + longValue);

        System.out.println("--비교--");
        System.out.println("(newInteger == integerObj) = " + (newInteger == integerObj));
        System.out.println("newInteger.equals(integerObj) = " + newInteger.equals(integerObj));

    }
}
```

```
newInteger = 10
integerObj = 10
longObj = 100
doubleObj = 0.5
--내부 값 읽기--
intValue = 10
longValue = 100
--비교--
(newInteger == integerObj) = false
newInteger.equals(integerObj) = true
```

* 기본형 → 래퍼 클래스로 변경한느 것을 박싱(Boxing)이라고 부른다



* `new Integer()`는 deprecated, 대신에 `valueOf()`를 사용하면 된다
  * `valueOf()` 내부에는 자주 사용하는 값인 `-128~127`을 캐싱해놓은 최적화를 적용
  * 최적화 기법은 미래에 변할 수 있다



* 래퍼 클래스에 들어있는 기본형 값을 꺼내는 것을 언박싱(Unboxing)이라고 한다
  * `intValue()`



* 래퍼 클래스는 객체이기 때문에 내부의 값을 비교하기 위해서는 `equals()`를 사용해야 한다
  * `==`는 참조값 비교



* 래퍼 클래스에 리터럴로 값을 초기화 할 때 타입 접미사를 붙여준다
  * 예) `Long longValue = 400L;`
  * 예) `Double doubleValue = 3.14d;`

<br>

---

### 2.2 오토박싱(Autoboxing)

이전의 기본형을 래퍼 클래스로 변환하거나, 래퍼 클래스를 기본형으로 변환하는 코드를 살펴보자.

<br>

```java
// Primitive -> Wrapper
int value = 7;
Integer boxedValue = Integer.valueOf(value);

// Wrapper -> Primitive
int unboxedValue = boxedValue.intValue();
```

```
boxedValue = 7
unboxedValue = 7
```

* 박싱 : `valueOf()`
* 언박싱: `xxxValue()` (예: `intValue()` , `doubleValue()` )

<br>

박싱과 언박싱을 진행하는 코드를 사용하는 것이 귀찮다는 것을 알 수 있다. 박싱과 언박싱은 개발하면서도 자주 사용되기 때문에, 자바는 자바 1.5 부터 오토박싱을 지원한다.

코드로 알아보자.

<br>

```java
public class WrapperTest2 {
    public static void main(String[] args) {

        // 1. Auto-boxing : Primitive -> Wrapper
        int value = 10;
        Integer boxedValue = value;

        // 2. Auto-unboxing : Wrapper -> Primitive
        int unboxedValue = boxedValue;

        System.out.println("boxedValue = " + boxedValue);
        System.out.println("unboxedValue = " + unboxedValue);
        
    }
}
```

```
boxedValue = 10
unboxedValue = 10
```

<br>

---

### 2.3 래퍼 클래스의 메서드

래퍼 클래스가 제공하는 주요 메서드들을 살펴보자.

<br>

```java
public class WrapperTest3 {
    public static void main(String[] args) {

        Integer int1 = Integer.valueOf(10);
        Integer int2 = Integer.valueOf("20"); // 문자열 -> 래퍼 객체

        int intValue = Integer.parseInt("30");

        // 비교 연산
        int compareResult = int1.compareTo(int2); // int1 = 10, int2 = 20
        System.out.println("compareResult = " + compareResult);

        // 산술 연산
        System.out.println("Integer.sum(10,20) = " + Integer.sum(10,20));
        System.out.println("Integer.max(10,20) = " + Integer.max(10,20));
        System.out.println("Integer.min(10,20) = " + Integer.min(10,20));
    }
}
```

```
compareResult = -1
Integer.sum(10,20) = 30
Integer.max(10,20) = 20
Integer.min(10,20) = 10
```

* `valueOf()` : 래퍼 타입을 반환한다. 숫자, 문자열을 모두 지원한다
* `parseInt()` : 문자열을 기본형으로 변환한다



* `compareTo()` : 객체 자신의 값과 인수로 넘어온 값을 비교한다
  * 내 값이 크면 `1`
  * 같으면 `0`
  * 내 값이 작으면 `-1`



* `Integer.sum()` , `Integer.min()` , `Integer.max()` : 합, 작은 값, 큰 값 연산을 수행
  *  `static` 메서드이다

<br>

---

### 2.4 래퍼 클래스의 성능

래퍼 클래스와 기본형의 성능에 대해서 알아보자.

* 보통의 경우 기본형 연산이 래퍼 클래스의 연산보다 빠르다 (대략 3~5배)



* 기본형의 경우 단순히 그 크기 만큼만 공간을 차지한다
  * `int` : 4byte 차지



* 래퍼 객체의 경우, 내부 필드로 가지고 있는 값 + 객체를 다루는데 필요한 메타데이터를 포함한다
  * 대략 8~16 byte 차지



* 일반적인 애플리케이션을 만드는 관점에서 볼때 기본형과 래퍼 클래스의 사용을 최적화하는 것은 미미한 영향을 끼친다
* 만약 cpu 연산이 아주 많이 수행되는 특수한 경우이거나, 수십만번 이상 연속해서 수행해야하는 연산이라면 기본형 사용을 통한 최적화 고려
* 그렇지 않으면 보통 유지보수가 편한 래퍼 클래스 사용

<br>

---

## 3) `System`, `Math`, `Random` 클래스

### 3.1 `System` 클래스

`System` 클래스는 시스템과 관련된 기본 기능들을 제공한다.

코드로 알아보자.

<br>

```java
public class SystemTest1 {
    public static void main(String[] args) {

        // 현재 시간 (milli second)
        long currentTimeMs = System.currentTimeMillis();
        System.out.println("(밀리초)currentTimeMs = " + currentTimeMs);

        // 현재 시간 (nano second)
        long currentItemNs = System.nanoTime();
        System.out.println("(나노초)currentItemNs = " + currentItemNs);

        // 환경 변수 읽기
        Map<String, String> getEnv = System.getenv();
        System.out.println("getEnv = " + getEnv);

        // 시스템 속성 읽기
        System.out.println("properties = " + System.getProperties());
        System.out.println("Java Version = " + System.getProperty("java.version"));

        // 배열 빠르게 복사 - 시스템 레벨에서 최적화된 메모리 복사 연산 사용, 반복문 보다 훨씬 빠름
        char[] originalArray = {'J', 'A', 'V', 'A', '!'};
        char[] copiedArray = new char[5];

        System.arraycopy(originalArray, 0, copiedArray, 0, originalArray.length);

        System.out.println("copiedArray = " + copiedArray);
        System.out.println("Arrays.toString(copiedArray) = " + Arrays.toString(copiedArray));

        // 프로그램 종료
        System.exit(0);
        
    }
}
```

```
(밀리초)currentTimeMs = 1711887249669
(나노초)currentItemNs = 535655169572916
getEnv = {PYENV_SHELL=zsh, PATH=/opt/homebrew/Cellar/pyenv-virtualenv/1.2.1/shims: .. 생략 ..
properties = {java.specification.version=17, sun.jnu.encoding=UTF-8, java.class.path=/Users .. 생략 ..
Java Version = 17.0.10
copiedArray = [C@a09ee92
Arrays.toString(copiedArray) = [J, A, V, A, !]
```

*  `System.in` , `System.out` , `System.err`은 각각 표준 입력, 표준 출력, 표준 오류 스트림을 나타낸다
* `System.getenv()` : OS에서 설정한 환경 변수의 값을 얻을 수 있다



* `System.getProperties()` : 현재의 시스템 속성들을 얻을 수 있다
  * `System.getProperty(String key)`로 특정 속성을 얻을 수 있다
  * 시스템 속성 : 자바에서 사용하는 설정값들



* `System.exit(int status)` : 프로그램 종료
  * OS에 프로그램 종료 상태 코드 전달
  * `0` : 정상 종료
  * 이외의 수는 오류나 예외적인 종료, 특정 코드로 설정해서 로깅하는 방식을 사용할 수도 있음(이런 경우가 많지는 않음)

<br>

---

### 3.2 `Math` 클래스

`Math` 클래스는 여러가지 수학적 연산을 해결할 수 있도록 메서드를 지원한다.

자바 `Math` API 문서 - [https://docs.oracle.com/javase/8/docs/api/java/lang/Math.html](https://docs.oracle.com/javase/8/docs/api/java/lang/Math.html)

<br>

연산에는 다음과 같은 연산들이 포함된다.(일부만 적음, 메서드들이 굉장히 많기 때문에 필요한 경우 API 문서 참고.)

1. 기본 연산
   * `abs(x)` : 절대값
   * `max(a, b)` : 최대값
2. 지수, 로그 연산
   * `pow(a, b)` : a^b 연산
   * `log(x)` : 자연 로그
3. 반올림, 정밀도 연산
   * `ceil(x)` : 올림
   * `floor(x)` : 내림
   * `rint(x)` : 가장 가까운 정수로 반올림
   * `round(x)` : 반올림
4. 삼각 함수 연산
   * `sin(x)` : 사인
5. 기타
   * `sqrt(x)` : 제곱근
   * `random()` : `0.0`과 `1.0` 사이의 무작위 값 생성

<br>

---

### 3.3 `Random` 클래스

`Random` 클래스를 통해 다양한 랜덤값을 얻을 수 있다. `Math.random()`도 내부적으로 `Random` 클래스를 이용한다

`Random`은 `java.util` 패키지 소속이다.

코드로 알아보자.

<br>

```java
public class RandomTest {
    public static void main(String[] args) {
      
        Random random = new Random();
        //Random random = new Random(777); // 시드(seed)가 같은 경우 랜덤의 결과가 똑같게 나온다

        int randomInt = random.nextInt();
        System.out.println("randomInt = " + randomInt);

        double randomDouble = random.nextDouble();
        System.out.println("randomDouble = " + randomDouble);

        boolean randomBoolean = random.nextBoolean();
        System.out.println("randomBoolean = " + randomBoolean);

        // 범위 조회
        int randomRange1 = random.nextInt(10); // 0 ~ 9의 범위에서 랜던한 값
        System.out.println("0 ~ 9 = " + randomRange1);

        int randomRange2 = random.nextInt(10) + 1; // 1 ~ 10의 범위에서 랜던한 값
        System.out.println("1 ~ 10 = " + randomRange2);
    }
}
```

```
randomInt = 1114421447
randomDouble = 0.687605609327408
randomBoolean = false
0 ~ 9 = 1
1 ~ 10 = 10
```

* `random.nextInt()` : 랜덤 `int` 값을 반환한다
* `nextDouble()` : `0.0d` ~ `1.0d` 사이의 랜덤 `double` 값을 반환한다
* `nextInt(int bound)` : `0` ~ `bound` 미만의 숫자를 랜덤으로 반환

<br>

> 시드(Seed)에 관하여
>
> 랜덤은 내부에서 씨드(Seed)값을 사용해서 랜덤 값을 구한다. 그래서 시드값을 고정시키면 항상 같은 결과가 출력된다.
>
> * `new Random()`을 이용하면 `System.nanoTime()`을 이용한 복잡한 알고리즘에 의해 시드값을 생성하기 때문에, 랜덤을 역추정하는 것을 크게 걱정하지 않아도 된다
> * 시드를 고정하면 테스트 코드 같은 곳에서 같은 결과를 반복적으로 검증할 수 있다
