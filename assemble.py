HEADERS = {
    "Acquisition": [
        "id",
        "channel",
        "seller",
        "interest_rate",
        "balance",
        "loan_term",
        "origination_date",
        "first_payment_date",
        "ltv",
        "cltv",
        "borrower_count",
        "dti",
        "borrower_credit_score",
        "first_time_homebuyer",
        "loan_purpose",
        "property_type",
        "unit_count",
        "occupancy_status",
        "property_state",
        "zip",
        "insurance_percentage",
        "product_type",
        "co_borrower_credit_score",
        "mortgage_insurance_type",
        "relocation_mortgage"
    ],
    "Performance": [
        "id",
        "reporting_period",
        "servicer_name",
        "interest_rate",
        "balance",
        "loan_age",
        "months_to_maturity",
        "adj_months_to_maturity",
        "maturity_date",
        "msa",
        "delinquency_status",
        "modification_flag",
        "zero_balance_code",
        "zero_balance_date",
        "last_paid_installment_date",
        "foreclosure_date",
        "disposition_date",
        "property_repair_costs",
        "recovery_costs",
        "misc_costs",
        "tax_costs",
        "sale_proceeds",
        "credit_enhancement_proceeds",
        "repurchase_proceeds",
        "other_foreclosure_proceeds",
        "non_interest_bearing_balance",
        "principal_forgiveness_balance",
        "repurchase_proceeds_flag",
        "foreclosure_principal_write_off",
        "servicing_activity"
    ]
}

SELECT = {
    "Acquisition": HEADERS["Acquisition"],
    "Performance": [
        "id",
        "foreclosure_date"
    ]
}

import os
import settings
import datetime as dt
import pandas as pd

def concatenate(prefix="Acquisition"):
    start = dt.datetime.now()
    chunksize = 100000
    imported_row_count = 0

    files = os.listdir(settings.DATA_DIR)
    full = []
    for f in files:
        if not f.startswith(prefix):
            continue

        for chunk in pd.read_csv(os.path.join(settings.DATA_DIR, f),
                                    sep = '|', header = None,
                                    names = HEADERS[prefix],
                                    index_col = False,
                                    low_memory = False,
                                    chunksize = chunksize):
            data = chunk
            data = data[SELECT[prefix]]
            data_size = len(data)
            imported_row_count += data_size
            full.append(data)
            elapsed_time = (dt.datetime.now() - start).seconds
            print('{} seconds: completed {} rows : total rows {}'.format(elapsed_time, data_size, imported_row_count))

    full = pd.concat(full, axis = 0)

    full.to_csv(os.path.join(settings.PROCESSED_DIR, "{}.txt".format(prefix)), sep = "|", header = SELECT[prefix], index = False)
    print('{} seconds: function concatenate complete'.format((dt.datetime.now() - start).seconds))

if __name__ == "__main__":
    concatenate("Acquisition")
    #concatenate("Performance")