 # RoBERTa: A Robustly Optimized BERT Pretraining Approach
 [archive Link](https://arxiv.org/abs/1907.11692)
 [paper Link](https://arxiv.org/pdf/1907.11692.pdf)
 ---
 
 ## 0) Abstract
 - pretraining을 활용한 BERT는 놀라운 성능을 보여주었지만, 키 하이퍼 파라미터와 학습 데이터 크기에 따라 결과값 차이가 크며, cost 경쟁력이 매우 떨어짐
 - 다양한 실험을 통해 BERT가 underfit 상태임을 확인했으며, 다양한 파라미터 및 데이터 사이즈 변화를 통해 BERT 이상의 모델을 만들 수 있음!!
 => RoBERTa 두두등장
 
 ## 1) Introduction
 undertrained인 BERT의 개선 방안을 다음과 같이 제시했다.
 - training the model longer, with bigger batches, over more data
 - removing NSP
 - training on longer sequences
 - dynamically changing the masking pattern applied to the training data
 
 저자가 말하길, contribution은 다음과 같다.
 (1) downstream task에서의 성능 향상을 위한 BERT의 design choices, traning 전략
 (2) 새로운 데이터셋 CCNEWS 수집
 (3) 적절한 degien choices에 기반한 MLM 학습으로 다른 methods들 대비 더 나은 성능을 입증
 
 ## 2) Backward
 - Bert pretraining apporach와 training choices를 보고오면 된다. 혹은 RoBERTa 논문의 2.1~2.5를 참고

## 3) Experimental Setup
- 전반적으로 BERT와 유사하나, peak learning rate, warmup steps, adam epsilon에 대해서는 tuning을 진행했고,
![\beta_2](https://latex.codecogs.com/svg.latex?\beta_2)는 기존 0.999(bert)에서 0.98로 변경
- 전체 sequence의 최대 길이는 512로 지정

### 3.1) Data 여기부터 
