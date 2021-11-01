# Retrieving and Reading : A ComprehensiveSurvey on Open-domain Question Answering

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

In  1999,  OpenQA  was  first  defined  as  extracting  top5  probable  snippets  containing  the  correct  answer  from  acollection  of  news  articles  in  the  QA  track  launched  by the Text REtrieval Conference (TREC). Compared to the previous  research  on  QA,  in  the  open-domain  setting,  alarge  number  of  unstructured  documents  is  used  as  the information source from which the correct answer to a given question would be extracted. In the later years, a series ofTREC  QA  Tracks  have  remarkably  advanced  the  research progress on OpenQA. It is worth noting that systems are required to return exact short answers to given questions starting from TREC-11 held in 2002.

The TREC campaign provides a local collection of doc-uments  as  the  information  source  for  generating  answers, but the popularity of World Wide Web (WWW), especially the  increasing  maturity  of  search  engines,  has  inspired  re-searchers  to  build  Web-based  OpenQA  systems  obtaining  answers  from  online  resources  like Google.com and Ask.com, using IR techniques. Web search engines are able to consistently and efficiently collect massive web pages, therefore capable of providing much more information to help find answers in response to user questions.  In  2001,  a  QA  system  called  MULDER  was  de-signed to automatically answer open-domain factoid questions with a search engine (e.g., Google.com). It first translates users’ questions to multiple search queries with several natural-language parsers and submits them to the search engine to search for relevant documents, and then employs ananswer extraction component to extract the answer from the returned results. Following this pipeline, a well-known QA system AskMSR was developed, which mainly dependson  data  redundancy  rather  than  sophisticated  linguistic analysis  of  either  questions  or  candidate  answers.  It  first translates  the  user’s  question  into  queries  relying  on  a  set of predefined re writing rules to gather relevant documents from  search  engines  and  then  adopts  a  series  of  n-gram based algorithms to mine, filter and select the best answer. For  such  OpenQA  systems,  the  search  engines  are  able to  provide  access  to  an  ocean  of  information,  significantly enlarging the possibility of finding precise answers to user questions. Nevertheless, such an ample information source also  brings  considerable  noisy  content  that  challenges  theQA system to filter out.











