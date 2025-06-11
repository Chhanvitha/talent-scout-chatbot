import streamlit as st
from utils import get_llm_response
from prompts import (
    greeting_prompt,
    question_generation_prompt,
    fallback_prompt,
    farewell_prompt,
    rephrase_question_prompt
)
import re
from utils import save_candidate_data

rephrased = False

# Page setup
st.set_page_config(page_title="TalentScout Hiring Assistant", layout="centered")
st.title("🤖 TalentScout Hiring Assistant")

# Session state init
if "step" not in st.session_state:
    st.session_state.step = "show_form"
    st.session_state.candidate_info = {}
    st.session_state.questions = []
    st.session_state.q_index = 0
    st.session_state.chat_history = []

# Step 1: Candidate Info Form

if st.session_state.step == "show_form":
    with st.form("Candidate Info Form"):
        st.subheader("Candidate Information")
        full_name = st.text_input("Full Name")
        email = st.text_input("Email")
        phone = st.text_input("Phone Number")
        experience = st.slider("Years of Experience", 0, 30)
        position = st.text_input("Desired Position(s)")
        location = st.text_input("Current Location")
        tech_stack = st.text_area("Tech Stack (languages, frameworks, tools)")

        submitted = st.form_submit_button("Start Chat")

        # Validation logic
        email_valid = re.match(r"[^@]+@[^@]+\.[^@]+", email)
        phone_valid = re.match(r"^\+?\d{10,15}$", phone.replace(" ", "").replace("-", ""))

        if submitted:
            if not email_valid:
                st.warning("⚠️ Please enter a valid email address (e.g. john@example.com)")
            elif not phone_valid:
                st.warning("⚠️ Please enter a valid phone number (10–15 digits, optional +)")
            else:
                # Save info and continue
                st.session_state.candidate_info = {
                    "Full Name": full_name,
                    "Email": email,
                    "Phone Number": phone,
                    "Years of Experience": experience,
                    "Desired Position": position,
                    "Location": location,
                    "Tech Stack": tech_stack,
                }


                # Generate technical questions
                tech_prompt = question_generation_prompt.format(tech_stack=tech_stack)
                raw_response = get_llm_response(tech_prompt)
                lines = raw_response.strip().split("\n")

# Extract lines that look like actual questions
                cleaned_questions = []
                for line in lines:
                    line = line.strip("-•: ").strip()
                    if (
                        line and
                        "question" not in line.lower() and
                        not line.lower().startswith("here are")
                        and len(line) > 10
                    ):
                        cleaned_questions.append(line)

                st.session_state.questions = cleaned_questions[:5]  # Limit to 5 questions

                # Add greeting to chat
                candidate_name = full_name.split()[0] if full_name else "there"
                welcome_message = f"""
Hi {candidate_name}, thank you for providing your details!  
I'm your Hiring Assistant, here to ask you a few technical questions based on your skills in:
**{tech_stack}**
This will help our team better understand your strengths. Ready? Let's begin!
"""
                st.session_state.chat_history.append({"role": "assistant", "content": welcome_message})
                st.session_state.step = "chat"
                st.rerun()



# Step 2: Chat-based Q&A
elif st.session_state.step == "chat":
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if st.session_state.q_index < len(st.session_state.questions):
        current_q = st.session_state.questions[st.session_state.q_index]
        if "last_asked" not in st.session_state or st.session_state.last_asked != current_q:
            with st.chat_message("assistant"):
                st.markdown(f"Question {st.session_state.q_index + 1}: {current_q}")
            st.session_state.chat_history.append(
                {"role": "assistant", "content": f"Question {st.session_state.q_index + 1}: {current_q}"}
            )
            st.session_state.last_asked = current_q

    if user_input := st.chat_input("Type your answer or ask to rephrase..."):
        with st.chat_message("user"):
            st.markdown(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        # Exit handling
        if any(word in user_input.lower() for word in ["bye", "exit", "quit", "thank you"]):
            farewell = get_llm_response(farewell_prompt)
            st.chat_message("assistant").markdown(farewell)
            st.session_state.chat_history.append({"role": "assistant", "content": farewell})
            st.session_state.step = "end"

        # Confusion / rephrasing
        elif any(kw in user_input.lower() for kw in ["don't understand", "repeat", "what do you mean", "confused", "not sure", "pardon","can't understand","rephrase"]):
            current_q = st.session_state.questions[st.session_state.q_index]
            rephrased=True
            rephrased_text = get_llm_response(rephrase_question_prompt.format(original_question=current_q))
            st.chat_message("assistant").markdown(f"Let me rephrase that:\n\n**{rephrased_text}**")
            st.session_state.chat_history.append({"role": "assistant", "content": f"Let me rephrase that:\n\n**{rephrased_text}**"})

        # Regular answer
        if not rephrased:
            st.session_state.q_index += 1
            if st.session_state.q_index < len(st.session_state.questions):
                st.rerun()
            else:
                info = st.session_state.candidate_info
                farewell_msg = get_llm_response(
                    farewell_prompt.format(
                        full_name=info.get("Full Name", "Candidate"),
                        position=info.get("Desired Position", "the applied role")
                    )
                )
                st.chat_message("assistant").markdown(farewell_msg)
                st.session_state.chat_history.append({"role": "assistant", "content": farewell_msg})
                st.session_state.step = "end"
