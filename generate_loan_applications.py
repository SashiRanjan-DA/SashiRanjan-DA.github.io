"""
Loan Application Generator Module
=================================
Generates 3000 loan application records enforcing exact status distribution ratios:
- 68% Approved (2,040 rows)
- 18% Rejected (540 rows)
- 14% Pending (420 rows)
Strictly applies financial business rules, risk pricing, and EMI calculations.
"""

import random
from datetime import date, timedelta
from typing import List, Dict
import pandas as pd

from generator.config import (
    NUM_LOAN_APPLICATIONS, LOAN_CHANNELS, LOAN_PURPOSES, REJECTION_REASONS
)
from generator.helper import (
    calculate_emi, determine_interest_rate, random_date_between
)


def generate_loan_applications(
    customers_df: pd.DataFrame,
    lenders_df: pd.DataFrame,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generates DataFrame of 3000 loan application records with financial rules.
    
    :param customers_df: pandas DataFrame of customers
    :param lenders_df: pandas DataFrame of lenders
    :param seed: Random seed for reproducibility
    :return: pandas DataFrame of loan applications
    """
    random.seed(seed)
    
    # Quick lookup maps
    customer_credit_map = dict(zip(customers_df["customer_id"], customers_df["credit_score"]))
    customer_income_map = dict(zip(customers_df["customer_id"], customers_df["monthly_income"]))
    lender_fee_map = dict(zip(lenders_df["lender_id"], lenders_df["processing_fee_percent"]))
    lender_max_loan_map = dict(zip(lenders_df["lender_id"], lenders_df["maximum_loan_amount"]))

    customer_ids = list(customers_df["customer_id"])
    lender_ids = list(lenders_df["lender_id"])

    # Target status counts (68% Approved, 18% Rejected, 14% Pending)
    num_approved = 2040
    num_rejected = 540
    num_pending = 420
    
    statuses = (
        ["Approved"] * num_approved +
        ["Rejected"] * num_rejected +
        ["Pending"] * num_pending
    )
    random.shuffle(statuses)

    app_start_date = date(2024, 1, 1)
    app_end_date = date(2025, 12, 15)

    tenure_options = [6, 12, 18, 24, 36, 48, 60]
    loan_apps_data: List[Dict] = []

    for idx, status in enumerate(statuses, start=10001):
        application_id = f"APP{idx}"
        cust_id = random.choice(customer_ids)
        lender_id = random.choice(lender_ids)

        credit_score = customer_credit_map.get(cust_id, 700)
        monthly_income = customer_income_map.get(cust_id, 50000)
        max_lender_amount = lender_max_loan_map.get(lender_id, 1000000.0)

        # Requested Loan Amount based on customer income and lender caps
        multiplier = random.uniform(2.0, 15.0)
        raw_amount = min(monthly_income * multiplier, max_lender_amount)
        # Clamp between ₹10,000 and ₹1,000,000 rounded to 5,000
        loan_amount = float(max(10000, min(1000000, round(raw_amount / 5000.0) * 5000)))

        loan_tenure_months = int(random.choice(tenure_options))
        loan_purpose = random.choice(LOAN_PURPOSES)
        loan_channel = random.choice(LOAN_CHANNELS)
        application_date = random_date_between(app_start_date, app_end_date)

        if status == "Approved":
            # Approved Amount must be <= requested loan_amount
            approval_pct = random.uniform(0.80, 1.00)
            approved_amount = float(round((loan_amount * approval_pct) / 5000.0) * 5000)
            approved_amount = float(max(10000.0, approved_amount))

            # Interest Rate based on Credit Score
            interest_rate = determine_interest_rate(credit_score)

            # Processing Fee
            fee_pct = lender_fee_map.get(lender_id, 2.0)
            processing_fee = round((approved_amount * fee_pct) / 100.0, 2)

            # Dates
            approval_delay = random.randint(0, 5)
            approval_date = application_date + timedelta(days=approval_delay)
            disbursement_delay = random.randint(0, 3)
            disbursement_date = approval_date + timedelta(days=disbursement_delay)

            # Exact EMI Calculation
            emi_amount = calculate_emi(approved_amount, interest_rate, loan_tenure_months)
            rejection_reason = None

            record = {
                "application_id": application_id,
                "customer_id": cust_id,
                "lender_id": lender_id,
                "loan_amount": loan_amount,
                "approved_amount": approved_amount,
                "interest_rate": interest_rate,
                "loan_tenure_months": loan_tenure_months,
                "loan_purpose": loan_purpose,
                "application_date": application_date.strftime("%Y-%m-%d"),
                "approval_date": approval_date.strftime("%Y-%m-%d"),
                "loan_status": status,
                "rejection_reason": rejection_reason,
                "loan_channel": loan_channel,
                "processing_fee": processing_fee,
                "emi_amount": emi_amount,
                "disbursement_date": disbursement_date.strftime("%Y-%m-%d")
            }

        elif status == "Rejected":
            record = {
                "application_id": application_id,
                "customer_id": cust_id,
                "lender_id": lender_id,
                "loan_amount": loan_amount,
                "approved_amount": None,
                "interest_rate": None,
                "loan_tenure_months": loan_tenure_months,
                "loan_purpose": loan_purpose,
                "application_date": application_date.strftime("%Y-%m-%d"),
                "approval_date": None,
                "loan_status": status,
                "rejection_reason": random.choice(REJECTION_REASONS),
                "loan_channel": loan_channel,
                "processing_fee": None,
                "emi_amount": None,
                "disbursement_date": None
            }

        else:  # Pending
            record = {
                "application_id": application_id,
                "customer_id": cust_id,
                "lender_id": lender_id,
                "loan_amount": loan_amount,
                "approved_amount": None,
                "interest_rate": None,
                "loan_tenure_months": loan_tenure_months,
                "loan_purpose": loan_purpose,
                "application_date": application_date.strftime("%Y-%m-%d"),
                "approval_date": None,
                "loan_status": status,
                "rejection_reason": None,
                "loan_channel": loan_channel,
                "processing_fee": None,
                "emi_amount": None,
                "disbursement_date": None
            }

        loan_apps_data.append(record)

    df = pd.DataFrame(loan_apps_data)
    print(f"[SUCCESS] Generated {len(df)} Loan Application records ({num_approved} Approved, {num_rejected} Rejected, {num_pending} Pending).")
    return df
