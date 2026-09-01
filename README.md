# Cold Outreach Email Generator

An AI-powered tool that generates personalized cold emails using Claude AI. Built to demonstrate how AI automation can streamline prospecting workflows for sales development.

## Overview

This tool solves a key pain point in outbound sales: the time-intensive process of researching prospects and crafting personalized outreach. Instead of manually writing dozens of cold emails, you provide prospect data once, and Claude generates targeted, personalized email copy at scale.

## Features

- **Personalized Email Generation**: Takes prospect and company information as input and generates unique, contextual cold emails
- **Claude AI Reasoning**: Uses Claude's reasoning capabilities to craft emails that reference specific company signals and prospect background
- **Batch Processing**: Generate multiple emails in one session and export all results to CSV
- **Easy Export**: All generated emails saved to timestamped CSV files for review and manual quality control

## Prerequisites

- Python 3.11 or higher
- Anthropic API key (get one free at https://console.anthropic.com/)
- `anthropic` Python library

## Setup

1. Clone this repository:
```bash
git clone https://github.com/yourusername/cold-email-generator.git
cd cold-email-generator
```

2. Install dependencies:
```bash
pip install anthropic
```

3. Set your Anthropic API key as an environment variable:

**On macOS/Linux:**
```bash
export ANTHROPIC_API_KEY=your_api_key_here
```

**On Windows (PowerShell):**
```powershell
$env:ANTHROPIC_API_KEY="your_api_key_here"
```

Or edit the script directly and replace `api_key = "your_api_key_here"` with your actual key (less secure).

## Usage

Run the script:
```bash
python cold_email_agent.py
```

The script will prompt you to enter:
- **Company Name**: Name of the target company
- **Industry**: Industry vertical (e.g., SaaS, Fintech, Cloud)
- **Company Size**: Employee count or size range
- **Recent News/Signals**: Recent funding, product launches, hiring spree, etc.
- **Prospect Name**: Full name of the person you're reaching out to
- **Prospect Title**: Job title or role
- **Prospect Background**: Relevant experience, education, interests

The tool will then generate a personalized cold email and display it. You can generate as many emails as you want in one session. When you're done, all emails are automatically saved to a CSV file with timestamp.

## Example

**Input:**
```
Company Name: Datadog
Industry: Cloud Monitoring
Company Size: 2000+ employees
Recent News/Signals: Just announced new AI-powered monitoring features
Prospect Name: Sarah Chen
Prospect Title: Engineering Manager
Prospect Background: 8 years in DevOps, Stanford CS grad, open source contributor
```

**Generated Email Output:**
```
Hi Sarah,

I came across your work in open source and your background caught my attention—8 years in DevOps 
is exactly the kind of hands-on experience that matters in infrastructure roles.

I'm reaching out because Datadog just announced the new AI-powered monitoring features, and I think 
there's a real opportunity to help teams like yours adopt this faster. The signal management piece 
alone could cut your alert noise by 40%.

Would you be open to a quick 15-minute chat about how other engineering teams are approaching this?

Best,
[Your name]
```

## Output

Each session generates a CSV file named `cold_emails_YYYYMMDD_HHMMSS.csv` containing:
- Company Name
- Prospect Name
- Prospect Title
- Industry
- Company Size
- Generated Email

You can open this file in Excel, Google Sheets, or any text editor to review, edit, and use emails.

## How It Works

1. You provide prospect and company data
2. The script sends this data to Claude along with a prompt asking for a personalized email
3. Claude uses reasoning to craft an email that references specific signals and the prospect's background
4. The generated email is displayed and stored
5. When you're done, all emails are exported to CSV for bulk use

## Tips for Best Results

- **Be specific with company signals**: The more recent and specific (e.g., "Series B funding round in March" vs just "growing company"), the more tailored the email
- **Include prospect background details**: Education, prior roles, open source contributions, or other signals make emails more personalized
- **Manual review**: Always review generated emails before sending. Claude generates great starting points, but your human judgment matters
- **A/B test**: Try different company signals or prospect backgrounds to see what resonates

## Limitations

- This tool generates email body copy only (no subject lines)
- Emails should be manually reviewed before sending
- Requires valid Anthropic API key and internet connection
- Best used for outbound prospecting, not for responding to inbound inquiries

## Next Steps

Phase 2 (planned): Hunter.io integration for automatic email discovery
Phase 3 (planned): Web interface for batch CSV uploads

## License

MIT

## Questions?

Feel free to open an issue or reach out.
