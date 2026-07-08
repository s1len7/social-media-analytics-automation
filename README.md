# Social Media Analytics Automation

SNS 데이터를 자동 수집하고 분석 리포트를 생성하는 자동화 프로젝트입니다.

## Features

- Instagram 공개 게시물 수집
- YouTube 채널 영상 데이터 수집
<!-- - Automated monthly report -->
<!-- - CSV/XLSX export -->
<!-- - Chart generation -->
<!-- - Email notification -->


## Supported Platforms

- Instagram
- YouTube


## Installation

### 개발 환경

- Windows 10
- VS Code
- WSL
- Python
- uv

### 패키지 설치

```bash
git clone https://github.com/xxx/social-media-analytics-automation.git
cd social-media-analytics-automation
uv sync
cp .env.example .env
```

## Configuration

### 환경 변수 설정

민감한 정보(API Key, Token, 이메일 계정 정보 등)는 `.env` 파일에서 관리합니다.

`.env` 파일 생성:

```env
APIFY_API_TOKEN=your_apify_token
YOUTUBE_API_KEY=your_youtube_api_key
```


## Apify API Token 발급 방법

Instagram 공개 게시물 수집을 위해 Apify API를 사용합니다.

### 1. Apify 가입

Apify Console 접속:

https://console.apify.com/

회원가입 후 로그인합니다.

### 2. API Token 확인

메뉴:

```text
Settings
 └─ Integrations
     └─ API tokens
```

에서 API Token을 생성합니다.

생성된 Token을 `.env` 파일에 입력합니다.

예:

```env
APIFY_API_TOKEN=apify_api_xxxxxxxxxxxxx
```

### 3. 사용 Actor

현재 Instagram 수집은 Apify Instagram Scraper Actor를 사용합니다.

필요 권한:

- 공개 Instagram 계정 데이터 조회
- 게시물 메타데이터 수집

## YouTube Data API Key 발급 방법

YouTube 데이터 수집을 위해 Google Cloud YouTube Data API v3를 사용합니다.

### 1. Google Cloud Console 접속

https://console.cloud.google.com/

### 2. 프로젝트 생성

상단 프로젝트 선택 메뉴에서 새 프로젝트 생성

예:

```text
프로젝트 이름:
social-media-analytics-automation
```

### 3. YouTube Data API v3 활성화

메뉴:

```text
API 및 서비스
 └─ 라이브러리
```

검색:

```text
YouTube Data API v3
```

선택 후:

```text
사용 설정
```

### 4. API Key 생성

메뉴:

```text
API 및 서비스
 └─ 사용자 인증 정보
```

선택:

```text
+ 사용자 인증 정보 만들기
 └─ API 키
```

생성된 API Key를 `.env` 파일에 입력합니다.

예:

```env
YOUTUBE_API_KEY=AIzaSyxxxxxxxxxxxxxxxx
```

### 5. API Key 제한 설정 (권장)

생성된 API Key 선택 후:

애플리케이션 제한:

```text
필요 시 IP 주소 제한
```

API 제한:

```text
YouTube Data API v3
```

으로 설정합니다.

## YouTube 채널 ID 설정 방법

YouTube 데이터 수집을 위해 대상 채널을 설정해야 합니다.

지원 방식:

1. 채널 ID 직접 입력
2. YouTube 핸들(@handle) 입력 후 자동 변환

### 방법 1. YouTube 채널 ID 직접 입력

YouTube 채널 ID 형식:

```text
UCxxxxxxxxxxxxxxxx
```

확인 방법:

```text
YouTube Studio
 └─ 설정
     └─ 채널
         └─ 고급 설정
```

에서 채널 ID를 확인합니다.

`config.yaml` 설정 예:

```yaml
youtube:
  channels:
    - UCxxxxxxxxxxxxxxxx
```

### 방법 2. YouTube 핸들 입력

YouTube 채널 URL의 핸들을 사용할 수 있습니다.

예:

```text
https://www.youtube.com/@channelname
```

핸들:

```text
@channelname
```

`config.yaml` 설정 예:

```yaml
youtube:
  channels:
    - "@channelname"
```

프로그램 실행 시 핸들을 자동으로 채널 ID로 변환한 후 데이터를 수집합니다.

### 권장 사항

- 장기 운영 환경에서는 채널 ID 사용을 권장합니다.
- 핸들은 변경될 수 있으므로 자동화 환경에서는 채널 ID가 더 안정적입니다.


## Scheduler Setup

Windows 작업 스케줄러를 이용해 자동 실행합니다.

예:

```text
매월 1일 09:00 실행
```

PC가 종료되어 예약 시간이 지나간 경우:

```text
예약된 시작 시간을 놓친 후 가능한 빨리 작업 시작
```

옵션을 활성화합니다.

## Output Example

생성 결과:

```text
data/
├─ raw/
│  ├─ instagram_raw.json
│  └─ youtube_raw.json
└─ processed/
   ├─ instagram_posts.csv
   └─ youtube_videos.csv
```

## License

MIT License