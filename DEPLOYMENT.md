# Deployment Guide

This guide will help you deploy the Organization Management Service to Render (free hosting).

## Prerequisites

1. GitHub account with the repository pushed
2. Render account (free at https://render.com)
3. MongoDB Atlas account (free at https://www.mongodb.com/cloud/atlas)

## Step 1: Set Up MongoDB Atlas (Free Cloud Database)

1. **Sign up for MongoDB Atlas**
   - Go to https://www.mongodb.com/cloud/atlas/register
   - Create a free account

2. **Create a Free Cluster**
   - Click "Build a Database"
   - Choose "FREE" (M0) tier
   - Select a cloud provider and region (choose closest to you)
   - Name your cluster (e.g., "organization-service")
   - Click "Create"

3. **Create Database User**
   - Go to "Database Access" in the left menu
   - Click "Add New Database User"
   - Choose "Password" authentication
   - Username: `admin` (or your choice)
   - Password: Create a strong password (save it!)
   - Database User Privileges: "Atlas admin"
   - Click "Add User"

4. **Configure Network Access**
   - Go to "Network Access" in the left menu
   - Click "Add IP Address"
   - Click "Allow Access from Anywhere" (0.0.0.0/0) for development
   - Click "Confirm"

5. **Get Connection String**
   - Go to "Database" → Click "Connect" on your cluster
   - Choose "Connect your application"
   - Copy the connection string
   - Replace `<password>` with your database user password
   - Example: `mongodb+srv://admin:yourpassword@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority`

## Step 2: Deploy to Render

1. **Sign up for Render**
   - Go to https://render.com
   - Sign up with your GitHub account

2. **Create New Web Service**
   - Click "New +" → "Web Service"
   - Connect your GitHub account if not already connected
   - Select repository: `raghavkapoor31/Organization-Management-Service`
   - Click "Connect"

3. **Configure Service**
   - **Name**: `organization-management-service` (or your choice)
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt`
   - **Start Command**: `uvicorn app.main:app --host 0.0.0.0 --port $PORT`
   - **Plan**: Select "Free" plan

4. **Set Environment Variables**
   Click "Advanced" → "Add Environment Variable" and add:
   
   - **MONGODB_URL**: Paste your MongoDB Atlas connection string
     - Example: `mongodb+srv://admin:password@cluster0.xxxxx.mongodb.net/?retryWrites=true&w=majority`
   
   - **MASTER_DB_NAME**: `master_db`
   
   - **JWT_SECRET_KEY**: Generate a random secret key
     - You can use: `openssl rand -hex 32` or any random string
   
   - **JWT_ALGORITHM**: `HS256`
   
   - **JWT_EXPIRATION_HOURS**: `24`

5. **Deploy**
   - Click "Create Web Service"
   - Render will automatically build and deploy your application
   - Wait for deployment to complete (usually 2-5 minutes)

6. **Get Your Live URL**
   - Once deployed, you'll see a URL like: `https://organization-management-service.onrender.com`
   - This is your live API endpoint!

## Step 3: Test Your Deployment

1. **Check Health**
   ```
   https://your-app-name.onrender.com/health
   ```

2. **View API Documentation**
   ```
   https://your-app-name.onrender.com/docs
   ```

3. **Test API Endpoints**
   - Use the Swagger UI at `/docs` to test all endpoints
   - Or use curl/Postman with your live URL

## Troubleshooting

### Common Issues

1. **Build Fails**
   - Check build logs in Render dashboard
   - Ensure all dependencies are in `requirements.txt`
   - Verify Python version compatibility

2. **Database Connection Fails**
   - Verify MongoDB Atlas IP whitelist includes `0.0.0.0/0`
   - Check connection string has correct password
   - Ensure database user has proper permissions

3. **Application Crashes**
   - Check logs in Render dashboard
   - Verify all environment variables are set
   - Check MongoDB connection string format

### Viewing Logs

- Go to your service in Render dashboard
- Click "Logs" tab to see real-time logs
- Check for any error messages

## Alternative: Railway Deployment

If Render doesn't work, you can also deploy on Railway:

1. Go to https://railway.app
2. Sign up with GitHub
3. Click "New Project" → "Deploy from GitHub repo"
4. Select your repository
5. Add environment variables (same as Render)
6. Railway will auto-detect Python and deploy

## Your Live API Endpoints

Once deployed, your endpoints will be:
- `POST https://your-app.onrender.com/org/create`
- `GET https://your-app.onrender.com/org/get`
- `PUT https://your-app.onrender.com/org/update`
- `DELETE https://your-app.onrender.com/org/delete`
- `POST https://your-app.onrender.com/admin/login`
- `GET https://your-app.onrender.com/docs` (API Documentation)

## Notes

- Free tier on Render may spin down after inactivity (takes ~30 seconds to wake up)
- MongoDB Atlas free tier has 512MB storage (enough for development)
- Keep your MongoDB connection string and JWT secret secure
- Don't commit `.env` files to GitHub

