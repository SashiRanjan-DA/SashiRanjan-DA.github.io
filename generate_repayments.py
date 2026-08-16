"""
Repayment Generator Module
==========================
Generates exactly 8,000 repayment records linked EXCLUSIVELY to approved loan applications.
Models repayment behavior including On-Time payments, Late payments with penalties,
Missed EMIs, and Partial payments.
"""

import random
from datetime import datetime, date, timedelta
from typing import List, Dict
import pandas as pd

from generator.config import NUM_REPAYMENTS, REPAYMENT_MODES


def generate_repayments(loan_apps_df: pd.DataFrame, seed: int = 42) -> pd.DataFrame:
    """
    Generates DataFrame of exactly 8,000 repayment records for approved loans.
    
    :param loan_apps_df: pandas DataFrame of loan applications
    :param seed: Random seed for reproducibility
    :return: pandas DataFrame of repayment records
    """
    random.seed(seed)
    
    # Filter strictly for approved loans
    approved_loans = loan_apps_df[loan_apps_df["loan_status"] == "Approved"].copy()
    approved_list = approved_loans.to_dict("records")

    repayments_data: List[Dict] = []
    repayment_counter = 100001
    
    # We will generate EMIs for approved loans in round-robin / schedule fashion until we reach 8,000 rows
    loan_schedules = {
        loan["application_id"]: {
            "loan": loan,
            "current_emi": 1,
            "disbursement_date": datetime.strptime(loan["disbursement_date"], "%Y-%m-%d").date()
        }
        for loan in approved_list
    }

    loan_ids = list(loan_schedules.keys())
    active_loan_ids = list(loan_ids)

    while len(repayments_data) < NUM_REPAYMENTS:
        if not active_loan_ids:
            # Reset active loans if all tenures exceeded (to maintain target count)
            active_loan_ids = list(loan_ids)

        app_id = random.choice(active_loan_ids)
        item = loan_schedules[app_id]
        loan = item["loan"]
        emi_num = item["current_emi"]
        disb_date = item["disbursement_date"]
        tenure = int(loan["loan_tenure_months"])

        if emi_num > tenure:
            active_loan_ids.remove(app_id)
            continue

        # Calculate Due Date (Approx 30 days * emi_num after disbursement)
        due_date = disb_date + timedelta(days=30 * emi_num)
        emi_amount = float(loan["emi_amount"])

        # Determine Payment Performance Behavior
        behavior_rand = random.random()
        if behavior_rand < 0.78:
            payment_status = "Paid On Time"
            days_overdue = 0
            late_fee = 0.00
            amount_due = emi_amount
            amount_paid = emi_amount
            # Payment date on or before due date
            pay_delay = random.randint(-5, 0)
            payment_date = due_date + timedelta(days=pay_delay)
            payment_mode = random.choice(REPAYMENT_MODES)
            remarks = "Regular monthly EMI paid on time."

        elif behavior_rand < 0.92:
            payment_status = "Paid Late"
            days_overdue = random.randint(1, 45)
            late_fee = float(500 + (50 * days_overdue))
            amount_due = emi_amount
            amount_paid = round(emi_amount + late_fee, 2)
            payment_date = due_date + timedelta(days=days_overdue)
            payment_mode = random.choice(REPAYMENT_MODES)
            remarks = f"Payment delayed by {days_overdue} days. Late fee penalty assessed."

        elif behavior_rand < 0.97:
            payment_status = "Missed"
            days_overdue = random.randint(15, 90)
            late_fee = float(500 + (50 * days_overdue))
            amount_due = emi_amount
            amount_paid = 0.00
            payment_date = None
            payment_mode = None
            remarks = f"EMI overdue by {days_overdue} days. No payment received."

        else:  # Partially Paid
            payment_status = "Partially Paid"
            days_overdue = random.randint(5, 60)
            late_fee = float(300 + (30 * days_overdue))
            amount_due = emi_amount
            pct_paid = random.uniform(0.3, 0.8)
            amount_paid = round(emi_amount * pct_paid, 2)
            payment_date = due_date + timedelta(days=days_overdue)
            payment_mode = random.choice(REPAYMENT_MODES)
            remarks = f"Partial payment of ₹{amount_paid} received against due amount ₹{amount_due}."

        repayment_id = f"REP{repayment_counter}"
        repayment_counter += 1

        record = {
            "repayment_id": repayment_id,
            "application_id": app_id,
            "emi_number": emi_num,
            "due_date": due_date.strftime("%Y-%m-%d"),
            "payment_date": payment_date.strftime("%Y-%m-%d") if payment_date else None,
            "amount_due": amount_due,
            "amount_paid": amount_paid,
            "payment_status": payment_status,
            "late_fee": late_fee,
            "days_overdue": days_overdue,
            "payment_mode": payment_mode,
            "remarks": remarks
        }
        repayments_data.append(record)
        item["current_emi"] += 1

    df = pd.DataFrame(repayments_data)
    print(f"[SUCCESS] Generated {len(df)} Repayment records.")
    return df
