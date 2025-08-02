import pandas as pd
from sqlalchemy import create_engine

df = pd.read_csv("sample_prescriptions.csv")
df.columns = [c.strip().lower() for c in df.columns]

engine = create_engine("mysql+pymysql://root:Teja%402610@localhost:3306/dap0")
df.to_sql("prescriptions", con=engine, if_exists="replace", index=False)
print("✅ Database created and populated.")
 