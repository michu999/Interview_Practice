# 🏗️ SYSTEM ARCHITECTURE (Simple Version)

## What You Built

```
┌─────────────────────────────────────────────────────────┐
│                    YOUR LAPTOP                          │
│                                                         │
│  ┌──────────────────────────────────────────────────┐  │
│  │              Docker Container                    │  │
│  │                                                  │  │
│  │  ┌──────────────────────────────────────────┐   │  │
│  │  │        Django Application                │   │  │
│  │  │                                          │   │  │
│  │  │  • Blog posts display                   │   │  │
│  │  │  • Rating system                        │   │  │
│  │  │  • Interactive map (Leaflet)            │   │  │
│  │  │  • Admin panel                          │   │  │
│  │  │  • AI post generation                   │   │  │
│  │  │                                          │   │  │
│  │  │  Listening on: 0.0.0.0:8000            │   │  │
│  │  └──────────────────────────────────────────┘   │  │
│  │                                                  │  │
│  └──────────────────────────────────────────────────┘  │
│                                                         │
│  Port 8000 exposed to network                          │
│                                                         │
└─────────────────────────────────────────────────────────┘
                         │
                         │ Network (WiFi)
                         │
         ┌───────────────┼───────────────┐
         │               │               │
    ┌────▼────┐    ┌────▼────┐    ┌────▼────┐
    │ Student │    │ Student │    │ Student │
    │ Device  │    │ Device  │    │ Device  │
    │         │    │         │    │         │
    │ Browse  │    │ Browse  │    │ Browse  │
    │ & Rate  │    │ & Rate  │    │ & Rate  │
    └─────────┘    └─────────┘    └─────────┘
```

## Data Flow

```
1. Student opens: http://[YOUR_IP]:8000
                          ↓
2. Sees list of blog posts with map
                          ↓
3. Clicks on a post to read it
                          ↓
4. Rates the post (1-5 stars) + optional comment
                          ↓
5. Rating saved to db.sqlite3
                          ↓
6. [Repeat for other posts]
                          ↓
7. You run ./stop.sh
                          ↓
8. Database backed up → Your thesis data! 🎓
```

## What's Inside the Container

```
/app/
├── core/              (Django settings)
├── blog/              (Your app logic)
│   ├── models.py      (Post, Rating, AIPrompt)
│   ├── views.py       (Page logic)
│   ├── ai_services.py (AI integrations)
│   └── templates/     (HTML pages)
├── static/            (CSS, JS)
├── db.sqlite3         (YOUR DATA!)
├── manage.py          (Django CLI)
└── requirements.txt   (Dependencies)
```

## AI Integration Flow

```
You (Admin) → Django Admin Panel
                    ↓
            Choose AI Model
         (Gemini/ChatGPT/DeepSeek)
                    ↓
            Enter Prompt
     "Write about Paris (48.8566, 2.3522)"
                    ↓
            API Call to AI Service
                    ↓
            AI Generates Content
                    ↓
            Saved as Blog Post
                    ↓
        Students Can Now Rate It!
```

## Tech Stack (What's Running)

```
┌─────────────────────────────────────┐
│ Frontend (What Students See)        │
│ • HTML/CSS (Polish language)        │
│ • JavaScript (interactive map)      │
│ • Leaflet.js (map rendering)        │
│ • Responsive design                 │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│ Backend (Django)                    │
│ • Python 3.12                       │
│ • Django 4.2                        │
│ • SQLite database                   │
│ • REST framework                    │
└─────────────────────────────────────┘
              ↕
┌─────────────────────────────────────┐
│ AI Services (External APIs)         │
│ • OpenAI (ChatGPT)                  │
│ • Google (Gemini)                   │
│ • DeepSeek                          │
└─────────────────────────────────────┘
```

## Database Schema (Simplified)

```
┌──────────────┐         ┌──────────────┐
│  blog_post   │         │ blog_rating  │
├──────────────┤         ├──────────────┤
│ id           │◄────────│ post_id      │
│ title        │         │ score (1-5)  │
│ content      │         │ comment      │
│ author       │         │ created_at   │
│ latitude     │         └──────────────┘
│ longitude    │
│ created_at   │
└──────────────┘
        ▲
        │
┌──────────────┐
│ blog_aiprompt│
├──────────────┤
│ model_name   │
│ prompt_text  │
│ created_at   │
└──────────────┘
```

## Security Model (Classroom Setting)

```
✅ ENABLED:
• Basic Django authentication
• CSRF protection for forms
• Admin panel requires login
• SQL injection protection (Django ORM)

❌ DISABLED/RELAXED:
• HTTPS (local network)
• Rate limiting (not needed for 1 day)
• Advanced firewall rules
• Session expiry
• Password complexity (simple admin password)

Why? Speed > Security for 1-day collection
```

## Performance Specs

```
Concurrent Users:     30-50 students
Database:            SQLite (sufficient for this use case)
Response Time:       < 500ms per page
Memory Usage:        ~500MB
Disk Space:          ~100MB (app + data)
Uptime Needed:       4-8 hours (one class session)
```

## What Happens When

```
./start.sh runs:
  1. Docker builds image (2-3 min first time)
  2. Installs Python packages
  3. Runs database migrations
  4. Creates admin user (admin/admin123)
  5. Starts Django dev server
  6. Exposes port 8000
  → Ready in ~3-5 minutes!

./stop.sh runs:
  1. Backs up database file
  2. Stops container
  3. Preserves all data
  → Complete in ~5 seconds
```

## Why This Architecture?

✅ **Simple**: One Docker container, one command
✅ **Fast**: Development server (enough for 30-50 users)
✅ **Portable**: Works on any OS with Docker
✅ **Data Safe**: SQLite file you can copy/backup
✅ **No External Dependencies**: No PostgreSQL, Redis, etc.
✅ **Easy Reset**: Delete container, start fresh
✅ **Perfect for Thesis**: All data in one file

## What You DON'T Need

❌ Nginx/Apache (overkill)
❌ PostgreSQL (SQLite is fine)
❌ Redis (no caching needed)
❌ Celery (no background tasks)
❌ Load balancer (only 1 server)
❌ Kubernetes (way overkill)
❌ Monitoring tools (logs are enough)

Keep it simple! 🎯

