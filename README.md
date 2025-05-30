


---
# OSS_pjt
2025 오픈소스소프트웨어 팀프로젝트 협업 규칙

## 📁 프로젝트 기본 구조
```
/client   → 클라이언트 코드 (PyQt, Tkinter 등)
/server   → 서버 코드 (Flask)
/data     → 이미지, 확률표, 설정 파일
/docs     → 문서, 기획안
```

## 📏 코드 컨벤션

✅ **언어**  
- Python 3.11
- 라이브러리 버전 통일 (requirements.txt로 관리)

✅ **네이밍 규칙**
| 요소         | 규칙                                  | 예시               |
|-------------|-------------------------------------|-------------------|
| 변수         | snake_case                          | click_count, user_id |
| 함수         | snake_case + 동사 중심             | send_click_data(), get_top10() |
| 클래스       | PascalCase                          | ClickerWindow, UserManager |
| 상수         | UPPER_SNAKE_CASE                   | DEFAULT_IMAGE_PATH, MAX_CLICK |
| 모듈/파일명   | snake_case                          | game_window.py, api_server.py |

✅ **코딩 스타일**
- [PEP8](https://peps.python.org/pep-0008/) 기본 준수
- 한 줄 최대 100자
- 들여쓰기 4칸
- 불필요한 import, 주석 제거

✅ **주석**
- 함수/클래스에는 **docstring** 사용
- 복잡한 로직은 코드 블록 내에 `#` 주석 추가

---

## 🌐 Git 규칙

✅ **브랜치 전략**
- `main`: 배포/완성 버전
- `dev`: 개발용 통합 브랜치
- `feature/xxx`: 각 기능별 작업 브랜치

✅ **커밋 메시지**
- Gitmoji 스타일 사용
- 메시지 예시:
  - ✨ feat: 이미지 클릭 이벤트 추가
  - 🐛 fix: 클릭 카운트 버그 수정
  - ♻️ refactor: 서버 응답 처리 리팩토링
  - 📝 docs: README 업데이트

✅ **PR (Pull Request)**
- 각 feature 브랜치는 dev로 PR
- PR 설명에: 변경 내용, 테스트 방법, 주의할 점 기재

---

## 📦 패키지/환경 관리

✅ `requirements.txt`로 의존성 관리  
- 새로운 라이브러리 추가 시, 꼭 `pip freeze > requirements.txt` 반영

✅ `.env` 파일로 비밀키/API키 관리 (git에 올리지 않기)

✅ AWS 자원은 별도 관리 (예: S3, DynamoDB 설정은 docs 폴더에 정리)

---

## 🏃‍♀️ 업무 배분/소통

✅ **회의록**  
- 매 주간 회의 내용은 docs/meeting_notes.md로 기록

✅ **할 일 관리**
- Github Issues나 Notion 등 사용 (합의 필요)

✅ **소통**
- 문제 생기면 카톡 즉시 공유
- 작업 멈출 땐 PR 올리거나 진행 상황 공유

---
