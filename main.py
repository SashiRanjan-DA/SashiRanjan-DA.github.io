"""
Main Orchestration Script
=========================
Digital Lending Funnel & Loan Portfolio Data Generator

Executes end-to-end synthetic dataset generation, runs validation checks,
and exports 6 production-grade CSV files:
1. customer.csv (1500 rows)
2. lender.csv (20 rows)
3. customer_bank_account.csv (1500 rows)
4. loan_application.csv (3000 rows)
5. repayment.csv (8000 rows)
6. collection.csv (2000 rows)
"""

import os
import sys
import time
from pathlib import Path
import pandas as pd

# Add project root to Python module search path
PROJECT_ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(PROJECT_ROOT))

from generator.config import DATA_DIR, RANDOM_SEED
from generator.generate_lenders import generate_lenders
from generator.generate_customers import generate_customers
from generator.generate_bank_accounts import generate_bank_accounts
from generator.generate_loan_applications import generate_loan_applications
from generator.generate_repayments import generate_repayments
from generator.generate_collections import generate_collections
from generator.validator import DataValidator


def main():
    start_time = time.time()
    print("==========================================================")
    print("    DIGITAL LENDING FUNNEL & PORTFOLIO DATA GENERATOR     ")
    print("==========================================================\n")

    # Ensure output data directory exists
    DATA_DIR.mkdir(parents=True, exist_ok=True)
    print(f"[INIT] Output directory initialized at: {DATA_DIR}\n")

    # Step 1: Generate Lenders Master Data (20 rows)
    print("Step 1/8: Generating Lender Master Data...")
    lenders_df = generate_lenders()

    # Step 2: Generate Customers Master Data (1,500 rows)
    print("\nStep 2/8: Generating Customer Demographic & Financial Data...")
    customers_df = generate_customers(seed=RANDOM_SEED)

    # Step 3: Generate Customer Bank Accounts (1,500 rows)
    print("\nStep 3/8: Generating Customer Bank Account Data...")
    bank_accounts_df = generate_bank_accounts(customers_df, seed=RANDOM_SEED)

    # Step 4: Generate Loan Applications (3,000 rows)
    print("\nStep 4/8: Generating Loan Application Lifecycle Data...")
    loan_apps_df = generate_loan_applications(customers_df, lenders_df, seed=RANDOM_SEED)

    # Step 5: Generate Repayments (8,000 rows)
    print("\nStep 5/8: Generating Repayment & EMI Schedule Data...")
    repayments_df = generate_repayments(loan_apps_df, seed=RANDOM_SEED)

    # Step 6: Generate Collections (2,000 rows)
    print("\nStep 6/8: Generating Delinquent Collection Data...")
    collections_df = generate_collections(repayments_df, loan_apps_df, seed=RANDOM_SEED)

    # Step 7: Run Validation Suite
    print("\nStep 7/8: Executing Data Integrity & Business Logic Validations...")
    validator = DataValidator(
        customers_df=customers_df,
        lenders_df=lenders_df,
        bank_accounts_df=bank_accounts_df,
        loan_apps_df=loan_apps_df,
        repayments_df=repayments_df,
        collections_df=collections_df
    )
    validation_passed = validator.run_all_validations()

    if not validation_passed:
        print("[WARNING] Data validation failed! Check log warnings above.")
    else:
        print("[SUCCESS] All 10 data validation tests passed cleanly!")

    # Step 8: Export Datasets to CSV
    print("\nStep 8/8: Exporting Datasets to CSV Files...")
    datasets = [
        ("customer.csv", customers_df),
        ("lender.csv", lenders_df),
        ("customer_bank_account.csv", bank_accounts_df),
        ("loan_application.csv", loan_apps_df),
        ("repayment.csv", repayments_df),
        ("collection.csv", collections_df),
    ]

    total_rows = 0
    for filename, df in datasets:
        file_path = DATA_DIR / filename
        # Export with clean formatting and UTF-8 encoding
        df.to_csv(file_path, index=False, encoding="utf-8")
        row_count = len(df)
        total_rows += row_count
        print(f" -> Exported '{filename}' ({row_count:,} rows) to {file_path}")

    elapsed = time.time() - start_time
    print("\n==========================================================")
    print(f" PROCESS COMPLETED SUCCESSFULLY IN {elapsed:.2f} SECONDS!")
    print(f" TOTAL ROWS GENERATED ACROSS 6 TABLES: {total_rows:,}")
    print("==========================================================")


if __name__ == "__main__":
    main()
