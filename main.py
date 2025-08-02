import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sqlalchemy import create_engine
import os

# Ensure reports directory exists
os.makedirs("reports", exist_ok=True)

# Connect to MySQL database
engine = create_engine("mysql+pymysql://root:Teja%402610@localhost:3306/dap0")
df = pd.read_sql("SELECT * FROM prescriptions", con=engine)
df.columns = df.columns.str.strip().str.lower()

# 1. Monthly Prescription Trends
def monthly_trends():
    df['month'] = pd.to_datetime(df['date']).dt.to_period('M')
    result = df.groupby('month').size().reset_index(name='total')
    result.to_csv("reports/monthly_trends.csv", index=False)
    plt.figure()
    plt.plot(result['month'].astype(str), result['total'], marker='o')
    plt.title('Monthly Prescription Trends')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.savefig("reports/monthly_trends.png")
    plt.show()

# 2. Top Drugs
def top_drugs():
    result = df.groupby("drug_name")["quantity"].sum().sort_values(ascending=False).head(5)
    result.to_csv("reports/top_drugs.csv")
    plt.figure()
    plt.pie(result, labels=result.index, autopct='%1.1f%%', startangle=140)
    plt.title('Top 5 Drugs by Quantity')
    plt.axis('equal')
    plt.savefig("reports/top_drugs.png")
    plt.show()

# 3. Doctor Summary
def doctor_summary():
    result = df.groupby("prescriber")["quantity"].sum().reset_index().sort_values("quantity", ascending=False)
    result.to_csv("reports/doctor_summary.csv", index=False)
    print(result.head())

# 4. Dosage Patterns
def dosage_patterns():
    result = df.groupby("drug_name")["dosage"].apply(lambda x: ', '.join(x.astype(str))).reset_index()
    result.to_csv("reports/dosage_patterns.csv", index=False)
    print(result.head())

# 6. Drug Utilization
def utilization_pattern():
    plt.figure()
    sns.scatterplot(data=df, x='quantity', y='cost', hue='drug_name')
    plt.title('Drug Utilization: Quantity vs Cost')
    plt.tight_layout()
    plt.savefig("reports/utilization_scatter.png")
    plt.show()

# 7. Geographic Analysis
def geo_analysis():
    result = df.groupby("region")["drug_name"].count().reset_index(name="prescription_count")
    result.to_csv("reports/geo_analysis.csv", index=False)
    plt.figure()
    plt.pie(result["prescription_count"], labels=result["region"], autopct="%1.1f%%")
    plt.title("Prescriptions by Region")
    plt.axis("equal")
    plt.savefig("reports/geo_analysis.png")
    plt.show()

# 8. Cost Summary
def cost_summary():
    result = df.groupby("drug_name")["cost"].sum().sort_values(ascending=False).head(5)
    result.to_csv("reports/cost_summary.csv")
    plt.figure()
    plt.barh(result.index, result.values)
    plt.title("Top 5 Drug Costs")
    plt.tight_layout()
    plt.savefig("reports/cost_summary.png")
    plt.show()

# 10. Most Expensive Drugs
def most_expensive_drugs():
    df['cost_per_unit'] = df['cost'] / df['quantity']
    result = df.groupby('drug_name')['cost_per_unit'].mean().sort_values(ascending=False).head(5)
    result.to_csv("reports/most_expensive_drugs.csv")
    print(result)

# 11. Cost per Prescription (Doctor-wise)
def cost_per_prescription():
    result = df.groupby("prescriber")["cost"].mean().sort_values(ascending=False).reset_index()
    result.to_csv("reports/cost_per_prescription.csv", index=False)
    print(result.head())

# 12. Daily Prescription Volume
def daily_volume():
    df['date'] = pd.to_datetime(df['date'])
    result = df.groupby(df['date'].dt.date).size().reset_index(name='prescription_count')
    result.to_csv("reports/daily_volume.csv", index=False)
    plt.figure()
    plt.plot(result['date'], result['prescription_count'], marker='.')
    plt.xticks(rotation=45)
    plt.title("Daily Prescription Volume")
    plt.tight_layout()
    plt.savefig("reports/daily_volume.png")
    plt.show()

# 14. Year-wise Trends
def yearly_trends():
    df['year'] = pd.to_datetime(df['date']).dt.year
    result = df.groupby('year').agg({
        'drug_name': 'count',   # Count prescriptions
        'cost': 'sum'           # Total cost per year
    }).reset_index()
    result.rename(columns={'drug_name': 'total_prescriptions'}, inplace=True)
    result.to_csv("reports/yearly_trends.csv", index=False)
    print(result)

# 15. Export All
def export_all():
    doctor_summary()
    dosage_patterns()
    geo_analysis()
    utilization_pattern()
    monthly_trends()
    top_drugs()
    cost_summary()
    most_expensive_drugs()
    cost_per_prescription()
    daily_volume()
    yearly_trends()
    print("\u2705 All reports exported!")

# Menu Function
def menu():
    print("\n DAP0 - Digital Prescription Record Analyst")
    print("1. Monthly Trends")
    print("2. Top Drugs")
    print("3. Doctor Summary")
    print("4. Dosage Patterns")
    print("5. Drug Utilization")
    print("6. Geographic Analysis")
    print("7. Cost Summary")
    print("8. Most Expensive Drugs")
    print("9. Cost per Prescription (Doctor-wise)")
    print("10. Daily Prescription Volume")
    print("11. Year-wise Cost and Volume Trends")
    print("12. Export All")
    print("0. Exit")

# Main Loop
while True:
    menu()
    ch = input("Enter choice: ")
    if ch == "1": monthly_trends()
    elif ch == "2": top_drugs()
    elif ch == "3": doctor_summary()
    elif ch == "4": dosage_patterns()
    elif ch == "5": utilization_pattern()
    elif ch == "6": geo_analysis()
    elif ch == "7": cost_summary()
    elif ch == "8": most_expensive_drugs()
    elif ch == "9": cost_per_prescription()
    elif ch == "10": daily_volume()
    elif ch == "11": yearly_trends()
    elif ch == "12": export_all()
    elif ch == "0": break
    else:
        print("\u274C Invalid choice.")
