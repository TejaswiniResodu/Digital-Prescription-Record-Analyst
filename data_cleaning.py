import pandas as pd

df = pd.read_csv("sample_prescriptions.csv")
df.dropna(inplace=True)
df.columns = df.columns.str.strip().str.lower()
df.to_csv("sample_prescriptions.csv", index=False)
print("✅ Data cleaned.")
