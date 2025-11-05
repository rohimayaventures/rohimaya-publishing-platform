# 🦚 Rohimaya Publishing - n8n Automation Workflows

Complete automation workflows for the Rohimaya Publishing platform.

## Workflows

1. **user-onboarding.json** - Automated user registration and welcome sequence
2. **book-publishing.json** - End-to-end book publishing automation
3. **content-publishing.json** - Blog and social media distribution
4. **payment-processing.json** - Payment handling and subscription management
5. **customer-support.json** - Support ticket routing and auto-responses

## Setup Instructions

### Prerequisites
- n8n installed (self-hosted or n8n Cloud)
- Webhook access enabled
- API credentials for integrated services

### Installation

1. **Import Workflows:**
   - Open n8n interface
   - Go to Workflows menu
   - Click "Import from File"
   - Select a JSON workflow file
   - Repeat for all 5 workflows

2. **Configure Credentials:**

   Each workflow requires specific credentials:

   **All Workflows:**
   - Supabase (database)
   - SendGrid or Mailgun (email)
   - Slack (notifications)

   **user-onboarding.json:**
   - Mailchimp or ConvertKit (email marketing)

   **book-publishing.json:**
   - KDP API (Amazon Kindle Direct Publishing)
   - IngramSpark API
   - Smashwords API
   - Draft2Digital API

   **content-publishing.json:**
   - Twitter OAuth2
   - Instagram API
   - LinkedIn OAuth2
   - Facebook API
   - Medium OAuth2
   - Dev.to API
   - Buffer or Hootsuite

   **payment-processing.json:**
   - Stripe (payments)
   - Google Sheets (revenue tracking)

   **customer-support.json:**
   - IMAP Email (support inbox)

3. **Test Connections:**
   - Click on each node
   - Test credential connections
   - Verify webhook URLs
   - Update any placeholder URLs

4. **Activate Workflows:**
   - Review workflow logic
   - Enable each workflow
   - Monitor execution logs

## Workflow Details

### 1. User Onboarding Workflow

**Trigger:** Webhook - New user signup

**Actions:**
1. Create user record in Supabase
2. Send welcome email (SendGrid)
3. Create default project workspace
4. Add to email list (Mailchimp)
5. Schedule onboarding email sequence:
   - Day 1: Getting started tips
   - Day 3: AI Writing Assistant tutorial
   - Day 7: Publishing readiness check
6. Notify admin team on Slack
7. Track signup event in analytics

**Webhook URL:** `https://your-n8n-instance.com/webhook/user-signup`

**Expected Payload:**
```json
{
  "email": "user@example.com",
  "name": "John Doe",
  "subscription_tier": "free"
}
```

---

### 2. Book Publishing Workflow

**Trigger:** Webhook - Publish button clicked

**Actions:**
1. Validate manuscript format
2. Generate ISBN (via ISBN agency API)
3. Create listing on KDP (Amazon)
4. Upload to IngramSpark (print-on-demand)
5. Generate EPUB format
6. Distribute to Smashwords
7. Distribute to Draft2Digital
8. Generate marketing assets
9. Schedule launch email campaign
10. Post to social media platforms
11. Update user dashboard
12. Notify team on Slack

**Webhook URL:** `https://your-n8n-instance.com/webhook/publish-book`

**Expected Payload:**
```json
{
  "manuscript": {
    "title": "Book Title",
    "author": "Author Name",
    "content": "Full manuscript text...",
    "genre": "Fantasy",
    "price": 9.99
  },
  "launch_date": "2025-01-15T00:00:00Z"
}
```

---

### 3. Content Publishing Workflow

**Triggers:**
- Webhook - New blog post published
- Schedule - Weekly newsletter (Mondays 10am)

**Actions:**
1. Fetch blog post from CMS
2. Generate platform-specific social posts:
   - Twitter (280 chars, hashtags)
   - Instagram (caption + hashtags)
   - LinkedIn (professional tone)
   - Facebook (longer form)
3. Post to all platforms
4. Create email newsletter
5. Send via Mailchimp
6. Publish to Medium (canonical link)
7. Publish to Dev.to
8. Schedule social posts via Buffer
9. Update analytics dashboard

**Webhook URL:** `https://your-n8n-instance.com/webhook/post-published`

**Expected Payload:**
```json
{
  "post_id": "123",
  "title": "10 Tips for Self-Publishing Success",
  "excerpt": "Short summary...",
  "content": "Full blog post content...",
  "url": "https://rohimayapublishing.com/blog/post-title",
  "tags": "writing,publishing,tips"
}
```

---

### 4. Payment Processing Workflow

**Trigger:** Stripe webhook events

**Actions:**

**On Payment Succeeded:**
1. Update subscription status in Supabase
2. Send receipt email
3. Grant feature access based on tier:
   - Free: Basic tools
   - Pro: All 7 tools, 50 projects
   - Premium: All features, unlimited usage
4. Update usage limits
5. Log revenue to Google Sheets
6. Notify team for high-value customers ($100+)
7. Track payment event in analytics

**On Payment Failed:**
1. Send payment failure email
2. Mark subscription as payment_failed
3. Provide payment update link

**Webhook URL:** Configured in Stripe dashboard

**Stripe Events:**
- `payment_intent.succeeded`
- `payment_intent.payment_failed`

---

### 5. Customer Support Workflow

**Triggers:**
- Webhook - Support form submission
- Email - support@rohimayapublishing.com

**Actions:**
1. Create ticket in Supabase
2. AI-powered categorization:
   - Technical (bugs, errors)
   - Billing (payments, subscriptions)
   - How-to (tutorials, help)
   - Feature requests
3. Check knowledge base for known issues
4. Auto-respond if solution available:
   - Password resets
   - API key questions
   - Export issues
   - Subscription cancellation
   - File upload problems
5. Route to appropriate team
6. Notify on Slack (#support or #urgent-support)
7. Track response time metrics
8. Schedule 24-hour follow-up
9. Send follow-up email if unresolved

**Webhook URL:** `https://your-n8n-instance.com/webhook/support-ticket`

**Expected Payload:**
```json
{
  "user_email": "user@example.com",
  "subject": "Cannot upload manuscript",
  "message": "I'm getting an error when trying to upload my DOCX file..."
}
```

---

## Customization

Each workflow can be customized by:

### Modifying Trigger Conditions
- Change webhook paths
- Adjust schedule timings
- Add conditional logic

### Adding/Removing Actions
- Drag nodes from sidebar
- Connect with existing flow
- Configure node settings

### Changing Email Templates
- Edit HTML content in email nodes
- Update sender addresses
- Modify subject lines

### Adjusting Timing & Delays
- Modify schedule nodes
- Add wait/delay nodes
- Change retry logic

## Common Configuration

### Webhook Security

Secure your webhooks:
```javascript
// Add to webhook nodes
if ($node["Webhook"].parameters.options.secret !== 'YOUR_SECRET_KEY') {
  throw new Error('Unauthorized');
}
```

### Error Handling

Add error handling to critical nodes:
```javascript
try {
  // Your code here
} catch (error) {
  // Log error
  // Notify team
  // Retry or fail gracefully
}
```

### Rate Limiting

Respect API rate limits:
- Add delay nodes between API calls
- Batch operations when possible
- Use queue systems for high volume

## Monitoring & Maintenance

### Execution Logs
- Check n8n execution history
- Monitor for failed workflows
- Review error messages

### Performance Optimization
- Minimize API calls
- Use bulk operations
- Cache repeated data

### Regular Updates
- Review workflow logic monthly
- Update API credentials
- Test all integrations

## Troubleshooting

### Common Issues

**"Webhook not receiving data"**
- Check webhook URL is correct
- Verify firewall/network settings
- Test with manual trigger

**"Credential authentication failed"**
- Regenerate API keys
- Check credential expiration
- Verify correct permissions

**"Workflow execution timeout"**
- Increase timeout settings
- Optimize long-running operations
- Split into smaller workflows

**"Email not sending"**
- Verify sender email is configured
- Check email service quotas
- Review spam/delivery settings

### Getting Help

- n8n Community Forum: https://community.n8n.io
- n8n Documentation: https://docs.n8n.io
- Rohimaya Support: rohimayapublishing@gmail.com

## Best Practices

1. **Test in Development First**
   - Use test credentials
   - Validate with sample data
   - Check all error paths

2. **Document Custom Changes**
   - Add notes to modified nodes
   - Keep changelog of updates
   - Share changes with team

3. **Monitor Actively**
   - Set up Slack alerts
   - Review logs regularly
   - Track success rates

4. **Secure Credentials**
   - Never commit credentials to git
   - Use environment variables
   - Rotate keys periodically

5. **Version Control**
   - Export workflows regularly
   - Keep backups
   - Track major changes

## Cost Considerations

### n8n Hosting
- Self-hosted: Free (server costs only)
- n8n Cloud: Starting at $20/month

### API Costs (Approximate)
- SendGrid: Free tier available (100 emails/day)
- Stripe: No API fees (transaction fees apply)
- Slack: Free tier sufficient
- Social media APIs: Free with limits

### Estimated Monthly Cost
- Small deployment (< 1000 users): $50-100
- Medium deployment (< 10,000 users): $200-300
- Large deployment (> 10,000 users): Custom pricing

## Support

For issues or questions:
- Email: rohimayapublishing@gmail.com
- GitHub: Open an issue
- Documentation: See main repo README

---

🦚 **Built with automation by Rohimaya Publishing**
*Ascend • Flourish • Enlighten*
