import csv
import requests
from datetime import datetime
from anthropic import Anthropic
 
# Initialize the Anthropic client
# Replace with your actual API key
api_key = "your_api_key_here"
client = Anthropic(api_key=api_key)
 
# Hunter.io API key
# Get one free at https://hunter.io/
hunter_api_key = "your_hunter_api_key_here"
 
# List to store all generated emails
emails_generated = []
 
def find_email_hunter(first_name, last_name, company_domain):
    """
    Uses Hunter.io API to find email address for a prospect.
    Returns email if found, None otherwise.
    """
    if not hunter_api_key or hunter_api_key == "your_hunter_api_key_here":
        return None
    
    try:
        url = "https://api.hunter.io/v2/email-finder"
        params = {
            "domain": company_domain,
            "first_name": first_name,
            "last_name": last_name,
            "api_key": hunter_api_key
        }
        
        response = requests.get(url, params=params, timeout=5)
        
        if response.status_code == 200:
            data = response.json()
            if data.get("data") and data["data"].get("email"):
                return data["data"]["email"]
        return None
    except requests.exceptions.Timeout:
        print("  ⚠ Hunter.io request timed out")
        return None
    except requests.exceptions.RequestException as e:
        print(f"  ⚠ Hunter.io API error: {e}")
        return None
    except Exception as e:
        print(f"  ⚠ Unexpected error finding email: {e}")
        return None
 
def generate_email(prospect_data):
    """
    Uses Claude to generate a personalized cold email based on prospect data.
    Returns the generated email text.
    """
    
    # Build the prompt with available data
    company_info = f"Company Name: {prospect_data['company_name']}\n"
    company_info += f"Industry: {prospect_data['industry']}\n"
    company_info += f"Company Size: {prospect_data['company_size']}\n"
    company_info += f"Recent News/Signals: {prospect_data['company_signals']}"
    
    prospect_info = f"Prospect Name: {prospect_data['prospect_name']}\n"
    prospect_info += f"Prospect Title: {prospect_data['prospect_title']}\n"
    prospect_info += f"Prospect Background: {prospect_data['prospect_background']}"
    
    prompt = f"""You are an expert cold outreach specialist. Generate a personalized, compelling cold email based on this prospect data:
 
{company_info}
 
{prospect_info}
 
Requirements:
- Email should be personalized and specific to this prospect
- Reference specific details from their LinkedIn profile and background when relevant
- Keep it concise (3-5 sentences max)
- Include a clear value proposition
- End with a specific call to action
- Professional but not stiff tone
- Do NOT include subject line, just the body
 
Generate only the email body, nothing else."""
 
    try:
        message = client.messages.create(
            model="claude-opus-4-6",
            max_tokens=500,
            messages=[
                {"role": "user", "content": prompt}
            ]
        )
        
        return message.content[0].text
    except Exception as e:
        print(f"  ✗ Error generating email: {e}")
        return None
 
def extract_domain(company_name):
    """
    Simple domain extraction. For better results, manually enter domain.
    Converts "Company Name Inc" to "companyname.com"
    """
    domain = company_name.lower().replace(" ", "").replace("inc", "").replace("ltd", "").strip()
    return f"{domain}.com"
 
def collect_prospect_data():
    """
    Collects prospect information from user input.
    Returns a dictionary with all prospect data.
    """
    print("\n" + "="*70)
    print("COLD EMAIL GENERATOR v2 - Enter Prospect Information")
    print("="*70)
    
    prospect_data = {}
    
    # Company information
    prospect_data['company_name'] = input("\nCompany Name: ").strip()
    if not prospect_data['company_name']:
        print("✗ Company name is required.")
        return None
    
    prospect_data['industry'] = input("Industry: ").strip()
    prospect_data['company_size'] = input("Company Size (e.g., 50-200 employees): ").strip()
    prospect_data['company_signals'] = input("Recent News/Signals (funding, product launches, hiring): ").strip()
    
    # Company domain for Hunter.io
    domain_input = input("Company Domain (e.g., datadog.com) [leave blank to auto-generate]: ").strip()
    if domain_input:
        prospect_data['company_domain'] = domain_input
    else:
        prospect_data['company_domain'] = extract_domain(prospect_data['company_name'])
    
    # Prospect information
    prospect_data['prospect_name'] = input("\nProspect Name: ").strip()
    if not prospect_data['prospect_name']:
        print("✗ Prospect name is required.")
        return None
    
    prospect_data['prospect_title'] = input("Prospect Title: ").strip()
    prospect_data['prospect_background'] = input("Prospect Background (education, experience, interests): ").strip()
    
    return prospect_data
 
def save_to_csv(emails_list):
    """
    Saves all generated emails to a CSV file.
    """
    if not emails_list:
        print("No emails to save.")
        return
    
    filename = f"cold_emails_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
    
    try:
        with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
            fieldnames = ['Company Name', 'Prospect Name', 'Prospect Title', 'Email Address', 'Industry', 'Company Size', 'Generated Email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for email in emails_list:
                writer.writerow({
                    'Company Name': email['company_name'],
                    'Prospect Name': email['prospect_name'],
                    'Prospect Title': email['prospect_title'],
                    'Email Address': email.get('email_address', 'Not found'),
                    'Industry': email['industry'],
                    'Company Size': email['company_size'],
                    'Generated Email': email['email']
                })
        
        print(f"\n✓ Emails saved to: {filename}")
    except Exception as e:
        print(f"\n✗ Error saving to CSV: {e}")
 
def main():
    """
    Main function to run the cold email generator.
    """
    print("\n🚀 Cold Email Generator - Phase 2")
    print("Generate personalized cold emails powered by Claude AI")
    print("with Hunter.io email discovery\n")
    
    # Check for Hunter.io API key
    if hunter_api_key == "your_hunter_api_key_here":
        print("⚠ Hunter.io API key not configured.")
        print("  Get a free key at https://hunter.io/")
        print("  Without it, you'll need to manually enter email addresses.\n")
    
    while True:
        # Collect prospect data
        prospect_data = collect_prospect_data()
        
        if prospect_data is None:
            continue
        
        print("\n⏳ Processing prospect...")
        
        # Try to find email using Hunter.io
        email_address = None
        if hunter_api_key != "your_hunter_api_key_here":
            print(f"  Searching for email address using Hunter.io...")
            first_name = prospect_data['prospect_name'].split()[0]
            last_name = " ".join(prospect_data['prospect_name'].split()[1:]) if len(prospect_data['prospect_name'].split()) > 1 else ""
            
            email_address = find_email_hunter(first_name, last_name, prospect_data['company_domain'])
            if email_address:
                print(f"  ✓ Found email: {email_address}")
            else:
                print(f"  ⚠ Email not found for {prospect_data['prospect_name']} at {prospect_data['company_domain']}")
        
        # Ask for manual email if not found
        if not email_address:
            manual_email = input("  Enter email address (or press Enter to skip): ").strip()
            if manual_email:
                email_address = manual_email
        
        print("⏳ Generating email...")
        
        try:
            # Generate email using Claude
            generated_email = generate_email(prospect_data)
            
            if generated_email is None:
                print("Skipping this prospect due to email generation error.\n")
                continue
            
            # Store the result
            emails_generated.append({
                'company_name': prospect_data['company_name'],
                'prospect_name': prospect_data['prospect_name'],
                'prospect_title': prospect_data['prospect_title'],
                'email_address': email_address,
                'industry': prospect_data['industry'],
                'company_size': prospect_data['company_size'],
                'email': generated_email
            })
            
            # Display the generated email
            print("\n" + "="*70)
            print(f"EMAIL FOR: {prospect_data['prospect_name']} at {prospect_data['company_name']}")
            if email_address:
                print(f"EMAIL ADDRESS: {email_address}")
            print("="*70)
            print(generated_email)
            print("="*70)
            
            print(f"\n✓ Email generated! ({len(emails_generated)} total)")
            
        except Exception as e:
            print(f"\n✗ Unexpected error: {e}")
        
        # Ask if user wants to generate another email
        another = input("\nGenerate another email? (yes/no): ").strip().lower()
        if another not in ['yes', 'y']:
            break
    
    # Save all emails to CSV
    if emails_generated:
        save_to_csv(emails_generated)
        print(f"\n✓ Session complete! Generated {len(emails_generated)} email(s).")
    else:
        print("\nNo emails were generated.")
 
if __name__ == "__main__":
    main()