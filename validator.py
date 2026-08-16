"""
Validation Suite Module
=======================
Executes automated quality control and verification checks across generated datasets:
1. Primary Key Uniqueness
2. Foreign Key Referential Integrity
3. Business & Financial Rule Compliance
4. Date Chronology Rules
5. Missing Values & NULL consistency
"""

import sys
from typing import Dict, List, Tuple
import pandas as pd


class DataValidator:
    def __init__(
        self,
        customers_df: pd.DataFrame,
        lenders_df: pd.DataFrame,
        bank_accounts_df: pd.DataFrame,
        loan_apps_df: pd.DataFrame,
        repayments_df: pd.DataFrame,
        collections_df: pd.DataFrame
    ):
        self.customers_df = customers_df
        self.lenders_df = lenders_df
        self.bank_accounts_df = bank_accounts_df
        self.loan_apps_df = loan_apps_df
        self.repayments_df = repayments_df
        self.collections_df = collections_df
        self.validation_results: List[Tuple[str, bool, str]] = []

    def log_result(self, check_name: str, passed: bool, message: str):
        self.validation_results.append((check_name, passed, message))
        status_str = "[PASS]" if passed else "[FAIL]"
        print(f"{status_str} {check_name}: {message}")

    def validate_duplicate_ids(self):
        """Verifies zero duplicate primary keys across all tables."""
        tables = [
            ("Customer", self.customers_df, "customer_id"),
            ("Lender", self.lenders_df, "lender_id"),
            ("Bank Account", self.bank_accounts_df, "account_id"),
            ("Loan Application", self.loan_apps_df, "application_id"),
            ("Repayment", self.repayments_df, "repayment_id"),
            ("Collection", self.collections_df, "collection_id"),
        ]
        
        all_passed = True
        for table_name, df, pk in tables:
            duplicates = df[pk].duplicated().sum()
            if duplicates > 0:
                self.log_result(f"Duplicate PK Check - {table_name}", False, f"Found {duplicates} duplicate key(s) in {pk}.")
                all_passed = False
            else:
                self.log_result(f"Duplicate PK Check - {table_name}", True, f"All {len(df)} records have unique {pk}.")

    def validate_foreign_keys(self):
        """Verifies complete referential integrity across all relationships."""
        cust_ids = set(self.customers_df["customer_id"])
        lender_ids = set(self.lenders_df["lender_id"])
        app_ids = set(self.loan_apps_df["application_id"])
        approved_app_ids = set(self.loan_apps_df[self.loan_apps_df["loan_status"] == "Approved"]["application_id"])

        # Bank Account -> Customer
        orphaned_bank = self.bank_accounts_df[~self.bank_accounts_df["customer_id"].isin(cust_ids)]
        if len(orphaned_bank) == 0:
            self.log_result("FK Integrity - Bank Account -> Customer", True, "100% foreign key match.")
        else:
            self.log_result("FK Integrity - Bank Account -> Customer", False, f"{len(orphaned_bank)} orphaned records.")

        # Loan App -> Customer
        orphaned_loan_cust = self.loan_apps_df[~self.loan_apps_df["customer_id"].isin(cust_ids)]
        if len(orphaned_loan_cust) == 0:
            self.log_result("FK Integrity - Loan Application -> Customer", True, "100% foreign key match.")
        else:
            self.log_result("FK Integrity - Loan Application -> Customer", False, f"{len(orphaned_loan_cust)} orphaned records.")

        # Loan App -> Lender
        orphaned_loan_lender = self.loan_apps_df[~self.loan_apps_df["lender_id"].isin(lender_ids)]
        if len(orphaned_loan_lender) == 0:
            self.log_result("FK Integrity - Loan Application -> Lender", True, "100% foreign key match.")
        else:
            self.log_result("FK Integrity - Loan Application -> Lender", False, f"{len(orphaned_loan_lender)} orphaned records.")

        # Repayment -> Approved Loan App ONLY
        orphaned_repay = self.repayments_df[~self.repayments_df["application_id"].isin(approved_app_ids)]
        if len(orphaned_repay) == 0:
            self.log_result("FK Integrity - Repayment -> Approved Loan App", True, "All repayments belong strictly to approved loans.")
        else:
            self.log_result("FK Integrity - Repayment -> Approved Loan App", False, f"{len(orphaned_repay)} repayments linked to non-approved/missing loans.")

        # Collection -> Loan App
        orphaned_coll = self.collections_df[~self.collections_df["application_id"].isin(app_ids)]
        if len(orphaned_coll) == 0:
            self.log_result("FK Integrity - Collection -> Loan App", True, "100% foreign key match.")
        else:
            self.log_result("FK Integrity - Collection -> Loan App", False, f"{len(orphaned_coll)} orphaned collection records.")

    def validate_loan_business_rules(self):
        """Verifies business logic compliance for loan applications."""
        approved_apps = self.loan_apps_df[self.loan_apps_df["loan_status"] == "Approved"]
        rejected_apps = self.loan_apps_df[self.loan_apps_df["loan_status"] == "Rejected"]
        pending_apps = self.loan_apps_df[self.loan_apps_df["loan_status"] == "Pending"]

        # Rule 1: Approved Amount <= Loan Amount
        exceeded = approved_apps[approved_apps["approved_amount"] > approved_apps["loan_amount"]]
        if len(exceeded) == 0:
            self.log_result("Loan Logic - Approved Amount Rule", True, "All approved amounts are <= requested amounts.")
        else:
            self.log_result("Loan Logic - Approved Amount Rule", False, f"{len(exceeded)} records violate approved_amount <= loan_amount.")

        # Rule 2: Rejected Loans fields are NULL
        non_null_rejected = rejected_apps[
            rejected_apps["approved_amount"].notna() |
            rejected_apps["approval_date"].notna() |
            rejected_apps["disbursement_date"].notna()
        ]
        if len(non_null_rejected) == 0:
            self.log_result("Loan Logic - Rejected Loans NULL Rule", True, "All rejected loans have NULL approved_amount/dates.")
        else:
            self.log_result("Loan Logic - Rejected Loans NULL Rule", False, f"{len(non_null_rejected)} rejected loans contain non-null approval details.")

        # Rule 3: Pending Loans fields are NULL
        non_null_pending = pending_apps[
            pending_apps["approved_amount"].notna() |
            pending_apps["approval_date"].notna() |
            pending_apps["disbursement_date"].notna()
        ]
        if len(non_null_pending) == 0:
            self.log_result("Loan Logic - Pending Loans NULL Rule", True, "All pending loans have NULL approval/disbursement details.")
        else:
            self.log_result("Loan Logic - Pending Loans NULL Rule", False, f"{len(non_null_pending)} pending loans contain non-null approval details.")

    def validate_date_logic(self):
        """Verifies date chronology compliance across workflow states."""
        approved_apps = self.loan_apps_df[self.loan_apps_df["loan_status"] == "Approved"].copy()
        
        # Application Date <= Approval Date
        app_date_check = approved_apps[approved_apps["application_date"] > approved_apps["approval_date"]]
        if len(app_date_check) == 0:
            self.log_result("Date Chronology - Application <= Approval", True, "All approval dates follow application dates.")
        else:
            self.log_result("Date Chronology - Application <= Approval", False, f"{len(app_date_check)} invalid date sequences.")

        # Approval Date <= Disbursement Date
        disb_date_check = approved_apps[approved_apps["approval_date"] > approved_apps["disbursement_date"]]
        if len(disb_date_check) == 0:
            self.log_result("Date Chronology - Approval <= Disbursement", True, "All disbursement dates follow approval dates.")
        else:
            self.log_result("Date Chronology - Approval <= Disbursement", False, f"{len(disb_date_check)} invalid date sequences.")

    def run_all_validations(self) -> bool:
        """Executes full suite of tests and prints summary."""
        print("\n==================================================")
        print("         EXECUTING DATASET VALIDATION SUITE       ")
        print("==================================================")
        self.validate_duplicate_ids()
        self.validate_foreign_keys()
        self.validate_loan_business_rules()
        self.validate_date_logic()

        passed_count = sum(1 for _, passed, _ in self.validation_results if passed)
        total_count = len(self.validation_results)
        print("--------------------------------------------------")
        print(f"VALIDATION SUMMARY: {passed_count}/{total_count} Checks Passed.")
        print("==================================================\n")

        return passed_count == total_count
