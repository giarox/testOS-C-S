# Deploy Crawl4AI to Cloud (Free)

Deploy the Crawl4AI Docker container to a cloud service so your GitHub Pages site can access it without localhost.

## 🚀 Option 1: Railway.app (Recommended - Easiest)

**Pros:** Free tier, one-click deploy, automatic HTTPS, no credit card needed
**Limits:** 500 hours/month free

### Deploy Steps:

1. **Sign up at Railway.app**
   - Go to https://railway.app
   - Sign up with GitHub (free)

2. **Deploy Docker Container**
   - Click "New Project"
   - Select "Deploy from Docker Image"
   - Enter image: `unclecode/crawl4ai:latest`
   - Click "Deploy"

3. **Configure Port**
   - Go to your service settings
   - Add environment variable: `PORT=11235`
   - Railway will automatically expose it

4. **Get Public URL**
   - Go to "Settings" → "Networking"
   - Click "Generate Domain"
   - You'll get: `https://your-app-name.railway.app`

5. **Update GitHub Pages**
   - Copy your Railway URL
   - Update `live-demo.html` API URL to: `https://your-app-name.railway.app`

**Deploy Button (Alternative):**
[![Deploy on Railway](https://railway.app/button.svg)](https://railway.app/new/template?template=https://hub.docker.com/r/unclecode/crawl4ai)

---

## 🌐 Option 2: Render.com (Also Free & Easy)

**Pros:** Free tier, simple setup, automatic HTTPS
**Limits:** Spins down after 15min inactivity, slow cold starts

### Deploy Steps:

1. **Sign up at Render.com**
   - Go to https://render.com
   - Sign up with GitHub

2. **Create Web Service**
   - Click "New +" → "Web Service"
   - Select "Deploy an existing image from a registry"
   - Enter image URL: `docker.io/unclecode/crawl4ai:latest`

3. **Configure Service**
   - Name: `crawl4ai-api`
   - Region: Choose closest to you
   - Instance Type: Free
   - Port: `11235`

4. **Deploy**
   - Click "Create Web Service"
   - Wait 5-10 minutes for deployment

5. **Get Public URL**
   - You'll get: `https://crawl4ai-api.onrender.com`

6. **Update GitHub Pages**
   - Update `live-demo.html` API URL to your Render URL

---

## ☁️ Option 3: Fly.io (Free Tier Available)

**Pros:** Good free tier, fast deployment, multiple regions
**Limits:** Requires credit card (not charged on free tier)

### Deploy Steps:

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login**
   ```bash
   flyctl auth signup  # or flyctl auth login
   ```

3. **Create fly.toml**
   ```toml
   app = "crawl4ai-YOUR-NAME"

   [build]
     image = "unclecode/crawl4ai:latest"

   [[services]]
     internal_port = 11235
     protocol = "tcp"

     [[services.ports]]
       handlers = ["http"]
       port = 80

     [[services.ports]]
       handlers = ["tls", "http"]
       port = 443
   ```

4. **Deploy**
   ```bash
   flyctl launch --image unclecode/crawl4ai:latest
   flyctl deploy
   ```

5. **Get URL**
   ```bash
   flyctl info
   # You'll get: https://crawl4ai-YOUR-NAME.fly.dev
   ```

---

## 🎯 Option 4: Use a Public Crawl4AI Instance

If someone has already deployed a public instance, you can use it directly!

**Community Instances** (check if available):
- Ask in Crawl4AI GitHub discussions
- Check Crawl4AI Discord/Community

⚠️ **Warning**: Public instances may have rate limits or be unreliable.

---

## 📝 After Deploying to Cloud

### Update Your GitHub Pages

1. **Edit `docs/live-demo.html`**

Change this line:
```html
<input type="url" id="apiUrl" value="http://localhost:11235" placeholder="http://localhost:11235">
```

To your cloud URL:
```html
<input type="url" id="apiUrl" value="https://your-app.railway.app" placeholder="https://your-app.railway.app">
```

2. **Commit and push**
```bash
git add docs/live-demo.html
git commit -m "Update API URL to cloud deployment"
git push origin claude/test-crawl4ai-scraper-15uh9
```

3. **Wait 2 minutes** for GitHub Pages to rebuild

4. **Test it!**
   - Visit: https://giarox.github.io/testOS-C-S/live-demo.html
   - Click "Test Crawl4AI"
   - Everything works online! ✅

---

## 🎉 Complete Online Solution

With cloud deployment, you get:

✅ **No Docker locally** - Runs in the cloud
✅ **No localhost** - Public HTTPS URL
✅ **GitHub Pages works** - No CORS issues
✅ **Always available** - 24/7 uptime
✅ **Free tier** - No cost for basic usage
✅ **Shareable** - Anyone can use your demo

### Full Stack:
```
User → GitHub Pages → Cloud API (Railway/Render) → Crawl4AI → Web Scraping
```

Everything runs online, nothing local needed! 🌐

---

## 💰 Cost Comparison

| Service | Free Tier | Limitations | Best For |
|---------|-----------|-------------|----------|
| **Railway** | 500 hrs/month | Good limits | Recommended |
| **Render** | Unlimited | Sleeps after 15min | Low usage |
| **Fly.io** | 3 VMs | Need credit card | Production |
| **Localhost** | Unlimited | Local only | Development |

---

## 🔒 Security Considerations

When deploying publicly:

1. **Add API Key Authentication** (optional but recommended)
2. **Rate Limiting** - Prevent abuse
3. **Allowlist Origins** - Only your GitHub Pages domain
4. **Monitor Usage** - Check if someone is abusing your API

For the free demo, basic deployment without auth is fine. For production, add security.

---

## 🆘 Troubleshooting

### Railway Deployment Issues
- Check logs: `railway logs`
- Verify port: Should be 11235
- Check memory: May need to upgrade plan

### Render Deployment Issues
- Cold starts are slow (15-30 seconds first request)
- May need to "ping" API regularly to keep it warm
- Check service logs in dashboard

### CORS Issues
- Make sure API URL is HTTPS (not HTTP)
- Check if API returns proper CORS headers
- May need to configure CORS in Crawl4AI

---

## ✨ Quick Start Summary

**Fastest path to fully online demo:**

1. Sign up at Railway.app (2 minutes)
2. Deploy Docker image: `unclecode/crawl4ai:latest` (5 minutes)
3. Get public URL: `https://your-app.railway.app` (instant)
4. Update GitHub Pages API URL (1 minute)
5. Push to GitHub (1 minute)
6. **Done!** - Fully online, no local setup needed

**Total time:** ~10 minutes to go from zero to fully online demo! 🚀
