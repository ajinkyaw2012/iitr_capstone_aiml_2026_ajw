# 2. **`clean_shipments(raw, medians=None)`** in `src/shipment_prep.py`. It takes a raw shipments DataFrame and returns a tuple `(clean_df, medians)`. Apply these steps in this order:
#    1. drop exact duplicate rows;
#    2. `service_type`: strip leading and trailing spaces and convert to title case, so exactly three spellings remain (`Express`, `Standard`, `Economy`);
#    3. `payment_mode`: replace a missing value with the placeholder `"Unknown"`;
#    4. `declared_value`: remove the rupee sign and the thousands commas, convert to a number, store it in a new column `declared_value_inr`, and drop the text column;
#    5. `dispatch_time`: convert to a datetime;
#    6. `parcel_weight_kg`: any value above 100 is a scanner-fault sentinel (the network accepts parcels up to 40 kg) — treat it as missing;
#    7. fill missing `distance_km`, `parcel_weight_kg` and `declared_value_inr` with that column's **median**. If `medians` is `None`, compute the three medians from the non-missing values left after steps 1–6; otherwise use the dictionary passed in. The returned `medians` is a dictionary with exactly the keys `distance_km`, `parcel_weight_kg`, `declared_value_inr` and float values.

#    The medians are computed on the full historical table before any split. They are fill-in values for gaps and carry no information about the target; the scaler and the feature selector in Parts B and C are fitted on training rows only.
# 3. **`build_features(clean, hubs)`** in `src/shipment_prep.py`. It returns a DataFrame with the hub columns attached by a **left merge** on `hub_id` (`hub_city`, `region`, `hub_tier`, `hub_daily_capacity`) plus these new columns: `promised_hours` (from `PROMISED_HOURS`, integer), `is_cod` (1 when `payment_mode` is `COD`, else 0 — `Unknown` gives 0), `is_weekend` (1 when the dispatch day is Saturday or Sunday), `dispatch_hour` (the hour of the dispatch timestamp as an integer; the generated data uses hours 6 to 21), and `log_declared_value` (natural log of `declared_value_inr`). It must not use `delivery_hours`, so that it also works on parcels that have not been delivered yet.
# 4. **`part_a_clean_eda.py`.** Read `data/raw_shipments.csv` and `data/hubs.csv`; call your two functions; add the target `is_delayed` (1 when `delivery_hours > promised_hours`, else 0); write the result to `data/modelling_table.csv` (all columns, one row per unique shipment).

import pandas as pd
import numpy as np

def clean_shipments(raw, medians=None):
    """Clean a raw shipments DataFrame and return (clean_df, medians)."""
    df = raw.copy()
    # 1. drop exact duplicate rows
    df = df.drop_duplicates()
    # 2. service_type: strip spaces and convert to title case
    df['service_type'] = df['service_type'].str.strip().str.title()
    # 3. payment_mode: replace missing with "Unknown"
    df['payment_mode'] = df['payment_mode'].fillna("Unknown")
    # 4. declared_value: remove rupee sign and commas, convert to number, store in new column
    if 'declared_value' in df.columns:
        df['declared_value_inr'] = df['declared_value'].str.replace('₹', '', regex=False).str.replace(',', '', regex=False).astype(float)
        df = df.drop(columns=['declared_value'])
    # 5. dispatch_time: convert to datetime
    df['dispatch_time'] = pd.to_datetime(df['dispatch_time'], format='%Y-%m-%d %H:%M')


    print("test")