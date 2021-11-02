# [Retrieving and Reading : A ComprehensiveSurvey on Open-domain Question Answering](https://arxiv.org/abs/2101.00774)
Fengbin Zhu, Wenqiang Lei*, Chao Wang, Jianming Zheng, Soujanya Poria, Tat-Seng Chua

---

## 0. Abstract
Open-domain Question Answering (OpenQA) is an important task in Natural Language Processing (NLP), which aims to answer a question in the form of natural language based on large-scale unstructured documents. Recently, there has been a surge in the amount of research literature on OpenQA, particularly on techniques that integrate with neural Machine Reading Comprehension(MRC). While these research works have advanced performance to new heights on benchmark datasets, they have been rarely covered in existing surveys on QA systems. In this work, we review the latest research trends in OpenQA, with particular attention to systems that incorporate neural MRC techniques. Specifically, we begin with revisiting the origin and development of OpenQA systems. We then introduce modern OpenQA architecture named “Retriever-Reader” and analyze the various systems that follow this architecture as well as the specific techniques adopted in each of the components. We then discuss key challenges to developing OpenQA systems and offer an analysis of benchmarks that are commonly used. We hope our work would enable researchers to be informed of the recent advancement and also the open challenges in OpenQA research, so as to stimulate further progress in this field.

Index Terms—Textual Question Answering, Open Domain Question Answering, Machine Reading Comprehension, Information Retrieval, Natural Language Understanding, Information Extraction
- ODQA : 대규모 비정형 문서를 기반으로 질문에 자연어 형태로 답변을 하는 것이 목표인 task
- ODQA는 Machine Reading Comprehension(기계독해, MRC) 분야와 통합된 기술에 대한 연구가 급증
- 이 논문은 ODQA의 origin & development를 다루고, 최근 Retriever-Reader 구조의 ODQA에 대한 각 요소를 분석하고, 이후 ODQA의 과제 및 관련 벤치마크에 대해 분석하고, 마지막으로 추후 발전 방향에 대해 다룸

## 1. Introduction
Question Answering (QA) aims to provide precise answers in response to the user’s questions in natural language. It is a long-standing task dating back to the 1960s. Compared with a search engine, the QA system aims to present the final answer to a question directly instead of returning a list of relevant snippets or hyperlinks, thusoffering better user-friendliness and efficiency. Nowadays many web search engines like Google and Bing have been evolving towards higher intelligence by incorporating QA techniques into their search functionalities. Empowered with these techniques, search engines now have the ability to respond precisely to some types of questions such as
> Q:“When was Barack Obama born?”   
> A:“4 August 1961”.

- Question Answering(QA) : 자연어에서 유저에 질문에 대한 정확한 답변을 해주는 분야로 1960년도에 시작 됨.
- QA 시스템은 단순히 질문에 대한 링크 혹은 스니펫를 전달해주는 대신, 보다 유저에게 친밀하고 효율적으로 동작하기 위해 직접적인 답변을 전달해주는 것을 목표로 함
   **[snippet](https://improveyourank.com/%EC%8A%A4%EB%8B%88%ED%8E%ABsnippet%EC%9D%98-%EC%A2%85%EB%A5%98-%EC%9D%BC%EB%B0%98-%EB%A6%AC%EC%B9%98-%EC%B6%94%EC%B2%9C-%EC%8A%A4%EB%8B%88%ED%8E%AB/) : 작은 조각을 뜻하며, 질문에 대한 대답이 포함되어 있는 글.  구글에서 일반적인 스니펫의 구조는 URL, 제목, 세부설명으로 구성
- 최근 google이나 bing의 검색엔진은 QA기술과 검색 기술을 통합하므로써 higher intelligence를 가능케 했으며, 위와 같이 답변이 가능해짐

The whole QA  landscape  can  roughly  be  divided  intotwo  parts:  textual  QA  and  Knowledge  Base  (KB)-QA,  ac-cording to the type of information source where answers are derived from. Textual QA mines answers from unstructured text documents while KB-QA from a predefined structured KB that is often manually constructed. Textual QA is generally more scalable than the latter, since most of the unstruc-tured text resources it exploits to obtain answers are fairly common and easily accessible, such as Wikipedia, news articlesand science books, etc. Specifically, textual QA is studied under two task settings based on the availability of  contextual  information,  i.e.  Machine  Reading  Comprehension  (MRC)  and  Open-domain  QA  (OpenQA).  MRC,which originally took inspiration from language proficiency exams,  aims  to  enable  machines  to  read  and  comprehend specified context passage(s) for answering a given question. In  comparison,  OpenQA  tries  to  answer  a  given  question without any specified context. It usually requires the system to first search for the relevant documents as the context w.r.t. a given question from either a local document repository or the World Wide Web (WWW), and then generate the answer, as  illustrated  in  Fig.  1.  OpenQA  therefore  enjoys  a  wider scope of application and is more in line with real-world QA behavior of human beings while MRC can be considered as a step to OpenQA. In fact, building an OpenQA system that is capable of answering any input questions is deemed as the ultimate goal of QA research.
- QA system은 크게 두 가지로 구분 : textual QA vs Knowledge Base(KB) QA
  - textual QA : 비정형 문서로부터 정답을 출력하며, 일반적으로 구할 수 있는 문서의 형태이므로 KB-QA에 비해 확장성이 좋음.
  - KB-QA : 학습한 것을 바탕으로 정답 출력
- textual QA는 MRC와 Open-domain QA(OpenQA)의 두 task로 연구가 진행됨
  - MRC : 기계가 질문에 답하기 위해 주어진 지문을 읽고 이해할 수 있도록 하는 것이 목표
  - OpenQA : (반면) 지정된 문서가 없이, 질문에 관련된 문서를 검색 후 답변을 생성하는 것이 목표 ![image](https://user-images.githubusercontent.com/74341192/139671229-a74adff8-f807-4868-8648-cd1a0fa1474b.png)
- OpenQA는 실제 인간이 수행하는 것과 비슷한 방식이기에 다양한 어플리케이션에 적용이 가능하고, MRC는 OpenQA의 일부 step으로 간주할 수 있음
- 따라서, 어떠한 질문에 대해서라도 답변을 할 수 있는 OpenQA system을 만드는 것이 QA 연구의 최종 목표

In literature, OpenQA has been studied closely with research in Natural Language Processing (NLP), Information Retrieval  (IR),  and  Information  Extraction  (IE). Traditional OpenQA systems mostly follow a pipeline consisting  of  three  stages,  i.e. Question  Analysis,Document Retrieval and Answer Extraction. Given an inputquestion  in  natural  language, Question  Analysis aims  to reformulate the question to generate search queries for facil-itating subsequent Document Retrieval and classify the question to obtain its expected answer type(s) that would guide Answer Extraction. In theDocument Retrieval stage, the system  searches  for  question-relevant  documents  or  passages with  the  generated  search  queries,  usually  using  existing IR techniques like TF-IDF and BM25, or specific techniques developed  for  Web  search  engines  like  Google.com  and Bing.com. After that, in the Answer Extraction stage, the final answer is extracted from related documents received from the previous stage.
- OpenQA는 Natural Language Processing(NLP), Information Retrieval(IR), Information Extraction(IE)를 연구
- OpenQA는 3개의 stage로 구성 => QUestion Analysis, Document Retrieval, Answer Extraction
- 자연어 형태로 질문이 주어졌을 때 Question Anlaysis의 역할은 두 가지로,
  1. Document Retrieval이 가능하도록 query를 재구성(컴퓨터가 이해할 수 있도록 숫자 형태로 변경, vectorization)
  2. Answer Extraction의 guideline이 될 수 있는, Answer type을 분류하기 위해 Question을분류
- Document Retrieval stage
  - google이나 Bing과 같은 검색엔진같은 특정 기술, 혹은 TF-IDF나 BM25같은 IR 기술을 사용하여 question과 관련있는 Document 또는 passage를 확보
- Answer Extraction stage
  - Document Retrieval을 통해 추려진, 관련 문서들로부터 정답을 추출 

Deep  learning  techniques,  which  have  driven  remark-able  progress  in  many  fields,  have  also  been  successfullyapplied to almost every stage of OpenQA systems [12]. Forexample, [13] and [14] develop the question classifier usinga CNN-base model and an LSTM-based model respectively.In  [15],  [16],  [17],  they  propose  neural  retrieval  models  tosearch  for  relevant  documents  in  a  latent  space.  In  recentyears, with the emergence of some large-scale QA datasets[18],   [19],   [20],   [21],   [22],   [23],   neural   MRC   techniqueshave  been  greatly  advanced  [18],  [24],  [25],  [26],  [27].  Byadopting  the  popular  neural  MRC  methods  to  extract  theanswer to a given question from the relevant document(s),traditional OpenQA systems have been revolutionized [3],[28],  [29],  [30]  and  evolved  to  a  modern“Retriever-Reader”architecture.Retrieveris  responsible  for  retrieving  relevantdocuments w.r.t. a given question, which can be regarded asan IR system, whileReaderaims at inferring the final answerfrom  the  received  documents,  which  is  usually  a  neuralMRC  model.  A  handful  of  works  [3],  [31],  [32]  even  re-name OpenQA as Machine Reading Comprehension at Scale(MRS).  Following  this  architecture,  extensive  research  hasbeen made along various directions, such as re-ranking theretrieved documents before feeding them into a neural MRCmodel  [28],  [33],  [34],  retrieving  the  relevant  documentsiteratively given a question [29], [35], [36], and training theentire OpenQA system in an end-to-end manner [15], [30],[37], [38], etc.
- 많은 분야에서 괄목할 만한 발전을 이끈 딥러닝은 OpenQA의 거의 모든 단계에도 적용됨
  - e.g.)
  - CNN or LSTM-based model을 통한 question classification
  - neural retrieval model을 통한 latent space에서 관련 문서 탐색
- 즉, 전통적인 OpenQA system에서 딥러닝 기술이 적용되어 현재의 "Retriever-Reader"의 구조로 발전했으며, 이는 관련 문서로부터 주어진 질문에 대한 답변을 출력하기 위해 유명한 neural MRC 방법론들이 적용되었음.
- 여기서, IR system으로 간주되는 Retriever는 주어진 질문에 대해 관련있는 문서를 찾고, Reader는 전달받은 문서에서 최종 답변을 출력.
- 이러한 연구를 진행하며, OpenQA는 Machine Reading Comprehension at Scale(MRS)라고 불리게 됨.
- Retriever-Reader 구조애 대한 광범위한 연구가 이뤄짐
  1. 검색된 문서에 대해 re-ranking 후 neural MRC model에 전달
  2. 주어진 질문에 대해 반복적으로 관련 문서를 탐색
  3. end-to-end OpenQA system 학습

Based  on  above  observations  and  insights,  we  believe it  is  time  to  provide  a  comprehensive  literature  review  on OpenQA  systems,  with  particular  attention  to  techniques that  incorporate  neural  MRC  models.  Our  review  is  ex-pected to acknowledge the advancement that has been made thus far and summarize the current challenges to stimulate further progress in this field. In the rest of this survey, we will present the following contents. In Section 2, we reviewthe development of OpenQA systems, including the origin, traditional  architecture,  and  recent  progress  in  using  deepneural  networks.  In  Section  3,  we  summarize  and  elaborate a“Retriever-Reader” architecture for OpenQA followed by  detailed  analysis  on  the  various  techniques  adopted.In  Section  4,  we  first  discuss  some  salient  challenges  towards  OpenQA,  identifying  the  research  gaps  and  hoping to enhance further research in this field, and subsequently provide  a  summary  and  analysis  of  QA  benchmarks  that are applicable to either MRC or OpenQA. Finally, we draw our  conclusions  based  on  the  presented  contents  above  in Section 5.
- 앞서 소개한 내용과 같이, OpenQA system에 대해 이해하려면 neural MRC Model을 포함하여 다양한 기술들에 대해 공부해야 하는만큼 오랜 시간이 걸리지만, 이 paper에선 앞으로의 발전을 위해 이전까지의 기술들에 대해 요약한 내용을 다루고자 한다고 밝힘.
- 앞으로 논문에서 소개할 구성은 다음과 같음
  - Section 2: OpenQA system의 전통적인 구조 및 발전,  architecture, deep neural networks의 현 상황
  - Sectoin 3: OpenQA를 위한 Retriever-Reade 구조 설명 및 관련 기술 분석
  - Section 4: OpenQA의 현재 도전중인 과제 및 research gap 및 앞으로 발전하고자 한 방향 및 분석
  - Section 5: concoluesions!!

## 2. Development of OpenQA
In this section, we first briefly introduce the origin of Open-domain  Question  Answering  (OpenQA)  and  then  review the  traditional  and  deep  learning  approaches  to  OpenQA sequentially to describe its remarkable advancement in thepast two decades.
- introduction: Open-domain  Question  Answering  (OpenQA)의 기원
- review : 전통적인 OpenQA, 지난 20년간 deep learning approachs를 통한 OpenQA의 발전 과정

### 2.1 Origin of OpenQA
Pioneering  research  on  Question  Answering  (QA)  system was  conducted  within  the  scope  of  Information  Retrieval(IR), with the focus on restricted domain or closed-domain settings.  The  earliest  QA  system,  as  is  widely  acknowledged,  is  the  Baseball,  which  was  designed  in  1961  to answer questions about American baseball games, such asgame  time,  location  and  team  name.  Within  this  system, all  the  relevant  information  is  stored  in  a  well-defined dictionary,  and  user  questions  are  translated  into  query statements using linguistic methods to extract final answers from  the  dictionary.  In  1973,  another  famous  QA  systemLUNAR  was  developed  as  a  powerful  tool  to  assist research  work  of  lunar  geologists,  where  chemical  analysis  data  about  lunar  rocks  and  soil  obtained  from  Apollomoon  missions  are  stored  in  one  data  base  file  provided by NASA MSC for each scientist to conveniently view and analyze.  In  1993,  MURAX  was  designed  to  answer simple  academic  questions  based  on  an  English  academic encyclopedia which mainly employs linguistic analysis andsyntactic pattern matching techniques.
- 초기 QA system은 제한된 domain 내의 information retrieval 범위에서 연구가 진행
- 초기 QA system은 1961년 baseball과 관련된 질문에 응답해주기 위해 생겨났으며, 게임 시간이나, 장소, 팀명 등과 관련된 질문에 대한 답변해주는 역할로 활용.
  - well-defined된 dictionary를 토대로, 사용자의 question을 linguistic methods를 활용하여 query statements에 맞게 번역 후 알맞은 답변을 dictionary로부터 출력해주는 형태
- 또 다른 유명한 QA system은 1973년 NASA에서 사용한 LUNAR라는 system으로, 아폴로 문 임무에서 얻은 달의 암석과 토양에 대한 화학 데이터를 과학자들이 편리하게 분석하기 위한 연구 보조 도구로 사용됨.
- 1993년에는 개발된 MURAX라는 QA system은 언어 분석과 문법 패턴 매칭 기술을 주로 사용하는 영어 백과사전을 기반으로 간단한 학문적 질문에 대한 답변을 해주는 도구로 사용.

In  1999,  OpenQA  was  first  defined  as  extracting  top5  probable  snippets  containing  the  correct  answer  from  acollection  of  news  articles  in  the  QA  track  launched  by the Text REtrieval Conference (TREC). Compared to the previous  research  on  QA,  in  the  open-domain  setting,  alarge  number  of  unstructured  documents  is  used  as  the information source from which the correct answer to a given question would be extracted. In the later years, a series ofTREC  QA  Tracks  have  remarkably  advanced  the  research progress on OpenQA. It is worth noting that systems are required to return exact short answers to given questions starting from TREC-11 held in 2002.
- 1999년 Text REtrieval Conference (TREC)에서 처음으로 정답이 있는 문서를 포함된, 확률이 높은 5개의 문서를 가져오는 openQA system이 공개됨
- 이전 연구와 비교하여, 오픈 도메인 환경에서 주어진 질문에 대한 정답을 추출할 수 있는 정보 출처로 대용량의 비정형 문서가 사용되며, 이 연구를 통해 연구가 급격히 진전됨
- 2011년 개최된 TREC-11에서, 주어진 질문에 대해 정확하고도 짧은 답변을 반환하기 위한 system에 주목하기 시작함.

The TREC campaign provides a local collection of doc-uments  as  the  information  source  for  generating  answers, but the popularity of World Wide Web (WWW), especially the  increasing  maturity  of  search  engines,  has  inspired  re-searchers  to  build  Web-based  OpenQA  systems  obtaining  answers  from  online  resources  like Google.com and Ask.com, using IR techniques. Web search engines are able to consistently and efficiently collect massive web pages, therefore capable of providing much more information to help find answers in response to user questions.  In  2001,  a  QA  system  called  MULDER  was  de-signed to automatically answer open-domain factoid questions with a search engine (e.g., Google.com). It first translates users’ questions to multiple search queries with several natural-language parsers and submits them to the search engine to search for relevant documents, and then employs ananswer extraction component to extract the answer from the returned results. Following this pipeline, a well-known QA system AskMSR was developed, which mainly dependson  data  redundancy  rather  than  sophisticated  linguistic analysis  of  either  questions  or  candidate  answers.  It  first translates  the  user’s  question  into  queries  relying  on  a  set of predefined re writing rules to gather relevant documents from  search  engines  and  then  adopts  a  series  of  n-gram based algorithms to mine, filter and select the best answer. For  such  OpenQA  systems,  the  search  engines  are  able to  provide  access  to  an  ocean  of  information,  significantly enlarging the possibility of finding precise answers to user questions. Nevertheless, such an ample information source also  brings  considerable  noisy  content  that  challenges  theQA system to filter out.
- TREC campaign은 답변 생성을 위해 정보 소스로 활용할 local collection of documents를 제공했지만, google.com이나 ask.com과 같은 웹의 검색엔진에 대한 활용이 증가함에 따라 IR 기술을 활용해 web-based OpenQA system을 구축하는 것을 고무함.
- 웹 검색 엔진은 일관적이면서도 효율적으로 웹 페이지를 수집할 수 있기에, 질문에 대한 답변을 찾는데 더 많고 도움이 되는 정보 제공이 가능.
- 2001년 MULDER라고 불리는 QA system이 질문이 들어오면 오픈 도메인에서 자동으로 답변을 제공해주는 검색엔진이 design됨
  - 과정은 다음과 같음: 유저 질문을 여러 개의 검색 query로 번역 => 검색엔진을 통해 관련 문서 검색 => 검색 문서들로부터 정답을 추출
- 이 검색 과정은 QA system AskMSR으로 정교한 언어 분석보단 데이터 중복성에 의존
  - 유저 질문에 대해 재작성 규칙에 의거하여 query로 변환하여 관련 문서를 검색하고, 일련의 n-gram 기반의 알고리즘을 통해 filtering하여 정답 추출
- 이러한 OpenQA system은 광범위한 정보에 대한 접근이 가능하여 질문에 대해 높은 가능성의 답을 출력할 순 있지만, 많은 noise도 발생함.

### 2.2 raditional Architecture of OpenQA

The  traditional  architecture  of  OpenQA  systems  is  illustrated in Fig. 2, which mainly comprises three stages:Ques-tion Analysis,Document Retrieval, and Answer Extraction.  Given  a  natural  language  question, Question Analysisaims to understand the question first so as to facilitate document retrieval and answer extraction in the following stages. Performance of this stage is found to have a noticeable infl-ence upon that of the following stages, and hence important to  the  final  output  of  the  system.  Then, Document  Retrieval stage searches for question-relevant documents based on a self-built IR system or Web search engine using the search queries generated by Question Analysis. Finally, Answer Extraction is responsible for extracting finalanswers to user questions from the relevant documentsreceived  in  the  preceding  step.  In  the  following,  we  willanalyze each stage one by one.
- 전통적인 OpenQA system의 구조는 그림과 같이 3개의 stages로 구성됨. => Question Analysis, Document Retrieval, Answer Extraction
- Question Analysis : 이후 문서 검색 및 답변 추출을 용이하도록 자연어로 된 질문을 이해하는 것이 목표
  - 이 단계의 성능은 다음 단계에 상당한 영향을 미치므로, 최종 출력에도 매우 중요
- Document Retrieval : Question Analysis에서 생성된 검색 쿼리를 기반으로, 웹 검색 엔진이나 자체구축은 IR system을 이용하여 질문과 관련된 문서를 검색 
- Answer Extraction : 선별된 문서들로부터 유저 질문에 적합한 답변 출력

![image](https://user-images.githubusercontent.com/74341192/139720402-a8b302b7-d4e4-4c1c-9062-76d170079e72.png)


#### 2.2.1 Question Analysis
The  goals  of Question  Analysis stage are two-fold. On one hand, it aims to facilitate the retrieval of question-relevant documents, for which a Query Formulation module is often adopted to generate search queries. On the other hand, it is expected  to  enhance  the  performance  of Answer  Extraction stage  by  employing  a  Question  Classification  module  to predict the type of the given question, which leads to a set of expected answer types. A simple illustration of this stageis given in the left most grey box of Fig. 2.
- Question Analysis은 두 가지 역할을 수행
  1. Document Retrieval stage에서 관련 문서 검색을 용이하도록 유저의 질문을 정해진 query formatulation으로 검색 쿼리를 생성
  2. Answer Extraction stage에서 질문 분류 모듈을 사용하여 주어진 질문 유형의 토픽을 예측하여 예상 답변 유형 set으로 유도시킴으로써 출력 성능 개선

In Query Formulation, linguistic techniques such as POS tagging [40], [44], stemming [40], parsing [44] and stopword removal [45], [48] are  usually  utilized  to  extract  keywords for  retrieving.  However,  the  terms  used  in  questions  are often  not  the  same  as  those  appearing  in  the  documentsthat  contain  the  correct  answers.  This  problem  is  called “term  mismatch”  and  is  a  long-standing  and  critical  issuein  IR.  To  address  this  problem,  query  expansion  [49],  [50]and  paraphrasing  techniques  [51],  [52],  [53],  [54]  are  oftenemployed to produce additional search words or phrases soas to retrieve more relevant documents.
- Query Formulation은 POS tagging, stemming(어간추출), parsing, stopword removal과 같은 언어 기법들은 일반적으로 검색어 추출 시 사용됨
- 단, 질문에 사용된 단어는 문서에서 쓰이지 않은 단어가 사용될 경우가 있는데, 이를 "term mismatch"라고 하며 일반적으로 IR에서 장기간 지속된 중요한 이슈 중 하나.
- 해결 방안으로, 쿼리 확장이나 페러프레이징 기법을 활용하여 검색 단어를 추가적으로 공급해주거나 변환하여 보다 관련 문서를 용이하게 검색하도록 함

Question  Classification,  the  other  module  that  is  often adopted for Question Analysis stage, aims to identify the type of the given question based on a set of question types (e.g.,where, when, who, what) or a taxonomy [55], [56] manually defined  by  linguistic  experts.  After  obtaining  the  type  ofthe  question,  expected  answer  types  can  be  easily  determined using rule-based mapping methods [9]. For example, given  a  question “When  was  Barack  Obama  born?”,  the answer type would be inferred as “Date” when knowing the question type is “When”. Identifying the question type can provide constraint upon answer extraction and significantly reduce  the  difficulty  of  finding  correct  answers.  Question Classification has attracted much interest in literature [44],[55],  [57],  [58],  [59].  For  instance,  [59]  proposed  to  extract relevant words from a given question and then classify the question based on rules associating these words to concepts;[57]  trained  a  list  of  question  classifiers  using  various  machine learning techniques such as Support Vector Machines(SVM), Nearest Neighbors and Decision Trees on top of thehierarchical taxonomy proposed by [55].
- Question Analysis stage의 또 다른 역할인 Question Classification은 문제 유형 셋(where,who,what 등)이나 언어 전문가가 정의한 분류법을 기반으로 주어진 문제의 유형을 식별하는 것이 목표
- 질문의 타입을 정한 이후엔 룰기반 매핑 방법을 활용하여 정답 타입을 쉽게 예측할 수 있음 => 문제 유형을 식별 시, 답을 추출할 때 제약이 생겨 정답을 찾는데 어려움을 줄일 수 있음(SVM, KNN, Decision Tree 등을 활용)
  - e.g.) question: “When  was  Barack  Obama  born?” => question type : "when" => expected answer type : "Date"

#### 2.2.2 Document Retrieval
This stage is aimed at obtaining a small number of relevant documents  that  probably  contain  the  correct  answer  to  agiven question from a collection of unstructured documents, which  usually  relies  on  an  IR  engine.  It  can  significantly reduce the search space for arriving at the final answer.
- 비정형 문서들로부터 정확한 정답을 포함할 것 같은 문서들을 확률적으로 선택하는 것이 목표

In the past decades, various retrieval models have been developed for Document Retrieval, among which some popular  ones  are  the  Boolean  model,  Vector  Space  Models, Probabilistic Models, Language Models [60], etc., which ar ebriefly revisited as follows.
- 지난 수십년동안 문서 검색을 위해 다양한 모델들이 개발되었으며, 그 중 유명한 모델들로는, boolean model, Vector Space Model, Probabilistic Model, Langage Model 등이 있음

> Boolean  Model:  The  Boolean  Model  is  one  of  the  simplest retrieval models. The question is transformed into the  form  of  a  Boolean  expression  of  terms,  which  are combined  with  the  operators  like  ”AND”,  ”OR”  and ”NOT” to exactly match with the documents, with each document viewed as a set of words.
- 가장 단순한 문서 검색 모델 중 하나로, 질문을 ans나 or과 같은 연산자와 결함된  boolean 표현의 terms으로 변환하고 단어 집합으로 보는 문서와 매칭시킴

> Vector Space Model: The Vector Space Models represent the  question  and  each  document  as  word  vectors  in a d-dimensional  word  space,  where d is  the  number of  words  in  the  vocabulary.  When  searching  for  relevant  documents  to  a  given  question,  the  relevance score  of  each  document  is  computed  by  computing the  similarity  (e.g.,  the  cosine  similarity)  or  distance(e.g., the euclidean distance) between its vector and the question vector. Compared to the Boolean model, this approach returns documents to the question even if the constraints posed by the question are only partially met, with precision sacrificed.
- 각 질문과 문서를 vocab 개수의 차원을 크기로 가지는 vector로 변환
- 관련 문서를 검색 시, 질문과 각 문서 사이의 유사도 혹은 거리를 계산
- boolean과 비교하여, 이 접근법은 부분적으로 충족하더라도 문서를 반환

> Probabilistic  Model:  The  Probabilistic  Models  provide  away  of  integrating  probabilistic  relationships  between words  into  a  model.  Okapi  BM25  [61]  is  a  probabilistic  model  sensitive  to  term  frequency  and  document length, which is one of the most empirically successful retrieval  models  and  widely  used  in  current  searchengines.
- 확률 모델은 단어간 확률적 관계를 통합하는 것을 배제
- Okapi BM25는 확률 모델 중 하나로, 특정 용어의 빈도수와 문서 길이를 활용하여 문서와 질문 간의 관계를 따짐. 경험적으로 가장 성공적인 검색 모델 중 하나로 현재까지도 검색 엔진에 사용됨

> Language  Model:  The  Language  Models  [62]  are  also very   popular,   among   which   the   Query   LikelihoodModel  [60]  is  the  most  widely  adopted.  It  builds  a probabilistic language model LM_d for each document d and ranks documents  according  to  the  probabilityP(q|LM_d)of the language model generating the given question q.
- 언어모델도 자주 사용되는 모델 중 하나로, 그 중 쿼리 우도 모델이 가장 많이 사용됨
- 질문을 생성해내기 위한 확률을 토대로 rank를 지정하여 문서를 반환

In practice, the documents received often contain irrelevant ones, or the number of documents is so large that the capacity of the Answer Extraction model is overwhelmed. To address  the  above  issues,  post-processing  on  the  retrieved documents is very demanded. Widely used approaches on processing retrieved documents include document filtering, document re-ranking and document selection [9], etc. Document  filtering  is  used  to  identify  and  remove  the  noise w.r.t. a given question; document re-ranking is developed to further sort the documents according to a plausibility degree of  containing  the  correct  answer  in  the  descending  order; document selection is to choose the top relevant documents. After  post-processing,  only  the  most  relevant  documents would be remained and fed to the next stage to extract the final answer.
- 실제론 전달된 문서가 자체가 부적절하거나 문서 수가 너무 많아 OOM이 발생되는 경우도 종종 있기에, 이러한 문제를 해결하기 위한 방법으로 검색 문서에 대한 post-processing이 요구됨
- 검색 문서에 대한 post-processing은 문서 filtering, 문서 re-ranking, 문서 selection의 방법이 있음.
  - document filtering : 주어진 질문의 노이즈를 식별하고 제거하는데 사용
  - document re-ranking : retrieved된 문서가 정확한 answer를 가지는 타당한 정도에 따라 문서의 ranking을 다시 매기고자 할 때 사용
  - document selection : 가장 적절한 documents 하나를 선택
- post-processing 이후엔 가장 적절한 문서를 정답 추출을 위해 Answer Extraction stage로 넘김


#### 2.2.3 Answer Extraction
The ultimate goal of an OpenQA system is to successfully answer  given  questions,  and Answer  Extraction stage  is responsible  for  returning  a  user  the  most  precise  answer to a question. The performance of this stage is decided by the complexity of the question, the expected answer types from Question Analysis stage, the retrieved documents from Document  Retrieval stage  as  well  as  the  extraction  method adopted,  etc.  With  so  many  influential  factors,  researchers need to take a lot of care and place special importance on this stage.
- OpenQA system의 목표는 주어진 질문에 정확한 답변을 해주는 것으로, Extraction stage에선 유저에게 정답을 전달해주는 역할을 수행
- Extraction Stage의 성능은 extraction 방법론 뿐만 아니라, Question analysis stage에서 넘어온 expected answer types도 영향을 미침.

In  traditional  OpenQA  systems,  factoid  questions  and list questions have been widely studied for a long time. Factoid questions (e.g., When, Where, Who...) to which the answers are usually a single text span in in the documents, such  as  such  as  an  entity  name,  a  word  token  or  a  noun phrase.  While  list  questions  whose  answers  are  a  set  of factoids that appeared in the same document or aggregated from  different  documents.  The  answer  type  received  from the stage of Question Analysis plays a crucial role, especially for  the  given  question  whose  answers  are  named  entities. Thus,  early  systems  heavily  rely  on  the  Named  Entity Recognition (NER) technique since comparing the recognised entities and the answer type may easily yield the final answer. In [65], the answer extraction is describedas a unified process, first uncovering latent or hidden infor-mation from the question and the answer respectively, andthen using some matching methods to detect answers, suchas surface text pattern matching [66], [67], word or phrasematching  [44],  and  syntactic  structure  matching  [40],  [48],[68].
- traditional OpenQA system은 factoid questions과 list questions에 대해 오랫동안 연구가 되어 왔음.
  - factoid questions : when, where, who와 같은 형태의 질문으로, 정답이 일정 text span(entity name, word token, noun phrase)
  - list question : 한 문서 혹은 여러 문서를 통합하여 얻는 set of factoids 형태의 answers.
- question analysis stage에서 전달받은 answer type은 특히 답이 entity로 명명된 질문에 대해 중요한 역할을 수행
- 따라서, 초기 QA system은 인식된 entity와 answer type을 비교하여 쉽게 최종 정답을 산출하기에 NER 기법에 크게 의존했음.
- 정답 추출은 통일된 프로세스로 설명되며, 우선 질문과 답변의 숨겨진 정보를 탐지하고, 매칭 기법(문법 구조, 텍스트 패턴, 단어나 구)을 통해 정답을 찾아냄.

In practice, sometimes the extracted answer needs to be validated when it is not confident enough before presenting to the end-users. Moreover, in some cases multiple answer candidates  may  be  produced  to  a  question  and  we  have to select one among them. Answer validation is applied to solve  such  issues.  One  widely  applied  validation  method is  to  adopt  an  extra  information  source  like  a  Web  search engine to validate the confidence of each candidate answer. The principle is that the system should return a sufficiently large  number  of  documents  which  contain  both  question and answer terms. The larger the number of such returned documents is, the more likely it will be the correct answer. This  principle  has  been  investigated  and  demonstratedfairly effective, though simple [9].
- 실제론, 실제 유저에게 전달하기 전 추출된 답변에 충분히 확신을 가지지 못할 때 검증을 해야 할 경우가 발생
- 특히, 하나의 질문에 대해 여러 개의 answer 후보군이 생성된 경우, 그 중 하나를 선태갷야 함.
- 널리 쓰이는 validation method 중 하나는, 답변 후보군 각각을 검증하기 위해 웹 검색 엔진과 같은 추가적인 정보 소스를 활용하는 것.
- 단, 추가적인 정보 소스는 질문과 답변의 용어를 포함한 문서를 많이 반환해야 하는 것이 원칙이며, 그 양이 많아질수록 정답일 가능성이 높음.

### 2.3 Application of Deep Neural Networks in OpenQA
In  the  recent  decade,  deep  learning  techniques  have  also been  successfully  applied  to  OpenQA.  In  particular,  deep learning has been used in almost every stage in an OpenQA system,  and  moreover,  it  enables  OpenQA  systems  to  be end-to-end  trainable.  For Question  Analysis,  some  works develop neural classifiers to determine the question types. For example, [13] and [14] respectively adopt a CNN-based and an LSTM-based model to classify the given questions, both achieving competitive results. For Document Retrieval, dense  representation  based  methods  [16],  [29],  [30],  [35] have  been  proposed  to  address  “term-mismatch”,  which is  a  long-standing  problem  that  harms  retrieval  performance.  Unlike  the  traditional  methods  such  as  TF-IDF and  BM25  that  use  sparse  representations,  deep  retrieval methods  learn  to  encode  questions  and  documents  into a  latent  vector  space  where  text  semantics  beyond  term match  can  be  measured.  For  example,  [29]  and  [35]  train their own encoders to encode each document and question independently  into  dense  vectors,  and  the  similarity  score between  them  is  computed  using  the  inner  product  of their vectors. The Sublinear Maximum Inner Product Search(MIPS)  algorithm  [69],  [70],  [71]  is  used  to  improve  the retrieval  efficiency  given  a  question,  especially  when  the document  repository  is  large-scale.  For Answer  Extraction, as  a  decisive  stage  for  OpenQA  systems  to  arrive  at  the final answer, neural models can also be applied. Extracting answers from some relevant documents to a given question essentially makes the task of Machine Reading Comprehension  (MRC).  In  the  past  few  years,  with  the  emergence  of some large-scale datasets such as CNN/Daily Mail [18], MSMARCO [20], RACE [21] and SQuAD 2.0 [22], research on neural  MRC  has  achieved  remarkable  progress  [24],  [25],[26],  [27].  For  example,  BiDAF  [24]  represents  the  given document at different levels of granularity via a multi-stage hierarchical  structure  consisting  of  a  character  embedding layer, a word embedding layer, and a contextual embedding layer,  and  leverages  a  bidirectional  attention  flow  mechanism  to  obtain  a  question-aware  document  representation without early summarization. QANet [26] adopts CNN and the  self-attention  mechanism  [72]  to  model  the  local  inter-actions and global interactions respectively, which performs significantly faster than usual recurrent models.
- 지난 10년간, 딥러닝 기술은 OpenQA의 모든 stage에 적용되었으며, 이로 인해 end-to-end로 학습이 가능해짐.
  - Question Analysis : CNN이나 LSTM과 같은 구조를 기반으로 한 모델을 사용하여 question type을 분류
  - Document Retrieval : dense representation based methods를 활용하여 term-mismatch를 해결(term-mismatch는 retrieval 성능에 악영향을 미쳤던 요소)
- sparse represeiontation을 사용한 기존 방법(TF-IDF, BM25)과 달리, 신경망 retrieval 기법은 단순히 term-match를 넘어 의미적으로 평가를 할 수 있도록 questions과 documents를 latent vector space로 인코딩을 함.
  - question과 documents 각각의 encoder를 개별적으로 학습시킨 후 question과 document의 내적을 통해 유사도를 평가.
  - 그 중 Maximum Inner Product Search(MIPS) 알고리즘은 특히 대용량의 문서군을 다룰 때, 주어진 retirever 효율을 개선하는데 사용됨.
  - e.g.) Extraction answers : OpenQA의 decisive stage로 neural model도 수행 가능하며, 주어진 일부 문서에서 답을 추출하는 것은 MRC task
- 지난 몇 년간 CNN/Daily Mail, RACE, SQuAD와 같은 대용량 데이터셋이 등장함에 따라 MRC의 눈부신 발전이 도모됨.
  - e.g.) BiDAF는 1) character embedding layer, 2) word embedding layer, 3) contextual embedding layer로 구성된 계층적 구조를 통하여 다양한 수준의 세분화를 진행했고,
          요약 없이 양방향 어텐션을 통해 질문에 알맞는 문서의 representation을 생성


Furthermore,  applying  deep  learning  enables  the OpenQA systems to be end-to-end trainable [15], [30], [37]. For  example,  [37]  argue  it  is  sub-optimal  to  incorporate a  standalone  IR  system  in  an  OpenQA  system,  and  they develop an ORQA system that treats the document retrieval from the information source as a latent variable and trains the  whole  system  only  from  question-answer  string  pairsbased on BERT [27]. REALM [30] is a pre-trained language model that contains a knowledge retriever and a knowledge augmented encoder. Both its retriever and encoder are differentiable neural networks, which are able to compute the gradient w.r.t. the model parameters to be back propagated all the way throughout the network. Similar to other pretraining language models, it also has two stages, i.e., pretraining and fine-tuning. In the pre-training stage, the model is trained in an unsupervised manner, using masked language modeling as the learning signal while the parameters are fine-tuned using supervised examples in the fine-tuning stage.
- 앞서 언급했듯이, 딥러닝의 적용을 통해 OpenQA system에 end-to-end 학습이 가능해짐.
- e.g.) latent retrival 관련 논문에 의하면, OpenQA system에 독립적인 IR system을 구축하는 건 차선책이라 주장하고,
        BERT를 기반으로 question-answer 쌍에서만 reader와 retriever를 동시에 학습하는 ORQA를 개발
- e.g.) REALM은 knowledge retriever and a knowledge augmented encoder으로 구성된 pretrained 언어모델로, retriever와 encoder는 다른 신경 네크워크임. 또한 REALM은 다른 pretrained model과 같이 두 stage(pretrain, finetune)로 진행됨   
****Retrieval-augmented language model(REALM)

In  early  OpenQA  systems,  the  success  of  answering  a question is highly dependent on the performance of Question Analysis, particularly Question Classification, that provides expected answer types [47]. However, either the types or the taxonomies of questions are hand-crafted by linguists, which  are  non-optimal  since  it  is  impossible  to  cover  all question types in reality, especially those complicated ones. Furthermore,  the  classification  errors  would  easily  result in  the  failure  of  answer  extraction,  thus  severely  hurting the  overall  performance  of  the  system.  According  to  the experiments in [47], about 36.4% of errors in early OpenQA systems are caused by miss-classification of question types. Neural  models  are  able  to  automatically  transform  questions from natural language to representations that are more recognisable  to  machines.  Moreover,  neural  MRC  models provide an unprecedented powerful solution to Answer Ex-tractionin OpenQA, largely offsetting the necessity of applying the traditional linguistic analytic techniques to questions and bringing revolutions to OpenQA systems [3], [28], [29],[37]. The very first work to incorporate neural MRC models into the OpenQA system is DrQA proposed by [3], evolving to  a  “Retriever-Reader”  architecture.  It  combines  TF-IDF based  IR  technique  and  a  neural  MRC  model  to  answer open-domain factoid questions over Wikipedia and achieves impressive performance. After [3], lots of works have been released [28], [30], [33], [34], [37], [73], [74], [75]. Nowadays, to build OpenQA systems following the “Retriever-Reader” architecture  has  been  widely  acknowledged  as  the  most efficient  and  promising  way,  which  is  also  the  main  focus of this paper.
- 초기 OpenQA system은 질의응답의 성공은 Question Analysis, 특히 question classification 성능에 의존적이었지만, answer type이나 언어학적으로 직접 손으로 분류하는건 비최적화된 방법으로 현실적으로 모든 question type을 지정하는건 불가하며, 붙일 수 없는 더 복잡한 것들도 많이 다룸.
- 또한, classification error로 인해 잘못된 answer extraction이 진행될 수 있으므로 전반적인 성능 저하를 유발함.
- 한 연구에 의하면 초기 OpenQA system의 36.4%의 error가 miss-classification이라고 함.
- 반면, 신경망 모델은 자연어 질문을 기계가 보다 인식하기 쉽도록 번역을 해줌.
- 특히 신경망 MRC 모델은 전례가 없던 뛰어난 솔루션을 제공하여 전통적인 언어 분석 방식 대체
- TF-IDF based IR 기술과 neural MRC 모델을 조합하여 open-domain factoid questions에 대한 답변을 하는 경우는 뛰어난 성능 개선을 확인.
- 따라서 최근 OpenQA는 Retirever-Reader 구조를 사용


## 3. Modern OpenQA : Retrieving And Reading
In this section, we introduce the “Retriever-Reader” architecture of the OpenQA system, as illustrated in Fig. 3. Retriever is  aimed  at  retrieving  relevant  documents  w.r.t.  a  given question,  which  can  be  regarded  as  an  IR  system,  while Reader aims at inferring the final answer from the received documents,  which  is  usually  a  neural  MRC  model.  They are two major components of a modern OpenQA system. In addition, some other auxiliary modules, which are marked in  dash  lines  in  Fig.  3,  can  also  be  incorporated  into  an OpenQA  system,  including Document  Post-processing that filters  and  re-ranks  retrieved  documents  in  a  fine-grained manner  to  select  the  most  relevant  ones,  andAnswer  Post-processingthat  is  to  determine  the  final  answer  amongmultiple  answer  candidates.  The  systems  following  thisarchitecture  can  be  classified  into  two  groups,  i.e.pipelinesystemsandend-to-end  systems.  In  the  following,  we  willintroduce  each  component  with  the  respective  approachesin  the  pipeline  systems,  then  followed  by  the  end-to-endtrainable  ones.  In  Fig.  4  we  provide  a  taxonomy  of  themodern  OpenQA  system  to  make  our  descriptions  betterunderstandable.
- ch3에선 Retriever-Reader 구조에 대해 다룰 예정
  - two major compnents of a modern OpenQA system : Retriever, Reader(usually using a neral MRC Model)
  - additional components : Document Post-processing(filters and re-ranks retrieved documents), Answer Post-processing(determine the final answer among multiple answer candidates)
  - OpenQA 구조는 두 개의 그룹으로 분류(pipeline systems, end-to-end systems), 3강에선 pipeline systems에 대해 다룰 예정

![image](https://user-images.githubusercontent.com/74341192/139782388-8c289603-0362-4018-96cc-850c2fb75524.png)

![image](https://user-images.githubusercontent.com/74341192/139788415-0318b705-4114-44c6-83ec-fd2e94691c34.png)

### 3.1  Retriever
Retriever is usually regarded as an IR system, with the goal of  retrieving  related  documents  or  passages  that  probably contain  the  correct  answer  given  a  natural  language  question as well as ranking them in a descending order according to  their  relevancy.  Broadly,  current  approaches  to Retriever can  be  classified  into  three  categories,  i.e.Sparse  Retriever,Dense Retriever, andIterative Retriever, which will be detailedin the following.
- Retriever는 종종 IR system으로 간주되며, 자연어로 된 질문에 대해 정확한 답변이 포함된 관련 문서나 지문을 검색하고 관련성에 따라 내림차순으로 순위를 매기는 것이 목표
- Retriever는 세 개의 category로 구분 => Sparse Retriever, Dense Retriever, Iterative Retriever

### 3.1.1 Sparse Retriever
It  refers  to  the  systems  that  search  for  the  relevant  documents  by  adopting  classical  IR  methods  as  introduced in  Section  2.2.2,  such  as  TF-IDF  [3],  [34],  [76],  [77]  and BM25  [78],  [79].  DrQA  [3]  is  the  very  first  approach  tomodern  OpenQA  systems  and  developed  by  combiningclassical IR techniques and neural MRC models to answeropen-domain  factoid  questions.  Particularly,  the  retriever in  DrQA  adopts  bi-gram  hashing  [80]  and  TF-IDF  matching  to  search  over  Wikipedia,  given  a  natural  language question.  BERTserini  [78]  employs  Anserini  [81]  as  its  retriever, which is an opensource IR toolkit based on Lucene.In  [78],  different  granularities  of  text  including  document-level,  paragraph-level  and  sentence-level  are  investigated experimentally, and the results show paragraph-level index achieves the best performance. Traditional retrieval methods such as TF-IDF and BM25 use sparse representations to measure term match. However, the terms used in user questions are often not the same as those appearing in the documents. Various methods based on dense representations [16], [29],[30], [35] have been developed in recent years, which learn to  encode  questions  and  documents  into  a  latent  vector space  where  text  semantics  beyond  term  match  can  be measured.
- Sparse Retriever는 section 2.2.2에서 언급한 TF-IDF나 BM25와 알고리즘을 적용하여 관련된 문서를 찾는 system
- DrQA는 Modern OpenQA system의 초기 방법으로, open domain의 factoid questions에 대한 질문을 생성하는 neural MRC Model과 기존 IR 기술이 결합된 시스템으로 발전됨.
- DrQA의 Retriever는 주어진 자연어 형태의 질문에 대해 bigram hashing과 TF-IDF matching 방법론을 통해 Wikipedia를 탐색
- BertSerini는 Lucene 기반의 오픈소스 IR 툴킷인 Anserini를 retriver로 사용
- BertSerini를 활용하여 여러 세분화된 텍스트(document-level, paragraph-level, sentence-level로)로 end-to-end OpenQA를 수행 시 paragraph-level이 가장 최고의 성능을 보임을 확인.
- TF-IDF 및 BM25와 같은 전통적인 retrival 방법론은 term match를 측정하여 sparse representations 생성했지만, 실제론 질문에 사용된 용어와 문서에 표시된 용어가 다른 형태일 수도 있음. 따라서 다양한 Dense 기반의 방법론들이 연구되고 있으며, 질문과 문서를 laten vector space에 투영시켜 질문과 문서 사이의 유사도를 측정. 이를 통해 term mis-match 해결
****DrQA : Domain Retriever Question Answering

### 3.1.2 Dense Retriever
Along  with  the  success  of  deep  learning  that  offers  remarkable  semantic  representation,  various  deep  retrieval models have been developed in the past few years, greatly enhancing  retrieval  effectiveness  and  thus  lifting  final  QA performance.  According  to  the  different  ways  of  encoding the  question  and  document  as  well  as  of  scoring  their similarity, dense retrievers in existing OpenQA systems can be  roughly  divided  into  three  types: Representation-based Retriever[16], [30], [37], [73],Interaction-based Retriever[15],[32], and Representation-interaction Retriever[17], [82], [83], asillustrated in Fig 5.
- deep retrieval model은 다음과 같이 세 타입이 존재함   
  => Representation-based Retriever, Interaction-based Retriever, Representation-interaction Retriever

![image](https://user-images.githubusercontent.com/74341192/139788528-8e775f4a-40f8-46d0-bbc6-3c04642d7599.png)

#### 3.1.2.1 Representation-based Retriever
Representation-based Retriever, also called Dual-encoder or Two-tower retriever, employs two independent encoders like BERT [27] to encode the question and the document respectively, and estimates their  relevance  by  computing  a  single  similarity  score  between two representations. For example, ORQA [37] adopts two  independent  BERT-based  encoders  to  encode  a  question  and  a  document  respectively  and  the  relevance  score between them is computed by the inner product of their vectors. In order to obtain a sufficiently powerful retriever, they pre-train the retriever using Inverse Cloze Task (ICT), i.e., topredict its context given a sentence. DPR [16] also employs two  independent  BERT  encoders  like  ORQA  but  denies the necessity of the expensive pre-training stage. Instead, it focuses on learning a strong retriever using pairwise questions and answers sorely. DPR carefully designs the ways to select negative samples to a question, including any random documents  from  the  corpus,  top  documents  returned  by BM25 that do not contain the correct answer, and in-batch negatives which are the gold documents paired with otherquestions in the same batch. It is worth mentioning that their experiments show the inner product function is optimal for calculating the similarity score for a dual-encoder retriever. Representation-based  method  [16],  [16],  [30],  [37]  can  be very fast since the representations of documents can be computed and indexed offline in advance. But it may sacrifice the retrieval effectiveness because the representations of the question and document are obtained independently, leading to only shallow interactions captured between them.

- Dual-encoder 혹은 Two-tower retriever라 불리는 Representation-based Retriever는 question과 document를 인코딩하기 위해 BERT와 같은 독립적인 두 개의 encoder를 사용하고, 두 representations에 대한 유사도를 측정하여 관련성을 평가함.
- e.g.) ORQA : 2개의 bert-based encoder를 통해 출력된 question과 context representation vector를 내적하여 score를 생성. 단 주어진 문장에 대한 context를 예측하기 위해Inverse Cloze Task(ICT)를 활용하여 retriever를 pretrain 시킴.
- e.g.) Dense Passage Retriever(DPR) : DPR 역시 두 개의 독립적인 BERT기반의 encoder를 사용. 다만 값비싼 pretraining 대신, pairwise된 questions와 answers로 고성능 retriver를 학습시키는 것에 초점을 맞춤
  -  이 때, DPR은 negative samples, 즉 정답을 포함하지 않은 임의의 문서와 정답을 쌍으로도 생성하여 학습하는데, 랜덤하게 생성하는게 아니라, BM25가 반환한 상위 문서 및 동일 배치의 다른 문서를 선택하는 등 negative sampling을 신중하게 진행함. 따라서 dual-encoder retriver의 유사성을 검증하는데 최적.
  -  다만, Representation-based Retriever는 문서 표현을 오프라인으로 미리 작업할 수 있어서 매우 빠르지만, 질문과 문서 표현이 독립적으로 얻어지기에 둘 사이에 얕은 상호작용을 초래할 수 있음.

#### 3.1.2.2 Interaction-based Retriever
Such  a  kind  of  retrievers take a question together with a document at the same time as input, and are powerful by usually modeling the token-level interactions between them, such as transformer-based encoder  [27],  [72].  [15]  propose  to  jointly  train Retriever and Reader using supervised multi-task learning [24]. Based on  BiDAF  [24],  a  retrieval  layer  is  added  to  compute  the relevance  score  between  question  and  document  while  a comprehension  layer  is  adopted  to  predict  the  start  and end  position  of  the  answer  span  in  [15].  [32]  develop  a paragraph-level dense Retriever and a sentence-level dense Retriever, both based on BERT [27]. They regard the process of  dense  retrieval  as  a  binary  classification  problem.  In particular, they take each pair of question and document as input and use the embedding of [CLS] token to determine whether they are relevant. Their experiments show that both paragraph-level  and  sentence-level  retrieval  are  necessary for obtaining good performance of the system. Interaction-based  method  [15],  [32]  is  powerful  as  it  allows  for  very rich interactions between question and document. However, such a method usually requires heavy computation, which is sometimes prohibitively expensive, making it hardly applicable to large-scale documents.
- 문서와 질문을 동시에 input으로 받고, token-level에서 두 representation간 interaction을 하도록 모델링.
- [15]Retrieve-and-read: Multi-task learning of information retrieval and reading comprehension
  - 해당 논문에선, Retriver와 Reader를 엮어서 supervised multi-task learning을 진행
- BiDAF은 retrieval layer에서 question과 document간 스코어를 매기는 동시에, comprehension layer에선 answer span의 start와 end position 예측.
- [32]Revealing the importance of semantic retrieval for machine reading at scale
  - 해당 논문에선, BERT based paragraph-level 및 sentence-level의 dense retriver를 만들고, dense retrieval process를 이진분류 문제로 간주함.
  - 또한, question-document이 각 pair를 input으로 사용하고, [cls] token을 사용하여 question과 document가 관련이 있는지에 대한 문제로 간주.
  - 해당 논문을 보면 paragraph-level 및 sentence-level의  retriever가 해당 시스템에서 좋은 성능을 내는데 매우 중요하다고 언급.
- Interaction-based Retriever 방법은 매우 성능이 좋지만, 많은 연산량과 비용이 요구되어 large-scale document에 적용하기에 어려움.

#### 3.1.2.3 Representation-interaction  Retriever
In order to achieve  both  high  accuracy  and  efficiency,  some  recent systems  [17],  [82],  [83]  combine  representation-based  and interaction-based methods. For instance, ColBERT-QA [17] develops its retriever based on ColBERT [84], which extends the dual-encoder architecture by performing a simple token-level interaction step over the question and document representations to calculate the similarity score. Akin to DPR [16], ColBERT-QA  first  encodes  the  question  and  document  in-dependently  with  two  BERT  encoders.  Formally,  given  aquestionq and  a  documentd,  with  corresponding  vectors denoted asEq(lengthn) andEd(lengthm), the relevance score between them is computed as follows:

![\Large S_{q,d}=\sum_{i=1}^n max_{j=1}^m E_{q_{i}} \cdot E_{d_{j}}^T\qquad\qquad(1)](https://latex.codecogs.com/svg.latex?\\Large&space;S_{q,d}=\sum_{i=1}^n&space;max_{j=1}^m&space;E_{q_{i}}&space;\cdot&space;E_{d_{j}}^T\qquad\qquad(1)) 

Then,  ColBERT  computes  the  score  of  each  token  embedding  of  the  question  over  all  those  of  the  document  first, and then sums all these scores as the final relevance score between q and d. As another example, SPARTA [82] develops a neural ranker to calculate the token-level matching score using dot product between a non-contextualized encoded(e.g.,BERT  word  embedding)  question  and  a contextualized  encoded(e.g., BERT encoder) document. Concretely, given therepresentations of the question and document, the weight of each question token is computed with max-pooling, ReLU and log sequentially; the final relevance score is the sum of each question token weight. The representation-interaction method is a promising approach to dense retrieval, due to its good trade-off between effectiveness and efficiency. But it still needs to be further explored.

- 성능과 효율을 모두 개선하기 위해, 최근 연구에선 위에 설명했던 representation-based & interaction-based methods를 통합하여 적용
  - e.g.) ColBERT-QA
    - ColBERT를 기반으로 retriever를 개발하는데, 유사성을 평가하기 위해 question과 document representation을 token-level에서 계산 
    - DPR과 유사하게, 두 개의 BERT 인코더가 독립적으로 질문과 문서를 인코딩, 이후 질문과 문서의 각 token들 간의 score를 생성한 이후 sum을 하여 최종 score를 계산
  - e.g.) SPARTA
    - non-contextualized encoded question과 contextualized encoded document 사이에 dot product를 통하여 token-matching score 계산을 위한 neural Ranker 개발
    - 여기서, question representation은 bert embedding의 결과이고, document representation은 BERT encoder를 통과 후 max-pooling & ReLU & log를 순차적으로 거쳐서 나온 값
    - 연관성 점수는 각 question token의 weight를 sum.
- representation-interaction method는 dense retrieval을 활용하기 위한 괜찮은 접근법이지만 아직 연구가 더 필요함.

Though  effective,  Dense  Retriever  often  suffers  heavy computational  burden  when  applied  to  large-scale  documents. In order to speed up the computation, some works propose  to  compute  and  cache  the  representations  of  all documents  offline  in  advance  [16],  [29],  [30],  [35],  [37].  In this  way,  these  representations  will  not  be  changed  once computed,  which  means  the  documents  are  encoded  independently of the question, to some extent sacrificing the effectiveness of retrieval.
- Dense Retriever는 매우 효과적이지만 대용량 문서를 다룰 때 연산량이 증폭하여 컴퓨터 리소스에 한계에 도달하게 됌.
- 그래서, 연산 속도를 향상시키기 위해 오프라인에서 모든 문서 표현을 미리 계산하여 캐시화를 진행.
- 단, 이 방식은 한 번 계산되면 변경되지 않으며, 문서가 질문에 어느 정도 의존적으로 인코딩되어 검색 효율성을 어느 정도 희생한다는 것으로 간주.

### 3.1.3 Iterative Retriever
Iterative Retriever aims to search for the relevant documents from  a  large  collection  in  multiple  steps  given  a  question , which  is  also  called  Multi-step  Retriever.  It  has  been  explored extensively in the past few years [29], [35], [36], [85],[86],  [87],  [88],  [89],  especially  when  answering  complex questions like those requiring multi-hop reasoning [90], [91]. In order to obtain a sufficient amount of relevant documents, the  search  queries  need  to  vary  for  different  steps  and  be reformulated based on the context information in the previous  step.  In  the  following,  we  will  elaborate  on  Iterative Retriever  based  on  its  workflow:  
1)  Document  Retrieval: the  IR  techniques  used  to  retrieve  documents  in  every retrieval step.
2)  Query Reformulation: the mechanism used to generate a query for each retrieval.
3)  Retrieval Stopping Mechanism:  the  method  to  decide  when  to  terminate  the retrieval process.

- Multi-step Retriever라고도 불리는 Iterative Retriever는 주어진 질문에 대해 여러 과정을 거쳐 적절한 문서를 검색해내는 것이 목표
- Mutti-step Retriever는 지난 몇 년 간 정답을 출력하기 위해 광범위한 검색을 수행했는데, 특히 특히 multi-hop reasoning이 요구되는 복잡한 질문에 대한 답변을 생성하기 위해 매우 넓게 문서를 탐색
- 관련 문서를 충분히 얻기 위해서, 검색 쿼리에 다양한 변화를 주어야 할 필요가 있어서, 이전 step의 context 정보를 기반으로 query를 변형.
- Iterative Retriever는 다음과 같이 세 단계로 구성
  1. retrieval precess마다 관련 문서를 검색하기 위한 IR 기술 적용
  2. retrieval 마다 query를 생성하기 위한 메커니즘을 적용
  3. 충분히 검색을 완료한 경우 retrieval process를 중단

#### 3.1.3.1 Document Retrieval




---

detail한 설명 글 : https://lilianweng.github.io/lil-log/2020/10/29/open-domain-question-answering.html







