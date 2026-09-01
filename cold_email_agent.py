import csv
from datetime import datetime
from anthropic import Anthropic


api_key = "your_api_key_here"
client = Anthropic(api_key=api_key)

# List to store all generated emails
emails_generated = []

def generate_email(prospect_data):
    """
    Uses Claude to generate a personalized cold email based on prospect data.
    Returns the generated email text.
    """
    
    prompt = f"""You are an expert cold outreach specialist. Generate a personalized, compelling cold email based on this prospect data:

Company Name: {prospect_data['company_name']}
Industry: {prospect_data['industry']}
Company Size: {prospect_data['company_size']}
Recent News/Signals: {prospect_data['company_signals']}

Prospect Name: {prospect_data['prospect_name']}
Prospect Title: {prospect_data['prospect_title']}
Prospect Background: {prospect_data['prospect_background']}

Requirements:
- Email should be personalized and specific to this prospect
- Keep it concise (3-5 sentences max)
- Include a clear value proposition
- End with a specific call to action
- Professional but not stiff tone
- Do NOT include subject line, just the body

Generate only the email body, nothing else."""

    message = client.messages.create(
        model="claude-opus-4-6",
        max_tokens=500,
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    
    return message.content[0].text

def collect_prospect_data():
    """
    Collects prospect information from user input.
    Returns a dictionary with all prospect data.
    """
    print("\n" + "="*60)
    print("COLD EMAIL GENERATOR - Enter Prospect Information")
    print("="*60)
    
    prospect_data = {}
    
    # Company information
    prospect_data['company_name'] = input("\nCompany Name: ").strip()
    prospect_data['industry'] = input("Industry: ").strip()
    prospect_data['company_size'] = input("Company Size (e.g., 50-200 employees): ").strip()
    prospect_data['company_signals'] = input("Recent News/Signals (funding, product launches, hiring): ").strip()
    
    # Prospect information
    prospect_data['prospect_name'] = input("\nProspect Name: ").strip()
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
            fieldnames = ['Company Name', 'Prospect Name', 'Prospect Title', 'Industry', 'Company Size', 'Generated Email']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            
            writer.writeheader()
            for email in emails_list:
                writer.writerow({
                    'Company Name': email['company_name'],
                    'Prospect Name': email['prospect_name'],
                    'Prospect Title': email['prospect_title'],
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
    print("\n🚀 Cold Email Generator - Phase 1")
    print("Generate personalized cold emails powered by Claude AI\n")
    
    while True:
        # Collect prospect data
        prospect_data = collect_prospect_data()
        
        print("\n⏳ Generating email...")
        
        try:
            # Generate email using Claude
            generated_email = generate_email(prospect_data)
            
            # Store the result
            emails_generated.append({
                'company_name': prospect_data['company_name'],
                'prospect_name': prospect_data['prospect_name'],
                'prospect_title': prospect_data['prospect_title'],
                'industry': prospect_data['industry'],
                'company_size': prospect_data['company_size'],
                'email': generated_email
            })
            
            # Display the generated email
            print("\n" + "="*60)
            print(f"EMAIL FOR: {prospect_data['prospect_name']} at {prospect_data['company_name']}")
            print("="*60)
            print(generated_email)
            print("="*60)
            
            print(f"\n✓ Email generated! ({len(emails_generated)} total)")
            
        except Exception as e:
            print(f"\n✗ Error generating email: {e}")
            print("Please check your API key and try again.")
        
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