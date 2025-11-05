# 🔑 Rohimaya Publishing - API Keys Setup Guide

Complete guide to obtaining and configuring all required API keys for the platform.

## Required API Services

1. **Anthropic Claude** - AI writing, plot outlining, character creation
2. **OpenAI** - GPT-4, DALL-E 3 (covers, portraits)
3. **ElevenLabs** - Text-to-speech (optional)
4. **Stripe** - Payment processing
5. **SendGrid** - Email delivery
6. **Supabase** - Database

---

## 1. Anthropic Claude API

**Used by:**
- AI Writing Assistant
- Manuscript Formatter
- Plot Outliner
- Character Creator
- Marketing Copy Generator

### Setup Steps

1. **Create Account:**
   - Go to https://console.anthropic.com/
   - Sign up with email
   - Verify email address

2. **Add Payment Method:**
   - Go to Settings → Billing
   - Add credit card
   - Set spending limit (recommended: $100/month to start)

3. **Get API Key:**
   - Go to Settings → API Keys
   - Click "Create Key"
   - Name: "Rohimaya Production"
   - Copy key (starts with `sk-ant-api03-`)
   - **Save immediately** - can't view again!

4. **Test Key:**
   ```bash
   curl https://api.anthropic.com/v1/messages \
     -H "x-api-key: $ANTHROPIC_API_KEY" \
     -H "anthropic-version: 2023-06-01" \
     -H "content-type: application/json" \
     -d '{
       "model": "claude-3-5-sonnet-20241022",
       "max_tokens": 1024,
       "messages": [{"role": "user", "content": "Hello!"}]
     }'
   ```

### Pricing

- **Claude 3.5 Sonnet:** $3.00 / million input tokens, $15.00 / million output tokens
- **Typical usage per request:** 1,000-5,000 tokens (~$0.02-$0.10)
- **Estimated monthly cost (1,000 users):** $50-200

### Rate Limits

- **Tier 1 (Default):** 50 requests/minute
- **Tier 2:** 1,000 requests/minute (after $100 spent)
- **Tier 3:** 2,000 requests/minute (after $1,000 spent)

### Best Practices

- Set up billing alerts
- Monitor usage in console
- Use caching to reduce costs
- Implement retry logic for rate limits

---

## 2. OpenAI API

**Used by:**
- AI Cover Designer (DALL-E 3)
- Character Creator (DALL-E 3)
- Audiobook Generator (TTS, optional)

### Setup Steps

1. **Create Account:**
   - Go to https://platform.openai.com/
   - Sign up with email or Google
   - Verify email

2. **Add Credits:**
   - Go to Settings → Billing
   - Add payment method
   - Purchase credits (minimum $5)

3. **Get API Key:**
   - Go to API Keys
   - Click "Create new secret key"
   - Name: "Rohimaya Publishing"
   - Copy key (starts with `sk-`)
   - **Save immediately!**

4. **Test Key:**
   ```bash
   curl https://api.openai.com/v1/chat/completions \
     -H "Authorization: Bearer $OPENAI_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "model": "gpt-4-turbo-preview",
       "messages": [{"role": "user", "content": "Hello!"}]
     }'
   ```

### Pricing

**DALL-E 3:**
- 1024×1024: $0.040 per image
- 1024×1792: $0.080 per image (used for covers)

**GPT-4:**
- $0.03 / 1K input tokens
- $0.06 / 1K output tokens

**TTS (Audiobook Generator):**
- Standard: $0.015 / 1K characters
- HD: $0.030 / 1K characters

### Rate Limits

**Tier 1 (Default):**
- 500 requests/day
- 10,000 tokens/minute

**Tier 2 ($50 spent):**
- 5,000 requests/day
- 90,000 tokens/minute

### Best Practices

- Use DALL-E 3 standard quality (not HD) to save costs
- Cache generated images
- Implement queue for batch processing
- Use TTS only when other options unavailable

---

## 3. ElevenLabs API (Optional)

**Used by:**
- Audiobook Generator (high-quality TTS)

### Setup Steps

1. **Create Account:**
   - Go to https://elevenlabs.io/
   - Sign up for account
   - Choose plan (Creator: $22/month)

2. **Get API Key:**
   - Go to Profile → API Keys
   - Click "Generate API Key"
   - Copy key
   - Save securely

3. **Test Key:**
   ```python
   from elevenlabs import generate, set_api_key

   set_api_key("your_api_key")
   audio = generate(
       text="Hello from Rohimaya!",
       voice="Rachel",
       model="eleven_monolingual_v1"
   )
   ```

### Pricing

- **Free:** 10,000 characters/month
- **Creator:** $22/month for 100,000 characters
- **Pro:** $99/month for 500,000 characters

**Cost per audiobook:**
- 50,000 word novel ≈ 300,000 characters
- Cost: ~$60 with Creator plan

### Voices Available

- 9 pre-built voices
- Custom voice cloning available (Pro plan)
- Different accents and languages

### Best Practices

- Use for final audiobooks only (not previews)
- Fallback to OpenAI TTS for cost savings
- Monitor character usage
- Batch process long texts

---

## 4. Stripe API

**Used by:**
- Payment processing
- Subscription management
- Billing automation

### Setup Steps

1. **Create Account:**
   - Go to https://stripe.com/
   - Sign up for account
   - Complete business verification

2. **Get API Keys:**
   - Go to Developers → API keys
   - Copy **Publishable key** (starts with `pk_test_` or `pk_live_`)
   - Copy **Secret key** (starts with `sk_test_` or `sk_live_`)
   - **Never expose secret key in frontend!**

3. **Test Mode vs Live Mode:**
   - **Test mode:** For development
   - **Live mode:** For production
   - Toggle in dashboard

4. **Set Up Webhooks:**
   ```
   Endpoint URL: https://your-n8n.com/webhook/stripe-payments
   Events to send:
   - payment_intent.succeeded
   - payment_intent.payment_failed
   - customer.subscription.created
   - customer.subscription.updated
   - customer.subscription.deleted
   ```

### Pricing

- **Transaction fees:** 2.9% + $0.30 per successful charge
- **No monthly fee**
- **No API usage fees**

### Subscription Tiers (Recommended)

```javascript
// Pricing structure
const plans = {
  free: {
    price: 0,
    features: ['2 tools', '3 projects', '10 exports/month']
  },
  pro: {
    price: 2900, // $29.00 in cents
    interval: 'month',
    features: ['All 7 tools', '50 projects', 'Unlimited exports']
  },
  premium: {
    price: 9900, // $99.00 in cents
    interval: 'month',
    features: ['Everything in Pro', 'Priority support', 'API access']
  }
};
```

### Security Best Practices

- **Never** commit API keys to GitHub
- Use environment variables
- Restrict API key permissions
- Enable webhook signature verification
- Use HTTPS only
- Implement CSRF protection

---

## 5. SendGrid API

**Used by:**
- Transactional emails (receipts, confirmations)
- Marketing emails (newsletters, announcements)
- Support emails (ticket responses)

### Setup Steps

1. **Create Account:**
   - Go to https://sendgrid.com/
   - Sign up for free tier (100 emails/day)

2. **Verify Sender Email:**
   - Go to Settings → Sender Authentication
   - Add sender email: support@rohimayapublishing.com
   - Verify email address
   - **Required before sending emails!**

3. **Get API Key:**
   - Go to Settings → API Keys
   - Click "Create API Key"
   - Name: "Rohimaya n8n"
   - Permissions: "Full Access"
   - Copy key (starts with `SG.`)
   - **Save immediately!**

4. **Test Key:**
   ```bash
   curl -X POST https://api.sendgrid.com/v3/mail/send \
     -H "Authorization: Bearer $SENDGRID_API_KEY" \
     -H "Content-Type: application/json" \
     -d '{
       "personalizations": [{
         "to": [{"email": "test@example.com"}]
       }],
       "from": {"email": "support@rohimayapublishing.com"},
       "subject": "Test Email",
       "content": [{"type": "text/plain", "value": "Hello!"}]
     }'
   ```

### Pricing

- **Free:** 100 emails/day (3,000/month)
- **Essentials:** $15/month (50,000 emails)
- **Pro:** $60/month (150,000 emails)

### Email Templates

Create templates in SendGrid:
1. Welcome email
2. Receipt email
3. Support response
4. Password reset
5. Newsletter

### Best Practices

- Verify sender domain for better deliverability
- Use templates for consistency
- Monitor bounce rates
- Implement unsubscribe handling
- Track open rates

---

## 6. Supabase API

**Used by:**
- User authentication
- Database storage
- Real-time subscriptions

### Setup Steps

1. **Create Project:**
   - Go to https://supabase.com/
   - Sign in with GitHub
   - Create new project
   - Name: "rohimaya-publishing"
   - Choose region (closest to users)

2. **Get API Keys:**
   - Go to Project Settings → API
   - Copy **URL** (e.g., `https://xxx.supabase.co`)
   - Copy **anon/public key** (for client-side)
   - Copy **service_role key** (for server-side, keep secret!)

3. **Test Connection:**
   ```javascript
   import { createClient } from '@supabase/supabase-js'

   const supabase = createClient(
     'https://xxx.supabase.co',
     'your-anon-key'
   )

   const { data, error } = await supabase
     .from('users')
     .select('*')
     .limit(1)
   ```

### Pricing

- **Free:** 500MB database, 1GB file storage, 2GB bandwidth
- **Pro:** $25/month - 8GB database, 100GB storage, 50GB bandwidth
- **Team:** $599/month - Dedicated resources

### Security

- Enable Row Level Security (RLS) on all tables
- Create policies for data access
- Never expose service_role key in frontend
- Use anon key for client-side operations

---

## Environment Variables Setup

### For Local Development

Create `.env` file (add to .gitignore):
```bash
# Anthropic
ANTHROPIC_API_KEY=sk-ant-api03-xxxxx

# OpenAI
OPENAI_API_KEY=sk-xxxxx

# ElevenLabs
ELEVENLABS_API_KEY=xxxxx

# Stripe
STRIPE_PUBLISHABLE_KEY=pk_test_xxxxx
STRIPE_SECRET_KEY=sk_test_xxxxx

# SendGrid
SENDGRID_API_KEY=SG.xxxxx

# Supabase
SUPABASE_URL=https://xxx.supabase.co
SUPABASE_ANON_KEY=xxxxx
SUPABASE_SERVICE_ROLE_KEY=xxxxx
```

### For Streamlit Cloud

Add to app secrets (TOML format):
```toml
[anthropic]
api_key = "sk-ant-xxxxx"

[openai]
api_key = "sk-xxxxx"

[elevenlabs]
api_key = "xxxxx"

[supabase]
url = "https://xxx.supabase.co"
anon_key = "xxxxx"
service_role_key = "xxxxx"
```

### For n8n Workflows

Add credentials in n8n dashboard:
1. Go to Credentials
2. Add new credential for each service
3. Enter API keys
4. Test connection
5. Save

---

## Cost Management

### Set Up Budgets

**Anthropic:**
- Dashboard → Billing → Usage Limits
- Set monthly limit: $100

**OpenAI:**
- Dashboard → Billing → Usage Limits
- Set hard limit: $100

**Stripe:**
- No usage fees, only transaction fees

**SendGrid:**
- Monitor daily email count
- Upgrade plan as needed

### Monitor Usage

Create a monitoring dashboard:
- Track API calls per day
- Monitor costs per service
- Set up alerts for thresholds
- Review monthly bills

### Optimization Tips

1. **Cache API responses** where possible
2. **Batch requests** to reduce calls
3. **Use cheaper models** for non-critical tasks
4. **Implement rate limiting** to prevent abuse
5. **Monitor error rates** to catch issues early

---

## Security Best Practices

### 1. Key Storage

✅ **Do:**
- Store in environment variables
- Use secrets management (1Password, AWS Secrets Manager)
- Rotate keys every 90 days
- Use different keys for dev/prod

❌ **Don't:**
- Commit to GitHub
- Share in Slack/email
- Hardcode in application
- Reuse across projects

### 2. Key Permissions

- Use least privilege principle
- Create separate keys for different services
- Restrict IP addresses where possible
- Enable 2FA on all accounts

### 3. Monitoring

- Enable audit logging
- Monitor for unusual activity
- Set up alerts for failed authentications
- Review access logs monthly

### 4. Incident Response

If key is compromised:
1. **Immediately rotate** the key
2. **Audit** recent usage
3. **Notify** affected users if needed
4. **Update** all services with new key
5. **Document** the incident

---

## Rate Limiting Implementation

Protect your API keys with rate limiting:

```python
from functools import wraps
import time

def rate_limit(max_per_minute):
    min_interval = 60.0 / max_per_minute
    last_called = [0.0]

    def decorate(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorate

@rate_limit(50)  # 50 requests per minute
def call_api():
    # API call here
    pass
```

---

## Error Handling

Implement robust error handling:

```python
import anthropic
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=4, max=10)
)
def call_claude_api(prompt):
    try:
        client = anthropic.Anthropic(api_key=api_key)
        message = client.messages.create(
            model="claude-3-5-sonnet-20241022",
            max_tokens=1024,
            messages=[{"role": "user", "content": prompt}]
        )
        return message.content[0].text

    except anthropic.RateLimitError:
        # Wait and retry
        time.sleep(60)
        raise

    except anthropic.APIError as e:
        # Log error
        logger.error(f"API Error: {e}")
        raise

    except Exception as e:
        # Catch-all
        logger.error(f"Unexpected error: {e}")
        return None
```

---

## Support & Troubleshooting

### Common Issues

**"Invalid API key"**
- Verify key is correct
- Check for extra spaces
- Ensure key hasn't expired
- Verify correct environment (test vs live)

**"Rate limit exceeded"**
- Implement backoff strategy
- Reduce request frequency
- Upgrade tier if needed
- Cache responses

**"Insufficient credits"**
- Add funds to account
- Set up auto-recharge
- Monitor usage more closely

### Getting Help

- **Anthropic:** support@anthropic.com
- **OpenAI:** help.openai.com
- **Stripe:** support.stripe.com
- **SendGrid:** support@sendgrid.com
- **Rohimaya:** rohimayapublishing@gmail.com

---

🦚 **Rohimaya Publishing**
*Ascend • Flourish • Enlighten*
