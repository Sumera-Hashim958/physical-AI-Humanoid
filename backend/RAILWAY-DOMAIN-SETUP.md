# Railway Public Domain Setup

## If you don't see a public URL:

### Steps to Generate Railway Domain:

1. **Railway Dashboard** → Open your service
2. **Settings** tab → Scroll to **Networking** section
3. Click **Generate Domain** button
4. Railway will create: `your-service-name.up.railway.app`
5. Wait 1-2 minutes for DNS propagation

### Alternative - Custom Domain:

1. **Settings** → **Networking** → **Custom Domain**
2. Add your own domain (e.g., `api.yourdomain.com`)
3. Configure DNS records as shown

## Once Domain is Active:

Test your endpoints:

```bash
# Replace with your actual Railway URL
export API_URL="https://your-app.up.railway.app"

# Health check
curl $API_URL/api/health

# API root
curl $API_URL/

# API documentation (browser)
# https://your-app.up.railway.app/docs
```

## Troubleshooting:

### "This site can't be reached"
- Check that domain is generated in Settings → Networking
- Wait 2-3 minutes for DNS to propagate
- Check deployment logs for startup errors

### Port Configuration:
Railway automatically sets `$PORT` environment variable.
Our `main.py` already handles this:
```python
port = int(os.getenv("PORT", 8000))
uvicorn.run(app, host="0.0.0.0", port=port)
```

### Health Check Failing:
- Check Railway logs for errors
- Verify environment variables are set
- Ensure DATABASE_URL is accessible
