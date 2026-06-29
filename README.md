# 📊 Superstore Sales Analysis

**Author:** Amiin Mohamed  
**Role:** Data Scientist / Data Analyst  
**Tools:** Python · pandas · Matplotlib · Seaborn · ReportLab  
**Dataset:** Superstore Sales (`train.csv`) — 9,800 rows × 18 columns  
**Period:** January 2015 – December 2018

---

## 📁 Repository Structure

```
superstore-analysis/
│
├── train.csv                        ← Raw dataset (input)
├── superstore_analysis.py           ← Main analysis script (Jupyter-ready)
├── requirements.txt                 ← Python dependencies
├── README.md                        ← This file
│
└── charts/                          ← Auto-generated visualizations
    ├── 01_monthly_sales_trend.png
    ├── 02_top10_states.png
    ├── 03_category_sales.png
    ├── 04_segment_donut.png
    ├── 05_subcategory_performance.png
    ├── 06_region_sales.png
    ├── 07_category_segment_stacked.png
    ├── 08_annual_segment_trend.png
    ├── 09_top10_products.png
    └── 10_heatmap_year_month.png
```

---

## 🚀 How to Run

### 1. Clone the repository
```bash
git clone https://github.com/YourUsername/superstore-analysis.git
cd superstore-analysis
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Run the script
```bash
python superstore_analysis.py
```

Or open it in Jupyter:
```bash
jupyter notebook
```
Then copy the code sections into notebook cells.

---

## 📌 What This Project Does

### ✅ Data Cleaning
- Strips whitespace from all text columns
- Converts `Order Date` and `Ship Date` to proper datetime format
- Fills missing Postal Codes (Burlington, Vermont → 05401)
- Removes fully duplicate rows
- Rounds Sales to 2 decimal places
- Engineers time features: Year, Month, Quarter, YearMonth

### ✅ Key Performance Indicators (KPIs)
| KPI | Value |
|-----|-------|
| Total Sales | $2,261,536.55 |
| Total Orders | 4,922 |
| Avg Order Value | $459.48 |
| Unique Customers | 793 |
| Top Region | West — $710,219.60 |
| Top Segment | Consumer — $1,148,060.29 |
| Top Category | Technology — $827,455.86 |
| Top Product | Canon imageCLASS 2200 Copier |

### ✅ Analysis Performed
- Monthly Sales Trend (2015–2018)
- Top 10 States by Revenue
- Sales by Category and Segment
- Regional Sales Performance
- Sub-Category Ranking (all 17 sub-categories)
- Top 10 Best-Selling Products
- Annual segment growth comparison
- Seasonality heatmap (Year × Month)

### ✅ Visualizations Generated (10 Charts)
| # | Chart | Type |
|---|-------|------|
| 1 | Monthly Sales Trend | Line Chart |
| 2 | Top 10 States | Horizontal Bar |
| 3 | Sales by Category | Bar Chart |
| 4 | Sales by Segment | Donut Chart |
| 5 | Sub-Category Performance | Horizontal Bar |
| 6 | Sales by Region | Bar Chart |
| 7 | Category × Segment | Stacked Bar |
| 8 | Annual Trend by Segment | Multi-Line |
| 9 | Top 10 Products | Horizontal Bar |
| 10 | Year × Month Heatmap | Heatmap |

---

## 💡 Key Findings

1. **Consumer Dominance** — Consumer segment = 50.8% of revenue but has the lowest Average Order Value ($225). Bundling strategies could significantly increase AOV.
2. **Technology Leads** — Technology category = 36.6% of total revenue. Phones and Machines are the top-2 sub-categories.
3. **West Region** = 31.4% of national revenue. California alone = 19.7%.
4. **Q4 Seasonality** — October–December is consistently the strongest quarter across all 4 years.
5. **Underperformers** — Fasteners ($3,001), Labels ($12,347), Envelopes ($16,128) = only 1.4% of revenue combined.

---

## 📄 License

This project is for educational and portfolio purposes.  
Dataset is publicly available via Kaggle (Superstore Sales Dataset).

---

*Built with Python · pandas · Matplotlib · Seaborn*
