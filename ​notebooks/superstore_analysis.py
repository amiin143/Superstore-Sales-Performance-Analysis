# =============================================================================
# SUPERSTORE SALES ANALYSIS
# Author  : Amiin Mohamed
# Role    : Data Scientist / Data Analyst
# Dataset : Superstore Sales (train.csv)
# Tools   : Python 3 | pandas | matplotlib | seaborn | openpyxl
# GitHub  : github.com/AmiinTech
# =============================================================================
# This script performs end-to-end data analysis on the Superstore Sales
# dataset. It covers:
#   1. Data Loading & Inspection
#   2. Data Cleaning
#   3. Exploratory Data Analysis (EDA)
#   4. Visualizations (10 charts)
#   5. Key Findings Summary
# =============================================================================


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 0 — IMPORT LIBRARIES
# ─────────────────────────────────────────────────────────────────────────────

import pandas as pd
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import seaborn as sns
import warnings
import os

warnings.filterwarnings("ignore")          # suppress minor warnings

# Create output folder for saved charts
os.makedirs("charts", exist_ok=True)

print("✅ Libraries loaded successfully.")
print(f"   pandas  version : {pd.__version__}")
print(f"   numpy   version : {np.__version__}")
print(f"   matplotlib version: {matplotlib.__version__}")
print(f"   seaborn version : {sns.__version__}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 1 — LOAD DATA
# ─────────────────────────────────────────────────────────────────────────────

# NOTE: Change the filename below if needed.
# The script supports both .csv and .xlsx formats.

FILE_PATH = "train.csv"   # ← update path here if your file is elsewhere

try:
    if FILE_PATH.endswith(".xlsx"):
        df = pd.read_excel(FILE_PATH, engine="openpyxl")
    else:
        df = pd.read_csv(FILE_PATH)
    print(f"\n✅ Dataset loaded → {df.shape[0]:,} rows × {df.shape[1]} columns")
except FileNotFoundError:
    raise FileNotFoundError(f"❌ File not found: '{FILE_PATH}'. Please check the path.")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 2 — DATA INSPECTION
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECTION 2 — DATA INSPECTION")
print("="*60)

# 2.1 First five rows
print("\n▸ First 5 rows:")
print(df.head())

# 2.2 Column names and data types
print("\n▸ Columns & dtypes:")
print(df.dtypes)

# 2.3 Dataset shape and memory
print(f"\n▸ Shape  : {df.shape}")
print(f"▸ Memory : {df.memory_usage(deep=True).sum() / 1024:.1f} KB")

# 2.4 Missing values
print("\n▸ Missing values per column:")
missing = df.isnull().sum()
missing = missing[missing > 0]
print(missing if not missing.empty else "   None — dataset has no missing values.")

# 2.5 Duplicate rows
print(f"\n▸ Fully duplicate rows : {df.duplicated().sum()}")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 3 — DATA CLEANING
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECTION 3 — DATA CLEANING")
print("="*60)

original_rows = len(df)

# 3.1 Strip whitespace from all string columns
str_cols = df.select_dtypes(include="object").columns
for col in str_cols:
    df[col] = df[col].str.strip()
print("✅ Stripped leading/trailing whitespace from all text columns.")

# 3.2 Convert date columns to datetime
for date_col in ["Order Date", "Ship Date"]:
    if date_col in df.columns:
        df[date_col] = pd.to_datetime(df[date_col], dayfirst=True, errors="coerce")
        print(f"✅ '{date_col}' converted to datetime.")

# 3.3 Fill missing Postal Codes
#     Burlington, Vermont has a known missing ZIP → 05401
if "Postal Code" in df.columns and df["Postal Code"].isnull().sum() > 0:
    mask = (df["City"] == "Burlington") & (df["State"] == "Vermont")
    df.loc[mask, "Postal Code"] = 5401
    df["Postal Code"] = df["Postal Code"].astype(int)
    print(f"✅ Filled {mask.sum()} missing Postal Codes for Burlington, Vermont → 05401")

# 3.4 Remove fully duplicate rows (keep first occurrence)
df.drop_duplicates(inplace=True)
removed = original_rows - len(df)
print(f"✅ Removed {removed} fully duplicate rows. Remaining rows: {len(df):,}")

# 3.5 Round Sales to 2 decimal places
if "Sales" in df.columns:
    df["Sales"] = df["Sales"].round(2)
    print("✅ Sales column rounded to 2 decimal places.")

# 3.6 Engineer useful time features from Order Date
df["Year"]       = df["Order Date"].dt.year
df["Month"]      = df["Order Date"].dt.month
df["YearMonth"]  = df["Order Date"].dt.to_period("M").astype(str)
df["Quarter"]    = df["Order Date"].dt.quarter
print("✅ Time features extracted: Year, Month, YearMonth, Quarter.")

print(f"\n✅ Cleaning complete. Final shape: {df.shape[0]:,} rows × {df.shape[1]} columns")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 4 — EXPLORATORY DATA ANALYSIS (EDA) — KPIs
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECTION 4 — KEY PERFORMANCE INDICATORS (KPIs)")
print("="*60)

total_sales      = df["Sales"].sum()
total_orders     = df["Order ID"].nunique()
avg_order_value  = total_sales / total_orders
unique_customers = df["Customer ID"].nunique()
top_region       = df.groupby("Region")["Sales"].sum().idxmax()
top_segment      = df.groupby("Segment")["Sales"].sum().idxmax()
top_category     = df.groupby("Category")["Sales"].sum().idxmax()
top_product      = df.groupby("Product Name")["Sales"].sum().idxmax()
top_product_val  = df.groupby("Product Name")["Sales"].sum().max()

print(f"\n  💰 Total Sales          : ${total_sales:>15,.2f}")
print(f"  📦 Total Orders         : {total_orders:>15,}")
print(f"  🧾 Avg Order Value      : ${avg_order_value:>15,.2f}")
print(f"  👥 Unique Customers     : {unique_customers:>15,}")
print(f"  🗺️  Top Region           : {top_region}")
print(f"  👔 Top Segment          : {top_segment}")
print(f"  📂 Top Category         : {top_category}")
print(f"  🥇 Top Product          : {top_product} (${top_product_val:,.2f})")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 5 — EDA TABLES
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECTION 5 — EDA ANALYSIS TABLES")
print("="*60)

# 5.1 Sales by Ship Mode
print("\n▸ Sales by Ship Mode:")
ship_mode = (df.groupby("Ship Mode")["Sales"]
               .agg(Total_Sales="sum", Orders="count")
               .assign(Avg_Sale=lambda x: x["Total_Sales"] / x["Orders"])
               .sort_values("Total_Sales", ascending=False)
               .round(2))
print(ship_mode.to_string())

# 5.2 Sales by Segment
print("\n▸ Sales by Customer Segment:")
segment = (df.groupby("Segment")["Sales"]
             .agg(Total_Sales="sum", Orders="count")
             .assign(Pct=lambda x: (x["Total_Sales"] / x["Total_Sales"].sum() * 100).round(1))
             .sort_values("Total_Sales", ascending=False))
print(segment.to_string())

# 5.3 Sales by Category
print("\n▸ Sales by Category:")
category = (df.groupby("Category")["Sales"]
              .sum()
              .sort_values(ascending=False)
              .round(2))
print(category.to_string())

# 5.4 Sales by Region
print("\n▸ Sales by Region:")
region = (df.groupby("Region")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .round(2))
print(region.to_string())

# 5.5 Top 10 States
print("\n▸ Top 10 States by Revenue:")
top_states = (df.groupby("State")["Sales"]
                .sum()
                .sort_values(ascending=False)
                .head(10)
                .round(2))
print(top_states.to_string())

# 5.6 Sub-Category performance
print("\n▸ Sub-Category Performance (all 17):")
subcat = (df.groupby("Sub-Category")["Sales"]
            .sum()
            .sort_values(ascending=False)
            .round(2))
print(subcat.to_string())

# 5.7 Top 10 Products
print("\n▸ Top 10 Best-Selling Products:")
top_products = (df.groupby("Product Name")["Sales"]
                  .sum()
                  .sort_values(ascending=False)
                  .head(10)
                  .round(2))
print(top_products.to_string())

# 5.8 Annual sales
print("\n▸ Annual Sales Summary:")
annual = (df.groupby("Year")["Sales"]
            .sum()
            .round(2))
print(annual.to_string())


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 6 — VISUALIZATION SETUP
# ─────────────────────────────────────────────────────────────────────────────

# ── Color palette ──────────────────────────────────────────────────────────
DARK_BLUE = "#1F3864"
MID_BLUE  = "#2E75B6"
TEAL      = "#17A589"
ORANGE    = "#ED7D31"
GREEN     = "#70AD47"
PURPLE    = "#8E44AD"
RED       = "#C0392B"
GOLD      = "#F4C518"
GRAY      = "#404040"
LGRAY     = "#F2F2F2"

PALETTE   = [MID_BLUE, TEAL, ORANGE, GREEN, PURPLE, RED, GOLD, "#2E86AB", "#C0392B", "#27AE60"]

# ── Global matplotlib style ─────────────────────────────────────────────────
sns.set_style("whitegrid")
plt.rcParams.update({
    "font.family"        : "DejaVu Sans",
    "axes.spines.top"    : False,
    "axes.spines.right"  : False,
    "figure.facecolor"   : "white",
    "axes.facecolor"     : "#FAFAFA",
    "axes.titlesize"     : 14,
    "axes.titleweight"   : "bold",
    "axes.titlecolor"    : DARK_BLUE,
    "axes.labelsize"     : 10,
    "axes.labelcolor"    : GRAY,
    "xtick.labelsize"    : 9,
    "ytick.labelsize"    : 9,
})


def save_chart(fig, filename):
    """Save chart to ./charts/ folder at high resolution."""
    path = f"charts/{filename}"
    fig.savefig(path, dpi=150, bbox_inches="tight", facecolor="white")
    plt.show()
    print(f"   💾 Saved → {path}")


# ─────────────────────────────────────────────────────────────────────────────
# CHART 1 — Monthly Sales Trend (Line Chart)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("CHART 1 — Monthly Sales Trend (2015–2018)")
print("="*60)

monthly = (df.groupby("YearMonth")["Sales"]
             .sum()
             .reset_index()
             .rename(columns={"Sales": "Total_Sales"}))
monthly["Sales_K"] = monthly["Total_Sales"] / 1000

fig, ax = plt.subplots(figsize=(14, 5))

# Main line + shaded fill
ax.plot(monthly["YearMonth"], monthly["Sales_K"],
        color=MID_BLUE, linewidth=2.2, zorder=3)
ax.fill_between(range(len(monthly)), monthly["Sales_K"],
                alpha=0.12, color=MID_BLUE)

# Mark the peak month
peak_idx = monthly["Sales_K"].idxmax()
ax.scatter(monthly["YearMonth"].iloc[peak_idx],
           monthly["Sales_K"].iloc[peak_idx],
           color=RED, s=100, zorder=5)
ax.annotate(
    f"Peak: ${monthly['Sales_K'].iloc[peak_idx]:.1f}K\n{monthly['YearMonth'].iloc[peak_idx]}",
    xy=(monthly["YearMonth"].iloc[peak_idx], monthly["Sales_K"].iloc[peak_idx]),
    xytext=(0, 16), textcoords="offset points",
    ha="center", fontsize=8.5, color=RED, fontweight="bold"
)

# Year boundary lines
year_starts = monthly[monthly["YearMonth"].str.endswith("-01")]["YearMonth"]
for yt in year_starts:
    ax.axvline(x=yt, color=DARK_BLUE, alpha=0.15, linewidth=1, linestyle="--")

# X-axis: show every 3rd label to avoid clutter
step = 3
ax.set_xticks(monthly["YearMonth"].iloc[::step])
ax.set_xticklabels(monthly["YearMonth"].iloc[::step], rotation=45, ha="right")

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax.set_xlim(monthly["YearMonth"].iloc[0], monthly["YearMonth"].iloc[-1])
ax.set_title("Monthly Sales Trend  (2015 – 2018)", pad=14)
ax.set_xlabel("Month")
ax.set_ylabel("Sales ($ Thousands)")
ax.grid(axis="y", alpha=0.4)
ax.grid(axis="x", alpha=0)

fig.tight_layout()
save_chart(fig, "01_monthly_sales_trend.png")


# ─────────────────────────────────────────────────────────────────────────────
# CHART 2 — Top 10 States by Revenue (Horizontal Bar)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("CHART 2 — Top 10 States by Revenue")
print("="*60)

states_10 = (df.groupby("State")["Sales"]
               .sum()
               .nlargest(10)
               .sort_values())   # ascending so highest is at top of chart

# Color-code: #1 = red, top 3 = gold, rest = blue
bar_colors = [
    RED  if i == 9 else
    GOLD if i >= 7 else
    MID_BLUE
    for i in range(10)
]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(states_10.index, states_10.values / 1000,
               color=bar_colors, edgecolor="white", linewidth=0.5)

# Value labels at the end of each bar
for bar, val in zip(bars, states_10.values):
    ax.text(val / 1000 + 2,
            bar.get_y() + bar.get_height() / 2,
            f"${val / 1000:.1f}K",
            va="center", fontsize=9, color=GRAY, fontweight="bold")

ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax.set_xlim(0, states_10.max() / 1000 * 1.2)
ax.set_title("Top 10 States by Revenue", pad=14)
ax.set_xlabel("Total Sales ($ Thousands)")
ax.set_ylabel("State")

legend_patches = [
    mpatches.Patch(color=RED,      label="#1 State"),
    mpatches.Patch(color=GOLD,     label="Top 3"),
    mpatches.Patch(color=MID_BLUE, label="Top 4–10"),
]
ax.legend(handles=legend_patches, loc="lower right", fontsize=9)
ax.grid(axis="x", alpha=0.4)
ax.grid(axis="y", alpha=0)

fig.tight_layout()
save_chart(fig, "02_top10_states.png")


# ─────────────────────────────────────────────────────────────────────────────
# CHART 3 — Sales by Product Category (Bar Chart)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("CHART 3 — Sales by Product Category")
print("="*60)

cat_sales = (df.groupby("Category")["Sales"]
               .sum()
               .sort_values(ascending=False))

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(cat_sales.index, cat_sales.values / 1000,
              color=[MID_BLUE, TEAL, ORANGE],
              edgecolor="white", linewidth=0.5, width=0.5)

# Annotate bars with value + percentage
total_cat = cat_sales.sum()
for bar, val in zip(bars, cat_sales.values):
    pct = val / total_cat * 100
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 4,
            f"${val / 1000:.1f}K\n({pct:.1f}%)",
            ha="center", fontsize=10, fontweight="bold", color=DARK_BLUE)

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax.set_ylim(0, cat_sales.max() / 1000 * 1.25)
ax.set_title("Sales by Product Category", pad=14)
ax.set_xlabel("Category")
ax.set_ylabel("Total Sales ($ Thousands)")
ax.grid(axis="y", alpha=0.4)
ax.grid(axis="x", alpha=0)

fig.tight_layout()
save_chart(fig, "03_category_sales.png")


# ─────────────────────────────────────────────────────────────────────────────
# CHART 4 — Sales by Customer Segment (Donut Chart)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("CHART 4 — Sales by Customer Segment (Donut)")
print("="*60)

seg_sales = df.groupby("Segment")["Sales"].sum()

fig, ax = plt.subplots(figsize=(7, 6))
wedges, texts, autotexts = ax.pie(
    seg_sales.values,
    labels=None,
    colors=[MID_BLUE, TEAL, ORANGE],
    autopct="%1.1f%%",
    startangle=90,
    pctdistance=0.78,
    wedgeprops=dict(width=0.52, edgecolor="white", linewidth=2),
)

# Style the percentage labels
for at in autotexts:
    at.set_fontsize(11)
    at.set_fontweight("bold")
    at.set_color("white")

# Center text showing total
ax.text(0, 0,
        f"${seg_sales.sum() / 1e6:.2f}M\nTotal",
        ha="center", va="center",
        fontsize=13, fontweight="bold", color=DARK_BLUE)

# Legend with dollar values
legend_labels = [
    f"{name}: ${val / 1000:.0f}K ({val / seg_sales.sum() * 100:.1f}%)"
    for name, val in zip(seg_sales.index, seg_sales.values)
]
ax.legend(wedges, legend_labels,
          loc="lower center", bbox_to_anchor=(0.5, -0.08),
          fontsize=10, frameon=False)

ax.set_title("Sales by Customer Segment", fontsize=14,
             fontweight="bold", color=DARK_BLUE, pad=16)
fig.tight_layout()
save_chart(fig, "04_segment_donut.png")


# ─────────────────────────────────────────────────────────────────────────────
# CHART 5 — Sub-Category Performance (Horizontal Bar — All 17)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("CHART 5 — Sub-Category Performance (All 17)")
print("="*60)

subcat_sorted = (df.groupby("Sub-Category")["Sales"]
                   .sum()
                   .sort_values())   # ascending → shortest bar at bottom

# Color-code by performance tier
q80 = subcat_sorted.quantile(0.8)
q20 = subcat_sorted.quantile(0.2)
sc_colors = [
    GREEN if v >= q80 else
    RED   if v <= q20 else
    MID_BLUE
    for v in subcat_sorted.values
]

fig, ax = plt.subplots(figsize=(10, 8))
bars = ax.barh(subcat_sorted.index, subcat_sorted.values / 1000,
               color=sc_colors, edgecolor="white", linewidth=0.4)

for bar, val in zip(bars, subcat_sorted.values):
    ax.text(val / 1000 + 1.5,
            bar.get_y() + bar.get_height() / 2,
            f"${val / 1000:.1f}K",
            va="center", fontsize=8.5, color=GRAY)

ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax.set_xlim(0, subcat_sorted.max() / 1000 * 1.22)
ax.set_title("Sub-Category Sales Performance  (All 17 Sub-Categories)", pad=14)
ax.set_xlabel("Total Sales ($ Thousands)")
ax.set_ylabel("Sub-Category")

legend_patches = [
    mpatches.Patch(color=GREEN,    label="Top Performer (Top 20%)"),
    mpatches.Patch(color=MID_BLUE, label="Average"),
    mpatches.Patch(color=RED,      label="Needs Attention (Bottom 20%)"),
]
ax.legend(handles=legend_patches, loc="lower right", fontsize=9)
ax.grid(axis="x", alpha=0.4)
ax.grid(axis="y", alpha=0)

fig.tight_layout()
save_chart(fig, "05_subcategory_performance.png")


# ─────────────────────────────────────────────────────────────────────────────
# CHART 6 — Sales by Region (Bar Chart)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("CHART 6 — Sales by Region")
print("="*60)

reg_sales = (df.groupby("Region")["Sales"]
               .sum()
               .sort_values(ascending=False))

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.bar(reg_sales.index, reg_sales.values / 1000,
              color=[RED, MID_BLUE, TEAL, ORANGE],
              edgecolor="white", linewidth=0.5, width=0.5)

total_reg = reg_sales.sum()
for bar, val in zip(bars, reg_sales.values):
    pct = val / total_reg * 100
    ax.text(bar.get_x() + bar.get_width() / 2,
            bar.get_height() + 3,
            f"${val / 1000:.1f}K\n({pct:.1f}%)",
            ha="center", fontsize=10, fontweight="bold", color=DARK_BLUE)

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax.set_ylim(0, reg_sales.max() / 1000 * 1.25)
ax.set_title("Sales by Region", pad=14)
ax.set_xlabel("Region")
ax.set_ylabel("Total Sales ($ Thousands)")
ax.grid(axis="y", alpha=0.4)
ax.grid(axis="x", alpha=0)

fig.tight_layout()
save_chart(fig, "06_region_sales.png")


# ─────────────────────────────────────────────────────────────────────────────
# CHART 7 — Stacked Bar: Category × Segment
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("CHART 7 — Sales by Category & Segment (Stacked Bar)")
print("="*60)

cat_seg = (df.groupby(["Category", "Segment"])["Sales"]
             .sum()
             .unstack()
             .fillna(0)
             / 1000)   # convert to $K

seg_colors_stack = [MID_BLUE, TEAL, ORANGE]
bottom = np.zeros(len(cat_seg))

fig, ax = plt.subplots(figsize=(9, 5))

for seg_name, color in zip(cat_seg.columns, seg_colors_stack):
    bars = ax.bar(cat_seg.index, cat_seg[seg_name],
                  bottom=bottom, label=seg_name,
                  color=color, edgecolor="white", linewidth=0.5)
    # Label segments inside bars if large enough
    for bar, b, val in zip(bars, bottom, cat_seg[seg_name]):
        if val > 25:
            ax.text(bar.get_x() + bar.get_width() / 2,
                    b + val / 2,
                    f"${val:.0f}K",
                    ha="center", va="center",
                    fontsize=9, color="white", fontweight="bold")
    bottom += cat_seg[seg_name].values

ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax.set_title("Sales by Category & Customer Segment", pad=14)
ax.set_xlabel("Category")
ax.set_ylabel("Sales ($ Thousands)")
ax.legend(title="Segment", fontsize=9, title_fontsize=9)
ax.grid(axis="y", alpha=0.4)
ax.grid(axis="x", alpha=0)

fig.tight_layout()
save_chart(fig, "07_category_segment_stacked.png")


# ─────────────────────────────────────────────────────────────────────────────
# CHART 8 — Annual Sales Trend by Segment (Multi-Line)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("CHART 8 — Annual Sales Trend by Segment")
print("="*60)

yr_seg = (df.groupby(["Year", "Segment"])["Sales"]
            .sum()
            .unstack()
            .fillna(0))

fig, ax = plt.subplots(figsize=(9, 5))

for seg_name, color in zip(yr_seg.columns, [MID_BLUE, TEAL, ORANGE]):
    ax.plot(yr_seg.index, yr_seg[seg_name] / 1000,
            marker="o", linewidth=2.2, color=color,
            label=seg_name, markersize=7)
    # Annotate each data point
    for yr, val in zip(yr_seg.index, yr_seg[seg_name]):
        ax.annotate(f"${val / 1000:.0f}K",
                    xy=(yr, val / 1000),
                    xytext=(0, 10), textcoords="offset points",
                    ha="center", fontsize=8, color=color)

ax.set_xticks(yr_seg.index)
ax.yaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax.set_title("Annual Sales Trend by Customer Segment  (2015–2018)", pad=14)
ax.set_xlabel("Year")
ax.set_ylabel("Total Sales ($ Thousands)")
ax.legend(title="Segment", fontsize=9, title_fontsize=9)
ax.grid(axis="y", alpha=0.4)

fig.tight_layout()
save_chart(fig, "08_annual_segment_trend.png")


# ─────────────────────────────────────────────────────────────────────────────
# CHART 9 — Top 10 Best-Selling Products (Horizontal Bar)
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("CHART 9 — Top 10 Best-Selling Products")
print("="*60)

top10_prod = (df.groupby("Product Name")["Sales"]
                .sum()
                .nlargest(10)
                .sort_values())   # ascending for horizontal chart

# Shorten product names longer than 33 chars for readability
short_names = [n[:32] + "…" if len(n) > 33 else n for n in top10_prod.index]
prod_colors = [
    RED  if i == 9 else
    GOLD if i >= 7 else
    MID_BLUE
    for i in range(10)
]

fig, ax = plt.subplots(figsize=(10, 6))
bars = ax.barh(short_names, top10_prod.values / 1000,
               color=prod_colors, edgecolor="white", linewidth=0.4)

for bar, val in zip(bars, top10_prod.values):
    ax.text(val / 1000 + 0.5,
            bar.get_y() + bar.get_height() / 2,
            f"${val / 1000:.1f}K",
            va="center", fontsize=9, color=GRAY)

ax.xaxis.set_major_formatter(plt.FuncFormatter(lambda x, _: f"${x:.0f}K"))
ax.set_xlim(0, top10_prod.max() / 1000 * 1.22)
ax.set_title("Top 10 Best-Selling Products", pad=14)
ax.set_xlabel("Total Sales ($ Thousands)")
ax.set_ylabel("Product")

legend_patches = [
    mpatches.Patch(color=RED,      label="#1 Product"),
    mpatches.Patch(color=GOLD,     label="Top 3"),
    mpatches.Patch(color=MID_BLUE, label="Top 4–10"),
]
ax.legend(handles=legend_patches, loc="lower right", fontsize=9)
ax.grid(axis="x", alpha=0.4)
ax.grid(axis="y", alpha=0)

fig.tight_layout()
save_chart(fig, "09_top10_products.png")


# ─────────────────────────────────────────────────────────────────────────────
# CHART 10 — Sales Heatmap: Year × Month
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("CHART 10 — Monthly Sales Heatmap (Year × Month)")
print("="*60)

hm_data = (df.groupby(["Year", "Month"])["Sales"]
             .sum()
             .unstack()
             .fillna(0))
hm_data.columns = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
                   "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(
    hm_data / 1000,
    annot=True,
    fmt=".0f",
    cmap="Blues",
    linewidths=0.5,
    linecolor="white",
    ax=ax,
    cbar_kws={"label": "Sales ($K)", "shrink": 0.8},
    annot_kws={"size": 9},
)
ax.set_title("Sales Heatmap — Year × Month  (values in $K)", pad=14,
             fontsize=14, fontweight="bold", color=DARK_BLUE)
ax.set_ylabel("Year", fontsize=10, color=GRAY)
ax.set_xlabel("Month", fontsize=10, color=GRAY)
ax.set_yticklabels(ax.get_yticklabels(), rotation=0)

fig.tight_layout()
save_chart(fig, "10_heatmap_year_month.png")


# ─────────────────────────────────────────────────────────────────────────────
# SECTION 7 — KEY FINDINGS SUMMARY
# ─────────────────────────────────────────────────────────────────────────────

print("\n" + "="*60)
print("SECTION 7 — KEY FINDINGS SUMMARY")
print("="*60)

findings = {
    "Total Revenue"      : f"${total_sales:,.2f}  across 4 years (2015–2018)",
    "Total Orders"       : f"{total_orders:,}  unique orders from {unique_customers} customers",
    "Avg Order Value"    : f"${avg_order_value:,.2f}  per order",
    "Top Region"         : f"{top_region}  —  leads with ${df.groupby('Region')['Sales'].sum()[top_region]:,.2f}",
    "Top Category"       : f"{top_category}  —  ${df.groupby('Category')['Sales'].sum()[top_category]:,.2f}",
    "Top Product"        : f"{top_product}  —  ${top_product_val:,.2f}",
    "Weakest Sub-Cat"    : f"Fasteners  —  ${df.groupby('Sub-Category')['Sales'].sum()['Fasteners']:,.2f}  (consider discontinuing)",
    "Peak Month"         : f"{monthly.loc[monthly['Total_Sales'].idxmax(), 'YearMonth']}  —  ${monthly['Total_Sales'].max():,.2f}",
    "Seasonality"        : "Q4 (Oct–Dec) is consistently the strongest quarter every year",
    "Growth Opportunity" : "South region (17.2%) is the most underserved — highest growth potential",
}

for key, val in findings.items():
    print(f"  ▸ {key:<22} : {val}")

print("\n" + "="*60)
print("✅ ANALYSIS COMPLETE — All 10 charts saved to ./charts/")
print("="*60)
