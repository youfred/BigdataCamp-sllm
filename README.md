# BigdataCamp-sLLM: 미래열쇠

방대한 입시 데이터와 LLM/RAG를 활용하여 학생 개인의 상황과 목표에 맞춘 입시 상담을 제공하는 AI 입시 컨설팅 서비스 프로젝트입니다.

> 프로젝트명: 미래열쇠  
> 프로젝트 주제: sLLM 기반 대학 입시 컨설팅 서비스  
> 주요 작업: 입시 요강 PDF 수집 → 텍스트/테이블 데이터 전처리 → FAISS Vector DB 구축 → RAG 기반 질의응답 API 구현

---

## 1. 프로젝트 개요

`미래열쇠`는 고액 입시 컨설팅 비용과 입시 정보 접근성 문제를 해결하기 위해 기획한 AI 입시 상담 서비스입니다.

대학 정시/수시 모집요강, 합격 결과 등 방대한 입시 자료를 기반으로 사용자의 질문에 맞는 정보를 검색하고, LLM을 통해 이해하기 쉬운 형태로 답변을 제공합니다.

본 저장소에는 RAG 기반 질의응답을 위한 데이터 전처리 코드, Vector DB 생성 코드, FastAPI 기반 스트리밍 챗봇 API 코드, 발표자료 및 구현 영상이 포함되어 있습니다.

---

## 2. 문제 인식

입시를 준비하는 학생과 학부모는 많은 정보를 직접 찾아야 하며, 대학별 전형 방식과 모집요강이 복잡해 정보 탐색에 어려움을 겪습니다.  
또한 전문 입시 컨설팅은 비용 부담이 크기 때문에 모든 학생이 충분한 상담 기회를 얻기 어렵습니다.

이 프로젝트는 다음 문제를 해결하는 것을 목표로 했습니다.

- 고액 입시 컨설팅 비용 부담 완화
- 입시 정보 부족으로 인한 의사결정 어려움 개선
- 대학별 모집요강 및 합격 정보를 쉽게 검색할 수 있는 서비스 제공
- 시간과 장소의 제약 없이 사용할 수 있는 AI 입시 상담 서비스 구현
- 입시 정보를 구조화하여 LLM 기반 질의응답에 활용

---

## 3. 팀원

| 이름 | 소속 | 역할 |
|---|---|---|
| 임은지 | 한동대학교 | 백엔드 |
| 박상범 | 한동대학교 | 프론트엔드 |
| 박수빈 | 경상국립대학교 | 데이터 수집 및 분석 |
| 김영준 | 전북대학교 | 데이터 수집 및 분석 |

---

## 4. 사용 데이터

본 프로젝트에서는 대학 입시 상담에 필요한 문서 및 데이터를 수집하여 활용했습니다.

주요 데이터는 다음과 같습니다.

- 대학교 정시 모집요강 PDF
- 대학교 수시 모집요강 PDF
- 대학교 합격 결과 데이터
- 입시 관련 안내 자료

전처리된 문서는 LLM이 검색 및 답변에 활용할 수 있도록 텍스트 데이터와 Vector DB 형태로 변환했습니다.

---

## 5. 데이터 전처리

입시 모집요강 PDF는 표, 문단, 항목이 복잡하게 섞여 있기 때문에 LLM이 바로 이해하기 어렵습니다.  
따라서 PDF 문서에서 텍스트와 테이블을 추출한 뒤, 검색 가능한 형태로 가공했습니다.

### 전처리 흐름

```text
입시 모집요강 PDF
→ PDF 텍스트 추출
→ 표 데이터 추출
→ 테이블 데이터를 텍스트 형태로 변환
→ 줄바꿈 및 문장 구조 정리
→ 통합 TXT 파일 생성
→ Chunking
→ Embedding
→ FAISS Vector DB 생성
```

### 주요 전처리 작업

- `PyPDF2`, `pdfplumber`를 활용한 PDF 텍스트 및 테이블 추출
- PDF 내 표 데이터를 LLM이 이해할 수 있는 일반 텍스트 형태로 변환
- 칼럼별, 행별 구분을 위해 줄바꿈 및 문장 구조 정리
- 추출된 입시 정보를 하나의 텍스트 파일로 통합
- `RecursiveCharacterTextSplitter`를 활용한 문서 chunk 분할
- OpenAI Embeddings를 활용한 임베딩 생성
- FAISS 기반 Vector DB 생성 및 저장

---

## 6. RAG 시스템 구조

본 프로젝트는 RAG, 즉 Retrieval-Augmented Generation 구조를 사용합니다.  
사용자의 질문이 들어오면 관련 입시 정보를 Vector DB에서 먼저 검색하고, 검색된 문맥을 기반으로 LLM이 답변을 생성합니다.

### RAG Workflow

```text
User Question
→ Retriever
→ FAISS Vector Similarity Search
→ Relevant Admission Information
→ Prompt Construction
→ LLM Answer Generation
→ Streaming Response
```

### 주요 구성 요소

| 구성 요소 | 설명 |
|---|---|
| PDF Parser | 입시 모집요강 PDF에서 텍스트와 테이블 추출 |
| Text Splitter | 긴 입시 문서를 chunk 단위로 분할 |
| Embedding Model | 문서 chunk를 벡터로 변환 |
| FAISS Vector DB | 입시 정보를 저장하고 유사도 기반 검색 수행 |
| Retriever | 사용자 질문과 관련 있는 문서 chunk 검색 |
| LLM | 검색된 문맥을 기반으로 한국어 답변 생성 |
| FastAPI | 질의응답 API 서버 구현 |
| StreamingResponse | 답변을 스트리밍 방식으로 반환 |

---

## 7. 주요 기능

### 1. 입시 정보 질의응답

사용자가 대학 입시 관련 질문을 입력하면, 시스템이 관련 문서를 검색한 뒤 한국어 답변을 생성합니다.

### 2. PDF 기반 입시 데이터 처리

입시 모집요강 PDF에서 텍스트와 테이블 데이터를 추출하고, LLM이 활용할 수 있는 검색 데이터로 변환합니다.

### 3. 벡터 검색 기반 문서 검색

FAISS Vector DB를 활용하여 사용자의 질문과 의미적으로 가까운 입시 정보를 검색합니다.

### 4. 스트리밍 응답 API

FastAPI와 `StreamingResponse`를 활용하여 챗봇 답변을 스트리밍 형식으로 출력할 수 있도록 구현했습니다.

### 5. 한국어 답변 프롬프트 설계

답변은 한국어로 생성되도록 설정했으며, 가독성을 높이기 위해 개조식 출력과 문장 단위 줄바꿈을 프롬프트에 반영했습니다.

---

## 8. Repository Structure

```text
BigdataCamp-sllm-main/
├── README.md
├── LICENSE
├── .gitignore
└── 미래열쇠/
    ├── 구현영상.mp4
    ├── 데이터 전처리 코드.png
    ├── 프롬프트코드.png
    ├── 미래열쇠_발표자료.pdf
    └── 소스코드/
        └── 4.all/
            ├── app.py              # FastAPI 기반 RAG 스트리밍 API 서버
            ├── data.py             # 텍스트 로드, chunking, FAISS DB 생성 코드
            ├── pdf.py              # PDF 텍스트 및 테이블 추출 코드
            ├── request_test.py     # API 요청 테스트 코드
            ├── Handong4.txt        # 전처리된 입시 텍스트 데이터
            └── db1/
                └── faiss/
                    ├── index.faiss
                    └── index.pkl
```

---

## 9. 코드 설명

### `pdf.py`

입시 모집요강 PDF에서 텍스트와 테이블을 추출하여 `Handong4.txt` 파일로 저장합니다.

주요 작업:

- PDF 페이지별 텍스트 추출
- 표 데이터 추출
- 표 내부 줄바꿈 제거 및 텍스트화
- 페이지별 텍스트를 하나의 TXT 파일로 통합

### `data.py`

전처리된 `Handong4.txt` 파일을 불러와 chunking을 수행하고, FAISS Vector DB를 생성합니다.

주요 작업:

- `TextLoader`로 텍스트 데이터 로드
- `RecursiveCharacterTextSplitter`로 문서 분할
- `OpenAIEmbeddings`로 임베딩 생성
- `FAISS.from_texts()`로 Vector DB 생성
- `save_local()`로 로컬 FAISS DB 저장

### `app.py`

FAISS DB와 LLM을 연결하여 RAG 기반 질의응답 API를 제공합니다.

주요 작업:

- FAISS Vector DB 로드
- Retriever 생성
- ChatOllama 기반 LLM 호출
- RAG Chain 구성
- FastAPI 서버 실행
- `/stream_chat/` 엔드포인트를 통한 스트리밍 응답 제공

### `request_test.py`

FastAPI 서버에 POST 요청을 보내고 스트리밍 응답을 확인하는 테스트 코드입니다.

---

## 10. Tech Stack

### Language

- Python

### LLM / RAG

- LangChain
- ChatOllama
- EEVE-Korean-10.8B
- OpenAI Embeddings
- Prompt Engineering
- Retrieval-Augmented Generation

### Vector Search

- FAISS

### Data Processing

- PyPDF2
- pdfplumber
- pandas
- regular expression
- TextLoader
- RecursiveCharacterTextSplitter

### Backend / API

- FastAPI
- StreamingResponse
- Pydantic
- Uvicorn
- requests

---

## 11. Installation

```bash
git clone https://github.com/YOUR_USERNAME/BigdataCamp-sllm.git
cd BigdataCamp-sllm/미래열쇠/소스코드/4.all
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

현재 저장소에 `requirements.txt`가 별도로 정리되어 있지 않은 경우, 아래 주요 패키지를 설치해야 합니다.

```bash
pip install fastapi uvicorn python-dotenv langchain langchain-community langchain-openai faiss-cpu pydantic requests pandas pdfplumber pypdf2
```

Ollama 기반 모델을 사용하는 경우, 로컬 환경에 Ollama와 사용 모델이 준비되어 있어야 합니다.

```bash
ollama pull EEVE-Korean-10.8B
```

OpenAI Embeddings를 사용하므로 `.env` 파일에 API Key를 설정합니다.

```text
OPENAI_API_KEY=YOUR_OPENAI_API_KEY
```

---

## 12. How to Run

### 1. PDF 전처리

```bash
python pdf.py
```

PDF 경로는 코드 내 로컬 경로에 맞게 수정해야 합니다.

### 2. FAISS Vector DB 생성

```bash
python data.py
```

`Handong4.txt` 경로가 현재 환경과 다를 경우 코드 내 경로를 수정해야 합니다.

### 3. FastAPI RAG 서버 실행

```bash
python app.py
```

또는:

```bash
uvicorn app:app --host 0.0.0.0 --port 8004
```

### 4. API 테스트

```bash
python request_test.py
```

`request_test.py`의 URL은 서버 실행 환경에 맞게 수정해야 합니다.

---

## 13. My Role

프로젝트에서 프론트엔드 역할을 맡아 서비스 사용자가 AI 입시 상담 기능을 직관적으로 이용할 수 있도록 하는 부분에 참여했습니다.  
또한 발표자료 구성과 서비스 흐름 정리에 참여하며, 프로젝트가 사용자 문제와 기술 구현을 연결해 설명될 수 있도록 기여했습니다.

주요 기여 내용은 다음과 같습니다.

- AI 입시 컨설팅 서비스의 사용자 흐름 구성 참여
- 프론트엔드 관점에서 서비스 화면 및 사용자 경험 방향 논의
- 데이터 전처리 결과와 RAG 응답이 사용자에게 이해하기 쉽게 전달되도록 출력 방식 검토
- 프롬프트 출력 형식 개선 방향 논의
- 프로젝트 발표자료 구성 및 문서화 참여
- 구현 결과 시연 및 서비스 기대효과 정리 참여

---

## 14. Project Outcome

본 프로젝트는 고액 입시 컨설팅에 대한 부담과 입시 정보 접근성 문제를 해결하기 위해, 입시 데이터를 기반으로 한 AI 상담 서비스의 가능성을 제시했습니다.

프로젝트를 통해 다음과 같은 결과를 도출했습니다.

- 입시 모집요강 PDF를 LLM/RAG 시스템에서 활용 가능한 텍스트 데이터로 변환
- FAISS Vector DB 기반 입시 정보 검색 구조 구현
- 한국어 LLM을 활용한 입시 질의응답 API 구현
- 스트리밍 방식의 챗봇 응답 구조 구현
- AI 기반 입시 상담 서비스의 초기 프로토타입 제시

---

## 15. Expected Effects

- 경제적 부담 없이 입시 정보를 확인할 수 있는 상담 서비스 제공 가능
- 온라인 기반 서비스로 시간과 장소의 제약 감소
- 학생 개인의 상황과 목표에 맞춘 입시 정보 탐색 지원
- 수시/정시뿐 아니라 고입, 대학원, 유학 상담 등으로 확장 가능
