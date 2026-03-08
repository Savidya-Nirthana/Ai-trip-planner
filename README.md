# 🌍 AI Trip Planner

An intelligent travel planning assistant powered by **LangGraph** agentic workflows, **LangChain** tools, and state-of-the-art LLMs. It generates personalised itineraries, fetches live weather data, searches places, converts currencies, and estimates expenses — all through a conversational interface.

---

## ✨ Features

| Feature | Description |
|---|---|
| 🗺️ **Personalised Itineraries** | AI-generated day-by-day travel plans tailored to your preferences |
| 🌤️ **Live Weather Info** | Real-time weather conditions for any destination |
| 📍 **Place Search** | Discover top attractions, restaurants, and hotels via Google Places API |
| 💱 **Currency Conversion** | Convert between currencies with up-to-date exchange rates |
| 🧮 **Expense Calculator** | Estimate travel budgets and costs |
| 🤖 **ReAct Agent** | A LangGraph ReAct agent that decides which tools to call step by step |
| 🖥️ **Streamlit UI** | Clean, browser-based chat interface |
| ⚡ **FastAPI Backend** | RESTful API serving the agent at `POST /query` |

---

## 🏗️ Architecture

```
User (Streamlit UI)
        │
        ▼
FastAPI Backend (main.py)  ──  POST /query
        │
        ▼
LangGraph ReAct Agent  ◄──────────────────────┐
        │                                      │
        ├─► WeatherInfoTool                    │
        ├─► PlaceSearchTool (Google Maps)      │
        ├─► CurrencyConverterTool              │
        └─► CalculatorTool              ───────┘
                                   (tool results fed back to agent)
```

The `GraphBuilder` class constructs a **LangGraph StateGraph** with:
- An **agent node** — the LLM bound with all tools, handles reasoning
- A **tools node** — executes whichever tool the agent selects
- **Conditional edges** — routes between agent ↔ tools until the agent produces a final answer

---

## 📁 Project Structure

```
ai_trip_planner/
├── main.py                          # FastAPI entry point
├── streamlit_app.py                 # Streamlit UI
├── requirements.txt                 # Python dependencies
├── pyproject.toml                   # Project metadata
├── config/
│   ├── models.yaml                  # LLM & embedding model catalogue
│   └── params.yaml                  # Runtime parameters (provider, temperature, etc.)
├── src/
│   ├── agents/
│   │   ├── agentic_workflow.py      # LangGraph GraphBuilder (ReAct loop)
│   │   ├── prompt_library/          # System prompts
│   │   └── tools/
│   │       ├── weather_information_tool.py
│   │       ├── place_search_tool.py
│   │       ├── currency_conversion_tool.py
│   │       └── expense_calculator_tool.py
│   ├── infrastructure/
│   │   ├── config.py                # Loads YAML configs & env vars
│   │   ├── llm_provider/
│   │   │   └── llm_client.py        # Multi-provider LLM factory
│   │   └── utils/
│   │       ├── weather_info.py
│   │       ├── place_info_search.py
│   │       ├── currency_convertor.py
│   │       └── calculator.py
│   ├── exception/                   # Custom exception classes
│   └── logger/                      # Logging setup
├── notebooks/                       # Jupyter exploration notebooks
├── aws/                             # AWS deployment configs
└── .github/workflows/               # CI/CD GitHub Actions
```

---

## 🤖 Supported LLM Providers

The project supports multiple LLM providers, configurable via `config/params.yaml`:

| Provider | General Model | Strong Model | Reasoning Model |
|---|---|---|---|
| **OpenRouter** *(default)* | Gemini 2.5 Flash | Gemini 2.5 Pro | Gemini 2.5 Pro |
| **OpenAI** | gpt-4o-mini | gpt-4o | o3-mini |
| **Groq** | Llama 3.1 8B | Llama 3.1 70B | DeepSeek R1 70B |
| **Anthropic** | Claude 3 Haiku | Claude 3.5 Sonnet | Claude 3.5 Sonnet |
| **Google** | Gemini 2.5 Flash | Gemini 2.5 Pro | Gemini 2.5 Pro |
| **DeepSeek** | deepseek-chat | deepseek-chat | deepseek-reasoner |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- API keys (see `.env` setup below)

### 1. Clone the Repository

```bash
git clone https://github.com/Savidya-Nirthana/Ai-trip-planner.git
cd ai_trip_planner
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

Or using `uv` (recommended):

```bash
uv sync
```

### 3. Configure Environment Variables

Create a `.env` file in the project root:

```env
# LLM Providers (add keys for the providers you want to use)
OPENROUTER_API_KEY=your_openrouter_api_key
OPENAI_API_KEY=your_openai_api_key
GROQ_API_KEY=your_groq_api_key
ANTHROPIC_API_KEY=your_anthropic_api_key
GOOGLE_API_KEY=your_google_api_key

# External Tools
GOOGLE_MAPS_API_KEY=your_google_maps_api_key   # For place search
TAVILY_API_KEY=your_tavily_api_key             # For web search (optional)
```

### 4. Configure Model Provider

Edit `config/params.yaml` to select your preferred LLM provider:

```yaml
provider:
  default: openrouter   # Change to: openai, groq, anthropic, google, deepseek
  tier: general         # Change to: strong, reason for more powerful models
```

---

## ▶️ Running the Application

### Start the FastAPI Backend

```bash
uvicorn main:app --reload --port 8000
```

The API will be available at `http://localhost:8000`.

### Start the Streamlit UI

In a **separate terminal**:

```bash
streamlit run streamlit_app.py
```

Open your browser at `http://localhost:8501` and start planning your trip!

---

## 🔌 API Reference

### `POST /query`

Send a natural language travel query to the agent.

**Request Body:**
```json
{
  "question": "Plan a 5-day trip to Bali for 2 people on a budget of $1500"
}
```

**Response:**
```json
{
  "answer": "Here's your personalised 5-day Bali itinerary..."
}
```

---

## 💡 Example Prompts

- *"Plan a 5-day trip to Goa for 2 people"*
- *"7-day Japan itinerary for couples with a €3000 budget"*
- *"What's the weather like in Paris right now?"*
- *"Convert 500 USD to Japanese Yen"*
- *"Find the top 5 restaurants in Rome"*
- *"Budget trip to Bali for 10 days — what will it cost?"*

---

## 🧰 Tech Stack

| Category | Technology |
|---|---|
| **Agent Framework** | LangGraph, LangChain |
| **LLM Providers** | OpenRouter, OpenAI, Groq, Anthropic, Google |
| **Backend API** | FastAPI, Uvicorn |
| **Frontend UI** | Streamlit |
| **External APIs** | Google Maps / Places, Tavily |
| **Config** | PyYAML, python-dotenv, Pydantic |
| **CI/CD** | GitHub Actions |

---

## 📄 License

This project is open-source. Feel free to use, modify, and contribute.

---

> ⚠️ AI-generated travel content is for planning purposes only. Always verify prices, entry requirements, and travel advisories before booking.
