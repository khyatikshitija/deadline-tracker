# 📚 Deadline Tracker

Deadline Tracker is an AI-powered academic assistant that helps students
find and organize important deadlines from syllabi, assignment sheets,
timetables, and academic notices.

## Features

- 📄 Upload syllabus or assignment documents
- 🤖 AI-powered deadline extraction using Google Gemini
- 📚 Organizes Subject, Task, Due Date, Time, and Notes
- 💬 Ask questions about uploaded deadlines
- 📧 Generate and email a deadline digest
- 🎨 Student-friendly Streamlit interface
- 🔐 Uses secrets for API credentials

## System Flow

```text
                    ┌─────────────────────┐
                    │       Student       │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Open Deadline     │
                    │      Tracker        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Enter Name & Email  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Upload Syllabus /   │
                    │ Assignment / Notice │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Google Gemini AI  │
                    │  analyzes document  │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Extract Deadlines   │
                    │                     │
                    │ Subject             │
                    │ Task                │
                    │ Due Date            │
                    │ Time                │
                    │ Notes               │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Display Results   │
                    │   in Chat Interface │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Student can ask     │
                    │ follow-up questions │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Generate Deadline   │
                    │       Digest        │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   Gmail SMTP        │
                    │ Send Digest Email   │
                    └─────────────────────┘

Technologies
Python
Streamlit
Google Gemini API
Gmail SMTP
How It Works
The student enters their name and email address.
The student uploads a syllabus, assignment sheet, timetable,
academic notice, or asks a question.
Google Gemini analyzes the uploaded content.
Important academic deadlines are extracted.
The deadlines are presented in a structured format.
The student can ask follow-up questions about the deadlines.
A deadline digest can be generated and sent to the student's email.
Future Scope

The current version focuses on extracting and organizing academic
deadlines. The system can be extended with several additional features.

📅 Calendar Integration

Future versions could automatically add detected deadlines to
Google Calendar or other calendar applications.

🔔 Automatic Reminders

The application could send reminders before an assignment or exam,
such as:

7 days before
3 days before
1 day before
On the due date
📱 WhatsApp Notifications

Deadline reminders could be delivered through WhatsApp so that
students receive notifications directly on their phones.

🗂️ Deadline Dashboard
A dedicated dashboard could show:
Upcoming deadlines
Overdue tasks
Completed tasks
Deadlines by subject
Weekly and monthly views

🎯 Priority Detection

The AI could classify deadlines based on urgency and importance,
helping students focus on high-priority tasks first.

👥 Multi-Student Support

The system could support multiple student profiles and maintain
individual deadline lists.

☁️ Cloud Database

A database could store deadlines securely so that students can access
their information across different devices.

🤖 Smarter Academic Assistant

Future versions could provide study planning, workload analysis,
assignment prioritization, and personalized study schedules.

Security

API keys and Gmail App Passwords are stored in
.streamlit/secrets.toml and are excluded from Git using .gitignore.

Never commit real credentials to GitHub.

Run Locally

Install the required packages:

pip install -r requirements.txt

Create:

.streamlit/secrets.toml

and add your API credentials.

Then run:

streamlit run app.py
Project Structure
deadline-tracker/
├── app.py
├── prompt.py
├── requirements.txt
├── .gitignore
├── README.md
├── assets/
│   └── deadline-background.png
└── .streamlit/
    ├── secrets.toml
    └── secrets.toml.example

### One small improvement

For GitHub, this **ASCII flowchart is actually better than an image** because it works directly inside `README.md` without needing another image file.

Once you've updated the README with the **System Flow** and **Future Scope**, tell me **DONE**.

Then we'll move to **Step 13.3 — GitHub repository setup**.            