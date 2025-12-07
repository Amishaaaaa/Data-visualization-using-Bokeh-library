# 📊 Data Visualization Dashboard with Bokeh

A comprehensive, interactive data visualization dashboard built using Python's **Bokeh** library. This project demonstrates how to visualize complex data through beautiful, interactive charts and graphs for better understanding and analysis.

![Python](https://img.shields.io/badge/Python-3.8%2B-blue)
![Bokeh](https://img.shields.io/badge/Bokeh-3.3%2B-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## ✨ Features

### Chart Types Included
- **📈 Line Charts** - Visualize sales trends over time with multi-series support
- **📊 Bar Charts** - Compare regional revenue with horizontal bars
- **🔮 Scatter Plots** - Explore multi-dimensional data with clustering
- **🍩 Donut Charts** - Display proportional data beautifully
- **📉 Area Charts** - Show cumulative data distribution
- **📈 Time Series** - Analyze stock-like data with moving averages
- **📊 Grouped Bar Charts** - Compare team performance metrics

### Interactive Features
- **Pan & Zoom** - Navigate through your data
- **Hover Tooltips** - Get detailed information on data points
- **Legend Toggle** - Click to hide/show data series
- **Lasso Select** - Select multiple points for analysis
- **Box Zoom** - Zoom into specific regions
- **Crosshair** - Track data across the chart

### Design
- Modern dark theme with gradient accents
- KPI summary cards with key metrics
- Responsive layout with organized sections
- Professional color palette

## 🚀 Getting Started

### Prerequisites
- Python 3.8 or higher
- pip (Python package manager)

### Installation

1. **Clone or navigate to the project directory**
   ```bash
   cd "Data visualization"
   ```

2. **Create a virtual environment (recommended)**
   ```bash
   python -m venv venv
   
   # On macOS/Linux:
   source venv/bin/activate
   
   # On Windows:
   venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

### Running the Dashboard

```bash
python dashboard.py
```

This will:
1. Generate the dashboard with sample data
2. Save it as `dashboard.html`
3. Automatically open the dashboard in your default web browser

## 📁 Project Structure

```
Data visualization/
├── dashboard.py        # Main dashboard application
├── data_generator.py   # Sample data generation module
├── requirements.txt    # Python dependencies
├── README.md          # This file
└── dashboard.html     # Generated dashboard (after running)
```

## 📊 Data Sources

The project includes a data generator module (`data_generator.py`) that creates realistic sample data:

| Function | Description |
|----------|-------------|
| `generate_sales_data()` | Monthly sales data for multiple products |
| `generate_regional_data()` | Revenue and metrics by region |
| `generate_performance_data()` | Team performance metrics |
| `generate_time_series_data()` | Stock-like price data with volume |
| `generate_scatter_data()` | Clustered scatter plot data |
| `generate_pie_data()` | Device traffic distribution |

### Using Your Own Data

Replace the data generator calls in `dashboard.py` with your own data sources:

```python
import pandas as pd

# Load from CSV
df = pd.read_csv('your_data.csv')

# Load from database
# df = pd.read_sql('SELECT * FROM table', connection)

# Load from API
# df = pd.DataFrame(requests.get('api_url').json())
```

## 🎨 Customization

### Theme Colors

Modify the `THEME` dictionary in `dashboard.py`:

```python
THEME = {
    'background': '#0a0a0f',      # Page background
    'plot_bg': '#12121a',          # Chart background
    'grid_color': '#2a2a3a',       # Grid lines
    'text_color': '#e0e0e0',       # Text color
    'accent_primary': '#00d4aa',   # Primary accent
    'accent_secondary': '#7c3aed', # Secondary accent
    'accent_tertiary': '#f59e0b',  # Tertiary accent
}
```

### Adding New Charts

1. Create a new function following the pattern:
   ```python
   def create_my_chart():
       # Generate or load data
       df = your_data_function()
       
       # Create figure
       fig = figure(
           title="My Chart",
           width=600,
           height=400,
           tools="pan,box_zoom,wheel_zoom,reset"
       )
       
       # Add glyphs (lines, bars, circles, etc.)
       fig.line(x='x', y='y', source=ColumnDataSource(df))
       
       # Apply theme
       return style_figure(fig)
   ```

2. Add the chart to the dashboard layout in `create_dashboard()`

## 🛠️ Advanced Usage

### Running as Bokeh Server

For real-time updates and callbacks:

```bash
bokeh serve dashboard.py --show
```

### Embedding in Web Applications

```python
from bokeh.embed import components

script, div = components(dashboard)
# Use script and div in your HTML template
```

## 📝 Dependencies

| Package | Version | Purpose |
|---------|---------|---------|
| bokeh | ≥3.3.0 | Visualization library |
| pandas | ≥2.0.0 | Data manipulation |
| numpy | ≥1.24.0 | Numerical operations |

## 🤝 Contributing

Contributions are welcome! Feel free to:
- Add new chart types
- Improve the UI/UX
- Add more interactive features
- Optimize performance

## 📄 License

This project is open source and available under the MIT License.

## 🙏 Acknowledgments

- [Bokeh Documentation](https://docs.bokeh.org/)
- [Bokeh Gallery](https://docs.bokeh.org/en/latest/docs/gallery.html)

---

**Happy Visualizing! 📊✨**

