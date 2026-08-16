"""
Lender Generator Module
=======================
Generates realistic Indian bank, NBFC, and fintech lender master data.
"""

import pandas as pd
from typing import List, Dict
from generator.config import REAL_LENDERS, NUM_LENDERS


def generate_lenders() -> pd.DataFrame:
    """
    Generates DataFrame of 20 lenders with fixed schema and business metrics.
    
    :return: pandas DataFrame containing lender records.
    """
    lenders_data: List[Dict] = []
    
    for idx, lender_info in enumerate(REAL_LENDERS[:NUM_LENDERS], start=1001):
        lender_id = f"LEN{idx}"
        record = {
            "lender_id": lender_id,
            "lender_name": lender_info["lender_name"],
            "lender_type": lender_info["lender_type"],
            "head_office_city": lender_info["head_office_city"],
            "state": lender_info["state"],
            "processing_fee_percent": round(float(lender_info["processing_fee_percent"]), 2),
            "minimum_credit_score": int(lender_info["minimum_credit_score"]),
            "maximum_loan_amount": round(float(lender_info["maximum_loan_amount"]), 2)
        }
        lenders_data.append(record)

    df = pd.DataFrame(lenders_data)
    print(f"[SUCCESS] Generated {len(df)} Lender records.")
    return df
