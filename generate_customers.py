"""
Customer Generator Module
=========================
Generates 1500 realistic Indian customer demographic, financial, and credit records.
"""

import random
from datetime import date
from typing import List, Dict, Set
import pandas as pd
from faker import Faker

from generator.config import (
    NUM_CUSTOMERS, INDIAN_LOCATIONS, EMPLOYMENT_TYPES, KYC_STATUSES
)
from generator.helper import (
    generate_indian_phone, generate_unique_email, random_date_between
)


def generate_customers(seed: int = 42) -> pd.DataFrame:
    """
    Generates DataFrame of 1500 unique Indian customers.
    
    :param seed: Random seed for reproducibility
    :return: pandas DataFrame containing customer records
    """
    random.seed(seed)
    fake = Faker("en_IN")
    Faker.seed(seed)

    existing_phones: Set[str] = set()
    existing_emails: Set[str] = set()
    customers_data: List[Dict] = []

    # Male and female Indian first names pool fallback if needed
    male_names = [
        "Aarav", "Aditya", "Amit", "Anand", "Aniket", "Arjun", "Deepak", "Devendra",
        "Gaurav", "Karan", "Kunal", "Manish", "Nikhil", "Pankaj", "Prashant", "Rahul",
        "Rajesh", "Rohan", "Sachin", "Sanjay", "Siddharth", "Sumit", "Tushar", "Vikas",
        "Vikram", "Vishal", "Yash"
    ]
    female_names = [
        "Ananya", "Anjali", "Anita", "Archana", "Divya", "Isha", "Kavita", "Megha",
        "Neha", "Pooja", "Priya", "Priyanka", "Ritu", "Riya", "Sangeeta", "Shweta",
        "Sneha", "Sunita", "Swati", "Tanvi", "Vandana", "Varsha"
    ]
    last_names = [
        "Sharma", "Verma", "Gupta", "Patel", "Mehta", "Joshi", "Kulkarni", "Deshmukh",
        "Nair", "Rao", "Reddy", "Singh", "Kumar", "Das", "Banerjee", "Chatterjee",
        "Agarwal", "Bhat", "Chawla", "Dutta", "Gowda", "Iyer", "Jain", "Kapoor"
    ]

    # Reference year for age calculation (2026)
    # Age range 21 to 60 -> DOB between 1966-01-01 and 2005-01-01
    dob_start = date(1966, 1, 1)
    dob_end = date(2005, 1, 1)

    for idx in range(10001, 10001 + NUM_CUSTOMERS):
        customer_id = f"CUST{idx}"
        
        # Gender selection
        gender = random.choice(["Male", "Male", "Female", "Female", "Female", "Other"])
        if gender == "Male":
            first_name = random.choice(male_names)
        elif gender == "Female":
            first_name = random.choice(female_names)
        else:
            first_name = fake.first_name()

        last_name = random.choice(last_names)

        # DOB & Phone & Email
        date_of_birth = random_date_between(dob_start, dob_end)
        phone_number = generate_indian_phone(existing_phones)
        email = generate_unique_email(first_name, last_name, existing_emails)

        # Location
        loc = random.choice(INDIAN_LOCATIONS)
        city = loc["city"]
        state = loc["state"]
        # Generate 6-digit PIN code starting with location prefix
        pincode = f"{loc['pincode_prefix']}{random.randint(100, 999):03d}"

        # Employment & Income (15000 to 200000)
        employment_type = random.choice(EMPLOYMENT_TYPES)
        # Log-normal distribution centered around ₹45,000 monthly income
        raw_income = int(random.lognormvariate(10.7, 0.55))
        monthly_income = max(15000, min(200000, raw_income))
        # Round income to nearest 500 for realistic look
        monthly_income = int(round(monthly_income / 500.0) * 500)

        # Credit Score (300 to 900, mean ~ 710)
        raw_score = int(random.normalvariate(710, 85))
        credit_score = max(300, min(900, raw_score))

        # KYC Status
        kyc_status = random.choice(KYC_STATUSES)

        record = {
            "customer_id": customer_id,
            "first_name": first_name,
            "last_name": last_name,
            "gender": gender,
            "date_of_birth": date_of_birth.strftime("%Y-%m-%d"),
            "phone_number": phone_number,
            "email": email,
            "city": city,
            "state": state,
            "pincode": pincode,
            "employment_type": employment_type,
            "monthly_income": monthly_income,
            "credit_score": credit_score,
            "kyc_status": kyc_status
        }
        customers_data.append(record)

    df = pd.DataFrame(customers_data)
    print(f"[SUCCESS] Generated {len(df)} Customer records.")
    return df
