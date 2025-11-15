# 🚀 DEPLOYMENT GUIDE - Django Travel Blog AI

## Quick Setup (3 Commands)

### 1. Export your ngrok token
```bash
export NGROK_AUTHTOKEN=35WrFWkmLqDuL22yKHTo99tbkik_6La2zP9rrdThFmRYDfsse
```

### 2. Make scripts executable
```bash
chmod +x deploy-secure.sh stop-ngrok.sh
```

### 3. Deploy
```bash
./deploy-secure.sh
```

**Done!** In 30 seconds you'll get a public URL to share with students.

---

## 🎓 For Your Class

### Before Class
```bash
./deploy-secure.sh
```

Copy the URL shown (example: `https://random-name.ngrok-free.dev`)

### During Class
Share the URL with students. They can:
- Browse travel blog posts
- View posts on interactive map
- Rate posts (1-5 stars)
- Leave comments
- **No login required**

### You Can Access Admin Panel
- **URL**: `https://your-url.ngrok-free.dev/admin`
- **Username**: `admin`
- **Password**: `admin123`
- **Create AI posts**: `/ai/add/` (choose Gemini, ChatGPT, or DeepSeek)

### After Class
```bash
./stop-ngrok.sh
```

Your data is saved in:
- `db.sqlite3` (main database)
- `db_backup_TIMESTAMP.sqlite3` (automatic backup)

---

## 🔒 Security

Your real IP is **COMPLETELY HIDDEN**.

Students only see: `https://random-name.ngrok-free.dev`

They **cannot** see:
- ❌ Your real IP address
- ❌ Your home network
- ❌ Your location
- ❌ Your computer details

---

## 📊 Monitor During Class (Optional)

### View traffic dashboard
Open in browser: `http://localhost:4040`

### View Django logs
```bash
docker logs -f django_travel_blog
```

### Check if running
```bash
docker ps
```

---

## 🆘 Troubleshooting

### URL doesn't work
```bash
# Restart everything:
docker stop django_travel_blog ngrok_tunnel
docker rm django_travel_blog ngrok_tunnel
./deploy-secure.sh
```

### Can't see the URL
```bash
# Get it manually:
curl http://localhost:4040/api/tunnels | grep public_url
```

### Students see warning page
The middleware should fix this. If not:
```bash
docker restart django_travel_blog
```

### Port 8000 already in use
```bash
sudo lsof -ti:8000 | xargs kill -9
./deploy-secure.sh
```

---

## 💾 Your Thesis Data

All student ratings, comments, and interactions are saved in `db.sqlite3`.

**Tables you need:**
- `blog_post` - All blog posts with AI model attribution
- `blog_rating` - Student ratings (1-5 stars) and comments
- `blog_aiprompt` - AI prompts you used

**To analyze:**
- Use SQLite Browser (free download)
- Or Django admin panel: `/admin`
- Or Python scripts to export data

---

## ✅ Pre-Class Checklist

- [ ] `.env` file has your API keys (OpenAI, Gemini, DeepSeek)
- [ ] Exported NGROK_AUTHTOKEN
- [ ] Ran `./deploy-secure.sh`
- [ ] Got the public URL
- [ ] Tested it in browser (loads without warning)
- [ ] Created 5-10 AI posts with different models
- [ ] Tested rating a post
- [ ] Ready to share URL with students

---

## 🎯 Complete Workflow Summary

```
Before class:
  export NGROK_AUTHTOKEN=your_token
  ./deploy-secure.sh
  → Copy URL shown

During class (1 hour):
  Share URL with students
  Students browse and rate posts
  Monitor: http://localhost:4040

After class:
  ./stop-ngrok.sh
  → Database auto-backed up
  → Your IP no longer exposed
```

---

## 📝 Important Notes

- **ngrok URL changes** each time you deploy (unless you have paid plan)
- **Free tier limit**: URL expires after 2 hours of inactivity
- **Your API keys** stay secure inside the Docker container
- **Database** is persistent - data survives restarts
- **Static files** are automatically collected

---

## 🔧 Advanced (If Needed)

### Update API keys
Edit `.env` file, then restart:
```bash
docker restart django_travel_blog
```

### Create admin user manually
```bash
docker exec -it django_travel_blog python manage.py createsuperuser
```

### Access Django shell
```bash
docker exec -it django_travel_blog python manage.py shell
```

### Export data for analysis
```bash
docker exec -it django_travel_blog python manage.py dumpdata blog > thesis_data.json
```

### View database directly
```bash
sqlite3 db.sqlite3
```

---

## 🎉 You're Ready!

**Deployment is now 3 commands:**
1. `export NGROK_AUTHTOKEN=...`
2. `chmod +x deploy-secure.sh stop-ngrok.sh`
3. `./deploy-secure.sh`

**Your IP is hidden, students can access, thesis data collected. Good luck! 🎓**

---

*For issues: Check `docker logs django_travel_blog` or `docker logs ngrok_tunnel`*

