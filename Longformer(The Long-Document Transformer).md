[Longformer: The Long-Document Transformer paper view](https://arxiv.org/abs/2004.05150) paper review
---

Transformer의 self-attention은 input의 sequence length에 메모리와 연산량이 quadratic하게 증가함에 따라 long sequence를 처리하는데 문제가 되는 걸림돌이 된다.
그 예로, Transformer 중 encoder 구조를 사용한 BERT는 리소스 및 연산량 문제를 max sequence length를 512로 제한였으며, 그로 인해 long sequence를 처리하기가 매우 어렵다.
이 논문에선 이 문제점을 지적하며 sequence length에 선형적으로 연산량이 증가하는 어텐션 메커니즘을 제안하였다.

long sequence를 처리하는 기존 연구는 크게 두 가지로 나뉜다.   

첫 번째 방법은 긴 텍스트를 **left-to-right**로 이동하며 ,Chunk 단위로 쪼개어 임베딩 한뒤, 이를 다시 시퀀스로 임베딩 하는 방법이다.
이 방식은 autoregressive language modeling엔 적합하나, 스퀀스를 임베딩하는 과정에서 정보 유실이 발생하기에 bidirectional context을 요구하는 테스크에는 적합하지 않다.
(관련 연구 : Transformer-XL, Adaptive Span Transformer)

두 번째 방식은 sparse attention pattern을 찾아 복잡도를 줄이는 방식으로, Longformer는 이 방식의 연구에 속한다.

Longformer의 attention 메커니즘은 windowed local-context self-attention과 global attention의 조합으로, 
local attention은 contextual representation이며, global attention은 full sequence representation이다.


#### Longformer에서 제시한 방법(a는 기존 transformer의 attention 방법)
**b) Sliding Window c) Dilated Sliding Window d) Global Attention**
![image](https://user-images.githubusercontent.com/74341192/144062051-f3dfba2c-d82b-4f4a-b838-a2d24e20e3e5.png)

##### Sliding Window
이 방식은 각 토큰별 고정된 크기의 window 만큼의 토큰에만 attention 연산릉 수행한다. 이 경우 window를 벗어나느 토큰과의 attention을 계산하지 않는다.
하지만 이러한 레이어를 여러 층 쌓으면, CNN을 여러 개 쌓을 때 receptive field가 커지는 것 처럼, 넓은 context 정보를 가지는 representation을 만들 수 있으며,
L개의 층을 쌓았을 때, receptive field 크기는 L\*w에 해당한다.
window size를 sequence length(전체 토큰 개수)를 n라 할 때, 각 토큰은 좌우 0.5 w개의 토큰들과 attention을 계산하므로, 이 경우 전체 연산량은 O(n x w)이 된다.

##### Dilated Sliding Window
이 방식은 연산량의 증가 없이 receptive field의 영역을 더 확장하기 위하여 고안되었다.
window size를 w, dilation size를 d, layer를 l이라고 할 때, 좌우 양끝에 각각 wxd/2 만큼의 receptive field가 넓어므로, 전체 receptive field size는 l x d x w가 된다.

##### Global Attention
BERT 기반의 모델들은 language model 학습과 downstream task 학습 시 서로 다른 방식으로 context를 바라본다. 
MLM의 경우 local text를 보려 masking된 단어를 예측하는 반면, classification의 경우 Bert에선 **[CLS]** 토큰을 활용하여 전체 문장을 바라본다. 
앞서 언급한 'Sliding Window' 방식과 'Dilated Sliding Window' 방식은 local context 정보를 담기에 긴 텍스트 정보가 필요한 task에는 적합하지 않은 부분이 있다.

따라서, 본 논문에선 input에서 특정 토큰(e.g. \[CLS\])을 몇 개 지정하여 global attention을 수행하도록 한다. 
이 토큰들은 입력 전체에 대해 attention을 수행하지만, sequence 길이에 비해 토큰 수가 매우 적기에 복잡도는 여전히 O(N)이 된다.

###### Linear Projections for Global Attention
transformer에서 attention은 Q,K,V의 linear projections으로 계산이 된다. 앞서 언급한 sliding window 방식의 attention과 global attention을 위해 각각 Qs,Ks,Vs, Qg, Ks, Vs로 나눠서 계산을 한다.




