# AiBackend

FastAPI 기반 AI 백엔드 서비스를 로컬에서 실행하는 방법을 안내합니다.

## 실행 전 준비
- Python 3.10 이상이 설치되어 있어야 합니다.
- (선택) 가상환경을 사용하면 의존성 충돌을 방지할 수 있습니다.

```bash
python -m venv .venv
source .venv/bin/activate  # Windows PowerShell은 .venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## 개발 서버 실행
Uvicorn으로 FastAPI 앱을 기동합니다.

```bash
uvicorn app.main:app --reload
```

- 서버가 기동되면 `http://127.0.0.1:8000/ping`에서 헬스 체크를 확인할 수 있습니다.
- 자동으로 제공되는 문서 UI는 `http://127.0.0.1:8000/docs`에서 Swagger(OpenAPI) 기반으로 확인할 수 있습니다.
- `--reload` 플래그 덕분에 코드 변경 시 서버가 자동으로 재시작됩니다.

## 테스트용 예시 요청
FastAPI에 정의된 `/api/request` 엔드포인트를 `httpie` 또는 `curl`로 호출하여 동작을 확인합니다.

```bash
curl -X POST http://127.0.0.1:8000/api/request \
  -H "Content-Type: application/json" \
  -d '{"keyword": "예시 키워드"}'
```

실제 응답 스키마는 `app/classes/responses.py`를 참고하세요.

## Docker Compose 실행
컨테이너 환경에서 서버를 실행하려면 Docker와 Docker Compose가 설치되어 있어야 합니다.

```bash
docker compose up --build
```

- 첫 실행 시 이미지를 빌드하며, 이후에는 `docker compose up`으로 빠르게 기동할 수 있습니다.
- 서비스를 중지하려면 `Ctrl+C` 후 `docker compose down`을 실행하세요.
- 컨테이너 역시 `http://127.0.0.1:8000/ping`과 `/docs`에서 동일한 엔드포인트를 제공합니다.
