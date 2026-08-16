"""
Collection Generator Module
===========================
Generates exactly 2,000 collection records linked EXCLUSIVELY to loans with missed
or delinquent repayment records. Models recovery workflows, agent assignments,
promise-to-pay commitments, and loan settlements.
"""

import random
from datetime import datetime, date, timedelta
from typing import List, Dict
import pandas as pd

from generator.config import (
    NUM_COLLECTIONS, COLLECTION_AGENTS, COLLECTION_STATUSES,
    COLLECTION_MODES, SETTLEMENT_STATUSES
)
from generator.helper import random_date_between


def generate_collections(
    repayments_df: pd.DataFrame,
    loan_apps_df: pd.DataFrame,
    seed: int = 42
) -> pd.DataFrame:
    """
    Generates DataFrame of 2000 collection records for delinquent loans.
    
    :param repayments_df: pandas DataFrame of repayment records
    :param loan_apps_df: pandas DataFrame of loan application records
    :param seed: Random seed for reproducibility
    :return: pandas DataFrame of collection records
    """
    random.seed(seed)

    # Filter repayments for delinquent cases ("Missed", "Paid Late", "Partially Paid")
    delinquent_repayments = repayments_df[
        repayments_df["payment_status"].isin(["Missed", "Paid Late", "Partially Paid"])
    ].copy()

    # Get unique application IDs that have delinquency history
    delinquent_app_ids = list(delinquent_repayments["application_id"].unique())

    if not delinquent_app_ids:
        # Fallback to any approved loan if list is empty
        approved_apps = loan_apps_df[loan_apps_df["loan_status"] == "Approved"]
        delinquent_app_ids = list(approved_apps["application_id"].unique())

    loan_amount_map = dict(zip(loan_apps_df["application_id"], loan_apps_df["approved_amount"]))
    emi_amount_map = dict(zip(loan_apps_df["application_id"], loan_apps_df["emi_amount"]))

    collections_data: List[Dict] = []
    base_start_date = date(2024, 6, 1)
    base_end_date = date(2026, 1, 31)

    for idx in range(10001, 10001 + NUM_COLLECTIONS):
        collection_id = f"COL{idx}"
        app_id = random.choice(delinquent_app_ids)

        agent = random.choice(COLLECTION_AGENTS)
        collection_mode = random.choice(COLLECTION_MODES)
        collection_status = random.choice(COLLECTION_STATUSES)

        # Financial amounts
        emi_amt = float(emi_amount_map.get(app_id, 5000.0) or 5000.0)
        app_approved_amt = float(loan_amount_map.get(app_id, 100000.0) or 100000.0)

        missed_factor = random.uniform(1.2, 4.5)
        outstanding_amount = round(min(app_approved_amt, emi_amt * missed_factor + random.uniform(500, 2500)), 2)

        collection_date = random_date_between(base_start_date, base_end_date)
        follow_up_count = random.randint(1, 12)
        last_follow_up_date = collection_date - timedelta(days=random.randint(0, 10))

        # Promise to Pay Logic
        if collection_status == "Promise to Pay":
            ptp_delay = random.randint(3, 20)
            promise_to_pay_date = collection_date + timedelta(days=ptp_delay)
            settlement_status = "Pending"
            settlement_amount = None
            remarks = f"Borrower promised to pay ₹{outstanding_amount} by {promise_to_pay_date.strftime('%Y-%m-%d')}."
        elif collection_status == "Settled":
            promise_to_pay_date = collection_date - timedelta(days=random.randint(5, 15))
            settlement_status = random.choice(["Full Settlement", "Partial Settlement", "Waived Off"])
            settle_pct = random.uniform(0.60, 0.95)
            settlement_amount = round(outstanding_amount * settle_pct, 2)
            remarks = f"Loan settled at ₹{settlement_amount} under {settlement_status} arrangement."
        elif collection_status == "Contacted":
            promise_to_pay_date = None
            settlement_status = "Pending"
            settlement_amount = None
            remarks = f"Customer contacted via {collection_mode}. Payment request sent."
        elif collection_status == "Unreachable":
            promise_to_pay_date = None
            settlement_status = "Pending"
            settlement_amount = None
            remarks = "Borrower unreachable on registered phone number. Escalated to field team."
        elif collection_status == "Legal Action Initiated":
            promise_to_pay_date = None
            settlement_status = "Rejected"
            settlement_amount = None
            remarks = "Section 25 / NI Act 138 legal notice issued for persistent loan default."
        else:  # Repossession Pending
            promise_to_pay_date = None
            settlement_status = "Pending"
            settlement_amount = None
            remarks = "Asset recovery team assigned for asset repossession proceedings."

        record = {
            "collection_id": collection_id,
            "application_id": app_id,
            "collection_agent": agent,
            "collection_date": collection_date.strftime("%Y-%m-%d"),
            "outstanding_amount": outstanding_amount,
            "collection_status": collection_status,
            "collection_mode": collection_mode,
            "promise_to_pay_date": promise_to_pay_date.strftime("%Y-%m-%d") if promise_to_pay_date else None,
            "settlement_amount": settlement_amount,
            "settlement_status": settlement_status,
            "follow_up_count": follow_up_count,
            "last_follow_up_date": last_follow_up_date.strftime("%Y-%m-%d"),
            "remarks": remarks
        }
        collections_data.append(record)

    df = pd.DataFrame(collections_data)
    print(f"[SUCCESS] Generated {len(df)} Collection records.")
    return df
