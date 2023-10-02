---
# layout: post
# title:  "(Coursera)Modern Data Ecosystem & Role of Data Engineering"
# author: seungki
# categories: [ Data Engineering ]
# image: post_images/ibm_coursera.png
# toc: True


---

---

해당 포스트는 coursera의 IBM Data Engineering 코스를 듣고 한글로 다시 정리한 내용입니다.

## Modern Data Ecosystem

### 현대의 데이터 생태계

현재 데이터 처리 속도와 bandwidth의 증가, 데이터의 생성 소비 및 공유에 대한 끊임 없는 발전으로 인해 데이터의 중요성은 나날이 커지고 있다. 이런 데이터의 source 부터 시작해서 데이터를 수집, 처리, 분석하는 인프라 및 유저들을 아우르는 생태계를 data ecosystem 이라고 한다. 이런 데이터 생태계 내부의 요소들은 상호적으로  연결 되어 있으면서 독립적이고, 지속적으로 발전해나가고 있다.

<img src="../post_images/2023-08-05-data_engineer_ibm_1/data_ecosystem.jpeg" alt="data_ecosystem" style="zoom:67%;" />

<p align="center">출처 - https://www.datameer.com/blog/the-how-to-guide-for-understanding-data-ecosystems/</p>

이런 데이터 생태계는 다음을 포함한다고 볼 수 있다.

* 서로 다른 data source로 부터 통합된 데이터
* 데이터에 대한 분석을 통해 얻은 insight
* 해당 insight를 통한 여러 이해관계자들과의 협업
* 필요한 데이터를 전달하기 위한 도구, 애플리케이션 그리고 인프라

### Data Sources

정형과 비정형 데이터로 정말 많은 곳에서 데이터가 올 수 있다.

<img src="../post_images/2023-08-05-data_engineer_ibm_1/data-sources.png" alt="data-sources" style="zoom:67%;" />

<p align='center'>출처 - https://www.fico.com/blogs/using-alternative-data-credit-risk-modelling</p>

* 텍스트
* 비디오
* clickstream
* 유저간 메세지
* IoT
* realtime data
* professional provider

위의 예시 말고도 다양한 data source들이 존재한다.
