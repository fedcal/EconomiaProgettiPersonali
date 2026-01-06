# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

This repository contains **business intelligence and project management tools** for three web-based projects owned by Federico Calò. It combines web scraping scripts, analytics analysis, financial tracking, and comprehensive project management documentation.

**Projects:**
1. **FedericoCalo.dev** - Professional portfolio and freelance services
2. **CasaDelleMagnolie.com** - Vacation rental property in Salento
3. **PlayTheEvent.com** - SaaS platform for event management

## Repository Structure

```
EconomiaProgettiPersonali/
├── Analisi Web Scraping progetti/     # Web scraping & analytics for all projects
│   ├── FedericoCalo/                  # Portfolio scraping & financial tracking
│   ├── CasaDelleMagnolie/             # Vacation rental scraping & metrics
│   ├── PlayTheEvent/                  # Event platform technical analysis
│   └── README.md                      # Detailed project documentation
│
├── Documentazione/                    # 150+ pages of PM guides
│   ├── INDEX.md                       # Entry point for all documentation
│   ├── PROJECT_MANAGEMENT_GUIDE.md    # Fundamentals & methodologies
│   ├── AGILE_SCRUM_GUIDE.md          # Agile/Scrum deep dive
│   ├── RISK_MANAGEMENT_GUIDE.md      # Risk identification & mitigation
│   ├── TEAM_LEADERSHIP_GUIDE.md      # Leadership & team management
│   ├── TIME_PRODUCTIVITY_GUIDE.md    # Time management & productivity
│   └── FINANCIAL_MANAGEMENT_GUIDE.md # Budget, ROI, tracking
│
├── PartitaIva/                        # Invoices, contracts, quotes
│   ├── PrjPersonali/                  # Project-specific documents
│   └── TemplateContratti/             # Contract templates
│
└── .claude/docs/                      # Claude-specific documentation
    ├── README-PROGETTI.md             # Project management reference
    ├── README-SEO.md                  # SEO strategies
    ├── README-MARKETING.md            # Marketing strategies
    ├── README-SVILUPPO.md             # Development best practices
    └── README-BUSINESS.md             # Business analysis
```

## Common Commands

### Web Scraping

Each project has its own virtual environment and scraper script:

```bash
# FedericoCalo portfolio scraping
cd "Analisi Web Scraping progetti/FedericoCalo"
source venv/bin/activate
python3 federicocalo_scraper.py

# CasaDelleMagnolie property scraping
cd "Analisi Web Scraping progetti/CasaDelleMagnolie"
source venv/bin/activate
python3 casadellemagnolie_scraper.py

# PlayTheEvent platform analysis
cd "Analisi Web Scraping progetti/PlayTheEvent"
source venv/bin/activate
python3 playtheevent_scraper.py
```

### Analytics & Visualization

```bash
# Both FedericoCalo and CasaDelleMagnolie have these tools:
python3 analytics_analyzer.py      # Parse Google Analytics CSV export
python3 visualize_analytics.py     # Generate 6 charts automatically
python3 strategic_analysis.py      # Generate strategic recommendations
```

### Financial Management

```bash
# Run financial tracking and reporting
python3 financial_manager.py

# Vacation rental metrics (CasaDelleMagnolie only)
# - Occupancy Rate, ADR, RevPAR automatically calculated
# - Platform commission tracking

# Freelance metrics (FedericoCalo only)
# - ROI calculation, hourly rate tracking
# - Client revenue analysis
```

### Setup New Project Environment

```bash
# Create and activate virtual environment
cd "Analisi Web Scraping progetti/<ProjectName>"
python3 -m venv venv
source venv/bin/activate  # Linux/Mac
# or: venv\Scripts\activate  # Windows

# Install dependencies
pip install -r requirements.txt
```

## Architecture & Key Concepts

### Multi-Project Structure

This repository manages **three distinct businesses** with different:
- **Business models**: Freelance services, vacation rental, SaaS
- **Metrics**: Revenue/client vs Occupancy/ADR vs MRR/Churn
- **Methodologies**: GTD vs Kanban vs Scrum
- **Stakeholders**: Solo vs small team vs development team

### Web Scraping Pattern

All scrapers follow a consistent OOP pattern:

```python
class ProjectScraper:
    def __init__(self, base_url: str)
    def fetch_page(self, url: str) -> BeautifulSoup
    def extract_<section>(self, soup) -> List[Dict]
    def scrape_all(self) -> Dict
    def save_to_json(self, data: Dict, filename: str)
```

**Key features:**
- Respectful scraping (User-Agent, timeouts, rate limiting)
- Robust error handling
- Structured JSON output
- Logging for debugging

### Financial Tracking System

Two specialized implementations:

**FedericoCalo (Freelance):**
- One-time costs (domain, branding)
- Recurring costs (hosting, tools)
- Revenue streams (projects, retainers)
- Metrics: ROI, break-even, hourly rate

**CasaDelleMagnolie (Vacation Rental):**
- Bookings with platform commission auto-calculation
- Occupancy tracking
- Metrics: ADR (Average Daily Rate), RevPAR, Occupancy Rate
- Platform-specific commission rates (Booking.com 15%, Airbnb 17%, etc.)

### Project Management Documentation

The `Documentazione/` folder contains a **comprehensive PM library** (~150 pages):

**Use INDEX.md as the entry point** - it provides:
- Guide selection by problem/role
- Project-specific examples
- Learning paths (beginner → intermediate → advanced)
- Templates and checklists

**Important:** These guides are **living documents** tailored to the three specific projects with concrete examples, not generic PM theory.

## Python Dependencies

**Core (all projects):**
- `requests` - HTTP client for web scraping
- `beautifulsoup4` - HTML parsing
- `lxml` - XML/HTML parser

**Analytics projects (FedericoCalo, CasaDelleMagnolie):**
- `matplotlib` - Chart generation
- `pandas` - Data analysis (Google Analytics CSV)
- `numpy` - Numerical operations

## Working with Financial Data

Financial data is stored in `financial_data.json` with project-specific schemas:

```python
# FedericoCalo schema
{
    "one_time_costs": [{"name": str, "amount": float, "category": str}],
    "recurring_costs": [{"name": str, "amount": float, "frequency": str}],
    "revenue_streams": [{"name": str, "amount": float, "type": str}]
}

# CasaDelleMagnolie schema
{
    "bookings": [{
        "checkin": "YYYY-MM-DD",
        "nights": int,
        "price": float,
        "platform": str,  # Auto-calculates commission
        "guests": int
    }],
    "occupancy": {
        "total_weeks": 52,
        "booked_weeks": float
    }
}
```

**Financial Manager Capabilities:**
- Add/remove costs and revenue
- Generate comprehensive reports (TXT/JSON)
- Auto-calculate metrics (ROI, profit, occupancy, etc.)
- Visualizations (4 charts: costs breakdown, revenue, profit trend, ROI)

## Google Analytics Integration

Both FedericoCalo and CasaDelleMagnolie use **CSV export** (not API):

1. Export from Google Analytics as CSV
2. Place in project folder as `Istantanea_report.csv`
3. Run `analytics_analyzer.py` to parse
4. Run `visualize_analytics.py` to generate charts:
   - Users by date
   - Sessions by device
   - Page views by page
   - Traffic sources
   - Conversions
   - User engagement

## Documentation Reference Guide

When working on specific tasks, consult these docs:

**Starting a new project:**
→ `Documentazione/PROJECT_MANAGEMENT_GUIDE.md` (Initiating phase)

**Sprint planning/Agile:**
→ `Documentazione/AGILE_SCRUM_GUIDE.md`

**Time management/productivity:**
→ `Documentazione/TIME_PRODUCTIVITY_GUIDE.md`

**Budget/financial decisions:**
→ `Documentazione/FINANCIAL_MANAGEMENT_GUIDE.md`

**Risk assessment:**
→ `Documentazione/RISK_MANAGEMENT_GUIDE.md`

**Team management:**
→ `Documentazione/TEAM_LEADERSHIP_GUIDE.md`

**SEO strategies:**
→ `.claude/docs/README-SEO.md`

**Marketing strategies:**
→ `.claude/docs/README-MARKETING.md`

## Important Notes

### Language
- All documentation is in **Italian** (target audience)
- Code comments and docstrings in **English** (best practice)
- Script outputs in **Italian** (user-facing)

### Virtual Environments
Each project has its own isolated virtual environment:
- Always activate the correct venv before running scripts
- Dependencies are project-specific (check `requirements.txt`)

### Data Privacy
- Scrapers respect robots.txt and rate limiting
- No API keys or credentials are committed to repo
- Financial data contains real business information
- Google Analytics data exported manually (no API tokens)

### Methodologies by Project

**FedericoCalo.dev** (Solo freelancer):
- GTD (Getting Things Done) + Time Blocking
- Deep work blocks: 9-12am, 2-5pm
- Tools: Todoist, Toggl, Notion

**CasaDelleMagnolie.com** (Small operations team):
- Kanban for ongoing operations
- Scrum for specific projects (e.g., website redesign)
- Tools: Trello, templates for guest communication

**PlayTheEvent.com** (Development team):
- Scrum with 1-2 week sprints
- Daily async standup
- Tools: Jira/Linear, GitHub Projects

## Key Metrics by Project

**FedericoCalo.dev:**
- Revenue per month (target: €3,000-€5,000)
- Projects on-time rate (target: >90%)
- Hourly rate effective
- Client satisfaction (target: >4.5/5)

**CasaDelleMagnolie.com:**
- Occupancy Rate (target: >60%)
- ADR - Average Daily Rate (target: >€150/night)
- RevPAR - Revenue Per Available Room
- Guest rating (target: >4.8/5)

**PlayTheEvent.com:**
- MRR - Monthly Recurring Revenue
- Churn Rate (target: <5%)
- Sprint Velocity
- CAC - Customer Acquisition Cost

## Extending the System

### Adding a New Project

1. Create folder in `Analisi Web Scraping progetti/<ProjectName>/`
2. Copy `requirements.txt` from similar project
3. Create virtual environment and install dependencies
4. Write scraper following the established pattern
5. Add financial_manager.py with appropriate schema
6. Update main README.md with project details

### Adding New Metrics

Modify `financial_manager.py` in the relevant project:
- Update schema in `financial_data.json`
- Add calculation methods
- Update report generation
- Add visualizations if needed

### Adding New Analytics

Extend `analytics_analyzer.py`:
- Parse additional columns from GA CSV
- Add new analysis functions
- Update `visualize_analytics.py` with new charts

## Integration Points

**Cross-Project:**
- All projects share the same PM documentation
- Common scraping patterns and best practices
- Consistent financial tracking approach

**External Services:**
- Google Analytics (manual CSV export)
- Booking platforms (Booking.com, Airbnb - data scraped or manually entered)
- GitHub (for PlayTheEvent development tracking)

## Strategic Analysis Tools

Both FedericoCalo and CasaDelleMagnolie have `strategic_analysis.py`:

**Generates:**
- SEO recommendations
- Content strategy
- Marketing channels analysis
- Competitive positioning
- Growth opportunities
- Risk factors

**Based on:**
- Google Analytics data
- Web scraping results
- Financial performance
- Industry benchmarks
