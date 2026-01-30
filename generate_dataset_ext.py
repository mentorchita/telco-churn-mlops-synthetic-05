import pandas as pd
import numpy as np
import random
import json
from faker import Faker
from datetime import datetime, timedelta
from pathlib import Path

fake = Faker()
random.seed(42)
np.random.seed(42)

# ============================================================================
# ЧАСТИНА 1: ТАБЛИЧНІ ДАНІ (твій оригінальний код з покращеннями)
# ============================================================================

def generate_tabular_data(
    n_samples: int = 50000,
    start_date: str = "2023-01-01",
    end_date: str = "2024-12-31"
):
    """Генерує табличні дані клієнтів з дрейфом"""
    data = []
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")
    total_days = (end - start).days

    for i in range(n_samples):
        record_date = start + timedelta(days=random.randint(0, total_days))
        progress = (record_date - start).days / total_days

        # Дрейф параметрів (твоя логіка)
        fiber_prob = 0.40 + 0.25 * progress
        dsl_prob = 0.40 - 0.20 * progress
        no_inet_prob = 0.20 - 0.05 * progress
        echeck_prob = max(0.15, 0.40 - 0.25 * progress)
        m2m_prob = max(0.30, 0.55 - 0.25 * progress)
        streaming_boost = 0.3 * progress
        senior_prob = max(0.08, 0.18 - 0.12 * progress)

        # Базові атрибути
        gender = random.choice(["Male", "Female"])
        senior_citizen = 1 if random.random() < senior_prob else 0
        has_partner = random.choices(["Yes", "No"], weights=[52 + 10*progress, 48 - 10*progress])[0]
        has_dependents = "Yes" if random.random() < (0.3 - 0.1*progress) else "No"
        tenure = int(np.random.beta(2 + progress, 3 - 0.5*progress) * 72)
        tenure = max(0, min(tenure, 72))

        phone_service = "Yes" if random.random() < 0.92 else "No"
        internet_service = random.choices(
            ["DSL", "Fiber optic", "No"],
            weights=[dsl_prob, fiber_prob, no_inet_prob]
        )[0]

        # Додаткові послуги
        if internet_service == "No":
            secs = ["No internet service"] * 6
            online_security, online_backup, device_protection, tech_support, streaming_tv, streaming_movies = secs
        else:
            base_yes = 0.5 + streaming_boost
            online_security = "Yes" if random.random() < (base_yes * 0.7) else "No"
            online_backup = "Yes" if random.random() < (base_yes * 0.8) else "No"
            device_protection = "Yes" if random.random() < (base_yes * 0.75) else "No"
            tech_support = "Yes" if random.random() < (base_yes * 0.6) else "No"
            streaming_tv = "Yes" if random.random() < (base_yes + 0.1) else "No"
            streaming_movies = "Yes" if random.random() < (base_yes + 0.1) else "No"

        multiple_lines = "No phone service" if phone_service == "No" else (
            "Yes" if random.random() < 0.45 + 0.1*progress else "No"
        )

        contract = random.choices(
            ["Month-to-month", "One year", "Two year"],
            weights=[m2m_prob, (1-m2m_prob)*0.6, (1-m2m_prob)*0.4]
        )[0]

        paperless_billing = "Yes" if random.random() < 0.59 + 0.15*progress else "No"
        payment_method = random.choices(
            ["Electronic check", "Mailed check", "Bank transfer (automatic)", "Credit card (automatic)"],
            weights=[echeck_prob, 0.25, 0.25 + 0.1*progress, 0.25 + 0.15*progress]
        )[0]

        # Ціноутворення
        base = 20.0
        if phone_service == "Yes":
            base += 25
            if multiple_lines == "Yes":
                base += 18
        if internet_service == "DSL":
            base += 50
        elif internet_service == "Fiber optic":
            base += 82 + 10*progress

        extra_count = sum([online_security=="Yes", online_backup=="Yes", device_protection=="Yes",
                          tech_support=="Yes", streaming_tv=="Yes", streaming_movies=="Yes"])
        base += extra_count * (8 + 3*progress)

        if contract == "One year":
            base *= 0.94
        elif contract == "Two year":
            base *= 0.88 - 0.03*progress

        monthly_charges = round(max(18.5, base + np.random.normal(0, 6)), 2)
        total_charges = round(monthly_charges * tenure * random.uniform(0.97, 1.03), 2)

        # Churn prediction
        churn_base = 0.45
        if contract == "Month-to-month": churn_base += 0.35
        if payment_method == "Electronic check": churn_base += 0.18
        if internet_service == "Fiber optic": churn_base += 0.08
        if tenure < 12: churn_base += 0.25 - tenure*0.02
        churn_base -= 0.20 * progress

        churn = "Yes" if random.random() < churn_base else "No"

        customer_id = f"{random.randint(1000,9999)}-{''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZ', k=5))}"

        row = {
            "customerID": customer_id,
            "gender": gender,
            "SeniorCitizen": senior_citizen,
            "Partner": has_partner,
            "Dependents": has_dependents,
            "tenure": tenure,
            "PhoneService": phone_service,
            "MultipleLines": multiple_lines,
            "InternetService": internet_service,
            "OnlineSecurity": online_security,
            "OnlineBackup": online_backup,
            "DeviceProtection": device_protection,
            "TechSupport": tech_support,
            "StreamingTV": streaming_tv,
            "StreamingMovies": streaming_movies,
            "Contract": contract,
            "PaperlessBilling": paperless_billing,
            "PaymentMethod": payment_method,
            "MonthlyCharges": monthly_charges,
            "TotalCharges": total_charges,
            "Churn": churn,
            "RecordDate": record_date.strftime("%Y-%m-%d")
        }
        data.append(row)

    return pd.DataFrame(data)


# ============================================================================
# ЧАСТИНА 2: CUSTOMER SUPPORT CONVERSATIONS (для LLMOps/RAG)
# ============================================================================

COMPLAINT_TEMPLATES = {
    "billing_high": [
        "My bill is too high this month. I was charged ${amount} but my usual is around ${normal}. Can you explain?",
        "I'm shocked by my ${amount} bill! This is way more than my typical ${normal}. What happened?",
        "Why am I being charged ${amount}? My contract says ${normal}/month. Please fix this immediately.",
    ],
    "service_slow": [
        "My internet has been incredibly slow for the past {days} days. I'm paying for {speed} but getting terrible speeds.",
        "The {service} service keeps buffering. This is unacceptable for what I'm paying.",
        "I can't work from home because the internet is so slow. When will this be fixed?",
    ],
    "service_outage": [
        "My {service} has been down since {time}. I need this fixed ASAP as I work from home.",
        "Complete service outage for {hours} hours now. No internet, no phone. What's going on?",
        "Still no {service} after {days} days! I'm paying for a service I'm not receiving.",
    ],
    "contract_confusion": [
        "I thought I signed up for a {contract} contract, but my bill says {actual_contract}. Please clarify.",
        "I want to cancel but you're saying I have a contract until {date}. I was told it was month-to-month!",
        "Your sales rep promised me {feature} with my {contract} plan but I don't see it on my account.",
    ],
    "want_to_cancel": [
        "I want to cancel my service. It's too expensive and I found a better deal elsewhere.",
        "Please cancel my account. I'm moving to a competitor who offers {feature} for less money.",
        "I've been a customer for {tenure} months but the service quality has declined. I'm leaving.",
    ]
}

RESOLUTION_TEMPLATES = {
    "billing_high": [
        "I apologize for the billing confusion. I see there was a one-time charge for {reason}. I've applied a ${credit} credit to your account.",
        "You're right, that charge was incorrect. I've adjusted your bill back to ${normal} and credited the difference.",
        "Let me explain: the extra ${diff} was for {reason}. I can waive this charge as a one-time courtesy.",
    ],
    "service_slow": [
        "I'm sorry about the speed issues. I've scheduled a technician visit for {date}. In the meantime, try resetting your router.",
        "I see there's network congestion in your area. We're upgrading infrastructure. I've applied a ${credit} credit for the inconvenience.",
        "I've run diagnostics and found an issue with your modem. We'll ship a new one overnight at no charge.",
    ],
    "service_outage": [
        "There's a known outage in your area due to {reason}. Estimated restoration time is {time}. I've credited your account for the downtime.",
        "I apologize for the disruption. The issue has been identified and our team is working on it. ETA: {time}.",
        "The outage was caused by {reason}. Service is now restored. I've applied a ${credit} credit to your next bill.",
    ],
    "contract_confusion": [
        "I see the confusion. Your contract is actually {contract_type}. I've updated your account notes and confirmed your terms.",
        "You're correct - there was an error in how your contract was entered. I've corrected it to {contract_type} as agreed.",
        "I apologize for the miscommunication. Let me clarify your current contract terms: {details}.",
    ],
    "want_to_cancel": [
        "I'm sorry to hear you want to leave. Before you go, let me offer you {offer} to stay. Would that work for you?",
        "I understand your frustration. I can offer you a special retention discount: {discount} for {months} months.",
        "I'd hate to see you go after {tenure} months. How about we upgrade you to {plan} at your current price?",
    ]
}

def generate_conversation(customer_data, support_data):
    """Генерує реалістичну розмову customer support"""
    
    issue_type = random.choice(list(COMPLAINT_TEMPLATES.keys()))
    
    # Customer complaint
    complaint_template = random.choice(COMPLAINT_TEMPLATES[issue_type])
    
    if issue_type == "billing_high":
        complaint = complaint_template.format(
            amount=customer_data['MonthlyCharges'],
            normal=round(customer_data['MonthlyCharges'] * 0.75, 2)
        )
    elif issue_type == "service_slow":
        service = customer_data['InternetService']
        complaint = complaint_template.format(
            days=random.randint(2, 14),
            speed="fiber optic" if service == "Fiber optic" else "DSL",
            service=service
        )
    elif issue_type == "service_outage":
        complaint = complaint_template.format(
            service=customer_data['InternetService'],
            time=random.choice(["this morning", "yesterday", "2 days ago"]),
            hours=random.randint(4, 48),
            days=random.randint(1, 5)
        )
    elif issue_type == "contract_confusion":
        complaint = complaint_template.format(
            contract=customer_data['Contract'],
            actual_contract=random.choice(["Month-to-month", "One year", "Two year"]),
            date=(datetime.now() + timedelta(days=random.randint(30, 365))).strftime("%Y-%m-%d"),
            feature=random.choice(["premium support", "free device protection", "HBO included"])
        )
    elif issue_type == "want_to_cancel":
        complaint = complaint_template.format(
            tenure=customer_data['tenure'],
            feature=random.choice(["faster speeds", "better customer service", "lower prices"])
        )
    else:
        complaint = complaint_template
    
    # Agent resolution
    resolution_template = random.choice(RESOLUTION_TEMPLATES[issue_type])
    
    if issue_type == "billing_high":
        diff = round(customer_data['MonthlyCharges'] * 0.25, 2)
        resolution = resolution_template.format(
            reason=random.choice(["equipment rental", "service upgrade", "installation fee"]),
            credit=diff,
            normal=round(customer_data['MonthlyCharges'] * 0.75, 2),
            diff=diff
        )
    elif issue_type == "service_slow":
        resolution = resolution_template.format(
            date=(datetime.now() + timedelta(days=random.randint(1, 5))).strftime("%B %d"),
            credit=random.choice([10, 15, 20, 25])
        )
    elif issue_type == "service_outage":
        resolution = resolution_template.format(
            reason=random.choice(["fiber cut", "equipment failure", "scheduled maintenance"]),
            time=random.choice(["4 hours", "by end of day", "within 24 hours"]),
            credit=random.choice([15, 20, 25, 30])
        )
    elif issue_type == "contract_confusion":
        resolution = resolution_template.format(
            contract_type=customer_data['Contract'],
            details=f"{customer_data['Contract']} at ${customer_data['MonthlyCharges']}/month"
        )
    elif issue_type == "want_to_cancel":
        resolution = resolution_template.format(
            offer=random.choice(["25% off for 6 months", "free premium channels", "upgraded speed at same price"]),
            discount="$15/month off",
            months=random.choice([6, 12]),
            plan=random.choice(["Fiber Optic", "Premium DSL", "Unlimited Plan"]),
            tenure=customer_data['tenure']
        )
    else:
        resolution = resolution_template
    
    # Sentiment & outcome
    sentiment = "negative" if issue_type == "want_to_cancel" else random.choice(["negative", "neutral"])
    outcome = random.choices(
        ["resolved", "escalated", "cancelled"],
        weights=[0.7, 0.2, 0.1] if issue_type != "want_to_cancel" else [0.3, 0.2, 0.5]
    )[0]
    
    conversation = {
        "conversation_id": f"CONV-{random.randint(100000, 999999)}",
        "customerID": customer_data['customerID'],
        "date": support_data['interaction_date'],
        "channel": random.choice(["phone", "chat", "email"]),
        "issue_type": issue_type,
        "customer_message": complaint,
        "agent_message": resolution,
        "agent_id": f"AGT-{random.randint(1000, 9999)}",
        "sentiment": sentiment,
        "outcome": outcome,
        "resolution_time_minutes": random.randint(5, 120),
        "satisfaction_score": random.randint(1, 5) if outcome == "resolved" else random.randint(1, 3)
    }
    
    return conversation


def generate_support_interactions(df_customers, interaction_rate=0.15):
    """Генерує customer support interactions для ~15% клієнтів"""
    
    conversations = []
    
    # Вибираємо клієнтів які контактували support
    support_customers = df_customers.sample(frac=interaction_rate, random_state=42)
    
    for _, customer in support_customers.iterrows():
        # Деякі клієнти контактують кілька разів
        num_interactions = random.choices([1, 2, 3], weights=[0.7, 0.25, 0.05])[0]
        
        for _ in range(num_interactions):
            # Дата взаємодії після дати запису клієнта
            customer_date = datetime.strptime(customer['RecordDate'], "%Y-%m-%d")
            interaction_date = customer_date + timedelta(days=random.randint(1, 365))
            
            support_data = {
                "interaction_date": interaction_date.strftime("%Y-%m-%d")
            }
            
            conv = generate_conversation(customer, support_data)
            conversations.append(conv)
    
    return pd.DataFrame(conversations)


# ============================================================================
# ЧАСТИНА 3: KNOWLEDGE BASE DOCUMENTS (для RAG)
# ============================================================================

def generate_knowledge_base():
    """Генерує базу знань компанії для RAG"""
    
    kb_documents = [
        {
            "doc_id": "KB-001",
            "category": "billing",
            "title": "Understanding Your Bill",
            "content": """Your monthly bill includes several components:
1. Base Service Fee: Cost of your internet and phone service
2. Equipment Rental: $10/month for modem/router (waived with 2-year contract)
3. Add-on Services: Streaming, security features, cloud backup ($5-15 each)
4. Taxes and Regulatory Fees: Approximately 8-12% of base charges

One-time charges may appear for:
- Installation or activation fees ($50-100)
- Service call fees if not covered by protection plan
- Early termination fees (if applicable)

Bill disputes: Contact billing department within 30 days. Credits typically processed within 2 billing cycles."""
        },
        {
            "doc_id": "KB-002",
            "category": "plans",
            "title": "Internet Speed Tiers",
            "content": """Available internet plans:

DSL Service:
- Basic DSL: Up to 25 Mbps download, $49.99/month
- Premium DSL: Up to 50 Mbps download, $64.99/month
Good for: Email, browsing, single device streaming

Fiber Optic Service:
- Fiber 100: Up to 100 Mbps, $79.99/month
- Fiber 500: Up to 500 Mbps, $99.99/month  
- Fiber Gigabit: Up to 1000 Mbps, $119.99/month
Good for: 4K streaming, gaming, multiple devices, working from home

All plans include unlimited data. Installation fee: $99 (waived with 1-year contract)."""
        },
        {
            "doc_id": "KB-003",
            "category": "contracts",
            "title": "Contract Terms and Cancellation",
            "content": """Contract Options:

Month-to-Month:
- No commitment, cancel anytime
- Standard pricing applies
- No early termination fee

One Year Contract:
- 6% discount on monthly rates
- Early termination fee: $150 or remaining months * $15 (whichever is less)
- Free installation and equipment

Two Year Contract:
- 12% discount on monthly rates
- Free installation, equipment, and premium support
- Early termination fee: $300 or remaining months * $20 (whichever is less)

To cancel: 30-day notice required. Call retention department for potential offers before cancelling."""
        },
        {
            "doc_id": "KB-004",
            "category": "technical",
            "title": "Troubleshooting Slow Internet",
            "content": """Common causes of slow internet and solutions:

1. Router Placement
- Keep router in central location
- Avoid walls, metal objects, microwaves
- Elevate router off the floor

2. Too Many Connected Devices
- Disconnect unused devices
- Upgrade to higher bandwidth plan if needed
- Consider mesh network for large homes

3. Outdated Equipment
- Modems older than 3 years may need replacement
- Contact us for free upgrade (with eligible plans)

4. Network Congestion
- Peak usage hours: 6-10 PM
- Consider usage during off-peak times
- Fiber optic less affected by congestion

5. Background Applications
- Disable automatic updates/backups during work hours
- Check for malware/viruses
- Close unused browser tabs

Still slow? Run speed test at speedtest.telco.com and contact support with results."""
        },
        {
            "doc_id": "KB-005",
            "category": "retention",
            "title": "Retention Offers and Discounts",
            "content": """Available retention offers for customers considering cancellation:

Loyalty Discounts (6+ months tenure):
- 15% off for 6 months (month-to-month contracts)
- 20% off for 12 months (upgrade to annual contract)
- 25% off for 24 months (upgrade to 2-year contract)

Service Upgrades (12+ months tenure):
- Free speed upgrade to next tier (12 months)
- Free premium add-ons: streaming, security, or cloud backup (6 months)
- Free equipment upgrade

Special Circumstances:
- Price match competitor offers (requires proof)
- Billing credits for documented service issues
- Flexible payment plans for financial hardship

To access offers: Contact retention department. Offers subject to approval and account status."""
        },
        {
            "doc_id": "KB-006",
            "category": "technical",
            "title": "Service Outage Protocol",
            "content": """What to do during a service outage:

Immediate Steps:
1. Check outage map at telco.com/outages
2. Restart modem/router (unplug for 30 seconds)
3. Check cable connections
4. Verify account is current (no billing issues)

Reporting Outages:
- Online: telco.com/support
- Phone: 1-800-TELCO-HELP (priority queue for outages)
- App: TelcoConnect mobile app

Our Response:
- Known outages: Updates every 30 minutes
- Individual issues: Technician within 24-48 hours
- Emergency/business accounts: Priority 4-hour response

Service Credits:
- Outages over 4 hours: Automatic prorated credit
- Outages under 4 hours: Credit by request
- Multiple outages: Additional compensation considered

Status updates sent via: Email, SMS, app notifications (opt-in required)."""
        },
        {
            "doc_id": "KB-007",
            "category": "billing",
            "title": "Payment Methods and Autopay",
            "content": """Accepted Payment Methods:

One-time Payments:
- Credit/debit card (Visa, MC, Amex, Discover)
- Bank account (checking/savings)
- PayPal or Venmo
- Cash at authorized payment centers
- Check by mail (allow 7-10 business days)

Autopay Options:
- Credit card autopay: $5/month discount
- Bank transfer autopay: $5/month discount
- Paperless billing: Additional $3/month discount
- Combined discount: Up to $8/month savings

Payment Schedule:
- Due date: Same day each month (choose during setup)
- Grace period: 10 days after due date
- Late fee: $10 after grace period
- Service suspension: 30 days past due
- Reconnection fee: $25

To update payment method: Account settings online or call customer service."""
        },
        {
            "doc_id": "KB-008",
            "category": "features",
            "title": "Premium Add-on Services",
            "content": """Available add-on services:

Security Suite ($9.99/month):
- Antivirus for up to 5 devices
- Firewall protection
- Identity theft monitoring
- Password manager
- Includes 24/7 security support

Cloud Backup ($7.99/month):
- 1TB secure cloud storage
- Automatic backup scheduling
- Access from any device
- File versioning and recovery
- Mobile app included

Streaming Packages:
- Premium TV: 150+ channels, $49.99/month
- Sports Package: 20+ sports channels, $19.99/month
- Movie Package: HBO, Showtime, Starz, $29.99/month
- All three: $89.99/month (save $10)

Premium Support ($14.99/month):
- Priority phone support (no hold time)
- 24/7 tech support chat
- Free in-home service calls
- Free equipment replacement
- Dedicated account manager

Bundle discounts: 2 add-ons = 10% off, 3+ add-ons = 20% off"""
        }
    ]
    
    return pd.DataFrame(kb_documents)


# ============================================================================
# MAIN ORCHESTRATION
# ============================================================================

def generate_complete_dataset(
    n_samples: int = 50000,
    output_dir: str = "data",
    start_date: str = "2023-01-01",
    end_date: str = "2024-12-31"
):
    """Головна функція - генерує всі компоненти датасету"""
    
    output_path = Path(output_dir)
    output_path.mkdir(exist_ok=True)
    
    print("=" * 70)
    print("🚀 TELCO MLOPS DATASET GENERATOR")
    print("=" * 70)
    
    # 1. Табличні дані
    print("\n📊 [1/3] Generating tabular customer data...")
    df_customers = generate_tabular_data(n_samples, start_date, end_date)
    df_customers = df_customers.sort_values("RecordDate").reset_index(drop=True)
    
    customer_file = output_path / "telco_customers.csv"
    df_customers.to_csv(customer_file, index=False)
    print(f"   ✓ Saved {len(df_customers):,} customer records → {customer_file}")
    
    # Статистика
    print(f"\n   Churn distribution:")
    print(df_customers['Churn'].value_counts(normalize=True).round(3))
    
    df_customers['Year'] = pd.to_datetime(df_customers['RecordDate']).dt.year
    print(f"\n   Churn by year:")
    print(df_customers.groupby('Year')['Churn'].apply(lambda x: (x=='Yes').mean()).round(3))
    
    # 2. Support conversations
    print("\n💬 [2/3] Generating customer support conversations...")
    df_conversations = generate_support_interactions(df_customers, interaction_rate=0.15)
    
    conv_file = output_path / "support_conversations.csv"
    df_conversations.to_csv(conv_file, index=False)
    print(f"   ✓ Saved {len(df_conversations):,} support interactions → {conv_file}")
    
    print(f"\n   Issue types:")
    print(df_conversations['issue_type'].value_counts())
    
    print(f"\n   Outcomes:")
    print(df_conversations['outcome'].value_counts())
    
    # 3. Knowledge base
    print("\n📚 [3/3] Generating knowledge base documents...")
    df_kb = generate_knowledge_base()
    
    kb_file = output_path / "knowledge_base.csv"
    df_kb.to_csv(kb_file, index=False)
    print(f"   ✓ Saved {len(df_kb)} KB documents → {kb_file}")
    
    # JSON version for RAG systems
    kb_json_file = output_path / "knowledge_base.json"
    df_kb.to_json(kb_json_file, orient='records', indent=2)
    print(f"   ✓ Saved KB as JSON → {kb_json_file}")
    
    print("\n" + "=" * 70)
    print("✅ DATASET GENERATION COMPLETE!")
    print("=" * 70)
    print(f"\nGenerated files in '{output_dir}/':")
    print(f"  • telco_customers.csv       - {len(df_customers):,} customer records")
    print(f"  • support_conversations.csv - {len(df_conversations):,} support interactions")
    print(f"  • knowledge_base.csv        - {len(df_kb)} knowledge articles")
    print(f"  • knowledge_base.json       - Same KB in JSON format")
    
    print("\n📖 Usage for course modules:")
    print("  Modules 1-9  (MLOps):    Use telco_customers.csv")
    print("  Modules 10-11 (LLMOps):  Use support_conversations.csv + knowledge_base.*")
    print("  Modules 12-14 (Agents):  Use all three files together")
    
    return df_customers, df_conversations, df_kb


# ============================================================================
# CLI INTERFACE
# ============================================================================

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(
        description="Generate comprehensive Telco MLOps dataset with tabular data, support conversations, and knowledge base"
    )
    parser.add_argument(
        "--samples", 
        type=int, 
        default=50000,
        help="Number of customer records to generate (default: 50000)"
    )
    parser.add_argument(
        "--output-dir",
        type=str,
        default="data",
        help="Output directory for generated files (default: data/)"
    )
    parser.add_argument(
        "--start-date",
        type=str,
        default="2023-01-01",
        help="Start date for customer records (default: 2023-01-01)"
    )
    parser.add_argument(
        "--end-date",
        type=str,
        default="2024-12-31",
        help="End date for customer records (default: 2024-12-31)"
    )
    
    args = parser.parse_args()
    
    # Generate complete dataset
    generate_complete_dataset(
        n_samples=args.samples,
        output_dir=args.output_dir,
        start_date=args.start_date,
        end_date=args.end_date
    )