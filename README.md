# 1. cuddle-server

## 1. dir Tree
```
cuddle-server
│
├── app/
│ ├── init.py
│ ├── main.py
│ ├── core/
│ │ ├── init.py
│ │ ├── config.py
│ │ ├── security.py
│ │ └── dependencies.py
│ ├── db/
│ │ ├── init.py
│ │ ├── base.py
│ │ └── session.py
│ ├── models/
│ │ ├── init.py
│ │ └── user.py
│ ├── schemas/
│ │ ├── init.py
│ │ └── user.py
│ ├── services/
│ │ ├── init.py
│ │ ├── auth_service.py
│ │ └── user_service.py
│ ├── routes/
│ │ ├── init.py
│ │ ├── auth_routes.py
│ │ └── user_routes.py
│ └── utils/
│ ├── init.py
│ ├── hashing.py
│ └── jwt.py
│
├── .env
├── requirements.txt
└── README.md
```

## 2. 디렉토리 및 파일 설명

### 2.1 `app/`
- FastAPI 애플리케이션의 루트 디렉토리입니다.
- `__init__.py`: 디렉토리가 파이썬 패키지로 인식되도록 합니다.
- `main.py`: FastAPI 애플리케이션의 진입점으로, 서버를 실행하고 라우터를 등록합니다.

### 2.2 `app/core/`
- 애플리케이션의 핵심 설정 및 보안 관련 파일들이 위치합니다.
  - `config.py`: 애플리케이션 설정(환경 변수, 설정 값 등)을 관리합니다.
  - `security.py`: 보안 관련 유틸리티(예: 비밀번호 해시화, 인증 로직)를 포함합니다.
  - `dependencies.py`: 의존성 주입을 관리하는 모듈로, FastAPI의 `Depends`를 통해 사용됩니다.

### 2.3 `app/db/`
- 데이터베이스와 관련된 설정 및 세션 관리 파일들이 위치합니다.
  - `base.py`: SQLAlchemy Base 클래스와 모델들을 초기화합니다.
  - `session.py`: 데이터베이스 세션 생성 및 관리 로직을 포함합니다.

### 2.4 `app/models/`
- 데이터베이스 테이블과 매핑되는 SQLAlchemy 모델들을 정의합니다.
  - `user.py`: 사용자 모델 정의 파일입니다.

### 2.5 `app/schemas/`
- Pydantic을 사용하여 데이터의 유효성 검사를 위한 스키마를 정의합니다.
  - `user.py`: 사용자와 관련된 요청 및 응답 데이터를 위한 스키마를 정의합니다.

### 2.6 `app/services/`
- 비즈니스 로직을 처리하는 서비스 레이어입니다. 컨트롤러에서 호출되어 실제 작업을 수행합니다.
  - `auth_service.py`: 인증 관련 서비스 로직을 포함합니다 (예: 로그인, 토큰 생성).
  - `user_service.py`: 사용자 관리 관련 서비스 로직을 포함합니다 (예: 사용자 생성, 정보 조회).

### 2.7 `app/routes/`
- API 엔드포인트를 정의하는 라우터 파일들이 위치합니다.
  - `auth_routes.py`: 인증 관련 엔드포인트를 정의합니다.
  - `user_routes.py`: 사용자 관리 관련 엔드포인트를 정의합니다.

### 2.8 `app/utils/`
- 다양한 유틸리티 함수들이 위치합니다.
  - `hashing.py`: 비밀번호 해시화 및 검증 로직을 포함합니다.
  - `jwt.py`: JWT 토큰 생성 및 검증 로직을 포함합니다.

### 2.9 `.env`
- 환경 변수를 정의하는 파일입니다. 데이터베이스 연결 정보, 비밀 키 등 민감한 정보를 관리합니다.

### 2.10 `requirements.txt`
- 프로젝트에서 사용되는 Python 패키지와 그 버전을 정의하는 파일입니다.