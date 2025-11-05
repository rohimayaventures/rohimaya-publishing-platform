# 🎨 Rohimaya Publishing - Streamlit Cloud Setup

Step-by-step guide to deploy all 7 Streamlit apps to Streamlit Cloud.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Streamlit Cloud Account Setup](#streamlit-cloud-account-setup)
4. [Per-App Deployment](#per-app-deployment)
5. [Secrets Management](#secrets-management)
6. [Custom Domains](#custom-domains)
7. [Environment Variables](#environment-variables)
8. [Debugging & Troubleshooting](#debugging--troubleshooting)
9. [Performance Optimization](#performance-optimization)
10. [Cost Considerations](#cost-considerations)

---

## Overview

Deploy these 7 AI-powered writing tools:
1. AI Writing Assistant
2. Manuscript Formatter
3. AI Cover Designer
4. Audiobook Generator
5. Plot Outliner
6. Character Creator
7. Marketing Copy Generator

---

## Prerequisites

### Required
- ✅ GitHub account
- ✅ Repository pushed to GitHub
- ✅ All API keys ready
- ✅ Email for Streamlit Cloud account

### Repository Structure
```
streamlit-apps/
├── ai-writing-assistant/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
├── manuscript-formatter/
│   ├── app.py
│   ├── requirements.txt
│   └── README.md
[... 5 more apps ...]
```

---

## Streamlit Cloud Account Setup

### Step 1: Create Account

1. Go to https://share.streamlit.io/
2. Click "Sign up"
3. Sign up with GitHub OAuth
4. Authorize Streamlit to access repositories
5. Verify email address

### Step 2: Connect GitHub Repository

1. Click "New app"
2. Select repository: `rohimayaventures/rohimaya-publishing-platform`
3. Allow Streamlit access to the repository
4. Confirm connection

---

## Per-App Deployment

### App 1: AI Writing Assistant

**Step 1: Create New App**
1. Click "New app" in Streamlit Cloud dashboard
2. Repository: `rohimayaventures/rohimaya-publishing-platform`
3. Branch: `main`
4. Main file path: `streamlit-apps/ai-writing-assistant/app.py`
5. App URL (custom): `rohimaya-ai-writing-assistant`

**Step 2: Advanced Settings**
- Python version: `3.11`
- Click "Advanced settings"
- Add custom requirements if needed

**Step 3: Add Secrets**
Click "Advanced settings" → "Secrets"

```toml
[anthropic]
api_key = "sk-ant-api03-xxxxx"
```

**Step 4: Deploy**
- Click "Deploy!"
- Wait for build (2-5 minutes)
- Test app once deployed

**App URL:** `https://rohimaya-ai-writing-assistant.streamlit.app`

---

### App 2: Manuscript Formatter

**Deployment Settings:**
- Repository: `rohimayaventures/rohimaya-publishing-platform`
- Branch: `main`
- Main file: `streamlit-apps/manuscript-formatter/app.py`
- URL: `rohimaya-manuscript-formatter`

**Secrets:**
```toml
[anthropic]
api_key = "sk-ant-api03-xxxxx"
```

**App URL:** `https://rohimaya-manuscript-formatter.streamlit.app`

---

### App 3: AI Cover Designer

**Deployment Settings:**
- Main file: `streamlit-apps/ai-cover-designer/app.py`
- URL: `rohimaya-ai-cover-designer`

**Secrets:**
```toml
[openai]
api_key = "sk-xxxxx"
```

**App URL:** `https://rohimaya-ai-cover-designer.streamlit.app`

---

### App 4: Audiobook Generator

**Deployment Settings:**
- Main file: `streamlit-apps/audiobook-generator/app.py`
- URL: `rohimaya-audiobook-generator`

**Secrets:**
```toml
[prasad_tts]
endpoint_url = "https://your-tts-endpoint/api/generate"
api_key = "optional"

[elevenlabs]
api_key = "your_elevenlabs_key"

[openai]
api_key = "sk-xxxxx"
```

**App URL:** `https://rohimaya-audiobook-generator.streamlit.app`

---

### App 5: Plot Outliner

**Deployment Settings:**
- Main file: `streamlit-apps/plot-outliner/app.py`
- URL: `rohimaya-plot-outliner`

**Secrets:**
```toml
[anthropic]
api_key = "sk-ant-api03-xxxxx"
```

**App URL:** `https://rohimaya-plot-outliner.streamlit.app`

---

### App 6: Character Creator

**Deployment Settings:**
- Main file: `streamlit-apps/character-creator/app.py`
- URL: `rohimaya-character-creator`

**Secrets:**
```toml
[anthropic]
api_key = "sk-ant-api03-xxxxx"

[openai]
api_key = "sk-xxxxx"
```

**App URL:** `https://rohimaya-character-creator.streamlit.app`

---

### App 7: Marketing Copy Generator

**Deployment Settings:**
- Main file: `streamlit-apps/marketing-copy-generator/app.py`
- URL: `rohimaya-marketing-copy`

**Secrets:**
```toml
[anthropic]
api_key = "sk-ant-api03-xxxxx"
```

**App URL:** `https://rohimaya-marketing-copy.streamlit.app`

---

## Secrets Management

### Best Practices

1. **Never commit secrets to GitHub**
   - Use `.streamlit/secrets.toml` locally
   - Add to `.gitignore`
   - Add secrets via Streamlit Cloud UI

2. **Rotate keys regularly**
   - Every 90 days minimum
   - Immediately if compromised
   - Update in Streamlit Cloud dashboard

3. **Use different keys per environment**
   - Development: Test API keys
   - Production: Live API keys
   - Separate Streamlit Cloud workspaces if needed

### Adding Secrets to Deployed Apps

1. Go to app dashboard
2. Click "Settings" (⚙️)
3. Click "Secrets" in sidebar
4. Paste TOML-formatted secrets
5. Click "Save"
6. App will restart automatically

### Updating Secrets

1. Go to app settings
2. Edit secrets
3. Save changes
4. App restarts with new secrets
5. Test app to confirm changes

---

## Custom Domains

### Streamlit Cloud Pro Feature

**Requirements:**
- Streamlit Cloud Pro plan ($250/month team plan)
- Domain ownership verification
- DNS access

**Setup Steps:**

1. **In Streamlit Cloud:**
   - App Settings → General
   - Click "Custom subdomain"
   - Enter: `tools.rohimayapublishing.com`
   - Get verification TXT record

2. **In DNS Provider:**
   - Add TXT record for verification
   - Add CNAME record:
     ```
     tools.rohimayapublishing.com → xxx.streamlit.app
     ```

3. **Verify:**
   - Wait for DNS propagation (up to 48 hours)
   - Streamlit auto-provisions SSL certificate
   - Custom domain active

### Alternative: URL Redirects

If on free plan, use redirects:

```javascript
// On your website
const appUrls = {
  'ai-assistant': 'https://rohimaya-ai-writing-assistant.streamlit.app',
  'formatter': 'https://rohimaya-manuscript-formatter.streamlit.app',
  'cover': 'https://rohimaya-ai-cover-designer.streamlit.app',
  'audiobook': 'https://rohimaya-audiobook-generator.streamlit.app',
  'outliner': 'https://rohimaya-plot-outliner.streamlit.app',
  'character': 'https://rohimaya-character-creator.streamlit.app',
  'marketing': 'https://rohimaya-marketing-copy.streamlit.app'
};
```

---

## Environment Variables

### Set via Secrets

All environment variables go in secrets.toml format:

```toml
# API Keys
[anthropic]
api_key = "sk-ant-xxxxx"

[openai]
api_key = "sk-xxxxx"

# App Configuration
[app]
environment = "production"
debug_mode = false
max_file_size = 10485760  # 10MB

# Feature Flags
[features]
enable_analytics = true
enable_feedback = true
show_beta_features = false
```

### Access in Code

```python
import streamlit as st

# Access secrets
api_key = st.secrets["anthropic"]["api_key"]
debug = st.secrets.get("app", {}).get("debug_mode", False)
```

---

## Debugging & Troubleshooting

### View Logs

1. Go to app dashboard
2. Click "Manage app"
3. Scroll to "Logs" section
4. View real-time logs
5. Download logs for analysis

### Common Issues

**1. "Module not found" Error**

**Cause:** Missing dependency in requirements.txt

**Fix:**
```bash
# Locally add missing package
pip install package-name
pip freeze > requirements.txt
# Commit and push
git add requirements.txt
git commit -m "Add missing dependency"
git push
```

**2. "Secrets not configured" Warning**

**Cause:** Missing API keys

**Fix:**
- Go to app settings
- Add secrets in TOML format
- Save and restart

**3. "App taking too long to load"**

**Cause:** Large dependencies or slow API calls

**Fix:**
```python
# Add caching
@st.cache_data
def load_model():
    return expensive_operation()

@st.cache_resource
def get_api_client():
    return client_initialization()
```

**4. "Memory limit exceeded"**

**Cause:** Large file processing or memory leaks

**Fix:**
- Process files in chunks
- Use generators instead of lists
- Clear session state when done
- Upgrade to paid plan for more resources

**5. "Rate limit exceeded"**

**Cause:** Too many API calls

**Fix:**
```python
# Add rate limiting
import time
from functools import wraps

def rate_limit(calls_per_minute):
    min_interval = 60.0 / calls_per_minute
    last_called = [0.0]

    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            wait = min_interval - elapsed
            if wait > 0:
                time.sleep(wait)
            result = func(*args, **kwargs)
            last_called[0] = time.time()
            return result
        return wrapper
    return decorator
```

### Debugging Locally

```bash
# Run app locally
cd streamlit-apps/ai-writing-assistant
streamlit run app.py

# With specific port
streamlit run app.py --server.port 8502

# With debug mode
streamlit run app.py --server.enableCORS false --server.enableXsrfProtection false
```

---

## Performance Optimization

### 1. Caching Strategies

```python
# Cache data that doesn't change
@st.cache_data(ttl=3600)  # Cache for 1 hour
def load_static_data():
    return expensive_data_load()

# Cache resources (connections, models)
@st.cache_resource
def get_anthropic_client():
    return anthropic.Anthropic(api_key=st.secrets["anthropic"]["api_key"])
```

### 2. Lazy Loading

```python
# Load components only when needed
if st.button("Generate"):
    with st.spinner("Loading..."):
        result = generate_content()
```

### 3. Session State Management

```python
# Efficient session state usage
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None

# Clear state when done
if st.button("Clear"):
    st.session_state.clear()
```

### 4. Reduce Redundant Calls

```python
# Bad: Calls on every rerun
data = expensive_api_call()

# Good: Only calls when needed
if 'data' not in st.session_state:
    st.session_state.data = expensive_api_call()
data = st.session_state.data
```

---

## Cost Considerations

### Streamlit Cloud Pricing

**Community (Free):**
- 1 private app
- Unlimited public apps
- 1 GB RAM per app
- 1 CPU core
- **Cost:** $0

**Team Plan:**
- Unlimited private apps
- 3 editors + unlimited viewers
- Custom domains
- Priority support
- **Cost:** $250/month

### Resource Usage

**Per App Estimated:**
- Small app (< 100 users/day): Free tier sufficient
- Medium app (100-1000 users/day): May hit limits
- Large app (1000+ users/day): Need paid plan

### Optimization for Free Tier

1. **Combine Apps:**
   - Create multi-page app instead of 7 separate apps
   - Use st.sidebar for navigation

2. **Efficient Caching:**
   - Cache everything possible
   - Use TTL to prevent stale data

3. **Minimize Dependencies:**
   - Only include required packages
   - Use lightweight alternatives

---

## Monitoring & Analytics

### Built-in Metrics

Streamlit Cloud provides:
- App health status
- Resource usage (RAM, CPU)
- Error rates
- Uptime percentage

### Custom Analytics

```python
# Add Google Analytics
import streamlit.components.v1 as components

components.html("""
    <!-- Global site tag (gtag.js) - Google Analytics -->
    <script async src="https://www.googletagmanager.com/gtag/js?id=G-XXXXXXXXXX"></script>
    <script>
        window.dataLayer = window.dataLayer || [];
        function gtag(){dataLayer.push(arguments);}
        gtag('js', new Date());
        gtag('config', 'G-XXXXXXXXXX');
    </script>
""")
```

### User Feedback

```python
# Add feedback widget
feedback = st.radio("Was this helpful?", ["👍 Yes", "👎 No"])
if feedback == "👎 No":
    comment = st.text_area("What went wrong?")
    if st.button("Submit Feedback"):
        # Log to database or analytics
        pass
```

---

## Deployment Checklist

Per app, verify:
- [ ] App deployed successfully
- [ ] All secrets configured
- [ ] App loads without errors
- [ ] All features work correctly
- [ ] API calls successful
- [ ] Error handling works
- [ ] UI looks correct
- [ ] Mobile responsive
- [ ] Load time acceptable (< 5 seconds)
- [ ] Documentation updated with URL

---

## Support Resources

- **Streamlit Docs:** https://docs.streamlit.io
- **Community Forum:** https://discuss.streamlit.io
- **GitHub Issues:** https://github.com/streamlit/streamlit/issues
- **Rohimaya Support:** rohimayapublishing@gmail.com

---

🦚 **Rohimaya Publishing**
*Ascend • Flourish • Enlighten*
