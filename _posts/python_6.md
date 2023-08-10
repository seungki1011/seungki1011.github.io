---
layout: post
title:  "Python - 6(OOP)"
author: seungki
categories: [ Python ]
image: post_images/python logo.png
toc: True


---

---

## Python Object Oriented Programming

### Python naming rule

* 변수명, class명, 함수명을 짓는 방식이 존재
* snake_case : 뛰어쓰기 부분에 "_" 추가, 파이썬 함수/변수명에 사용
* CamelCase : 뛰어쓰기 부분에 대문자, 파아썬 Class명에 사용



### Attribute 추가하기

```python
class SoccerPlayer(): # class명은 SoccerPlayer, ()안에는 상속받을 클래스 넣기
    def __init__(self,name,position,back_number): # __init__은 객체 초기화 예약함수
        self.name=name
        self.position=position
        self.back_number=back_number
```



### __ 의 의미

* 특수한 예약 함수나 변수 그리고 함수명 변경(맹글링)으로 사용

```python
class SoccerPlayer():
    # __init__생략
    def __str__(self):
        return f"Hello, my name is {self.name}. I play as a {self.position}"

instance1 = SoccerPlayer("Park","MF",10)
print(instance1)
```

```
Hello, my name is Park. I play as a MF
```



### Method 구현하기

* method 추가는 기존 함수와 같으나, 반드시 self를 추가해야만 class 함수로 인정됨

```python
class SoccerPlayer(): 
    # __init__생략
    def change_back_number(self, new_number):
        print(f"선수의 등번호를 변경합니다: from {self.back_number} to {new_number}")
        self.back_number = new_number
```

```python
park = SoccerPlayer("Park","MF",10) # 인스턴스 생성, 초기값 입력
print(park.back_number)
```

```
10
```

```python
park.change_back_number(5)
```

```
선수의 등번호를 변경합니다: from 10 to 5
```



### OOP 구현 연습



## 상속(Inheritance)

* 부모 클래스로 부터 속성과 메소드를 물려받은 자식 클래스를 생성하는 것

```python
class Person(): # 부모 클래스
    def __init__(self,name,age):
        self.name=name
        self.age=age

class Korean(Person): # 부모 클래스인 Person을 상속 받음
    pass

first_korean=Korean("kimseungki",28)
print(first_korean.name)
```

```
kimseungki
```



### inheritence example 1, super()

```python
class Person(): # 부모 클래스
    def __init__(self,name,age,gender):
        self.name=name
        self.age=age
        self.gender=gender
        
    def about_me(self): # 부모 클래스의 메소드
        print("제 이름은", self.name,"나이는",str(self.age),"입니다")

class Employee(Person): # 부모 클래스인 Person으로 부터 상속
    def __init__(self,name,age,gender,salary,hire_date):
        super().__init__(name,age,gender) # super로 부모객체 사용
        # Employee의 속성값(attribute) 추가
        self.salary=salary
        self.hire_date=hire_date
        
    def do_work(self): # Employee의 새로운 메소드
        print("일을 하고 있습니다")
        
    def about_me(self): # 부모 클래스의 함수 재정의
        super().about_me() # 부모 클래스의 함수 사용
        print("제 급여는",self.salary,"제 입사일은",self.hire_date)
```

```python
person_instance = Person("kimseungki","28","gender")
person_instance.about_me()
```

```
제 이름은 kimseungki 나이는 28 입니다
```

```python
employee_instance = Employee("ksk", "100", "male", "10000$", "2222-12-31")
employee_instance.do_work()
employee_instance.about_me()
```

```
일을 하고 있습니다
제 이름은 ksk 나이는 100 입니다
제 급여는 10000$ 제 입사일은 2222-12-31
```



## 가시성(visibilty)

* 객체의 정보를 볼 수 있는 레벨을 조절하는 것
* 누구나 객체 안의 변수를 보고 접근 할 필요가 없음
  1. 객체를 사용하는 사용자가 임의로 정보 수정 할 수 없게
  2. 필요 없는 정보에는 접근 할 필요가 없음
  3.  소스의 보호를 위해



### Encapsulation

* 캡슐화, 은닉화
* class를 설계할 때, 클래스 간 간섭/정보고유의 최소화
* 인터페이스만 알아서 써야함



### visibilty example 1

* product 객체를 inventory 객체에 추가
* inventory에는 오직 product 객체만 들어감
* inventory에 product가 몇 개인지 확인 필요
* inventory에 product items는 직접 접근이 불가능하게



```python
# -----------------------------모두가 접근이 가능한 경우-----------------------------
class Product():
    pass

class Inventory():
    def __init__(self):
        self.items=[] 
    
    def add_new_item(self,product):
        if type(product)==Product: # type이 Product면, items에 product 추가
            self.items.append(product)
            print("new item added")
        else:
            raise ValueError("invalid item")
    
    def get_number_of_items(self):
        return len(self.items)
```

```python
# private 변수 없이 모두 접근 가능한 경우
my_inventory=Inventory()
my_inventory.add_new_item(Product())
my_inventory.add_new_item(Product())
my_inventory
```

```
new item added
new item added
<__main__.Inventory at 0x246526807f0>
```

```python
my_inventory.items # items에 접근해보면 마음대로 들어다 볼 수 있음
```

```
[<__main__.Product at 0x24652680e20>, <__main__.Product at 0x24652680610>]
```

```python
my_inventory.items.append("abc") # 다른 사용자가 임의로 items에 추가 가능
my_inventory.items 
```

```
[<__main__.Product at 0x24652680e20>,
 <__main__.Product at 0x24652680610>,
 'abc']
```



```python
# -----------------------------private 변수 선언으로 접근 막는 경우-----------------------------
class Product():
    pass

class Inventory():
    def __init__(self):
        self.__items=[] # private 변수로 선언해서 타객체에서 접근 불가능
    
    def add_new_item(self,product):
        if type(product)==Product: # type이 Product면, items에 product 추가
            self.__items.append(product)
            print("new item added")
        else:
            raise ValueError("invalid item")
    
    def get_number_of_items(self):
        return len(self.__items)
```

```python
my_inventory_2=Inventory()
my_inventory_2.add_new_item(Product())
my_inventory_2.add_new_item(Product())
my_inventory_2
```

```
new item added
new item added
<__main__.Inventory at 0x24650c925b0>
```

```python
my_inventory_2.__items # 접근이 불가
```

```python
---------------------------------------------------------------------------
AttributeError                            Traceback (most recent call last)
~\AppData\Local\Temp\ipykernel_16516\3260174018.py in <module>
----> 1 my_inventory_2.__items

AttributeError: 'Inventory' object has no attribute '__items'
```



### visibility example 2

* product 객체를 inventory 객체에 추가
* inventory에는 오직 product 객체만 들어감
* inventory에 product가 몇 개인지 확인 필요
* inventory에 product items 접근을 허용



```python
class Product():
    pass

class Inventory():
    def __init__(self):
        self.__items=[]
    
    @property # property decorator 숨겨진 변수를 반환하게 해줌
    # 보통은 그대로 리턴하지 않고 copy한 걸 리턴해줌
    def items(self):
        return self.__items
    
    def add_new_item(self,product):
        if type(product)==Product: # type이 Product면, items에 product 추가
            self.__items.append(product)
            print("new item added")
        else:
            raise ValueError("invalid item")
    
    def get_number_of_items(self):
        return len(self.__items)
```

```python
my_inventory=Inventory()
my_inventory.add_new_item(Product())
my_inventory.add_new_item(Product())
print(my_inventory.get_number_of_items())
```

```
new item added
new item added
2
```

```python
items=my_inventory.items # property decorator로 함수를 변수처럼 호출
items.append(Product())
print(my_inventory.get_number_of_items())
```

```
3
```

```python
my_inventory.items # items로는 접근 가능
```

```
[<__main__.Product at 0x276fff8b4f0>,
 <__main__.Product at 0x276fff71640>,
 <__main__.Product at 0x2768006d4c0>]
```



## First-Class Objects

* 일등 함수 또는 일급 객체
* 변수나 데이터 구조에 할당이 가능한 객체
* 파라미터로 전달이 가능, 리턴 값으로 사용가능
* 파이썬의 함수는 일급함수

```python
def square(x):
    return x*x

f=square
f(5) # 함수를 변수 처럼 사용
```

```
25
```



* 함수를 파라미터 처럼 사용

```python
def cube(x):
    return x*x*x

def formula(method, argument_list):
    return [method(value) for value in argument_list]
```

```python
ex_list = [1,2,3,4,5]
formula(cube,ex_list)
```

```
[1, 8, 27, 64, 125]
```



## Inner function

* 함수 내에 또 다른 함수가 존재

```python
def print_msg(msg):
    def printer():
        print(msg)
    printer()

print_msg("hello python!")
```

```
hello python!
```

* closures : inner function을 return 값으로 반환

```python
def print_msg_closure(msg):
    def printer():
        print(msg)
    return printer

another=print_msg_closure("hello python?")
another()
```

```
hello python?
```



### closure example 1

```python
def tag_func(tag,text):
    text=text
    tag=tag
    
    def inner_func():
        return "<{0}>{1}<{0}>".format(tag,text)
    
    return inner_func

h1_func = tag_func("title","this is a python class")
p_func = tag_func("p", "data academy")

h1_func()
```

```
'<title>this is a python class<title>'
```



## decorator function

* 복잡한 클로져 함수를 간단하게

### decorator example 1

```python
def star(func):
    def inner(*args,**kwargs):
        print("*"*30)
        func(*args, **kwargs)
        print("*"*30)
    return inner

@star # star 아래의 printer라는 함수는 star(func)로 전달됨
def printer(msg):
    print(msg)
    
printer("hello")
```

```
******************************
hello
******************************
```

```python
def star(func):
    def inner(*args,**kwargs):
        print(args[1]*30) # mark 넘겨받음
        func(*args, **kwargs)
        print(args[1]*30)
    return inner

@star
def printer(msg, mark):
    print(msg)
    
printer("hello", "X")
```

```
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
hello
XXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
```



### decorator example 2  - 다단계 형태로도 만들기 가능

```python
@star
@percent # msg를 percent로 넘겨주고 그 결과를 star에 넘겨주는 방식
def printer(msg, mark):
    print(msg)
printer("hello!")
```



### decorator example 3

```python
def generate_power(exponent):
    def wrapper(f):
        def inner(*args): # f는 raise_two를 받은거임
            result=f(*args)
            return exponent**result
        return inner
    return wrapper

@generate_power(2) # 2는 generate_power의 exponent에 들어감
def raise_two(n): # raise_two는 wrapper로 전달
    return n**2

print(raise_two(7))
```

```
562949953421312
```

## 참고

---

1. [boostcourse - 머신러닝을 위한 파이썬](https://www.boostcourse.org/ai222)
2. [Python documentation](https://docs.python.org/3/)
