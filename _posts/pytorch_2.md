pytorch basics



## Pytorch Operations

* 파이토치는 numpy + AutoGrad



### Tensor

* 다차원 Array를 표현하는 PyTorch 클래스
* 사실상 numpy의 ndarray 와 동일 
* Tensor를 생성하는 함수도 거의 동일

```python
import numpy as np

n_array=np.arange(10).reshape(2,5)
print(n_array)
print("ndim : ",n_array.ndim, "shape : ",n_array.shape)
```

```
[[0 1 2 3 4]
 [5 6 7 8 9]]
ndim :  2 shape :  (2, 5)
```



```python
import torch

t_array=torch.FloatTensor(n_array)
print(t_array)
print("ndim : ",t_array.ndim, "shape : ",t_array.shape)
```

```
tensor([[0., 1., 2., 3., 4.],
        [5., 6., 7., 8., 9.]])
ndim :  2 shape :  torch.Size([2, 5])
```



### Array to Tensor

* Tensor 생성은 list나 ndarray를 사용 가능

#### list to tensor

```python
data = [[3,5],[10,5]]
x_data = torch.tensor(data)
x_data
```

```
tensor([[ 3,  5],
        [10,  5]])
```

#### ndarray to tensor

```python
nd_array_ex = np.array(data)
tensor_array = torch.from_numpy(nd_array_ex)
tensor_array
```

```
tensor([[ 3,  5],
        [10,  5]], dtype=torch.int32)
```



### Tensor data types

* tensor가 가질 수 있는 data 타입은 numpy와 동일

![ptdatatype](https://user-images.githubusercontent.com/120040458/222897476-3aed01a5-64ce-4ff2-bec6-8501bdae4de0.png)

<p align="center"> https://pytorch.org/docs/stable/tensors.html </p>



### numpy like operations

* numpy 대부분의 사용법과 유사

```python
data = [[3,5,20],[10,5,50],[1,5,10]]
x_data = torch.tensor(data)

x_data[1:]
```

```
tensor([[10,  5, 50],
        [ 1,  5, 10]])
```

```python
x_data[:2,1:]
```

```
tensor([[ 5, 20],
        [ 5, 50]])
```

```python
x_data.flatten()
```

```
tensor([ 3,  5, 20, 10,  5, 50,  1,  5, 10])
```

```python
torch.ones_like(x_data)
```

```
tensor([[1, 1, 1],
        [1, 1, 1],
        [1, 1, 1]])
```



### GPU 에 tensor 올려서 사용

```python
x_data.device
```

```
device(type='cpu')
```

```python
if torch.cuda.is_available():
    x_data_cuda = x_data.to("cuda")
x_data_cuda.device
```

```
device(type='cuda', index=0)
```



### Tensor handling

* view : reshape과 동일하게 tensor의 shape 변환
* squeeze : 차원의 개수가 1인 차원을 삭제 (압축)
* unsqueeze :  차원의 개수가 1인 차원을 추가

#### view vs reshape

* view 쓰는 것 권장

```python
tensor_ex.view([-1,6])
```

```
tensor([[0.2078, 0.5975, 0.1303, 0.4684, 0.0908, 0.4422],
        [0.0051, 0.0136, 0.8748, 0.0650, 0.1050, 0.4723]])
```

```python
tensor_ex.reshape([-1,6])
```

```
tensor([[0.2078, 0.5975, 0.1303, 0.4684, 0.0908, 0.4422],
        [0.0051, 0.0136, 0.8748, 0.0650, 0.1050, 0.4723]])
```



#### view vs reshape의 contiguity 보장의 차이

##### view는 contiguity 보장

```python
a = torch.zeros(3,2)
b = a.view(2,3)
print(a.fill_(1))
print(b) # 기존 메모리주소는 동일하게 쓰면서 표현 형태만 바뀜
```

```
tensor([[1., 1.],
        [1., 1.],
        [1., 1.]])
tensor([[1., 1., 1.],
        [1., 1., 1.]])
```

##### reshape은 보장 안함

* 모양이 깨지는 순간 copy

```python
a = torch.zeros(3,2)
b = a.t().reshape(6)
print(a.fill_(1))
print(b)
```

```
tensor([[1., 1.],
        [1., 1.],
        [1., 1.]])
tensor([0., 0., 0., 0., 0., 0.])
```



#### squeeze vs unsqueeze



![squeeze1](https://user-images.githubusercontent.com/120040458/222899860-ebc3d18f-2067-4cf4-8c81-9a181438b84e.png)



```python
tensor_ex = torch.rand(size=(2,1,2))
tensor_ex
```

```
tensor([[[0.8575, 0.8543]],

        [[0.6678, 0.2064]]])
```

```python
squeeze_tensor = tensor_ex.squeeze()
squeeze_tensor
```

```
tensor([[0.8575, 0.8543],
        [0.6678, 0.2064]])
```



```python
squeeze_tensor.size()
```

```
torch.Size([2, 2])
```



```python
squeeze_tensor.unsqueeze(0)
```

```
torch.Size([1, 2, 2])
```

```python
squeeze_tensor.unsqueeze(1).shape
```

```
torch.Size([2, 1, 2])
```

```python
squeeze_tensor.unsqueeze(2).shape
```

```
torch.Size([2, 2, 1])
```



### Tensor muliplication

#### dot, mm, matmul

* 행렬곱셈 연산은 dot가 아닌 mm, matmul 사용
* 양쪽이 벡터인 경우 내적을 구하기 위해 dot 사용 가능

```python
t1 = torch.FloatTensor([[1,2],[3,4]])
t2= torch.FloatTensor([[1,2],[3,4]])
t1
```

```
tensor([[1., 2.],
        [3., 4.]])
```

```python
t1.dot(t2) # dot 연산은 벡터(1d tensor) 끼리
```

```python
---------------------------------------------------------------------------
RuntimeError                              Traceback (most recent call last)
~\AppData\Local\Temp\ipykernel_13196\2372691299.py in <module>
----> 1 t1.dot(t2)

RuntimeError: 1D tensors expected, but got 2D and 2D tensors
```

```python
a = torch.FloatTensor([1,2])
b = torch.FloatTensor([3,4])
a.dot(b)
```

```
tensor(11.)
```



```python
t1.mm(t2)
```

```
tensor([[ 7., 10.],
        [15., 22.]])
```

```python'
t1.matmul(t2)
```

```
tensor([[ 7., 10.],
        [15., 22.]])
```



#### mm vs matmul

* mm은 자동 브로드캐스팅 지원 안함
* matmul은 자동 브로드캐스팅 지원함
* 텐서연산에 익숙하지 않다면 mm 권장



## nn.functional 모듈

* nn.functional 모듈을 통해 다양한 수식 변환을 지원함

```python
import torch.nn.functional as F

tensor_ex = torch.FloatTensor([0.5,0.7,0.1])
h_tensor = F.softmax(tensor_ex, dim=0) # 소프트맥스 지원
h_tensor
```

```
tensor([0.3458, 0.4224, 0.2318])
```

```python
y = torch.randint(5, (10,5))
y_label = y.argmax(dim=1)

torch.nn.functional.one_hot(y_label) # 원핫 인코딩 지원
```

```
tensor([[0, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 1, 0],
        [0, 0, 1, 0],
        [0, 1, 0, 0],
        [1, 0, 0, 0],
        [1, 0, 0, 0],
        [0, 0, 0, 1],
        [1, 0, 0, 0]])
```



## AutoGrad

* 자동 미분의 지원, backward 함수

```python
w=torch.tensor(2.0, requires_grad=True)
y=w**2
z=10*y+25
z.backward()
w.grad
```

```
tensor(40.)
```



```python
a=torch.tensor([2.,3.], requires_grad=True)
b=torch.tensor([6.,4.], requires_grad=True)
Q = 3*a**3-b**2
external_grad = torch.tensor([1.,1.])
Q.backward(gradient=external_grad)

a.grad
```

```
tensor([36., 81.])
```

```python
b.grad
```

```
tensor([-12.,  -8.])
```

