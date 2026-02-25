## File Inspect

특정 파일의 내부 구조와 의존성을 분석하여 시각화한다.

### 사용법

```
/inspect <파일경로>
```

### Procedure

#### 1단계: 파일 확인

- 인자로 전달된 파일 경로가 유효한지 확인한다.
- 파일이 존재하지 않으면 "파일을 찾을 수 없습니다: `<경로>`" 를 출력하고 종료한다.
- 파일이 존재하면 파일명, 언어/타입, 크기 등 기본 정보를 확인한다.

#### 2단계: 의존성 분석 깊이 선택

사용자에게 선택지를 제시한다:

- **1. 직접 의존성**: 대상 파일이 직접 import/require/include 하는 파일만 분석
- **2. 재귀적 (전체 트리)**: 의존 파일이 또 의존하는 파일까지 재귀적으로 전부 분석

#### 3단계: 출력 형식 선택

사용자에게 선택지를 제시한다:

- **1. 의존성 트리 + 파일별 요약**: 트리 구조 시각화 + 각 파일의 역할/구조 한 줄 요약
- **2. 의존성 트리만**: 트리 구조 시각화만 제공
- **3. 파일별 상세 분석**: 각 파일의 함수, 클래스, export 등 내부 구조 상세 분석

#### 4단계: 분석 실행

대상 파일을 읽고 언어/프레임워크에 맞는 의존성 구문을 파싱한다.

**언어별 의존성 탐지 패턴:**

| 언어/파일 타입 | 탐지 구문 |
|---|---|
| JS/TS | `import ... from`, `require(...)` |
| Vue | `import`, `<script>` 내 의존성, `<component>` |
| Python | `import`, `from ... import` |
| Go | `import` |
| Java/Kotlin | `import` |
| Rust | `use`, `mod` |
| C/C++ | `#include` |
| YAML | 참조 파일 (`include`, 파일 경로 패턴) |
| Dockerfile | `FROM`, `COPY`, `ADD` 참조 |
| 기타 | 파일 내용 기반으로 최선의 판단 |

**분석 규칙:**

- **프로젝트 내부 파일**과 **외부 패키지(node_modules, pip 패키지 등)**를 구분한다.
- 내부 파일만 의존성 트리에 포함한다. 외부 패키지는 별도 섹션에 나열한다.
- 상대 경로(`./`, `../`)와 프로젝트 alias(`@/`, `~/ ` 등)를 프로젝트 루트 기준 절대 경로로 해석한다.
- tsconfig, webpack, vite 등의 alias 설정이 있으면 참고하여 경로를 해석한다.
- 2단계에서 "재귀적"을 선택한 경우, 각 내부 의존 파일에 대해 동일한 파싱을 반복한다. 순환 의존성이 발견되면 `(circular)` 로 표시하고 더 이상 탐색하지 않는다.

#### 5단계: 결과 출력

3단계에서 선택한 형식에 따라 결과를 출력한다.

##### 형식 1: 의존성 트리 + 파일별 요약

```
📂 의존성 트리: src/components/UserProfile.tsx

src/components/UserProfile.tsx        ── 사용자 프로필 UI 컴포넌트
├── src/hooks/useUser.ts              ── 사용자 데이터 fetch 커스텀 훅
│   ├── src/api/userApi.ts            ── 사용자 API 호출 함수 모음
│   │   └── src/lib/httpClient.ts     ── Axios 기반 HTTP 클라이언트 래퍼
│   └── src/types/user.ts             ── User 타입 정의
├── src/components/Avatar.tsx         ── 아바타 이미지 컴포넌트
│   └── src/utils/image.ts            ── 이미지 URL 처리 유틸
└── src/styles/profile.module.css     ── 프로필 스타일 모듈

📦 외부 패키지: react, react-dom, axios, classnames
```

##### 형식 2: 의존성 트리만

```
📂 의존성 트리: src/components/UserProfile.tsx

src/components/UserProfile.tsx
├── src/hooks/useUser.ts
│   ├── src/api/userApi.ts
│   │   └── src/lib/httpClient.ts
│   └── src/types/user.ts
├── src/components/Avatar.tsx
│   └── src/utils/image.ts
└── src/styles/profile.module.css

📦 외부 패키지: react, react-dom, axios, classnames
```

##### 형식 3: 파일별 상세 분석

각 파일에 대해 다음 항목을 분석하여 출력한다:

```
📄 src/components/UserProfile.tsx
  - 타입: React 함수 컴포넌트
  - Exports: UserProfile (default), UserProfileProps (named)
  - 함수: UserProfile(), formatJoinDate()
  - 의존성: useUser, Avatar, profile.module.css
  - 줄 수: 87

📄 src/hooks/useUser.ts
  - 타입: 커스텀 훅
  - Exports: useUser (named)
  - 함수: useUser()
  - 의존성: userApi, User 타입
  - 줄 수: 34
```

### Rules

- 모든 출력은 한국어로 작성한다.
- 트리 시각화에는 유니코드 박스 드로잉 문자(`├──`, `└──`, `│`)를 사용한다.
- 파일을 읽을 수 없거나 파싱에 실패한 경우, 해당 파일을 `(읽기 실패)` 로 표시하고 나머지 분석을 계속한다.
- 순환 의존성은 `(circular)` 로 표시하고 무한 루프를 방지한다.
- 분석 대상 파일이 매우 많을 경우 (50개 이상), 사용자에게 알리고 계속할지 확인한다.
- 외부 패키지 목록은 트리 하단에 별도로 나열한다.
