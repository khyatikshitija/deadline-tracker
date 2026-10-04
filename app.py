import time
import smtplib
import base64

from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import streamlit as st

from google import genai
from google.genai import types

from prompt import (
    SYSTEM_PROMPT,
    WELCOME_PROMPT,
    SUMMARY_PROMPT
)

MODEL_NAME = "gemini-3.8-flash"

st.set_page_config(
    page_title="Deadline Tracker",
    page_icon="📚",
)

# Background

with open("assets/deadline-background.png", "rb") as image_file:
    encoded_image = base64.b64encode(
        image_file.read()
    ).decode()

st.markdown(
    f"""
    <style>

    .stApp {{
        background-image:
            linear-gradient(
                rgba(10, 20, 35, 0.68),
                rgba(10, 20, 35, 0.68)
            ),
            url("data:image/png;base64,{encoded_image}");

        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}

    /* Main title */

    h1 {{
        color: #ffffff !important;
        text-shadow: 0 2px 6px rgba(0, 0, 0, 0.65);
    }}

    /* Subtitle */

    .stCaption,
    [data-testid="stCaptionContainer"] {{
        color: #ffffff !important;
    }}

    /* Chat messages */

    [data-testid="stChatMessage"] {{
        background-color: rgba(255, 255, 255, 0.97);
        border-radius: 16px;
        padding: 18px;
        margin-bottom: 12px;
        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.20);
    }}

    [data-testid="stChatMessage"] p,
    [data-testid="stChatMessage"] li,
    [data-testid="stChatMessage"] strong,
    [data-testid="stChatMessage"] span {{
        color: #111827 !important;
    }}

    /* Onboarding labels */

    label {{
        color: #ffffff !important;
    }}

    /* Text inputs */

    input {{
        color: #111827 !important;
    }}

    /* Email digest button */

    div.stButton > button {{
        background-color: #ffffff !important;
        color: #111827 !important;
        border: 1px solid #d1d5db !important;
        border-radius: 10px !important;
        font-weight: 600 !important;
    }}

    div.stButton > button:hover {{
        background-color: #f3f4f6 !important;
        color: #111827 !important;
        border-color: #9ca3af !important;
    }}

    /* Deadline digest container */

    .deadline-digest {{
        background-color: rgba(255, 255, 255, 0.98);
        color: #111827;
        padding: 22px;
        border-radius: 16px;
        margin-top: 15px;
        margin-bottom: 15px;
        box-shadow: 0 5px 18px rgba(0, 0, 0, 0.20);
        line-height: 1.7;
        font-size: 16px;
    }}

    .deadline-digest h2 {{
        color: #111827 !important;
        margin-top: 0;
        margin-bottom: 15px;
    }}

    .deadline-digest p,
    .deadline-digest li,
    .deadline-digest strong,
    .deadline-digest span {{
        color: #111827 !important;
    }}

    /* Success message */

    [data-testid="stAlert"] {{
        color: #111827 !important;
    }}

    /* Gemini temporary message */

    [data-testid="stAlert"] p {{
        color: #111827 !important;
    }}

    /* Divider */

    hr {{
        border-color: rgba(255, 255, 255, 0.35);
    }}

    </style>
    """,
    unsafe_allow_html=True,
)

# API keys and Gmail settings

GEMINI_API_KEY = st.secrets["GEMINI_API_KEY"]
GMAIL_ADDRESS = st.secrets["GMAIL_ADDRESS"]
GMAIL_APP_PASSWORD = st.secrets["GMAIL_APP_PASSWORD"]


@st.cache_resource
def get_gemini_client():
    return genai.Client(
        api_key=GEMINI_API_KEY
    )


gemini_client = get_gemini_client()

# Send email function

def send_email(recipient, subject, body):

    message = MIMEMultipart()

    message["From"] = GMAIL_ADDRESS
    message["To"] = recipient
    message["Subject"] = subject

    message.attach(
        MIMEText(body, "plain")
    )

    with smtplib.SMTP_SSL(
        "smtp.gmail.com",
        465,
    ) as server:

        server.login(
            GMAIL_ADDRESS,
            GMAIL_APP_PASSWORD,
        )

        server.send_message(message)

# Student onboarding

if "onboarded" not in st.session_state:

    st.title("📚 Deadline Tracker")

    st.caption(
        "Snap it. Find it. Never miss an academic deadline."
    )

    with st.form("onboarding_form"):

        name = st.text_input(
            "Your name",
            placeholder="Enter your name",
        )

        email = st.text_input(
            "Your email address",
            placeholder="you@example.com",
        )

        submitted = st.form_submit_button(
            "Let's go 🚀"
        )

    if submitted:

        if not name.strip() or not email.strip():

            st.warning(
                "Please fill in both your name and email."
            )

        else:

            st.session_state.name = name.strip()
            st.session_state.email = email.strip()

            st.session_state.chat = gemini_client.chats.create(
                model=MODEL_NAME,
                config=types.GenerateContentConfig(
                    system_instruction=SYSTEM_PROMPT
                ),
            )

            st.session_state.messages = [
                {
                    "role": "assistant",
                    "content": WELCOME_PROMPT.format(
                        name=st.session_state.name
                    ),
                }
            ]

            st.session_state.onboarded = True

            st.rerun()

    st.stop()

# Main application

st.title("📚 Deadline Tracker")

st.caption(
    f"Welcome, {st.session_state.name}! "
    "Let's keep your deadlines organized."
)

# Display previous messages

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# Gemini response function

def ask_gemini(text, uploaded_file=None):

    parts = []

    if text:
        parts.append(text)

    if uploaded_file is not None:

        image_part = types.Part.from_bytes(
            data=uploaded_file.getvalue(),
            mime_type=uploaded_file.type,
        )

        parts.append(image_part)

    wait_times = [2, 5, 10, 20]

    for attempt in range(len(wait_times) + 1):

        try:

            response = st.session_state.chat.send_message(
                parts
            )

            return response.text

        except Exception as e:

            error_message = str(e)

            is_temporary_error = (
                "503" in error_message
                or "UNAVAILABLE" in error_message
            )

            if (
                is_temporary_error
                and attempt < len(wait_times)
            ):

                st.info(
                    f"Gemini is temporarily busy. "
                    f"Retrying in {wait_times[attempt]} seconds..."
                )

                time.sleep(
                    wait_times[attempt]
                )

            else:

                raise e

# Email deadline digest

st.divider()

if st.button("📧 Email Deadline Digest"):

    with st.spinner(
        "Creating your deadline digest..."
    ):

        try:

            digest = ask_gemini(
                SUMMARY_PROMPT
            )

            st.markdown(
                f"""
                <div class="deadline-digest">

                <h2>
                📚 Your Deadline Digest
                </h2>

                {digest}

                </div>
                """,
                unsafe_allow_html=True,
            )

            send_email(
                st.session_state.email,
                "📚 Your Deadline Tracker Digest",
                digest,
            )

            st.success(
                f"Deadline digest sent to "
                f"{st.session_state.email}! 📧"
            )

        except Exception as e:

            st.error(
                f"Could not create or send the digest: {e}"
            )

# Chat input

prompt = st.chat_input(
    "Upload a syllabus or ask about a deadline...",
    accept_file=True,
    file_type=[
        "jpg",
        "jpeg",
        "png",
        "pdf"
    ],
)

if prompt:

    user_text = prompt.text

    uploaded_file = None

    if prompt.files:

        uploaded_file = prompt.files[0]

    # Display user's message

    display_text = user_text

    if uploaded_file:

        if display_text:

            display_text += "\n\n"

        display_text += (
            f"📎 Uploaded: **{uploaded_file.name}**"
        )

    if display_text:

        st.session_state.messages.append(
            {
                "role": "user",
                "content": display_text,
            }
        )

        with st.chat_message("user"):

            st.markdown(display_text)

    # Ask Gemini

    with st.chat_message("assistant"):

        with st.spinner(
            "🔎 Finding your deadlines..."
        ):

            try:

                response_text = ask_gemini(
                    user_text,
                    uploaded_file,
                )

                st.markdown(
                    response_text
                )

                st.session_state.messages.append(
                    {
                        "role": "assistant",
                        "content": response_text,
                    }
                )

            except Exception as e:

                st.error(
                    f"Something went wrong: {e}"
                )