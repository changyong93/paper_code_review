- MLM(Masked Language Modeling) : 전체에서 15% tokens를 [mask]로 변경하고, masking된 token의 원래 값이 무엇인지 맞추는 학습 방법
- 단, MLM은 전체에서 15%만 학습하기에, 자원 손실이 발생하며, 많은 학습량(연산량)이 요구됨
- 따라서, 해당 논문에서는, 똑같이 masking에 대해 특정 token을 생성하는 generator와 아니면 원래 token인지 맞추는 discriminator 구조를 제안(contribution)
- 이 방법은 GAN과 비슷하지만, GAN은 adversarial하여 G와 D가 적대적으로 서로를 속고 속이는 관계이지만
- ELECTRA는 G에서 생성한 것을 D가 잘 맞추는지에 대한 성능을 개선해나감 => MLE를 최대화

![image](https://user-images.githubusercontent.com/74341192/133956782-7feaa813-b581-434d-bf4b-8735d076372d.png)

- 학습 방법
  - Generator G와 Discriminator D인 두 neural network 학습
  - 두 NN은 Transformer의 Encoder이며, 토큰 시퀀스 x = [x1,x2,...,xn]을 입력으로 받아 문맥 정보를 반영하는 벡터 시퀀스 h(x)= [h1,h2,...,hn]으로 매핑
  
  - Generator : BERT의 MLM과 똑같음
    - 입력 x에 대해 마스킹할 위치 집합 m=[m1,m2,...,mk]를 결정
    - 모든 마스킹 위치는 1과 n 사이의 정수이며 수학적으로 다음과 같이 표시 ![image](https://user-images.githubusercontent.com/74341192/133957602-99a8912f-ad40-41bb-97ea-c933d4dc5217.png)
    - 마스킹할 개수 k는 보통 0.15n (전체 토큰의 15%)
    - 결정한 위치는 [MASK]로 치환, 이 과정을 다음과 같이 표현 ![image](https://user-images.githubusercontent.com/74341192/133957672-0138a94c-5049-4528-a40b-54f7733c110b.png)
    - 마스킹 된 입력 x^masked에 대해 generator는 아래와 같은 원리로 토큰이 무엇인지 예측(t 번째 토큰에 대한 예측) ![image](https://user-images.githubusercontent.com/74341192/133957189-39b07efa-66c2-4930-b4e8-744e69552ab2.png)
    - e는 임베딩을 의미이며, 위 식은 language model의 출력 레이어와 임베딩 레이어의 가중치를 공유(weight sharing)하겠다는 의미
    - 최종적으로 아래와 같이 MLM loss 학습 ![image](https://user-images.githubusercontent.com/74341192/133957812-8be9c6b5-6025-4e7c-bcd5-278a9587dc87.png)
  - Disriminator : 입력 토큰시퀀스에 대해 각 토큰이 original인지 replaced인지 이진 분류로 학습
    - G를 이용해 마스킹된 입력 토큰을 예측
    - G에서 마스킹할 위치 집합 m에 해당하는 위치 토큰을 [MASK]가 아닌 G의 softmax 분포 P_G(xt|x)에 대해 샘플링한 토큰으로 치환(corrupt)
    - 치환된 입력 x에 대해 D는 토큰이 원래 입력과 동일한 지 치환된 것인지 예측 ![image](https://user-images.githubusercontent.com/74341192/133957944-793a78c9-ccce-4793-8e6d-4054be9d1852.png)
    - 최종적으로 아래와 같이 loss 학습 ![image](https://user-images.githubusercontent.com/74341192/133958048-72334533-15ed-4c90-9cdb-10084deded48.png)

    

