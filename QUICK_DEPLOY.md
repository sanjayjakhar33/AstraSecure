# 🚀 Quick Deploy AstraSecure to Vercel

Deploy AstraSecure cybersecurity platform to Vercel in **under 10 minutes** with this single-step guide.

## ⚡ Super Quick Start

1. **Clone and navigate:**
   ```bash
   git clone https://github.com/sanjayjakhar33/AstraSecure.git
   cd AstraSecure
   ```

2. **Run the automated deployment:**
   ```bash
   ./deploy-to-vercel.sh
   ```

3. **Follow the interactive prompts** to set up:
   - Database (PostgreSQL on Neon/Supabase)
   - Backend (Python API on Railway/Render)
   - Frontend (React app on Vercel)

That's it! 🎉

## 📋 What You'll Need (2 minutes to set up)

**Free Accounts (click to create):**
- [Vercel](https://vercel.com) - Frontend hosting
- [Railway](https://railway.app) - Backend hosting  
- [Neon](https://neon.tech) - PostgreSQL database

## 🏗️ What Gets Deployed

- **Frontend**: React dashboard on Vercel (free)
- **Backend**: Python FastAPI on Railway (~$5/month)
- **Database**: PostgreSQL on Neon (free tier: 3GB)
- **Security**: HTTPS, security headers, CORS configured
- **Features**: User auth, vulnerability scanning, compliance tracking

## 💰 Cost

- **Free tier**: ~$5/month (just for backend hosting)
- **Production ready**: All services included
- **Scales automatically**: Handle thousands of users

## 🔧 Manual Steps (if you prefer)

### 1. Database Setup (2 min)
```bash
# Create Neon database
# 1. Visit https://neon.tech → Create project
# 2. Copy connection string
# 3. Run database setup:
./setup-cloud-database.sh "postgresql://user:pass@host:port/db"
```

### 2. Backend Deployment (3 min)
```bash
# Deploy to Railway
# 1. Visit https://railway.app → Connect GitHub
# 2. Deploy backend_python folder
# 3. Copy the generated URL
```

### 3. Frontend Deployment (2 min)
```bash
# Deploy to Vercel
npm install -g vercel
vercel login
vercel --prod
```

## ✅ Post-Deployment

Your app will be live at: `https://your-app.vercel.app`

**Test everything works:**
1. Open the URL
2. Register a new account
3. Explore the security dashboard
4. Run a test vulnerability scan

## 🆘 Need Help?

- **Issues**: [GitHub Issues](https://github.com/sanjayjakhar33/AstraSecure/issues)
- **Full Guide**: [VERCEL_DEPLOYMENT.md](./VERCEL_DEPLOYMENT.md)
- **Documentation**: [README.md](./README.md)

## 🔒 Security Features

- Multi-tenant architecture
- Role-based access control
- Automated vulnerability scanning
- Compliance framework support
- Real-time security dashboard
- PDF/CSV report generation

---

**Ready to secure your infrastructure? Run `./deploy-to-vercel.sh` now! 🚀**