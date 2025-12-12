# Deployment Guide

This guide explains how to deploy the Organization Management Service to various hosting platforms.

## Option 1: Render (Recommended - Free Tier Available)

Render offers a free tier perfect for this application.

### Steps:

1. **Create a Render Account**
   - Go to https://render.com
   - Sign up with your GitHub account

2. **Create a New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub repository: `raghavkapoor31/Organization-Management-Service`
   - Select the repository

3. **Configure the Service**
   - **Name**: `organization-management-service`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Free

4. **Set Environment Variables**
   - `MONGODB_URL`: Your MongoDB connection string (use MongoDB Atlas free tier)
   - `MASTER_DB_NAME`: `master_db`
   - `JWT_SECRET_KEY`: Generate a secure random string
   - `JWT_ALGORITHM`: `HS256`
   - `JWT_EXPIRATION_HOURS`: `24`

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically deploy on every push to main branch

### MongoDB Setup (MongoDB Atlas - Free)

1. Go to https://www.mongodb.com/cloud/atlas
2. Create a free account
3. Create a free cluster (M0)
4. Get your connection string
5. Add your Render app's IP to MongoDB Atlas IP whitelist (or use 0.0.0.0/0 for development)

## Option 2: Railway

Railway offers easy deployment with GitHub integration.

### Steps:

1. **Create a Railway Account**
   - Go to https://railway.app
   - Sign up with GitHub

2. **Create New Project**
   - Click "New Project"
   - Select "Deploy from GitHub repo"
   - Choose `raghavkapoor31/Organization-Management-Service`

3. **Configure Environment Variables**
   - Add all required environment variables (same as Render)

4. **Deploy**
   - Railway will auto-detect Python and deploy
   - Service will be live at `https://your-app-name.up.railway.app`

## Option 3: Fly.io

Fly.io offers global deployment.

### Steps:

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   fly auth login
   ```

3. **Launch App**
   ```bash
   fly launch
   ```

4. **Set Secrets**
   ```bash
   fly secrets set MONGODB_URL="your-mongodb-url"
   fly secrets set JWT_SECRET_KEY="your-secret-key"
   ```

## Option 4: PythonAnywhere

Good for Python-specific hosting.

### Steps:

1. Create account at https://www.pythonanywhere.com
2. Upload your code via Git
3. Configure web app
4. Set environment variables
5. Reload web app

## Option 5: Heroku (Paid, but has free alternatives)

1. Install Heroku CLI
2. Create `Procfile` (already created)
3. Deploy:
   ```bash
   heroku create your-app-name
   heroku config:set MONGODB_URL=your-url
   git push heroku main
   ```

## Environment Variables Required

All platforms need these environment variables:

```bash
MONGODB_URL=mongodb+srv://username:password@cluster.mongodb.net/?retryWrites=true&w=majority
MASTER_DB_NAME=master_db
JWT_SECRET_KEY=your-secret-key-here
JWT_ALGORITHM=HS256
JWT_EXPIRATION_HOURS=24
```

## Quick Deploy Script

For Render, you can use the included `render.yaml`:

1. Go to Render Dashboard
2. Click "New" → "Blueprint"
3. Connect your GitHub repo
4. Render will auto-detect `render.yaml` and configure everything

## Post-Deployment

After deployment:

1. **Test the API**
   - Visit `https://your-app-url.onrender.com/docs` (or your platform's URL)
   - Test the endpoints

2. **Update README**
   - Add your live API URL to the README
   - Update example curl commands with your URL

3. **Monitor**
   - Check logs for any errors
   - Monitor MongoDB connection

## Troubleshooting

### Common Issues:

1. **MongoDB Connection Failed**
   - Check MongoDB Atlas IP whitelist
   - Verify connection string format
   - Ensure network access is enabled

2. **Port Issues**
   - Make sure you're using `$PORT` environment variable
   - Render/Railway provide this automatically

3. **Dependencies Not Found**
   - Ensure `requirements.txt` is up to date
   - Check Python version compatibility

## GitHub Actions CI/CD

The repository includes a GitHub Actions workflow (`.github/workflows/deploy.yml`) that:
- Runs on every push to main
- Tests the application
- Can trigger deployments (configure webhooks)

## Recommended Setup

For the best free hosting experience:

1. **MongoDB**: Use MongoDB Atlas (Free M0 tier)
2. **Backend**: Use Render (Free tier, auto-deploys from GitHub)
3. **CI/CD**: GitHub Actions (already configured)

This gives you:
- ✅ Free hosting
- ✅ Automatic deployments
- ✅ HTTPS/SSL certificates
- ✅ Custom domain support (optional)
- ✅ Environment variable management

