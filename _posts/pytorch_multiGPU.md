## MultiGPU 학습

* gpu 확보는 매우 중요



## Model parallel

* 다중 GPU에 학습을 분산하는 두가지 방법

  +모델을 나누기 / 데이터를 나누기

* 모델을 나누는 것은 생각보다 예전부터 썻음(alexnet)

* 모델의 병목, 파이프라인의 어려움 등으로 인해 모델 병렬화는 고난이도 과제



### 병렬화의 문제점

* 좋은 병렬화를 위해서는 데이터 처리가 겹쳐야함

![model parallelization](https://user-images.githubusercontent.com/120040458/225496893-413a8037-1253-47f1-b3ed-d0d3afa9616e.PNG)

<p align="center">출처 : http://www.idris.fr/eng/ia/model-parallelism-pytorch-eng.html</p>



### GPU parallel  example

```python
import torch
import torch.nn as nn
class ModelParallel(nn.Module):
    def __init__(self):
        super(ModelParallel, self).__init__()
        self.net0 = nn.Linear(20, 10).to('cuda:0') # 첫번째 모델을 cuda 0에 할당
        self.relu = nn.ReLU()
        self.net1 = nn.Linear(10, 10).to('cuda:1') # 첫번째 모델을 cuda 1에 할당

    def forward(self, x):
        x = self.relu(self.net0(x.to('cuda:0'))) # 두 모델을 연결, copy
        return self.net1(x.to('cuda:1'))
```



## Data parallel

* 데이터를 나눠 GPU에 할당후 결과의 평균을 취하는 방법
* minibatch 수식과 유사, 한번에 여러 GPU에서 수행

![dataparellel](https://miro.medium.com/v2/resize:fit:720/format:webp/1*FpDHkWJhkLL7KxU01Lf9Lw.png)

<p align="center">출처 : https://bit.ly/37usURV</p>

* Pytorch에서는 아래 두 가지 방식을 제공
  * DataParallel, DistributedDataParallel
  
* DataParallel - 단순히 데이터를 분배한후 평균을 취함
  * GPU 사용 불균형 문제 발생, batch 사이즈 감소(한 GPU가 병목), GIL(global interpreter lock)문제

* DistributedDataParallel - 각 CPU마다 process 생성하여 개별 GPU에 할당
  * 기본적으로 DataParallel로 하나 개별적으로 연산의 평균을 냄(모아서 처리 X)




### Data parallel example

```python
train_sample = torch.utils.data.distributed.DistributedSampler(train_data) # Sampler 사용
shuffle = False
pin_memory = True # dram에 메모리 바로 올릴 수 있도록

trainloader = torch.utils.data.Dataloader(train_data, batch_seize=20, shuffle=False
pin_memory=pin_memory, num_workers=3, sampler=train_sampler)
```

