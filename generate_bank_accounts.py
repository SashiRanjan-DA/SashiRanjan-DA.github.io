"""
Customer Bank Account Generator Module
======================================
Generates 1500 bank account records linked 1-to-1 to Customers.
"""

import random
from datetime import date
from typing import List, Dict
import pandas as pd

from generator.config import (
    NUM_BANK_ACCOUNTS, INDIAN_BANKS, ACCOUNT_TYPES
)
from generator.helper import (
    generate_ifsc_code, random_date_between
)


def generate_bank_accounts(customers_df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """
    Generates DataFrame of 1500 bank account records linked to customers.
    
    :param customers_df: pandas DataFrame of existing customer records
    :param seed: Random seed for reproducibility
    :return: pandas DataFrame containing customer bank accounts
    """
    random.seed(seed)
    bank_accounts_data: List[Dict] = []

    # Map customer income for balance modeling
    customer_income_map = dict(zip(customers_df["customer_id"], customers_df["monthly_income"]))
    customer_ids = list(customers_df["customer_id"])

    account_start_date = date(2015, 1, 1)
    account_end_date = date(2023, 12, 31)

    for idx, cust_id in enumerate(customer_ids, start=10001):
        account_id = f"ACC{idx}"
        
        bank = random.choice(INDIAN_BANKS)
        bank_name = bank["bank_name"]
        ifsc_code = generate_ifsc_code(bank["ifsc_prefix"])
        
        account_type = random.choice(ACCOUNT_TYPES)
        account_open_date = random_date_between(account_start_date, account_end_date)
        
        # Account Status
        status_rand = random.random()
        if status_rand < 0.94:
            account_status = "Active"
        elif status_rand < 0.98:
            account_status = "Inactive"
        else:
            account_status = "Blocked"

        # Salary Account flag (more likely if account_type == "Salary" or income > 40000)
        monthly_inc = customer_income_map.get(cust_id, 45000)
        if account_type == "Salary":
            salary_account = "TRUE"
        elif monthly_inc >= 50000 and random.random() < 0.6:
            salary_account = "TRUE"
        else:
            salary_account = "FALSE"

        # Average balance linked to monthly income
        balance_factor = random.uniform(0.3, 3.5)
        average_balance = round(monthly_inc * balance_factor, 2)

        # UPI Linked
        upi_linked = "TRUE" if random.random() < 0.92 else "FALSE"

        record = {
            "account_id": account_id,
            "customer_id": cust_id,
            "bank_name": bank_name,
            "account_type": account_type,
            "ifsc_code": ifsc_code,
            "account_open_date": account_open_date.strftime("%Y-%m-%d"),
            "account_status": account_status,
            "salary_account": salary_account,
            "average_balance": average_balance,
            "upi_linked": upi_linked
        }
        bank_accounts_data.append(record)

    df = pd.DataFrame(bank_accounts_data)
    print(f"[SUCCESS] Generated {len(df)} Customer Bank Account records.")
    return df
