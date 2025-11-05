# 🚀 Rohimaya Publishing - Deployment Guide

Complete deployment guide for the Rohimaya Publishing platform.

## Table of Contents

1. [Overview](#overview)
2. [Prerequisites](#prerequisites)
3. [Environment Setup](#environment-setup)
4. [Database Configuration](#database-configuration)
5. [API Services Setup](#api-services-setup)
6. [Streamlit Apps Deployment](#streamlit-apps-deployment)
7. [n8n Workflows Deployment](#n8n-workflows-deployment)
8. [DNS & SSL Configuration](#dns--ssl-configuration)
9. [Monitoring & Logging](#monitoring--logging)
10. [Backup Strategies](#backup-strategies)
11. [Scaling Considerations](#scaling-considerations)

---

## Overview

The Rohimaya Publishing platform consists of:
- **7 Streamlit Applications** - AI-powered writing tools
- **5 n8n Workflows** - Business automation
- **1 Next.js Website** - Marketing and landing pages
- **Database** - Supabase PostgreSQL
- **External APIs** - Anthropic, OpenAI, ElevenLabs, Stripe

## Prerequisites

### Required Accounts
- ✅ GitHub account (for code repository)
- ✅ Streamlit Cloud account (for app hosting)
- ✅ Supabase account (for database)
- ✅ n8n Cloud or VPS (for workflows)
- ✅ Vercel or Cloudflare Pages (for website)
- ✅ Domain registrar access (for DNS)

### API Keys Required
- Anthropic Claude API key
- OpenAI API key (GPT-4 + DALL-E 3)
- ElevenLabs API key (optional)
- Stripe API keys (live + test)
- SendGrid API key
- Slack webhook URLs

### Development Tools
- Git
- Node.js 18+ (for website)
- Python 3.8+ (for local testing)
- Terminal/command line access

---

## Environment Setup

### 1. Clone Repository

```bash
git clone https://github.com/rohimayaventures/rohimaya-publishing-platform.git
cd rohimaya-publishing-platform
```

### 2. Set Up Python Environment

```bash
# Create virtual environment
python -m venv venv

# Activate (Linux/Mac)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Install dependencies for all apps
cd streamlit-apps/ai-writing-assistant
pip install -r requirements.txt
# Repeat for each app
```

### 3. Set Up Node.js Environment

```bash
cd website
npm install
```

---

## Database Configuration

### Supabase Setup

1. **Create Project:**
   - Go to https://supabase.com
   - Click "New Project"
   - Name: "rohimaya-publishing"
   - Region: Choose closest to users
   - Database password: Generate strong password

2. **Create Tables:**

```sql
-- Users table
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  email TEXT UNIQUE NOT NULL,
  name TEXT NOT NULL,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  subscription_tier TEXT DEFAULT 'free',
  last_login TIMESTAMP WITH TIME ZONE
);

-- Projects table
CREATE TABLE projects (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  name TEXT NOT NULL,
  description TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);

-- Subscriptions table
CREATE TABLE user_subscriptions (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  subscription_status TEXT NOT NULL,
  subscription_tier TEXT NOT NULL,
  subscription_start TIMESTAMP WITH TIME ZONE,
  subscription_end TIMESTAMP WITH TIME ZONE,
  payment_method TEXT,
  last_payment TIMESTAMP WITH TIME ZONE
);

-- Support tickets table
CREATE TABLE support_tickets (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_email TEXT NOT NULL,
  subject TEXT NOT NULL,
  message TEXT NOT NULL,
  status TEXT DEFAULT 'open',
  priority TEXT DEFAULT 'normal',
  category TEXT,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  resolved_at TIMESTAMP WITH TIME ZONE
);

-- Usage limits table
CREATE TABLE usage_limits (
  id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
  user_id UUID REFERENCES users(id),
  tier TEXT NOT NULL,
  max_projects INT,
  max_exports TEXT,
  features JSONB,
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW()
);
```

3. **Enable Row Level Security (RLS):**

```sql
-- Enable RLS on all tables
ALTER TABLE users ENABLE ROW LEVEL SECURITY;
ALTER TABLE projects ENABLE ROW LEVEL SECURITY;
ALTER TABLE user_subscriptions ENABLE ROW LEVEL SECURITY;

-- Create policies (example for users table)
CREATE POLICY "Users can view their own data"
  ON users FOR SELECT
  USING (auth.uid() = id);

CREATE POLICY "Users can update their own data"
  ON users FOR UPDATE
  USING (auth.uid() = id);
```

4. **Get Connection Details:**
   - Go to Settings > API
   - Copy Project URL
   - Copy anon/public key
   - Copy service_role key (for server-side)

---

## API Services Setup

### 1. Anthropic Claude

1. Go to https://console.anthropic.com/
2. Create account / sign in
3. Go to API Keys
4. Create new key
5. Copy key (starts with `sk-ant-`)
6. Add credits to account

**Cost:** $3 per million input tokens (Claude 3.5 Sonnet)

### 2. OpenAI

1. Go to https://platform.openai.com/
2. Create account / sign in
3. Go to API Keys
4. Create new secret key
5. Copy key (starts with `sk-`)
6. Add payment method and credits

**Cost:**
- GPT-4: $0.03 per 1K input tokens
- DALL-E 3: $0.040 per image (1024x1024)

### 3. ElevenLabs (Optional)

1. Go to https://elevenlabs.io/
2. Create account
3. Go to Settings > API Keys
4. Generate new API key
5. Copy key

**Cost:** ~$0.30 per 1000 characters

### 4. Stripe

1. Go to https://stripe.com/
2. Create account
3. Get API keys from Dashboard > Developers > API keys
4. Copy Publishable key and Secret key
5. Set up test mode first, then live mode

**Cost:** 2.9% + $0.30 per transaction (no API fees)

### 5. SendGrid

1. Go to https://sendgrid.com/
2. Create account (free tier: 100 emails/day)
3. Settings > API Keys
4. Create API key with "Full Access"
5. Verify sender email address

**Cost:** Free tier available, paid starts at $15/month

---

## Streamlit Apps Deployment

### Deploy to Streamlit Cloud

1. **Prepare Repository:**
   - Ensure all apps have `requirements.txt`
   - Ensure secrets.toml.example exists
   - Push to GitHub

2. **For Each App:**

   **AI Writing Assistant:**
   ```bash
   # App settings
   Path: streamlit-apps/ai-writing-assistant/app.py
   Python version: 3.11
   ```

   **Secrets to add:**
   ```toml
   [anthropic]
   api_key = "sk-ant-xxxxx"
   ```

3. **Deploy All 7 Apps:**
   - Go to https://share.streamlit.io/
   - Click "New app"
   - Connect GitHub repository
   - Select branch: `main`
   - Main file path: `streamlit-apps/{app-name}/app.py`
   - Click "Deploy"
   - Add secrets in app settings
   - Repeat for each app

4. **App URLs:**
   ```
   https://rohimaya-ai-writing-assistant.streamlit.app
   https://rohimaya-manuscript-formatter.streamlit.app
   https://rohimaya-ai-cover-designer.streamlit.app
   https://rohimaya-audiobook-generator.streamlit.app
   https://rohimaya-plot-outliner.streamlit.app
   https://rohimaya-character-creator.streamlit.app
   https://rohimaya-marketing-copy.streamlit.app
   ```

5. **Custom Domains (Optional):**
   - Streamlit Cloud Pro required
   - Settings > General > Custom subdomain
   - Or use CNAME DNS records

---

## n8n Workflows Deployment

### Option 1: n8n Cloud (Recommended)

1. **Sign up:**
   - Go to https://n8n.io/cloud/
   - Create account
   - Choose plan ($20/month starter)

2. **Import Workflows:**
   - Click "Workflows"
   - Click "Import from File"
   - Upload each JSON file
   - Configure credentials
   - Activate workflows

3. **Configure Webhooks:**
   - Each workflow has webhook URLs
   - Update URLs in your application
   - Test with Postman or curl

### Option 2: Self-Hosted

1. **Set up VPS:**
   ```bash
   # Install Node.js
   curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
   sudo apt-get install -y nodejs

   # Install n8n globally
   npm install -g n8n

   # Run n8n
   n8n start --tunnel
   ```

2. **Production Setup with PM2:**
   ```bash
   # Install PM2
   npm install -g pm2

   # Start n8n with PM2
   pm2 start n8n -- start
   pm2 save
   pm2 startup
   ```

3. **Configure Nginx Reverse Proxy:**
   ```nginx
   server {
       listen 80;
       server_name n8n.yourdomain.com;

       location / {
           proxy_pass http://localhost:5678;
           proxy_set_header Host $host;
           proxy_set_header X-Real-IP $remote_addr;
       }
   }
   ```

---

## DNS & SSL Configuration

### 1. Domain Setup

**Main Domain:**
```
rohimayapublishing.com → Vercel/Cloudflare (website)
```

**Subdomains:**
```
app.rohimayapublishing.com → Streamlit apps (via redirects)
api.rohimayapublishing.com → n8n workflows
docs.rohimayapublishing.com → Documentation site
```

### 2. SSL Certificates

**Automatic (Recommended):**
- Streamlit Cloud: Automatic HTTPS
- Vercel: Automatic Let's Encrypt
- Cloudflare: Automatic SSL

**Manual (if self-hosting):**
```bash
# Install Certbot
sudo apt-get install certbot python3-certbot-nginx

# Get certificate
sudo certbot --nginx -d yourdomain.com -d www.yourdomain.com

# Auto-renewal
sudo certbot renew --dry-run
```

---

## Monitoring & Logging

### 1. Application Monitoring

**Streamlit Apps:**
- Built-in metrics in Streamlit Cloud
- Monitor app health, resource usage
- View logs in real-time

**n8n Workflows:**
- Execution history in n8n dashboard
- Email alerts on failures
- Slack notifications

### 2. Error Tracking

**Sentry Integration:**
```python
# Add to each Streamlit app
import sentry_sdk

sentry_sdk.init(
    dsn="your-sentry-dsn",
    traces_sample_rate=1.0
)
```

### 3. Uptime Monitoring

**Tools:**
- UptimeRobot (free)
- Pingdom
- Better Stack

**Setup:**
```
Monitor URLs:
- All 7 Streamlit apps
- Website
- n8n webhook endpoints
Alert: Email + Slack
Check interval: 5 minutes
```

---

## Backup Strategies

### 1. Database Backups

**Supabase:**
- Automatic daily backups (paid plans)
- Manual backups via Dashboard > Database > Backups
- Export SQL:
  ```bash
  pg_dump -h db.xxx.supabase.co -U postgres -d postgres > backup.sql
  ```

### 2. Code Backups

- GitHub repository (primary)
- Local clones on multiple machines
- Tagged releases for production versions

### 3. Configuration Backups

- Export n8n workflows monthly
- Save secrets securely (1Password, Bitwarden)
- Document all API keys and credentials

---

## Scaling Considerations

### Traffic Levels

**Small (< 1,000 users):**
- Streamlit Cloud: Community plan
- Supabase: Free tier
- n8n: Cloud starter ($20/month)
- **Total:** ~$50/month

**Medium (1,000 - 10,000 users):**
- Streamlit Cloud: Team plan ($250/month)
- Supabase: Pro ($25/month)
- n8n: Cloud pro ($50/month)
- CDN: Cloudflare (free)
- **Total:** ~$350/month

**Large (10,000+ users):**
- Self-hosted Streamlit (VPS)
- Supabase: Team ($599/month)
- n8n: Self-hosted
- CDN: Cloudflare Pro
- Load balancer
- **Total:** Custom pricing

### Performance Optimization

1. **Enable Caching:**
   ```python
   # In Streamlit apps
   @st.cache_data
   def expensive_function():
       pass
   ```

2. **Database Indexing:**
   ```sql
   CREATE INDEX idx_user_email ON users(email);
   CREATE INDEX idx_project_user ON projects(user_id);
   ```

3. **CDN for Static Assets:**
   - Use Cloudflare for website
   - Cache images, CSS, JS
   - Enable compression

4. **Rate Limiting:**
   - Implement in API endpoints
   - Protect against abuse
   - Use Redis for tracking

---

## Security Checklist

- [ ] All API keys stored in secrets (never in code)
- [ ] Database RLS policies enabled
- [ ] HTTPS enforced on all domains
- [ ] Regular security audits
- [ ] Rate limiting on APIs
- [ ] Input validation on all forms
- [ ] SQL injection prevention
- [ ] CORS properly configured
- [ ] Regular dependency updates
- [ ] Backup encryption enabled

---

## Deployment Checklist

- [ ] All 7 Streamlit apps deployed
- [ ] All 5 n8n workflows imported and active
- [ ] Website deployed
- [ ] Database tables created
- [ ] All API keys configured
- [ ] DNS records set up
- [ ] SSL certificates active
- [ ] Monitoring configured
- [ ] Backups automated
- [ ] Documentation updated

---

## Support & Troubleshooting

**Common Issues:**

1. **App won't start on Streamlit Cloud**
   - Check requirements.txt versions
   - Verify Python version compatibility
   - Check logs for error messages

2. **Database connection fails**
   - Verify Supabase URL and keys
   - Check RLS policies
   - Ensure proper permissions

3. **Workflow not executing**
   - Verify webhook URLs
   - Check n8n execution logs
   - Test credentials

**Getting Help:**
- Email: rohimayapublishing@gmail.com
- GitHub Issues: Open an issue with logs
- Community: n8n forum, Streamlit forum

---

🦚 **Rohimaya Publishing**
*Ascend • Flourish • Enlighten*
