# AI powered bug identifier
> An intelligent REST API that takes code snippets and returns bugs, explainations or suggestions powered by Google Gemini.

# Project Architecture

```bash
bug-identifier-api/
│
├── app/
│   ├── main.py                # FastAPI app entry point
│   ├── routes/                # API endpoints
│   ├── core/                  # LLM client, config, prompt engineering
│   ├── models/                # Request/response schemas
│   ├── utils/                 # Error handling and helpers
│   └── sample_data/           # Sample buggy cases
│
├── tests/                     # Unit & integration tests
├── .env                       # API key stored here
├── requirements.txt           # Python dependencies
├── README.md                  # You're reading this
└── run.sh                     # Script to launch app easily
