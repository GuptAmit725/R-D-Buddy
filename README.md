# R&D Buddy

This project is a LangGraph-powered chatbot application with support for arXiv article analysis, company news, and chat history storage in DynamoDB. It uses Streamlit for the UI and integrates with Google Gemini for LLM and embeddings.

---

## Prerequisites

- Python 3.9+
- AWS account with DynamoDB table `ChatHistory` (with at least `SessionId` as the primary key)
- Google Gemini API key
- [Optional] AWS credentials configured for DynamoDB access

---

## Installation

1. **Clone the repository:**
   ```sh
   git clone <your-repo-url>
   cd AGENTICAICHATBOT_MODEL
   ```

2. **Create and activate a virtual environment:**
   ```sh
   python -m venv profile_match_venv
   profile_match_venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```sh
   pip install -r requirements.txt
   ```

---

## Configuration

1. **Set your Google Gemini API key:**

   - Option 1: Set as an environment variable  
     ```sh
     set GOOGLE_API_KEY=your-gemini-api-key
     ```
   - Option 2: Provide in the UI or config as prompted

2. **Ensure AWS credentials are set up for DynamoDB access:**
   - Configure using `aws configure` or set `AWS_ACCESS_KEY_ID` and `AWS_SECRET_ACCESS_KEY` as environment variables.

---

## Running the Application

### Streamlit UI

To launch the Streamlit app:

```sh
streamlit run src/langgraphagenticai/ui/streamlit/display_result.py
```

### CLI or Script

To run the main application logic:

```sh
python -m src.langgraphagenticai.main
```

Or, if you want to run the entry point directly:

```sh
python app.py
```

---

## Project Structure

```
AGENTICAICHATBOT_MODEL/
│
├── app.py
├── requirements.txt
├── src/
│   └── langgraphagenticai/
│       ├── main.py
│       ├── nodes/
│       ├── graph/
│       ├── LLMS/
│       ├── DynamoDB_Ops/
│       └── ui/
│           └── streamlit/
│               └── display_result.py
└── ...
```

---

## Notes

- The application will automatically create and store chat message embeddings in DynamoDB.
- Make sure your DynamoDB table allows storing lists of `Decimal` values for embeddings.
- For arXiv and news features, ensure your API keys and models are set correctly.

---

## Troubleshooting

- **ModuleNotFoundError:** Always run scripts from the project root and use the `-m` flag for modules.
- **No event loop errors:** The code is designed to handle event loops in threaded environments like Streamlit.
- **DynamoDB errors:** Ensure your AWS credentials and table schema are correct.

---

## License

MIT License (or your chosen license)

