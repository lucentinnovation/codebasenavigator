# Codebase Navigator Agent

The **Codebase Navigator Agent** is an AI-powered assistant that allows developers to explore and query large codebases using natural language. It's especially useful for onboarding, debugging, and maintaining complex Node.js or multi-language repositories.

Built using **LangChain**, **OpenAI**, and **FAISS**, this tool lets you ask questions like:

> "Where is user authentication handled?"
> "Which files deal with coupon logic?"

And receive intelligent answers with file references and summaries.

---

## Features

- Support for JavaScript, TypeScript, JSON, Markdown files
- Automatically excludes irrelevant directories like `node_modules`, `.git`, etc.
- Context-aware answers using GPT-4
- Available in both CLI and Streamlit web app
- Customizable via `.env` or UI input

---

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repo-url>
cd codebase-navigator
```

### 2. Create and Activate Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Option 1: CLI Version (main.py)

### 4A. Configure Environment Variables

Create a `.env` file at the root:

```env
OPENAI_API_KEY=your_openai_key
DIRECTORY_PATH=./your-nodejs-project
```

### 5A. Run the CLI Tool

```bash
python main.py
```

You'll see:

```
Codebase Navigator Ready. Ask a question about the Node.js project.
>>
```

---

## Option 2: Web App Version (Streamlit)

### 4B. Run the Streamlit App

```bash
streamlit run app.py
```

### 5B. In your browser:

- Enter your **OpenAI API Key**
- Enter the **directory path** to your codebase
- Ask a question like:
  - "Where is user role validation implemented?"
  - "How is the login flow handled?"

---

## Supported File Types

- `.js`, `.ts`, `.json`, `.md`

## Excluded Folders

- `node_modules`
- `.git`
- `dist`, `build`
- `__pycache__`, `coverage`

---

## Roadmap Ideas

- Web UI enhancements
- Multi-language support (Python, Java, etc.)
- Context memory for multi-turn conversations
- GitHub integration for PR summaries

---

## License

MIT (or your preferred license)

---

## Maintainer

Lucent Innovation
