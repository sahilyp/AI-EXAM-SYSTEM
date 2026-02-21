# 🧠 AI-Based Intelligent Exam Question Generator & Online Examination System

An AI-powered web application that generates MCQs, Fill-in-the-Blanks, and Question–Answer exams from uploaded documents with automatic grading, timer-based exams, performance tracking, and PDF result reports.

---

## 🚀 Features

* 📄 Upload PDF / TXT syllabus
* 🤖 AI-based question generation using NLP (spaCy)
* 📝 MCQ, Fill in the Blank, and QA exams
* ⏱ Timer-based secure exams
* 🎯 Automatic grading & score calculation
* 📊 Performance history dashboard
* 📥 PDF result report generation
* 🔐 Authentication using Supabase
* ☁ Cloud storage for PDF reports

---

## 🛠 Tech Stack

**Frontend**

* HTML
* CSS (Glass UI)
* Bootstrap
* JavaScript

**Backend**

* Python
* Flask
* spaCy NLP
* PyPDF2

**Database & Storage**

* Supabase Auth
* Supabase PostgreSQL
* Supabase Storage

---

## ⚙️ Installation & Setup

### 1️⃣ Clone repository

```bash
git clone https://github.com/YOUR_USERNAME/ai-exam-system.git
cd ai-exam-system
```

---

### 2️⃣ Create virtual environment

```bash
python -m venv .venv
.venv\Scripts\activate
```

---

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

---

### 4️⃣ Download spaCy model

```bash
python -m spacy download en_core_web_sm
```

---

### 5️⃣ Create `.env` file

```env
SUPABASE_URL=your_supabase_url
SUPABASE_SERVICE_KEY=your_service_key
SECRET_KEY=exam_secret
```

⚠️ Do NOT upload `.env` to GitHub

---

## 🧾 Supabase Database Setup

### Create table `tests`

```sql
create table tests (
  id uuid default uuid_generate_v4() primary key,
  user_id uuid,
  score int,
  total int,
  grade text,
  difficulty text,
  pdf_url text,
  created_at timestamp default now()
);
```

---

## ☁ Supabase Storage Setup

1. Go to **Storage**
2. Create bucket named:

```
pdfs
```

3. Make bucket **Public**

---

### Storage Policy (allow upload)

```sql
create policy "Allow upload"
on storage.objects
for insert
to authenticated
with check (bucket_id = 'pdfs');
```

---

## ▶️ Run the application

```bash
python app.py
```

Open:

```
http://127.0.0.1:5000
```

---

## 📸 Screenshots

Add screenshots here:

* Home page
* <img width="1919" height="872" alt="Screenshot 2026-02-21 194357" src="https://github.com/user-attachments/assets/b19488ea-34d1-479f-8a72-e545f5112fe3" />

* Dashboaard page
* <img width="1919" height="886" alt="Screenshot 2026-02-21 194438" src="https://github.com/user-attachments/assets/bca4f8b7-0b2c-43b9-b9e4-b5ac7ab5f5a6" />


* Exam generation
* <img width="1919" height="872" alt="Screenshot 2026-02-21 194502" src="https://github.com/user-attachments/assets/b8b84be4-67fe-428b-9aab-66f8ca59066b" />

* Quiz interface
* <img width="1919" height="876" alt="Screenshot 2026-02-21 194524" src="https://github.com/user-attachments/assets/37a6b62e-3a39-4590-ab12-d55ea92b1c82" />

* Result history
* <img width="1919" height="863" alt="Screenshot 2026-02-21 194543" src="https://github.com/user-attachments/assets/2b89d266-a9f9-49dd-8cc8-2503e33d5734" />


---

## 🎓 Project Use Case

This project helps:

* Students practice exams automatically
* Teachers generate question papers instantly
* Institutes conduct secure online exams
* Performance analysis using AI-generated assessments

---

## 👨‍💻 Author

**Sahil Patel**
B.Tech CSE Final Year
AI + NLP Based Examination System
