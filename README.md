# 📧 AI Email Assistant
 
A Streamlit web app that uses Google's Gemini API to help write and manage emails.
 
## Features
 
- **Rewrite emails:** turn rough notes into a polished email, with a choice of tone (professional, friendly, formal, concise)
- **Summarize emails:** condense long emails into 2-4 sentences with action items
- **Subject lines:** generate 5 subject line options for any email
- **Retry and error handling:** automatically retries when the API is overloaded and shows a friendly message instead of crashing
## Tech Stack
 
Python, Streamlit, Google Gemini API (`google-genai`), python-dotenv
 
## How to Run Locally
 
**Step 1: Clone the repo and open the folder.**
 
**Step 2: Create and activate a virtual environment.**
 
```
python -m venv venv
venv\Scripts\activate
```
 
**Step 3: Install dependencies.**
 
```
pip install -r requirements.txt
```
 
**Step 4: Create a `.env` file in the project root.**
 
```
GEMINI_API_KEY=your_key_here
```
 
Get a free key at [aistudio.google.com](https://aistudio.google.com).
 
**Step 5: Run the app.**
 
```
streamlit run app.py
```
 
## How It Works
 
The app builds a system prompt for each feature (and each tone), sends it along with the user's text to the Gemini API, and displays the response.
 
All API calls go through one reusable helper function that handles retries and errors.
 
## What I Learned
 
- Prompt engineering with dynamic system prompts
- Integrating an LLM API and keeping secrets out of source control
- Handling API errors with retries
- Building a multi-tab UI with Streamlit
