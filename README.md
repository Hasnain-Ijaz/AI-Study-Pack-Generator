# 📚 AI Study Pack Generator

A personalized AI Study Pack Generator built with Python, Groq API, and Streamlit.

The application uses a multi-stage AI workflow to transform a student's topic and learning goals into a structured study pack.

## 🚀 AI Workflow

The app follows five stages:

1. **Planning** — creates learning objectives, prerequisites, concepts, and a study schedule.
2. **Content Generation** — generates explanations, examples, tips, and takeaways.
3. **Assessment** — creates MCQs, short questions, and a challenge question.
4. **Review** — checks quality, completeness, clarity, and alignment.
5. **Refinement** — uses review feedback to produce the final study pack.

Context is passed from one stage to the next.

## 🛠 Tech Stack

- Python
- Groq API
- Llama 3.3 70B Versatile
- Streamlit
- python-dotenv
- Google Colab for development
- GitHub for source control
- Streamlit Cloud for deployment

## 📁 Project Structure

```text
ai-study-pack-generator/
├── app.py
├── ai_workflow.py
├── utils.py
├── requirements.txt
├── README.md
├── .env
├── .env.example
└── .gitignore
```

## 🔑 Local Setup

### 1. Install dependencies

```bash
pip install -r requirements.txt
```

### 2. Create `.env`

```env
GROQ_API_KEY=your_groq_api_key_here
```

Never upload your real `.env` file to GitHub.

### 3. Run Streamlit

```bash
streamlit run app.py
```

## ☁️ Streamlit Cloud Deployment

Push these files to GitHub:

```text
app.py
ai_workflow.py
utils.py
requirements.txt
README.md
.gitignore
.env.example
```

Do **not** upload `.env`.

In Streamlit Cloud, open your app's **Settings → Secrets** and add:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

## 🧪 Example Input

- Subject: Artificial Intelligence
- Topic: Generative AI
- Level: Beginner
- Study Time: 1 hour
- Language: English
- Goal: Understand the fundamentals and prepare for an exam.

## ✨ Output

The app generates:

- Personalized study plan
- Topic summary
- Key concepts
- Practical examples
- Study tips
- MCQs with answers and explanations
- Short questions
- Challenge question
- Key takeaways
- Review information
- Downloadable Markdown study pack

## 🔐 Security

- API keys are loaded from environment variables locally.
- `.env` is excluded through `.gitignore`.
- Streamlit Cloud should use Streamlit Secrets.
- Never hard-code API keys in Python files.
