
# 🤖 TalentScout Hiring Assistant Chatbot

##  Project Overview

**TalentScout Hiring Assistant** is an AI-powered chatbot designed to streamline the candidate screening process for recruiters. Built with **Python** and **Streamlit**, this assistant gathers candidate information, dynamically generates technical questions based on the candidate’s skillset, and maintains context throughout the conversation. It provides a user-friendly interface that simulates an intelligent and engaging interview assistant.

---
##  .env file 

Replace the OPENROUTER API KEY with your openrouter api key 
The api key can be created by logging into to openrouter and generating a secret key for project.

---
##  Installation Instructions

Follow these steps to run the project locally:

1. **Clone the Repository**
   ```bash
   git clone https://github.com/chhanvitha/talent-scout-chatbot.git
   cd talent-scout-chatbot
   ```

3. **Install the Required Packages**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the Streamlit App**
   ```bash
   streamlit run app2.py
   ```



## 🛠️ Usage Guide

1. Launch the app using the command above.
2. You will be prompted to enter your basic information (e.g., name, experience, tech stack).
3. The chatbot will greet you and start generating technical questions based on your inputs.
4. You can interact with the chatbot:
   - Ask it to rephrase a question if it's unclear or you do not understand it properly.
   - Say "bye","exit","quit","thank you"  to end the conversation.

> 💡 Pro Tip: The chatbot maintains context to follow up based on prior inputs.

---

## ⚙️ Technical Details

### 📚 Libraries Used
- **Streamlit** – for UI and interactivity
- **LLM API (e.g., LLaMA 3)** – for question generation and context management
- **re / regex** – for input pattern recognition to get the email and mobile number in correct format
- **Custom Python Utilities** – for prompt management and candidate data saving

### 🧠 Model Details
- **Model:** LLaMA 3 (can also be configured with any LLM like GPT-4 or Claude or any other)
- **Backend Logic:** Custom prompts for task-specific outputs like greetings, question generation, rephrasing, and fallback

---

## ✍️ Prompt Design

Prompts are modular and task-specific:
- **Greeting Prompt:** Initiates the conversation warmly with personalized text.
- **Question Generation Prompt:** Takes candidate skills as input and generates domain-relevant questions.
- **Rephrase Prompt:** Triggered when user indicates confusion or asks for clarification.
- **Fallback Prompt:** Handles unexpected or off-topic inputs gracefully.
- **Farewell Prompt:** Ends the session politely.

Each prompt is fine-tuned using few-shot examples and pattern-driven instructions to maintain relevance, tone, and context flow.

---

## 🧩 Challenges & Solutions

| Challenge | Solution |
|----------|----------|
| **Context Retention** | Used `st.session_state` to track inputs and preserve dialogue flow across steps. |
| **Unclear Prompts** | Created a separate prompt handler to rephrase questions using LLM if users indicate confusion. |
| **LLM Misbehavior** | Added prompt instructions to maintain control over tone, length, and intent of generated outputs. |

---
