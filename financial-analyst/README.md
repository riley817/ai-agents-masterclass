# Google ADK (Agent Development Kit) 강의 요약

이 문서는 Google ADK 강의 시리즈(Introduction, ADK Web, Tools and Sub-agents)의 내용을 요약한 것입니다.

## 1. Google ADK 소개
Google ADK는 AI 에이전트를 구축하기 위한 Google의 최신 프레임워크입니다. LangGraph, OpenAI Swarm, CrewAI보다 최신이며, Google 내부에서도 에이전트 개발에 사용됩니다.

### 주요 특징
*   **최신 프레임워크**: 다른 프레임워크들의 장점을 흡수하고 Google 스타일로 개선했습니다.
*   **뛰어난 개발자 경험 (DX)**: Streamlit 등을 사용하여 별도의 UI를 만들 필요 없이, 강력한 내장 UI를 제공합니다.
*   **유연성**: Python과 Java를 지원하며, Gemini뿐만 아니라 OpenAI 모델(via `litellm`)과도 잘 작동합니다.

## 2. 프로젝트 설정 및 구조

### 기본 구조
프로젝트는 다음과 같은 구조를 가집니다:

```
financial-analyst/
├── .env                  # API 키 (OPENAI_API_KEY 등)
├── pyproject.toml        # 의존성 관리 (google-adk, litellm 등)
├── tools.py              # (선택) 외부 도구 정의
└── financial_advisor/    # 에이전트 패키지 폴더
    ├── __init__.py       # 패키지 진입점
    └── agent.py          # 에이전트 로직 정의
```

### 필수 요구사항
*   **`__init__.py`**: 폴더를 Python 패키지로 만들고 `agent` 모듈을 노출해야 합니다.
*   **`root_agent`**: `agent.py` 파일 내에 반드시 `root_agent`라는 이름의 변수가 정의되어 있어야 ADK가 이를 인식합니다.

## 3. 에이전트 생성 (Agent Creation)

`Agent` 클래스(또는 `LlmAgent`)를 사용하여 에이전트를 정의합니다.

```python
from google.adk.agents import Agent
from google.adk.models.lite_llm import LiteLlm

MODEL = LiteLlm("openai/gpt-4o")

# 서브 에이전트 (Sub-agent)
geo_agent = Agent(
    name="GeoAgent",
    instruction="You help the user with geo questions",
    model=MODEL,
    description="Transfer to this agent when you have a geo related question." # Handoff를 위한 설명
)

# 메인 에이전트 (Root Agent)
weather_agent = Agent(
    name="WeatherAgent",
    instruction="You help the user with weather related questions",
    model=MODEL,
    tools=[get_weather, convert_units], # 도구 등록
    sub_agents=[geo_agent]              # 서브 에이전트 등록
)

# 필수: ADK가 찾을 수 있도록 root_agent 변수 할당
root_agent = weather_agent
```

## 4. ADK Web (개발용 UI)

터미널에서 프로젝트 루트(패키지 폴더 상위)에서 다음 명령어를 실행합니다:

```bash
adk web
```

### 주요 기능
*   **Chat UI**: 완성도 높은 Material Design 기반의 채팅 인터페이스.
*   **Multi-modality**: 파일 첨부(이미지 등)를 기본적으로 지원합니다.
*   **Session Management**: 새로운 세션을 생성하거나 삭제하여 대화 맥락을 관리할 수 있습니다.
*   **Event Tracking (Trace)**:
    *   에이전트의 사고 과정, 도구 호출(Request), 결과 반환(Response) 등 모든 이벤트를 시각적으로 확인할 수 있습니다.
    *   디버깅에 매우 유용합니다.

## 5. Tools (도구)

파이썬 함수를 정의하고 `Agent`의 `tools` 리스트에 추가하기만 하면 됩니다.

```python
def get_weather(city):
    return f"The weather in {city} is 30 degrees."

weather_agent = Agent(
    ...,
    tools=[get_weather]
)
```
ADK Web UI에서 도구 호출 및 반환 값을 상세히 모니터링할 수 있습니다.

## 6. Sub-agents & Handoffs (위임)

하나의 에이전트가 모든 것을 처리하는 대신, 특정 작업을 전문 에이전트에게 위임할 수 있습니다.

1.  **서브 에이전트 생성**: `geo_agent`와 같이 별도의 에이전트를 만듭니다.
2.  **Description 작성**: **중요!** 메인 에이전트가 언제 이 서브 에이전트로 작업을 넘겨야(Transfer) 할지 알 수 있도록 `description`을 명확히 작성해야 합니다.
3.  **등록**: 메인 에이전트의 `sub_agents` 리스트에 추가합니다.

사용자가 지리학 관련 질문을 하면, `WeatherAgent`는 자동으로 `GeoAgent`로 대화를 전환(Transfer)합니다.

## 7. API Server (배포용)

개발이 완료되면 API 서버를 실행할 수 있습니다.

```bash
adk api_server
```

*   **Swagger UI**: `http://127.0.0.1:8000/docs`에서 API 문서를 확인하고 테스트할 수 있습니다.
*   자체 프론트엔드를 구축하여 이 API 서버와 연동할 수 있습니다.
