/**
 * SASHI RANJAN — DATA & BUSINESS ANALYST PORTFOLIO
 * Core Interactive Client Script
 * Features: Command Center Simulation, Dynamic Tesla 5-Page BI Switcher,
 * Animated Numbers, Interactive Process Pipeline, Skills Filter,
 * Case Study Modals with Dynamic Tabs, Resume Modal & Accessibility.
 */

document.addEventListener('DOMContentLoaded', () => {
  'use strict';

  // ==========================================================================
  // 1. PROJECT CASE STUDY DATA STORE
  // ==========================================================================
  const CASE_STUDIES = {
    'digital-lending': {
      category: 'FINTECH · SQL · PYTHON · POWER BI',
      title: 'Digital Lending & FinTech Analytics Pipeline',
      image: 'assets/projects/digital-lending.jpg',
      tech: ['Python', 'MySQL', 'SQLAlchemy', 'PyMySQL', 'Pandas', 'NumPy', 'Power BI', 'Faker'],
      tabs: {
        overview: `
          <div class="modal-artwork-banner fintech-theme">
            <img src="assets/projects/digital-lending.jpg" alt="Digital Lending & FinTech Analytics Pipeline" class="modal-banner-img" />
          </div>
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Project Overview &amp; Commercial Problem</h4>
            <p class="modal-p">
              In retail and fintech digital lending, credit underwriters and portfolio managers need real-time visibility into customer risk profiles, EMI delinquency buckets, and loan recovery funnels to de-risk capital while maintaining loan disbursement growth.
            </p>
            <p class="modal-p">
              This project provides an end-to-end data engineering and analytics pipeline modeling <strong>592,000+ records</strong> across <strong>7 relational tables</strong> that simulate customer credit scores, banking links, underwriting criteria, daily EMI payment statuses, and debt recovery.
            </p>
          </div>
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Key Executive Metrics</h4>
            <div class="project-metrics-grid">
              <div class="p-metric"><span class="p-val">592K+</span><span class="p-lbl">Synthesized &amp; Validated Records</span></div>
              <div class="p-metric"><span class="p-val">7 Tables</span><span class="p-lbl">3NF Normalized Schema</span></div>
              <div class="p-metric"><span class="p-val">14.8%</span><span class="p-lbl">Simulated Default Risk Reduction</span></div>
            </div>
          </div>
        `,
        approach: `
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Data Architecture &amp; Pipeline Design</h4>
            <p class="modal-p">
              Engineered using Python with <code>Faker</code>, <code>Pandas</code>, and <code>NumPy</code> to generate statistically accurate financial distributions (credit scores between 300–900, realistic income-to-loan ratios, and time-stamped repayment logs).
            </p>
            <p class="modal-p">
              The normalized relational schema was deployed on <strong>MySQL</strong> via <code>SQLAlchemy</code> and <code>PyMySQL</code> with automated foreign key cascade rules, primary keys, and data-type validation assertions.
            </p>
          </div>
          <div class="modal-section-block">
            <h4 class="modal-sec-title">7 Relational Tables Modeled:</h4>
            <ul class="project-bullets">
              <li><strong>customer_master:</strong> Demographics, credit score, monthly income, employment sector.</li>
              <li><strong>customer_bank_account:</strong> Account types, IFSC codes, average balance tiers.</li>
              <li><strong>lender_master:</strong> Lender risk tolerance, interest rates, capital allocation.</li>
              <li><strong>loan_application:</strong> Loan amounts, tenure, approval status, disbursement dates.</li>
              <li><strong>repayment_schedule:</strong> Scheduled EMI dates, principal/interest breakdown.</li>
              <li><strong>payments:</strong> Real-time payment transactions, gateway modes, settlement timestamps.</li>
              <li><strong>collections_recovery:</strong> DPD triggers, agency allocation, recovery amounts.</li>
            </ul>
          </div>
        `,
        analysis: `
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Analytical Techniques &amp; SQL Querying</h4>
            <p class="modal-p">
              Leveraged advanced SQL including <strong>Common Table Expressions (CTEs)</strong>, <strong>Window Functions</strong> (<code>ROW_NUMBER()</code>, <code>RANK()</code>, <code>LEAD()</code>/<code>LAG()</code>), and statistical aggregations to segment customer risk and monitor loan health.
            </p>
            <p class="modal-p">
              Calculated critical lending KPIs:
            </p>
            <ul class="project-bullets">
              <li><code>Approval Rate %</code> = Approved Loans / Total Applications</li>
              <li><code>Delinquency Rate (30+ DPD)</code> = Overdue EMI Amount / Total Portfolio Exposure</li>
              <li><code>Collection Efficiency</code> = Total Amount Collected / Total Scheduled Due</li>
              <li><code>Customer Acquisition Cost (CAC) vs. Lifetime Value (LTV)</code> cohorts</li>
            </ul>
          </div>
        `,
        insights: `
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Strategic Business Insights &amp; Decision Impact</h4>
            <p class="modal-p">
              <strong>Finding 1:</strong> Applicants with credit scores between 620–680 borrowing for tenures exceeding 24 months showed a 2.4x higher probability of transitioning into 60+ DPD delinquency.
            </p>
            <p class="modal-p">
              <strong>Strategic Recommendation:</strong> Cap loan tenure at 18 months for mid-tier risk brackets and mandate auto-debit (eNACH) verification, preserving an estimated ₹38.5 Lakhs in capital per underwriting quarter.
            </p>
          </div>
        `,
        code: `
          <div class="modal-section-block">
            <h4 class="modal-sec-title">SQL Pipeline Schema &amp; Ingestion Script</h4>
            <div class="mini-query-box">
              <div class="mini-query-label">PYTHON &amp; MYSQL PIPELINE SNIPPET</div>
              <pre class="sql-code"><code>from sqlalchemy import create_engine
import pandas as pd

# Connect to MySQL Relational Database
engine = create_engine('mysql+pymysql://analyst:secret@localhost:3306/fintech_lending')

# Query DPD Cohort Segmentation with Window CTEs
query = """
WITH RiskCohorts AS (
    SELECT 
        c.customer_id,
        c.credit_score,
        c.employment_type,
        l.loan_amount,
        r.dpd_days,
        ROW_NUMBER() OVER(PARTITION BY c.customer_id ORDER BY r.payment_date DESC) as latest_rank
    FROM customer_master c
    JOIN loan_application l ON c.customer_id = l.customer_id
    JOIN repayment_schedule r ON l.application_id = r.application_id
)
SELECT 
    employment_type,
    AVG(credit_score) as avg_credit_score,
    SUM(loan_amount) as total_exposure,
    COUNT(CASE WHEN dpd_days > 30 THEN 1 END) * 100.0 / COUNT(*) as delinquency_pct
FROM RiskCohorts
WHERE latest_rank = 1
GROUP BY employment_type
ORDER BY delinquency_pct DESC;
"""

df_risk = pd.read_sql(query, engine)
print("Pipeline ETL & Analytics extraction completed successfully.")</code></pre>
            </div>
          </div>
        `
      }
    },
    'tesla-analytics': {
      category: 'BUSINESS INTELLIGENCE · POWER BI · DAX',
      title: 'Tesla Business Performance Analytics (2015–2025)',
      image: 'assets/projects/tesla-analytics.jpg',
      tech: ['Power BI', 'DAX', 'Power Query', 'Data Modeling', 'Dashboard Design'],
      tabs: {
        overview: `
          <div class="modal-artwork-banner automotive-theme">
            <img src="assets/projects/tesla-analytics.jpg" alt="Tesla Business Performance Analytics" class="modal-banner-img" />
          </div>
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Project Scope &amp; Objective</h4>
            <p class="modal-p">
              Designed a multi-page interactive Power BI dashboard tracking Tesla's decade-long transformation (2015–2025). The goal was to provide executives with instantaneous visibility into vehicle production numbers, automotive gross margins, regional deliveries, and energy sector growth.
            </p>
          </div>
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Dashboard Dimensions</h4>
            <div class="project-metrics-grid">
              <div class="p-metric"><span class="p-val">5 Pages</span><span class="p-lbl">Interactive Architecture</span></div>
              <div class="p-metric"><span class="p-val">30+</span><span class="p-lbl">DAX Calculated Measures</span></div>
              <div class="p-metric"><span class="p-val">10 Years</span><span class="p-lbl">Historical Trend Data</span></div>
            </div>
          </div>
        `,
        approach: `
          <div class="modal-section-block">
            <h4 class="modal-sec-title">ETL &amp; Star-Schema Modeling</h4>
            <p class="modal-p">
              Financial and operational disclosures were aggregated and cleaned in Power Query. Constructed a Star Schema featuring central fact tables (<code>Fact_Deliveries</code>, <code>Fact_Financials</code>, <code>Fact_Energy</code>) linked to conformed dimensions (<code>Dim_Date</code>, <code>Dim_Vehicle_Model</code>, <code>Dim_Region</code>).
            </p>
          </div>
        `,
        analysis: `
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Complex DAX Calculations</h4>
            <p class="modal-p">
              Engineered over 30 DAX measures incorporating time-intelligence (<code>SAMEPERIODLASTYEAR</code>, <code>TOTALYTD</code>), dynamic currency parameter switchers, and rolling margin calculations.
            </p>
            <div class="mini-query-box">
              <pre class="sql-code"><code>// DAX Measure: Automotive Gross Margin Ex-Regulatory Credits
Auto Gross Margin % = 
DIVIDE(
    [Automotive Revenue] - [Automotive Regulatory Credits] - [Auto COGS],
    [Automotive Revenue] - [Automotive Regulatory Credits],
    0
)</code></pre>
            </div>
          </div>
        `,
        insights: `
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Key Executive Insights</h4>
            <p class="modal-p">
              <strong>Volume vs. Margin:</strong> Revealed how Model 3/Y mass scaling compressed per-unit gross margins while expanding absolute gross profit dollars by 420% between 2019 and 2023.
            </p>
            <p class="modal-p">
              <strong>Energy Diversification:</strong> Highlighted Megapack utility storage deployments growing at a 125% CAGR, emerging as a major margin stabilizer.
            </p>
          </div>
        `,
        code: `
          <div class="modal-section-block">
            <h4 class="modal-sec-title">DAX Measure Catalog Snippet</h4>
            <div class="mini-query-box">
              <pre class="sql-code"><code>// Production vs Delivery Variance
Delivery-to-Production Ratio = 
DIVIDE(
    SUM(Fact_Deliveries[Deliveries_Count]),
    SUM(Fact_Deliveries[Production_Count]),
    1.0
)

// Rolling 4-Quarter Revenue
Rolling_4Q_Revenue = 
CALCULATE(
    [Total Revenue],
    DATESINPERIOD(Dim_Date[DateKey], MAX(Dim_Date[DateKey]), -4, QUARTER)
)</code></pre>
            </div>
          </div>
        `
      }
    },
    'ai-economy': {
      category: 'ECONOMICS · ADVANCED EXCEL · DATA STORYTELLING',
      title: 'AI & Its Impact on the Global Economy (1st Place Winner)',
      image: 'assets/projects/ai-global-economy.jpg',
      tech: ['Advanced Excel', 'Pivot Tables', 'Dashboard Design', 'KPI Analysis', 'Data Storytelling'],
      tabs: {
        overview: `
          <div class="modal-artwork-banner ai-theme">
            <img src="assets/projects/ai-global-economy.jpg" alt="AI & Its Impact on the Global Economy" class="modal-banner-img" />
          </div>
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Award-Winning Economic Analysis</h4>
            <p class="modal-p">
              Conducted an in-depth exploratory data analysis on <strong>1,600+ records</strong> evaluating the global impact of artificial intelligence adoption across 12 major industry sectors, analyzing productivity gains against workforce disruption.
            </p>
            <p class="modal-p">
              Awarded <strong>1st Place</strong> at the ITVedant Data Analytics Hackathon for analytical depth, dashboard ergonomics, and persuasive data storytelling.
            </p>
          </div>
        `,
        approach: `
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Excel Architecture &amp; Methodology</h4>
            <p class="modal-p">
              Constructed multi-tab dynamic spreadsheets utilizing multi-level Pivot Tables, nested <code>XLOOKUP</code> functions, dynamic array formulas, and conditional formatting heatmaps to provide instant visual clarity to macro-economic indicators.
            </p>
          </div>
        `,
        analysis: `
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Exploratory &amp; Sectoral Modeling</h4>
            <p class="modal-p">
              Segmented industries into high, medium, and low AI exposure tiers. Quantified cross-elasticity between technology capital investment and labor displacement over a 5-year forecast horizon.
            </p>
          </div>
        `,
        insights: `
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Hackathon Winning Insights</h4>
            <p class="modal-p">
              Disproved the assumption that AI generates net job destruction in all sectors. High-adoption industries (Finance &amp; IT) experienced short-term friction followed by a 34% net productivity surplus and reallocation toward higher-value analytical roles.
            </p>
          </div>
        `,
        code: `
          <div class="modal-section-block">
            <h4 class="modal-sec-title">Formula Architecture</h4>
            <div class="mini-query-box">
              <pre class="sql-code"><code>=XLOOKUP(A2, Dim_Sector[SectorID], Dim_Sector[Adoption_Rate], 0, 1)
=IFERROR(INDEX(Data_Matrix, MATCH(1, (Country=C2)*(Year=D2), 0), 4), "N/A")
=SUMIFS(Fact_Productivity[Delta], Fact_Productivity[Tier], "High", Fact_Productivity[Region], "North America")</code></pre>
            </div>
          </div>
        `
      }
    }
  };

  // ==========================================================================
  // 2. TESLA 5-PAGE DASHBOARD SIMULATION DATA
  // ==========================================================================
  const TESLA_PAGES = {
    exec: {
      kpis: [
        { label: 'TOTAL REVENUE (YoY)', val: '$96.7B', trend: '↑ +19% YoY' },
        { label: 'ANNUAL DELIVERIES', val: '1.81M Units', trend: '↑ +38% YoY' },
        { label: 'OPERATING MARGIN', val: '9.2%', trend: 'Industry Leading' }
      ],
      bars: [25, 35, 48, 65, 82, 95, 98],
      labels: ["'18", "'19", "'20", "'21", "'22", "'23", "'24"],
      dax: 'YoY Revenue Growth % = DIVIDE([Total Revenue] - [Revenue LY], [Revenue LY], 0)'
    },
    rev: {
      kpis: [
        { label: 'AUTOMOTIVE REVENUE', val: '$82.4B', trend: '85.2% Total' },
        { label: 'GROSS PROFIT', val: '$17.7B', trend: '18.2% Gross Margin' },
        { label: 'FREE CASH FLOW', val: '$4.4B', trend: 'Strong Liquidity' }
      ],
      bars: [20, 28, 42, 60, 78, 88, 92],
      labels: ["'18", "'19", "'20", "'21", "'22", "'23", "'24"],
      dax: 'Auto Gross Margin % = DIVIDE([Automotive Revenue] - [Auto COGS], [Automotive Revenue], 0)'
    },
    prod: {
      kpis: [
        { label: 'MODEL 3/Y VOLUME', val: '1.74M Units', trend: '96.1% Share' },
        { label: 'MODEL S/X & CYBERTRUCK', val: '70.8K Units', trend: 'Premium Tier' },
        { label: 'PRODUCTION CAPACITY', val: '2.35M / Year', trend: 'Global Run Rate' }
      ],
      bars: [15, 25, 38, 55, 75, 92, 99],
      labels: ["'18", "'19", "'20", "'21", "'22", "'23", "'24"],
      dax: 'Delivery-to-Production Ratio = DIVIDE([Total Deliveries], [Total Produced Units], 1.0)'
    },
    seg: {
      kpis: [
        { label: 'ENERGY STORAGE (GWh)', val: '14.7 GWh', trend: '↑ +125% YoY' },
        { label: 'SERVICES & OTHER REV', val: '$8.3B', trend: 'Supercharging/Parts' },
        { label: 'ENERGY MARGIN %', val: '24.6%', trend: 'Rapid Expansion' }
      ],
      bars: [10, 18, 26, 40, 58, 80, 96],
      labels: ["'18", "'19", "'20", "'21", "'22", "'23", "'24"],
      dax: 'Energy Growth % = DIVIDE([Energy Rev] - [Energy Rev LY], [Energy Rev LY], 0)'
    },
    geo: {
      kpis: [
        { label: 'NORTH AMERICA', val: '47.2%', trend: 'Primary Market' },
        { label: 'CHINA (GIGA SHANGHAI)', val: '31.5%', trend: 'High Margin Export Hub' },
        { label: 'EUROPE & OTHER', val: '21.3%', trend: 'Giga Berlin Scaling' }
      ],
      bars: [30, 42, 54, 68, 80, 90, 95],
      labels: ["'18", "'19", "'20", "'21", "'22", "'23", "'24"],
      dax: 'Regional Share % = DIVIDE([Regional Revenue], [Total Global Revenue], 0)'
    }
  };

  // ==========================================================================
  // 3. "HOW I THINK" INTERACTIVE PROCESS PIPELINE DATA
  // ==========================================================================
  const PROCESS_STEPS = [
    {
      tag: 'PHASE 01: PROBLEM FORMULATION',
      title: '01. Understand The Business Question',
      desc: 'Before writing a single query or script, I deconstruct the commercial objective. What decision hinges on this analysis? Who are the stakeholders? What constitutes success? This prevents vanity metrics and guarantees commercial alignment.',
      deliverables: [
        '• Problem Statement Definition',
        '• Key Metric Identification',
        '• Stakeholder Alignment'
      ],
      simTitle: 'DATA_STATE: RAW_CHAOTIC',
      visualHtml: `
        <div class="sim-state-visual step-1-visual">
          <div class="chaotic-nodes">
            <span class="c-dot">?</span>
            <span class="c-dot">?</span>
            <span class="c-dot">?</span>
            <span class="c-dot">?</span>
            <span class="c-dot">?</span>
          </div>
          <span class="sim-caption">Untangled Raw Signals &amp; Business Objectives</span>
        </div>
      `
    },
    {
      tag: 'PHASE 02: DATA INTEGRITY & AUDITING',
      title: '02. Clean & Audit The Data',
      desc: 'Flawed inputs produce dangerous conclusions. I profile datasets for missing records, anomalies, duplicate keys, and invalid categorical entries using automated Python checks and SQL assertions.',
      deliverables: [
        '• Missing Value Imputation',
        '• Outlier Detection & Tagging',
        '• Duplicate Key Elimination'
      ],
      simTitle: 'DATA_STATE: CLEANED_STRUCTURED',
      visualHtml: `
        <div class="sim-state-visual">
          <div style="display:flex; gap:10px; width:100%; justify-content:center;">
            <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:6px; padding:8px 12px; font-family:var(--font-mono); font-size:0.75rem; color:#10B981;">✓ 0 Null Keys</div>
            <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:6px; padding:8px 12px; font-family:var(--font-mono); font-size:0.75rem; color:#10B981;">✓ Normalized Types</div>
            <div style="background:rgba(16,185,129,0.1); border:1px solid rgba(16,185,129,0.3); border-radius:6px; padding:8px 12px; font-family:var(--font-mono); font-size:0.75rem; color:#10B981;">✓ Valid Ranges</div>
          </div>
          <span class="sim-caption">100% Validated Analytics-Ready Schema</span>
        </div>
      `
    },
    {
      tag: 'PHASE 03: ARCHITECTURE & ETL',
      title: '03. Transform & Model Relationships',
      desc: 'Structuring normalized relational tables (3NF) or star schemas in Power BI and MySQL. Implementing primary/foreign key integrity, date dimension tables, and automated ETL workflows.',
      deliverables: [
        '• Relational Star-Schema Design',
        '• Power Query M-Code & ETL Pipelines',
        '• Primary / Foreign Key Indexing'
      ],
      simTitle: 'DATA_STATE: RELATIONAL_MODEL',
      visualHtml: `
        <div class="sim-state-visual">
          <div style="display:grid; grid-template-columns:1fr 1fr; gap:8px; width:100%; max-width:280px;">
            <div style="background:rgba(139,92,246,0.15); border:1px solid var(--purple-primary); border-radius:4px; padding:6px; font-family:var(--font-mono); font-size:0.7rem; text-align:center; color:#fff;">Dim_Customer (PK)</div>
            <div style="background:rgba(139,92,246,0.15); border:1px solid var(--purple-primary); border-radius:4px; padding:6px; font-family:var(--font-mono); font-size:0.7rem; text-align:center; color:#fff;">Dim_Date (PK)</div>
            <div style="grid-column: span 2; background:rgba(192,132,252,0.2); border:1px solid var(--purple-bright); border-radius:4px; padding:8px; font-family:var(--font-mono); font-size:0.75rem; text-align:center; color:#fff; font-weight:700;">Fact_Transactions (FKs)</div>
          </div>
          <span class="sim-caption">Relational Star Schema Configured</span>
        </div>
      `
    },
    {
      tag: 'PHASE 04: QUANTITATIVE EXPLORATION',
      title: '04. Analyze & Compute Metrics',
      desc: 'Writing optimized SQL CTEs, window functions, statistical aggregates, and sophisticated DAX calculations to extract patterns, test hypotheses, and quantify distributions.',
      deliverables: [
        '• SQL Joins, CTEs & Window Functions',
        '• Time-Intelligence & YoY Variance Calculations',
        '• Borrower & Segment Cohort Analysis'
      ],
      simTitle: 'DATA_STATE: METRICS_COMPUTED',
      visualHtml: `
        <div class="sim-state-visual">
          <div style="background:#050308; border:1px solid var(--border-purple); border-radius:6px; padding:10px; width:100%; font-family:var(--font-mono); font-size:0.72rem; color:var(--text-secondary);">
            <div><span style="color:#C084FC;">AVG(</span>conversion_rate<span style="color:#C084FC;">)</span> = <span style="color:#10B981; font-weight:bold;">18.4%</span></div>
            <div><span style="color:#C084FC;">SUM(</span>revenue_yoy_delta<span style="color:#C084FC;">)</span> = <span style="color:#10B981; font-weight:bold;">+$14.2M</span></div>
            <div><span style="color:#C084FC;">DPD_30+_Risk</span> = <span style="color:#F59E0B; font-weight:bold;">3.8% (Target &lt; 5%)</span></div>
          </div>
          <span class="sim-caption">Verified Statistical Indicators Extracted</span>
        </div>
      `
    },
    {
      tag: 'PHASE 05: INTERACTIVE VISUALIZATION',
      title: '05. Visualize & Build Dashboards',
      desc: 'Designing uncluttered, intuitive dashboards in Power BI, Tableau, and Excel. Leveraging visual hierarchy, slicers, bookmarks, and drill-throughs so decision-makers see answers in seconds.',
      deliverables: [
        '• Executive KPI Command Centers',
        '• Interactive Slicers & Drill-Throughs',
        '• Clean Visual Information Hierarchy'
      ],
      simTitle: 'DATA_STATE: EXECUTIVE_DASHBOARD',
      visualHtml: `
        <div class="sim-state-visual">
          <div style="display:flex; align-items:flex-end; gap:8px; height:80px; width:200px; padding:10px; background:rgba(255,255,255,0.02); border:1px solid var(--border-subtle); border-radius:6px;">
            <div style="flex:1; height:30%; background:#8B5CF6; border-radius:3px 3px 0 0;"></div>
            <div style="flex:1; height:50%; background:#8B5CF6; border-radius:3px 3px 0 0;"></div>
            <div style="flex:1; height:75%; background:#8B5CF6; border-radius:3px 3px 0 0;"></div>
            <div style="flex:1; height:100%; background:#C084FC; border-radius:3px 3px 0 0; box-shadow:0 0 10px #C084FC;"></div>
          </div>
          <span class="sim-caption">Executive Visual Reporting Active</span>
        </div>
      `
    },
    {
      tag: 'PHASE 06: COMMERCIAL EXECUTION',
      title: '06. Recommend & Drive Impact',
      desc: 'Translating numbers into concrete business actions. Providing clear recommendations that reduce operational costs, de-risk lending portfolios, and accelerate revenue conversion.',
      deliverables: [
        '• Commercial Strategy Recommendations',
        '• Quantified ROI & Risk Mitigation',
        '• Stakeholder Presentation Deck'
      ],
      simTitle: 'DATA_STATE: BUSINESS_DECISION_ENABLED',
      visualHtml: `
        <div class="sim-state-visual">
          <div style="background:linear-gradient(135deg, rgba(139,92,246,0.2) 0%, rgba(16,185,129,0.2) 100%); border:1px solid var(--purple-bright); border-radius:8px; padding:12px; width:100%; text-align:center;">
            <div style="font-family:var(--font-mono); font-size:0.7rem; color:var(--purple-bright); font-weight:700;">STRATEGIC ACTION EXECUTED</div>
            <div style="font-size:0.9rem; font-weight:700; color:#FFFFFF; margin-top:4px;">14.8% Projected Risk Reduction</div>
          </div>
          <span class="sim-caption">Data Converted into Measurable Business Impact</span>
        </div>
      `
    }
  ];

  // ==========================================================================
  // 4. NAVIGATION BAR SCROLL SPY & STICKY STATE
  // ==========================================================================
  const mainNav = document.getElementById('mainNav');
  const desktopNavLinks = document.querySelectorAll('.nav-link');
  const sections = document.querySelectorAll('section[id], header[id]');

  function updateNavScroll() {
    if (window.scrollY > 40) {
      mainNav.classList.add('scrolled');
    } else {
      mainNav.classList.remove('scrolled');
    }

    let currentId = 'hero';
    sections.forEach(section => {
      const top = section.offsetTop - 140;
      const height = section.offsetHeight;
      if (window.scrollY >= top && window.scrollY < top + height) {
        currentId = section.getAttribute('id');
      }
    });

    desktopNavLinks.forEach(link => {
      link.classList.remove('active');
      if (link.getAttribute('href') === `#${currentId}`) {
        link.classList.add('active');
      }
    });
  }

  window.addEventListener('scroll', updateNavScroll, { passive: true });
  updateNavScroll();

  // ==========================================================================
  // 5. MOBILE DRAWER CONTROLS
  // ==========================================================================
  const mobileMenuToggle = document.getElementById('mobileMenuToggle');
  const mobileNavDrawer = document.getElementById('mobileNavDrawer');
  const drawerCloseBtn = document.getElementById('drawerCloseBtn');
  const mobileNavLinks = document.querySelectorAll('.mobile-nav-link, .mobile-cta-close');

  function openMobileNav() {
    mobileNavDrawer.classList.add('open');
    mobileNavDrawer.setAttribute('aria-hidden', 'false');
    mobileMenuToggle.setAttribute('aria-expanded', 'true');
    document.body.style.overflow = 'hidden';
  }

  function closeMobileNav() {
    mobileNavDrawer.classList.remove('open');
    mobileNavDrawer.setAttribute('aria-hidden', 'true');
    mobileMenuToggle.setAttribute('aria-expanded', 'false');
    document.body.style.overflow = '';
  }

  if (mobileMenuToggle) mobileMenuToggle.addEventListener('click', openMobileNav);
  if (drawerCloseBtn) drawerCloseBtn.addEventListener('click', closeMobileNav);
  mobileNavLinks.forEach(link => link.addEventListener('click', closeMobileNav));

  // ==========================================================================
  // 6. CUSTOM CURSOR TRACKER (Desktop)
  // ==========================================================================
  const cursorGlow = document.getElementById('cursorGlow');
  if (cursorGlow && window.matchMedia('(pointer: fine)').matches) {
    let mouseX = window.innerWidth / 2;
    let mouseY = window.innerHeight / 2;
    let currentX = mouseX;
    let currentY = mouseY;

    window.addEventListener('mousemove', e => {
      mouseX = e.clientX;
      mouseY = e.clientY;
    });

    function renderCursor() {
      currentX += (mouseX - currentX) * 0.15;
      currentY += (mouseY - currentY) * 0.15;
      cursorGlow.style.left = `${currentX}px`;
      cursorGlow.style.top = `${currentY}px`;
      requestAnimationFrame(renderCursor);
    }
    requestAnimationFrame(renderCursor);
  }

  // ==========================================================================
  // 7. HERO COMMAND CENTER PARALLAX EFFECT
  // ==========================================================================
  const heroVisualWrapper = document.getElementById('heroVisualWrapper');
  const commandCenter = document.getElementById('commandCenter');

  if (heroVisualWrapper && commandCenter && window.matchMedia('(min-width: 1024px)').matches) {
    heroVisualWrapper.addEventListener('mousemove', e => {
      const rect = heroVisualWrapper.getBoundingClientRect();
      const x = e.clientX - rect.left - rect.width / 2;
      const y = e.clientY - rect.top - rect.height / 2;
      const rotateX = (-y / rect.height) * 6;
      const rotateY = (x / rect.width) * 6;
      commandCenter.style.transform = `perspective(1000px) rotateX(${rotateX}deg) rotateY(${rotateY}deg) scale3d(1.01, 1.01, 1.01)`;
    });

    heroVisualWrapper.addEventListener('mouseleave', () => {
      commandCenter.style.transform = 'perspective(1000px) rotateX(0deg) rotateY(0deg) scale3d(1, 1, 1)';
    });
  }

  // ==========================================================================
  // 8. ANIMATED NUMBER COUNTERS
  // ==========================================================================
  const counters = document.querySelectorAll('.counter');
  const counterObserver = new IntersectionObserver((entries, observer) => {
    entries.forEach(entry => {
      if (entry.isIntersecting) {
        const counter = entry.target;
        const target = parseInt(counter.getAttribute('data-count'), 10);
        const duration = 1500;
        const startTime = performance.now();

        function step(currentTime) {
          const progress = Math.min((currentTime - startTime) / duration, 1);
          const currentVal = Math.floor(progress * target);
          counter.textContent = currentVal.toLocaleString();
          if (progress < 1) {
            requestAnimationFrame(step);
          } else {
            counter.textContent = target.toLocaleString();
          }
        }
        requestAnimationFrame(step);
        observer.unobserve(counter);
      }
    });
  }, { threshold: 0.5 });

  counters.forEach(counter => counterObserver.observe(counter));

  // ==========================================================================
  // 9. TESLA 5-PAGE DASHBOARD TAB SWITCHER
  // ==========================================================================
  const teslaTabButtons = document.querySelectorAll('#teslaTabs .dash-tab');
  const teslaDashContent = document.getElementById('teslaDashContent');

  function renderTeslaTab(tabKey) {
    const page = TESLA_PAGES[tabKey];
    if (!page || !teslaDashContent) return;

    let kpiHtml = '<div class="dash-kpi-row">';
    page.kpis.forEach(k => {
      kpiHtml += `
        <div class="mini-kpi">
          <span class="m-label">${k.label}</span>
          <span class="m-val">${k.val} <span class="trend-up">${k.trend}</span></span>
        </div>
      `;
    });
    kpiHtml += '</div>';

    let barHtml = `
      <div class="dash-chart-area">
        <div class="chart-legend-row">
          <span class="legend-item"><span class="leg-color bg-purple"></span> Segment Volume</span>
          <span class="legend-item"><span class="leg-color bg-lavender"></span> Efficiency Trend</span>
          <span class="legend-tag">DAX Dynamic Model</span>
        </div>
        <div class="bar-chart-simulation">
    `;

    page.bars.forEach((height, idx) => {
      const isLatest = idx === page.bars.length - 1;
      barHtml += `
        <div class="bar-col">
          <div class="bar-fill ${isLatest ? 'active' : ''}" style="height: ${height}%"></div>
          <span>${page.labels[idx]}</span>
        </div>
      `;
    });
    barHtml += `
        </div>
      </div>
      <div class="mini-dax-bar">
        <span class="dax-label">DAX Measure:</span>
        <code>${page.dax}</code>
      </div>
    `;

    teslaDashContent.innerHTML = kpiHtml + barHtml;
  }

  teslaTabButtons.forEach(button => {
    button.addEventListener('click', () => {
      teslaTabButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
      const tabKey = button.getAttribute('data-tab');
      renderTeslaTab(tabKey);
    });
  });

  // ==========================================================================
  // 10. "HOW I THINK" INTERACTIVE PROCESS PIPELINE
  // ==========================================================================
  const stepButtons = document.querySelectorAll('.process-step-btn');
  const procTag = document.getElementById('procTag');
  const procTitle = document.getElementById('procTitle');
  const procDesc = document.getElementById('procDesc');
  const procDeliverables = document.getElementById('procDeliverables');
  const simTitle = document.getElementById('simTitle');
  const simPill = document.getElementById('simPill');
  const simCanvas = document.getElementById('simCanvas');

  function renderProcessStep(stepIndex) {
    const data = PROCESS_STEPS[stepIndex];
    if (!data) return;

    if (procTag) procTag.textContent = data.tag;
    if (procTitle) procTitle.textContent = data.title;
    if (procDesc) procDesc.textContent = data.desc;
    if (simTitle) simTitle.textContent = data.simTitle;
    if (simPill) simPill.textContent = `Step ${stepIndex + 1} of 6`;

    if (procDeliverables) {
      procDeliverables.innerHTML = data.deliverables
        .map(deliv => `<span class="deliv-item">${deliv}</span>`)
        .join('');
    }

    if (simCanvas) {
      simCanvas.innerHTML = data.visualHtml;
    }
  }

  stepButtons.forEach(button => {
    button.addEventListener('click', () => {
      stepButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
      const stepIdx = parseInt(button.getAttribute('data-step'), 10);
      renderProcessStep(stepIdx);
    });
  });

  // ==========================================================================
  // 11. SKILLS FILTERING MATRIX
  // ==========================================================================
  const skillFilterButtons = document.querySelectorAll('.skill-filter-btn');
  const skillCards = document.querySelectorAll('.skill-category-card');

  skillFilterButtons.forEach(button => {
    button.addEventListener('click', () => {
      skillFilterButtons.forEach(btn => btn.classList.remove('active'));
      button.classList.add('active');
      const filter = button.getAttribute('data-filter');

      skillCards.forEach(card => {
        const cat = card.getAttribute('data-cat');
        if (filter === 'all' || cat === filter) {
          card.style.display = 'block';
          card.style.opacity = '1';
        } else {
          card.style.display = 'none';
          card.style.opacity = '0';
        }
      });
    });
  });

  // ==========================================================================
  // 12. CASE STUDY DETAILED MODAL SYSTEM
  // ==========================================================================
  const caseStudyModal = document.getElementById('caseStudyModal');
  const openCaseStudyBtns = document.querySelectorAll('.open-case-study');
  const closeCaseStudyModalBtn = document.getElementById('closeCaseStudyModal');
  const modalCloseAction = document.getElementById('modalCloseAction');
  const modalCategory = document.getElementById('modalCategory');
  const modalProjectTitle = document.getElementById('modalProjectTitle');
  const modalDynamicBody = document.getElementById('modalDynamicBody');
  const modalTechSummary = document.getElementById('modalTechSummary');
  const modalTabButtons = document.querySelectorAll('.modal-tab-btn');

  let activeProjectKey = 'digital-lending';

  function openCaseStudy(projectKey) {
    const study = CASE_STUDIES[projectKey];
    if (!study) return;

    activeProjectKey = projectKey;
    modalCategory.textContent = study.category;
    modalProjectTitle.textContent = study.title;

    // Reset Tabs
    modalTabButtons.forEach(btn => btn.classList.remove('active'));
    modalTabButtons[0].classList.add('active');

    // Populate Overview
    modalDynamicBody.innerHTML = study.tabs.overview;

    // Populate Tech Chips
    modalTechSummary.innerHTML = study.tech
      .map(t => `<span class="tech-chip">${t}</span>`)
      .join('');

    caseStudyModal.classList.add('open');
    caseStudyModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeCaseStudy() {
    caseStudyModal.classList.remove('open');
    caseStudyModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  openCaseStudyBtns.forEach(btn => {
    btn.addEventListener('click', () => {
      const pKey = btn.getAttribute('data-project');
      openCaseStudy(pKey);
    });
  });

  if (closeCaseStudyModalBtn) closeCaseStudyModalBtn.addEventListener('click', closeCaseStudy);
  if (modalCloseAction) modalCloseAction.addEventListener('click', closeCaseStudy);

  modalTabButtons.forEach(btn => {
    btn.addEventListener('click', () => {
      modalTabButtons.forEach(b => b.classList.remove('active'));
      btn.classList.add('active');
      const tabType = btn.getAttribute('data-m-tab');
      const study = CASE_STUDIES[activeProjectKey];
      if (study && study.tabs[tabType]) {
        modalDynamicBody.innerHTML = study.tabs[tabType];
      }
    });
  });

  // ==========================================================================
  // 13. RESUME PREVIEW & PRINT MODAL
  // ==========================================================================
  const resumeModal = document.getElementById('resumeModal');
  const resumeTriggerBtns = [
    document.getElementById('navResumeBtn'),
    document.getElementById('heroResumeBtn'),
    document.getElementById('mobileResumeBtn')
  ].filter(Boolean);
  const closeResumeModalBtn = document.getElementById('closeResumeModal');
  const printResumeBtn = document.getElementById('printResumeBtn');

  function openResumeModal() {
    if (!resumeModal) return;
    resumeModal.classList.add('open');
    resumeModal.setAttribute('aria-hidden', 'false');
    document.body.style.overflow = 'hidden';
  }

  function closeResumeModal() {
    if (!resumeModal) return;
    resumeModal.classList.remove('open');
    resumeModal.setAttribute('aria-hidden', 'true');
    document.body.style.overflow = '';
  }

  resumeTriggerBtns.forEach(btn => btn.addEventListener('click', openResumeModal));
  if (closeResumeModalBtn) closeResumeModalBtn.addEventListener('click', closeResumeModal);
  if (printResumeBtn) {
    printResumeBtn.addEventListener('click', () => {
      window.print();
    });
  }

  // Close modals on outside click & Escape key
  window.addEventListener('click', e => {
    if (e.target === caseStudyModal) closeCaseStudy();
    if (e.target === resumeModal) closeResumeModal();
  });

  window.addEventListener('keydown', e => {
    if (e.key === 'Escape') {
      closeCaseStudy();
      closeResumeModal();
      closeMobileNav();
    }
  });

  // ==========================================================================
  // 14. INTERACTIVE CONTACT FORM VALIDATION & FEEDBACK
  // ==========================================================================
  const contactForm = document.getElementById('portfolioContactForm');
  const formFeedback = document.getElementById('formFeedback');

  if (contactForm && formFeedback) {
    contactForm.addEventListener('submit', e => {
      e.preventDefault();
      const name = document.getElementById('contactName').value.trim();
      const email = document.getElementById('contactEmail').value.trim();
      const subject = document.getElementById('contactSubject').value.trim();
      const message = document.getElementById('contactMessage').value.trim();

      if (!name || !email || !message) {
        formFeedback.textContent = 'Please fill out all required fields.';
        formFeedback.className = 'form-feedback-msg';
        formFeedback.style.display = 'block';
        formFeedback.style.color = '#EF4444';
        return;
      }

      formFeedback.textContent = `Thank you, ${name}! Your message has been prepared. Opening your email client to connect with Sashi...`;
      formFeedback.className = 'form-feedback-msg success';

      setTimeout(() => {
        const mailtoLink = `mailto:ranjans0022@gmail.com?subject=${encodeURIComponent(subject || 'Data & Business Analyst Inquiry')}&body=${encodeURIComponent(`Hi Sashi,\n\n${message}\n\nFrom: ${name} (${email})`)}`;
        window.location.href = mailtoLink;
      }, 900);
    });
  }
});
