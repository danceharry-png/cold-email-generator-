# Cold Outreach Email Generator

An AI-powered tool that generates personalized cold emails using Claude AI with Hunter.io email discovery integration.

## Overview

This tool solves a key pain point in outbound sales: the time-intensive process of researching prospects, finding their email addresses, and crafting personalized outreach. Instead of manually writing dozens of cold emails and searching for contact info, you provide prospect data once, and Claude generates targeted, personalized email copy while Hunter.io automatically discovers email addresses.

## Features

- **Personalized Email Generation**: Takes prospect and company information as input and generates unique, contextual cold emails using Claude AI
- **Hunter.io Email Discovery**: Automatically finds prospect email addresses using the Hunter.io API (with manual fallback)
- **Claude AI Reasoning**: Uses Claude's reasoning to craft emails that reference specific company signals and prospect background
- **Batch Processing**: Generate multiple emails in one session and export all results to CSV
- **Robust Error Handling**: Gracefully handles API timeouts, missing data, invalid emails, and network issues
- **Easy Export**: All generated emails saved to timestamped CSV files with discovered email addresses ready for outreach
- **Input Validation**: Validates required fields and provides clear feedback on errors

## Prerequisites

- Python 3.11 or higher
- Anthropic API key (free at https://console.anthropic.com/)
- Hunter.io API key (free tier at https://hunter.io/ — optional but recommended)
- `anthropic` and `requests` Python libraries

## Setup

### 1. Clone the repository
```bash
git clone https://github.com/danceharry-png/cold-email-generator-.git
cd cold-email-generator-
```

### 2. Install dependencies
```bash
pip install anthropic requests
```

### 3. Configure API keys

Edit `cold_email_agent.py` and replace:
```python
api_key = "your_api_key_here"
hunter_api_key = "your_hunter_api_key_here"
```

With your actual API keys:
```python
api_key = "sk-ant-api03-xxxxx..."
hunter_api_key = "xxxxx..."
```

**Note**: Keep these keys private. Never commit them to GitHub.

## Usage

Run the script:
```bash
python cold_email_agent.py
```

### Interactive Input

The script will prompt you to enter:

**Company Information:**
- **Company Name**: Name of the target company (required)
- **Industry**: Industry vertical (e.g., SaaS, Fintech, Cloud Monitoring)
- **Company Size**: Employee count or size range (e.g., "50-200 employees")
- **Recent News/Signals**: Recent funding, product launches, hiring activity, or other relevant signals
- **Company Domain**: Company website domain (e.g., "datadog.com" — auto-generated if left blank)

**Prospect Information:**
- **Prospect Name**: Full name of the person you're reaching out to (required)
- **Prospect Title**: Job title or role
- **Prospect Background**: Relevant experience, education, interests, and other details from their LinkedIn or professional profile

### Processing Flow

1. **Email Discovery**: Script searches Hunter.io for the prospect's email address
   - If found: Email is displayed and used
   - If not found: You're prompted to enter it manually or skip

2. **Email Generation**: Claude generates a personalized cold email referencing:
   - Specific company signals and recent news
   - Prospect's background and experience
   - Relevant value proposition

3. **Review & Continue**: Email is displayed and saved, you choose to generate another or exit

4. **Export**: All generated emails are saved to a timestamped CSV file

## Example

### Input:
```
Company Name: Datadog
Industry: Cloud Monitoring
Company Size: 2000+ employees
Recent News/Signals: Just announced new AI-powered monitoring features
Company Domain: datadog.com
Prospect Name: Sarah Chen
Prospect Title: Engineering Manager
Prospect Background: 8 years DevOps experience, Stanford CS grad, open source contributor
```

### Output (Generated Email):
```
Hi Sarah,

I came across your open source contributions and your 8 years in DevOps stood out—that's exactly 
the hands-on infrastructure experience that matters for scaling platforms.

I'm reaching out because Datadog just announced AI-powered monitoring features, and I think there's 
a real opportunity to help teams like yours adopt this faster. The signal management piece alone 
could cut your alert noise by 40%.

Would you be open to a quick 15-minute chat about how other engineering teams are approaching this?

Best,
[Your name]
```

### CSV Export:
All emails are saved to `cold_emails_YYYYMMDD_HHMMSS.csv` with:
- Company Name
- Prospect Name
- Prospect Title
- Email Address (discovered or manually entered)
- Industry
- Company Size
- Generated Email body

## How It Works

1. **Input**: You provide prospect and company data through interactive prompts
2. **Email Discovery**: Script queries Hunter.io API to find prospect's email address
3. **Email Generation**: Claude receives prospect + company context and generates personalized email
4. **Storage**: Email is saved in memory and added to CSV export list
5. **Export**: All emails exported to timestamped CSV for bulk outreach or CRM import
6. **Repeat**: Continue generating for more prospects in same session

## Tips for Best Results

**Company Signals:**
- Be specific: "Series B funding in March 2024" vs "growing company"
- Include recent announcements, hiring sprees, product launches
- Mention partnerships or integrations relevant to your product

**Prospect Background:**
- Include education (college, certifications)
- List relevant roles and experience years
- Mention skills, open source work, or speaking engagements
- Note any mutual connections or shared interests

**Email Quality:**
- Always review emails before sending—Claude provides great starting points
- Personalization improves response rates
- A/B test different company signals to see what resonates

**Hunter.io Tips:**
- Accuracy depends on company domain and name matching
- Free tier has discovery limits; consider paid tier for volume
- If email not found, you can look up manually on LinkedIn or company website

## Limitations

- Generates email body copy only (no subject lines or send functionality)
- Hunter.io free tier has rate limits and accuracy varies by company
- Requires valid API keys and internet connection
- Best used for outbound prospecting, not inbound responses
- Manual review of emails recommended before sending

## Error Handling

The script gracefully handles:
- **API timeouts**: Hunter.io requests that time out are skipped
- **Invalid companies**: Hunter.io failures prompt for manual email entry
- **Missing data**: Required fields (company name, prospect name) are validated upfront
- **Network issues**: Connection errors display clear messages

## Project Structure

```
cold-email-generator/
├── cold_email_agent.py    # Main script
├── README.md              # This file
├── .gitignore            # (recommended: ignore API keys)
└── cold_emails_*.csv     # Generated output files
```

## Future Enhancements

Planned features:
- Subject line generation
- Batch CSV upload (process 100+ prospects at once)
- Web interface for non-developers
- CRM integration (Salesforce, HubSpot)
- A/B testing framework for email variants
- Response rate tracking

## License

MIT

## Troubleshooting

**"ModuleNotFoundError: No module named 'anthropic'"**
- Run: `pip install anthropic requests`

**"API key is invalid"**
- Check your API key is correct in the script
- Ensure no extra spaces before/after the key

**"Connection error" when generating emails**
- Check internet connection
- Verify Anthropic API is accessible
- Try again (may be temporary outage)

**Hunter.io not finding emails**
- Free tier has limitations
- Company domain must be exact (e.g., "datadog.com" not "datadoghq.com")
- Try manually entering email when prompted

## Questions or Issues?

Feel free to open an issue on GitHub or reach out directly.

---

**Built to demonstrate AI-driven sales automation for SDR/BDR workflows.**
