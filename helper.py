"""
Helper Utilities Module
=======================
Financial calculation formulas, Indian data string generators, date math,
and format converters for the Digital Lending Data Generator.
"""

import math
import random
import re
from datetime import date, timedelta
from typing import Set


def calculate_emi(principal: float, annual_interest_rate: float, tenure_months: int) -> float:
    """
    Calculates exact Equated Monthly Installment (EMI) using standard compound interest formula:
    EMI = P * r * (1+r)^n / ((1+r)^n - 1)
    
    :param principal: Approved loan principal amount in INR
    :param annual_interest_rate: Annual interest rate percentage (e.g., 14.5 for 14.5%)
    :param tenure_months: Total loan tenure in months
    :return: Rounded EMI amount to 2 decimal places
    """
    if principal is None or annual_interest_rate is None or tenure_months is None:
        return None
    if principal <= 0 or tenure_months <= 0:
        return 0.0

    if annual_interest_rate == 0:
        return round(principal / tenure_months, 2)

    monthly_rate = (annual_interest_rate / 100.0) / 12.0
    growth_factor = math.pow(1.0 + monthly_rate, tenure_months)
    
    emi = principal * (monthly_rate * growth_factor) / (growth_factor - 1.0)
    return round(emi, 2)


def determine_interest_rate(credit_score: int) -> float:
    """
    Determines realistic interest rate percentage based on risk tier of credit score.
    Higher credit scores receive lower interest rates.
    """
    if credit_score >= 780:
        base = random.uniform(10.5, 13.5)
    elif credit_score >= 720:
        base = random.uniform(13.6, 16.5)
    elif credit_score >= 670:
        base = random.uniform(16.6, 21.0)
    elif credit_score >= 600:
        base = random.uniform(21.1, 26.0)
    else:
        base = random.uniform(26.1, 32.0)

    return round(base, 2)


def generate_indian_phone(existing_phones: Set[str]) -> str:
    """
    Generates a unique 10-digit Indian phone number starting with 6, 7, 8, or 9.
    """
    while True:
        first_digit = str(random.choice([6, 7, 8, 9]))
        remaining_digits = "".join([str(random.randint(0, 9)) for _ in range(9)])
        phone = first_digit + remaining_digits
        if phone not in existing_phones:
            existing_phones.add(phone)
            return phone


def generate_unique_email(first_name: str, last_name: str, existing_emails: Set[str]) -> str:
    """
    Generates a unique professional email address using customer name and popular domains.
    """
    clean_fn = re.sub(r'[^a-zA-Z0-9]', '', first_name.lower())
    clean_ln = re.sub(r'[^a-zA-Z0-9]', '', last_name.lower())
    domains = ["gmail.com", "yahoo.co.in", "outlook.com", "hotmail.com", "rediffmail.com"]

    suffix_num = ""
    attempt = 0
    while True:
        domain = random.choice(domains)
        if attempt == 0:
            email_candidate = f"{clean_fn}.{clean_ln}@{domain}"
        elif attempt == 1:
            email_candidate = f"{clean_fn}{clean_ln}{random.randint(10, 99)}@{domain}"
        else:
            email_candidate = f"{clean_fn}.{clean_ln}{random.randint(100, 9999)}@{domain}"

        if email_candidate not in existing_emails:
            existing_emails.add(email_candidate)
            return email_candidate
        attempt += 1


def generate_ifsc_code(bank_prefix: str) -> str:
    """
    Generates an 11-character valid Indian Financial System Code (IFSC).
    Format: 4 letter bank code + '0' + 6 alphanumeric branch code.
    """
    branch_code = f"{random.randint(1000, 9999):04d}"
    return f"{bank_prefix}{branch_code}"


def random_date_between(start_date: date, end_date: date) -> date:
    """
    Generates a random date strictly between start_date and end_date.
    """
    if start_date >= end_date:
        return start_date
    delta_days = (end_date - start_date).days
    random_days = random.randint(0, delta_days)
    return start_date + timedelta(days=random_days)
