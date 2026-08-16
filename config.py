"""
Configuration Module for Digital Lending Funnel & Portfolio Generator
======================================================================
Defines all constants, row counts, categorical domains, location maps,
and output path configurations.
"""

import os
from pathlib import Path
from typing import Dict, List, Tuple

# Base Project Directories
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SQL_DIR = BASE_DIR / "sql"

# Target Row Counts
NUM_CUSTOMERS = 1500
NUM_LENDERS = 20
NUM_BANK_ACCOUNTS = 1500
NUM_LOAN_APPLICATIONS = 3000
NUM_REPAYMENTS = 8000
NUM_COLLECTIONS = 2000

# Random Seed for Reproducibility
RANDOM_SEED = 42

# Loan Status Distribution Rules
LOAN_STATUS_DISTRIBUTION = {
    "Approved": 0.68,
    "Rejected": 0.18,
    "Pending": 0.14
}

# Indian City, State & Pincode Mapping (Tier 1 & Tier 2 Cities)
INDIAN_LOCATIONS: List[Dict[str, str]] = [
    {"city": "Mumbai", "state": "Maharashtra", "pincode_prefix": "400"},
    {"city": "Pune", "state": "Maharashtra", "pincode_prefix": "411"},
    {"city": "Nagpur", "state": "Maharashtra", "pincode_prefix": "440"},
    {"city": "Thane", "state": "Maharashtra", "pincode_prefix": "400"},
    {"city": "Bengaluru", "state": "Karnataka", "pincode_prefix": "560"},
    {"city": "Mysuru", "state": "Karnataka", "pincode_prefix": "570"},
    {"city": "Hubballi", "state": "Karnataka", "pincode_prefix": "580"},
    {"city": "New Delhi", "state": "Delhi", "pincode_prefix": "110"},
    {"city": "Chennai", "state": "Tamil Nadu", "pincode_prefix": "600"},
    {"city": "Coimbatore", "state": "Tamil Nadu", "pincode_prefix": "641"},
    {"city": "Madurai", "state": "Tamil Nadu", "pincode_prefix": "625"},
    {"city": "Hyderabad", "state": "Telangana", "pincode_prefix": "500"},
    {"city": "Warangal", "state": "Telangana", "pincode_prefix": "506"},
    {"city": "Ahmedabad", "state": "Gujarat", "pincode_prefix": "380"},
    {"city": "Surat", "state": "Gujarat", "pincode_prefix": "395"},
    {"city": "Vadodara", "state": "Gujarat", "pincode_prefix": "390"},
    {"city": "Kolkata", "state": "West Bengal", "pincode_prefix": "700"},
    {"city": "Howrah", "state": "West Bengal", "pincode_prefix": "711"},
    {"city": "Jaipur", "state": "Rajasthan", "pincode_prefix": "302"},
    {"city": "Jodhpur", "state": "Rajasthan", "pincode_prefix": "342"},
    {"city": "Lucknow", "state": "Uttar Pradesh", "pincode_prefix": "226"},
    {"city": "Noida", "state": "Uttar Pradesh", "pincode_prefix": "201"},
    {"city": "Kanpur", "state": "Uttar Pradesh", "pincode_prefix": "208"},
    {"city": "Chandigarh", "state": "Punjab", "pincode_prefix": "160"},
    {"city": "Ludhiana", "state": "Punjab", "pincode_prefix": "141"},
    {"city": "Kochi", "state": "Kerala", "pincode_prefix": "682"},
    {"city": "Thiruvananthapuram", "state": "Kerala", "pincode_prefix": "695"},
    {"city": "Indore", "state": "Madhya Pradesh", "pincode_prefix": "452"},
    {"city": "Bhopal", "state": "Madhya Pradesh", "pincode_prefix": "462"},
    {"city": "Patna", "state": "Bihar", "pincode_prefix": "800"},
    {"city": "Bhubaneswar", "state": "Odisha", "pincode_prefix": "751"},
    {"city": "Guwahati", "state": "Assam", "pincode_prefix": "781"}
]

# Real Indian Banks & IFSC Prefixes
INDIAN_BANKS: List[Dict[str, str]] = [
    {"bank_name": "State Bank of India", "ifsc_prefix": "SBIN00"},
    {"bank_name": "HDFC Bank", "ifsc_prefix": "HDFC00"},
    {"bank_name": "ICICI Bank", "ifsc_prefix": "ICIC00"},
    {"bank_name": "Axis Bank", "ifsc_prefix": "UTIB00"},
    {"bank_name": "Kotak Mahindra Bank", "ifsc_prefix": "KKBK00"},
    {"bank_name": "IndusInd Bank", "ifsc_prefix": "INDB00"},
    {"bank_name": "Punjab National Bank", "ifsc_prefix": "PUNB00"},
    {"bank_name": "Bank of Baroda", "ifsc_prefix": "BARB00"},
    {"bank_name": "IDFC FIRST Bank", "ifsc_prefix": "IDFB00"},
    {"bank_name": "YES Bank", "ifsc_prefix": "YESB00"},
    {"bank_name": "Canara Bank", "ifsc_prefix": "CNRB00"},
    {"bank_name": "Union Bank of India", "ifsc_prefix": "UBIN00"}
]

# 20 Real Indian Lenders
REAL_LENDERS: List[Dict[str, any]] = [
    {
        "lender_name": "Bajaj Finance Limited",
        "lender_type": "NBFC",
        "head_office_city": "Pune",
        "state": "Maharashtra",
        "processing_fee_percent": 2.50,
        "minimum_credit_score": 650,
        "maximum_loan_amount": 1500000.00
    },
    {
        "lender_name": "Tata Capital Financial Services",
        "lender_type": "NBFC",
        "head_office_city": "Mumbai",
        "state": "Maharashtra",
        "processing_fee_percent": 2.00,
        "minimum_credit_score": 680,
        "maximum_loan_amount": 1200000.00
    },
    {
        "lender_name": "HDFC Bank Digital Loans",
        "lender_type": "Bank",
        "head_office_city": "Mumbai",
        "state": "Maharashtra",
        "processing_fee_percent": 1.50,
        "minimum_credit_score": 720,
        "maximum_loan_amount": 2000000.00
    },
    {
        "lender_name": "ICICI Bank Express Credit",
        "lender_type": "Bank",
        "head_office_city": "Mumbai",
        "state": "Maharashtra",
        "processing_fee_percent": 1.75,
        "minimum_credit_score": 700,
        "maximum_loan_amount": 1800000.00
    },
    {
        "lender_name": "Aditya Birla Finance Ltd",
        "lender_type": "NBFC",
        "head_office_city": "Mumbai",
        "state": "Maharashtra",
        "processing_fee_percent": 2.25,
        "minimum_credit_score": 660,
        "maximum_loan_amount": 1000000.00
    },
    {
        "lender_name": "KrazyBee Services Pvt Ltd",
        "lender_type": "Fintech NBFC",
        "head_office_city": "Bengaluru",
        "state": "Karnataka",
        "processing_fee_percent": 3.00,
        "minimum_credit_score": 600,
        "maximum_loan_amount": 500000.00
    },
    {
        "lender_name": "Navi Finserv Limited",
        "lender_type": "Fintech NBFC",
        "head_office_city": "Bengaluru",
        "state": "Karnataka",
        "processing_fee_percent": 2.75,
        "minimum_credit_score": 620,
        "maximum_loan_amount": 800000.00
    },
    {
        "lender_name": "L&T Finance Limited",
        "lender_type": "NBFC",
        "head_office_city": "Mumbai",
        "state": "Maharashtra",
        "processing_fee_percent": 2.00,
        "minimum_credit_score": 670,
        "maximum_loan_amount": 1000000.00
    },
    {
        "lender_name": "Muthoot Finance Ltd",
        "lender_type": "NBFC",
        "head_office_city": "Kochi",
        "state": "Kerala",
        "processing_fee_percent": 1.80,
        "minimum_credit_score": 630,
        "maximum_loan_amount": 750000.00
    },
    {
        "lender_name": "Mahindra & Mahindra Financial",
        "lender_type": "NBFC",
        "head_office_city": "Mumbai",
        "state": "Maharashtra",
        "processing_fee_percent": 2.50,
        "minimum_credit_score": 640,
        "maximum_loan_amount": 900000.00
    },
    {
        "lender_name": "Poonawalla Fincorp Limited",
        "lender_type": "NBFC",
        "head_office_city": "Pune",
        "state": "Maharashtra",
        "processing_fee_percent": 2.20,
        "minimum_credit_score": 680,
        "maximum_loan_amount": 1200000.00
    },
    {
        "lender_name": "Hero Fincorp Limited",
        "lender_type": "NBFC",
        "head_office_city": "New Delhi",
        "state": "Delhi",
        "processing_fee_percent": 2.50,
        "minimum_credit_score": 650,
        "maximum_loan_amount": 600000.00
    },
    {
        "lender_name": "TVS Credit Services Ltd",
        "lender_type": "NBFC",
        "head_office_city": "Chennai",
        "state": "Tamil Nadu",
        "processing_fee_percent": 2.40,
        "minimum_credit_score": 630,
        "maximum_loan_amount": 500000.00
    },
    {
        "lender_name": "IDFC FIRST Bank Personal Loans",
        "lender_type": "Bank",
        "head_office_city": "Mumbai",
        "state": "Maharashtra",
        "processing_fee_percent": 1.90,
        "minimum_credit_score": 710,
        "maximum_loan_amount": 1500000.00
    },
    {
        "lender_name": "PayU Finance India Pvt Ltd",
        "lender_type": "Fintech NBFC",
        "head_office_city": "Gurugram",
        "state": "Haryana",
        "processing_fee_percent": 3.25,
        "minimum_credit_score": 600,
        "maximum_loan_amount": 400000.00
    },
    {
        "lender_name": "InCred Financial Services",
        "lender_type": "Fintech NBFC",
        "head_office_city": "Mumbai",
        "state": "Maharashtra",
        "processing_fee_percent": 2.80,
        "minimum_credit_score": 650,
        "maximum_loan_amount": 1000000.00
    },
    {
        "lender_name": "Northern Arc Capital Ltd",
        "lender_type": "NBFC",
        "head_office_city": "Chennai",
        "state": "Tamil Nadu",
        "processing_fee_percent": 2.10,
        "minimum_credit_score": 660,
        "maximum_loan_amount": 1200000.00
    },
    {
        "lender_name": "Vivriti Capital Limited",
        "lender_type": "NBFC",
        "head_office_city": "Chennai",
        "state": "Tamil Nadu",
        "processing_fee_percent": 2.00,
        "minimum_credit_score": 670,
        "maximum_loan_amount": 1500000.00
    },
    {
        "lender_name": "DMI Finance Private Limited",
        "lender_type": "Fintech NBFC",
        "head_office_city": "New Delhi",
        "state": "Delhi",
        "processing_fee_percent": 3.00,
        "minimum_credit_score": 620,
        "maximum_loan_amount": 500000.00
    },
    {
        "lender_name": "Faircent P2P Lending",
        "lender_type": "P2P Platform",
        "head_office_city": "Gurugram",
        "state": "Haryana",
        "processing_fee_percent": 3.50,
        "minimum_credit_score": 600,
        "maximum_loan_amount": 300000.00
    }
]

# Categorical Domains
EMPLOYMENT_TYPES = ["Salaried", "Self-Employed Professional", "Self-Employed Business", "Freelancer"]
KYC_STATUSES = ["Verified", "Verified", "Verified", "Verified", "Verified", "Pending", "Failed"]
ACCOUNT_TYPES = ["Savings", "Savings", "Savings", "Current", "Salary"]
LOAN_CHANNELS = ["Mobile App", "Mobile App", "Website", "DSA / Partner", "Branch", "Direct Telecall"]
LOAN_PURPOSES = [
    "Personal Expenses", "Medical Emergency", "Home Renovation", "Education",
    "Debt Consolidation", "Business Expansion", "Vehicle Purchase", "Wedding"
]
REJECTION_REASONS = [
    "Low Credit Score",
    "High Debt-to-Income Ratio",
    "KYC Verification Failed",
    "Insufficient Monthly Income",
    "Past Loan Default",
    "Incomplete Documentation"
]

REPAYMENT_MODES = ["UPI", "Net Banking", "NACH Auto-Debit", "Debit Card", "Credit Card", "Wallet"]

COLLECTION_AGENTS = [
    "Rajesh Sharma (Internal)",
    "Anita Roy (Internal)",
    "Vikramaditya Singh (Internal)",
    "Priya Deshmukh (Internal)",
    "Apex Recovery Agency",
    "Prudence Resolution Services",
    "Vanguard Legal & Recovery Services",
    "Zenith Financial Recovery",
    "Suresh Kumar (Field Specialist)",
    "Meenakshi Sundaram (Legal Agent)"
]

COLLECTION_STATUSES = [
    "Contacted", "Promise to Pay", "Settled", "Unreachable",
    "Legal Action Initiated", "Repossession Pending"
]

COLLECTION_MODES = ["Tele-calling", "Field Visit", "Legal Notice", "Digital Reminder", "WhatsApp Bot"]

SETTLEMENT_STATUSES = ["Full Settlement", "Partial Settlement", "Waived Off", "Pending", "Rejected"]
