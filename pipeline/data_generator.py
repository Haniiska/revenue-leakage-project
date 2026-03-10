import pandas as pd
import random
from datetime import datetime, timedelta

data = []

for i in range(100):
    encounter = {
        "encounter_id": f"ENC{i}",
        "patient_id": f"PAT{i}",
        "visit_date": datetime.now() - timedelta(days=random.randint(1,30)),
        "charges": random.randint(100,2000),
        "submitted": random.choice([True, False]),
        "paid_amount": random.randint(0,2000)
    }
    data.append(encounter)

df = pd.DataFrame(data)

df.to_excel("data/sample_data.xlsx", index=False)

print("Sample healthcare data created!")