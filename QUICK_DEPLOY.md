# Quick Deploy Guide

## 🚀 Deploy to Render (Easiest - 5 minutes)

### Step 1: Setup MongoDB Atlas (Free)
1. Go to https://www.mongodb.com/cloud/atlas
2. Sign up for free account
3. Create a free cluster (M0)
4. Click "Connect" → "Connect your application"
5. Copy the connection string (looks like: `mongodb+srv://username:password@cluster.mongodb.net/`)

### Step 2: Deploy to Render
1. Go to https://render.com
2. Sign up with GitHub
3. Click "New +" → "Web Service"
4. Connect repository: `raghavkapoor31/Organization-Management-Service`
5. Configure:
   - **Name**: `organization-management-service`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
6. Add Environment Variables:
   - `MONGODB_URL`: (paste your MongoDB Atlas connection string)
   - `MASTER_DB_NAME`: `master_db`
   - `JWT_SECRET_KEY`: (generate a random string)
   - `JWT_ALGORITHM`: `HS256`
   - `JWT_EXPIRATION_HOURS`: `24`
7. Click "Create Web Service"
8. Wait 2-3 minutes for deployment
9. Your API will be live at: `https://your-app-name.onrender.com`

### Step 3: Test Your API
- Visit: `https://your-app-name.onrender.com/docs`
- Test the endpoints!

## 🎯 Alternative: Railway (Also Easy)

1. Go to https://railway.app
2. Sign up with GitHub
3. "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables (same as Render)
6. Railway auto-detects Python and deploys
7. Your API: `https://your-app-name.up.railway.app`

## 📝 After Deployment

1. **Update README.md** with your live URL
2. **Test all endpoints** using the Swagger UI
3. **Share the link** in your assignment submission

## 🔗 Your Live API Will Have:

- ✅ HTTPS/SSL certificate (automatic)
- ✅ Public URL (shareable)
- ✅ Auto-deploy on every GitHub push
- ✅ Free tier (with some limitations)

## 💡 Pro Tips

- Render free tier spins down after 15 min of inactivity (first request may be slow)
- For always-on, consider Railway or upgrade Render plan
- MongoDB Atlas free tier is perfect for development/testing

