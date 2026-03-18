# 🧠 QuizMaster

A fun, interactive quiz web application built with Python and Streamlit. Test your knowledge across multiple categories, track your scores, and compete with others on the leaderboard.

---

## ✨ Features

- **Multiple Quiz Categories** — Choose from Mathematics, Science, History, and more
- **User Accounts** — Register and log in to save your progress and scores
- **Guest Mode** — Play without an account by entering your name
- **Leaderboard** — See how you rank against other players
- **Instant Feedback** — Get scored at the end of each quiz session

---

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Frontend & Backend | [Streamlit](https://streamlit.io/) |
| Language | Python 3.11 |
| Database | SQLite (via `database.py`) |
| Hosting | [Streamlit Community Cloud](https://streamlit.io/cloud) |

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11 (recommended — see note below)
- pip

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/s6-quizmaster.git
   cd s6-quizmaster
   ```

2. **Set the Python version** *(important for Streamlit Cloud compatibility)*

   Create a `.python-version` file in the project root:
   ```
   3.11
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the app locally**
   ```bash
   streamlit run Home.py
   ```

   The app will open at `http://localhost:8501`

### Deploying to Streamlit Cloud

1. Push your repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) and connect your repo
3. Set the main module to `Home.py`
4. Make sure your `requirements.txt` specifies compatible versions (see Troubleshooting below)

---

## 📖 How to Use

1. **Visit the app** via the live URL or run it locally
2. **Create an account** using the Account section on the Home page, or simply enter your name to play as a guest
3. **Select a quiz category** from the dropdown menu
4. **Click "Start Quiz"** to begin
5. **Answer the questions** — your score is calculated at the end
6. **Check the Leaderboard** to see how you compare to other players

---

## 📁 Project Structure

```
s6-quizmaster/
│
├── Home.py                 # Main entry point & authentication
├── database.py             # Database init, user creation & verification
├── requirements.txt        # Python dependencies
├── .python-version         # Pin Python to 3.11 for compatibility
│
└── pages/
    ├── 1_Quiz.py           # Quiz page
    └── ...                 # Additional pages (leaderboard, etc.)
```

---

## 📄 License

This project is for educational purposes. Feel free to fork and adapt it for your own use.
