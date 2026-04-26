# State of Future Index 2035
### Vietnam vs Philippines — Country-Level SOFI Analysis

**Course:** Information Visualization | Indiana University Bloomington  
**Client:** Elizabeth Florescu, The Millennium Project  
**Team D:** Nerice Rodrigues · Rachana Dharani · Tanvica Samudrala · Pooja Reddy · Shubham Khupase

---

## Project Overview

This project applies the State of Future Index (SOFI) methodology at the country level to compare Vietnam and Philippines across 22 development indicators spanning four domains — Economic, Health, Environment, and Social — using historical data from 2000 to 2023 and forecasts through 2035.

The dashboard combines two visualization tools: a 3-page interactive Power BI report and a Python-powered Streamlit web application, providing both embedded and standalone access to the analysis.

---

## Live Links

| Resource | URL |
|----------|-----|
| Streamlit Dashboard | https://nericee03-sofi-dashboard.streamlit.app |
| Power BI Dashboard | https://app.powerbi.com/view?r=eyJrIjoiYzBlOGEwYTItOTIxZC00NGY1LTg3NjctNmNiOGJjYmY0NTcxIiwidCI6IjExMTNiZTM0LWFlZDEtNGQwMC1hYjRiLWNkZDAyNTEwYmU5MSIsImMiOjN9 |
| GitHub Repository | https://github.com/nericee03/sofi-dashboard |
| Dataset — World Bank WDI | https://data.worldbank.org/indicator |

---

## Repository Structure

```
sofi-dashboard/
├── app.py                        ← Main Streamlit dashboard application
├── requirements.txt              ← Python package dependencies
├── README.md                     ← This file
└── data/
    ├── SOFI_final_v5.xlsx        ← Master dataset with SOFI scores + 2035 forecast
    ├── final_sofi_scores.csv     ← Cleaned SOFI scores per country per year
    ├── final_master_long.csv     ← All 22 indicators in long format (1,017 records)
    └── final_indicator_summary.csv ← Latest normalized scores per indicator
```

---

## Dataset

| Property | Details |
|----------|---------|
| Source | World Bank World Development Indicators (WDI) + Our World in Data (OWID CO2) |
| Countries | Vietnam, Philippines |
| Historical Period | 2000 – 2023 (24 years) |
| Forecast Period | 2024 – 2035 (linear regression, avg R² = 0.82) |
| Indicators | 22 total (20 from WDI, 2 from OWID) |
| SOFI Weight Coverage | 75.1% of full SOFI weight (1,420 of 1,890 points) |
| Total Records | 1,017 historical data points |

### Domain Breakdown

| Domain | Indicators | Key WDI Fields |
|--------|-----------|---------------|
| Economic | 6 | GNI per capita, GDP growth, Unemployment, Poverty rate, FDI inflows, R&D expenditure |
| Health | 6 | Life expectancy, Infant mortality, Undernourishment, Health expenditure, Access to healthcare |
| Environment | 5 | CO2 per capita, Forest area, Energy intensity, Access to clean water, Sanitation |
| Social | 5 | Education index, Income inequality (Gini), HDI components, Internet access, Safety |

### Scoring Methodology

- Each raw indicator is normalized to a 0–1 scale using min-max normalization
- A score above 1.0 means performance is better than the 2019 baseline
- A score below 1.0 means performance is worse than the 2019 baseline
- Composite SOFI score = weighted sum of all normalized indicator scores

---

## Visualization Tools

### Power BI — 3 Interactive Pages

Built in Microsoft Power BI Web using `SOFI_final_v5.xlsx`.

**Page 1 — SOFI Overview**
- KPI cards for Vietnam SOFI, Philippines SOFI, and gap
- SOFI trajectory line chart (2000–2035)
- Gap bar chart showing which country leads each year
- Year range slicer and Historical / Projected period filter

**Page 2 — Domain Breakdown**
- 4 line charts — one per domain (Economic, Health, Environment, Social)
- Vietnam vs Philippines comparison with 2035 forecast lines

**Page 3 — Scenario Simulator**
- Domain weight slicers — adjust how much each domain contributes
- Ribbon chart showing SOFI ranking over time
- Area chart for simulated SOFI trajectories

### Python — Streamlit Dashboard

Built using Plotly for interactive charts. Three unique visualizations not replicated in Power BI:

**Domain Decomposition (Stacked Bar)**
- Stacked bars for 6 snapshot years (2000, 2005, 2010, 2015, 2019, 2023)
- Vietnam (solid) vs Philippines (light) side by side
- Shows which domain contributes most to each country's total score

**Environment Deep Dive (Scatter Bubble)**
- CO2 per Capita vs Forest Area for each year
- Bubble size = Environment domain score
- Reveals the industrialization vs conservation trade-off

**22-Indicator Heatmap**
- All 22 indicators for both countries in a single heatmap
- Latest available year, sorted by domain
- Color intensity = normalized score (0–1 scale)

**Additional interactive features:**
- Sidebar year range slider (2000–2035)
- Spotlight year selector — updates 6 KPI cards instantly
- Domain filter — highlights selected domain across charts
- Indicator explorer — select any of 22 indicators for raw + normalized charts
- Data table — filter by country and domain, download as CSV

---

## Running Locally

### Prerequisites

- Python 3.9 or higher
- pip package manager

### Steps

```bash
# Clone the repository
git clone https://github.com/nericee03/sofi-dashboard.git
cd sofi-dashboard

# Install dependencies
pip install -r requirements.txt

# Run the dashboard
streamlit run app.py
```

The app opens automatically at **http://localhost:8501**

### Dependencies

```
streamlit>=1.32.0
pandas>=2.0.0
plotly>=5.18.0
numpy>=1.24.0
openpyxl>=3.1.0
```

---

## Key Findings

1. **Philippines overtook Vietnam around 2015** and forecasts project a widening lead through 2035, driven by stronger Social and Health domain growth.

2. **Environment is the critical weakness for both countries.** CO2 emissions are rising while forest area declines, pulling Environment scores down from 2020 onward. This is the highest-priority domain for policy intervention.

3. **Vietnam's Economic score peaked around 2019** and is projected to decline. Reducing export dependency and boosting domestic R&D investment is the recommended policy response.

4. **Health scores are converging.** Both countries show strong improvements — Vietnam leads slightly but the gap is closing, suggesting regional health infrastructure investments are working.

---

## Sidebar Controls

| Control | What It Does |
|---------|-------------|
| Year Range slider | Filters all Python charts to the selected period |
| Include Projection toggle | Adds or removes 2024–2035 forecast data |
| Spotlight Year | Updates the 6 KPI cards at the top of every page |
| Domain | Filters domain decomposition chart and heatmap |
| Indicator | Selects one of 22 indicators for the Indicator Explorer tab |

---

## Dashboard Tabs

| Tab | Content |
|-----|---------|
| Overview | Project summary, key finding note, dataset stats, domain snapshot bar |
| Power BI Dashboard | Live embedded Power BI report with all 3 pages |
| Python Charts | Domain Decomposition, CO2 vs Forest scatter, 22-Indicator Heatmap |
| Indicator Explorer | Raw value + normalized score charts for any selected indicator |
| Data | Filterable data table — view SOFI scores, indicator data, or summary |

---

## Deploying to Streamlit Cloud

```bash
# Push to GitHub
git add .
git commit -m "update"
git push origin main
```

Then go to **share.streamlit.io**, connect the repository `nericee03/sofi-dashboard`, set main file as `app.py`, and click Deploy.

---

## Acknowledgements

- **Client:** Elizabeth Florescu, The Millennium Project — for the SOFI methodology and project direction
- **Data:** World Bank Open Data (WDI) and Our World in Data (CO2 dataset)
- **Course:** Information Visualization, Indiana University Bloomington

---

*SOFI 2035 — Team D — Indiana University Bloomington — April 2026*
