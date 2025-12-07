"""
Data Visualization Dashboard with Bokeh
========================================
A comprehensive dashboard showcasing various chart types and interactive features
using the Bokeh visualization library.
"""

from bokeh.plotting import figure, curdoc
from bokeh.layouts import column, row, gridplot
from bokeh.models import (
    ColumnDataSource, HoverTool, Legend, LegendItem,
    Div, Select, DateRangeSlider, Panel, Tabs,
    NumeralTickFormatter, DatetimeTickFormatter,
    BoxAnnotation, Span, Label
)
from bokeh.palettes import Category10, Spectral6, Viridis256
from bokeh.transform import factor_cmap, cumsum
from bokeh.io import show, output_file
import numpy as np
import pandas as pd

from data_generator import (
    generate_sales_data,
    generate_regional_data,
    generate_performance_data,
    generate_time_series_data,
    generate_scatter_data,
    generate_pie_data
)


# ============================================================================
# THEME & STYLING
# ============================================================================

THEME = {
    'background': '#0a0a0f',
    'plot_bg': '#12121a',
    'grid_color': '#2a2a3a',
    'text_color': '#e0e0e0',
    'accent_primary': '#00d4aa',
    'accent_secondary': '#7c3aed',
    'accent_tertiary': '#f59e0b',
    'accent_quaternary': '#ec4899',
    'accent_fifth': '#3b82f6'
}

PALETTE = [
    THEME['accent_primary'],
    THEME['accent_secondary'],
    THEME['accent_tertiary'],
    THEME['accent_quaternary'],
    THEME['accent_fifth']
]


def style_figure(fig):
    """Apply consistent dark theme styling to a figure"""
    fig.background_fill_color = THEME['plot_bg']
    fig.border_fill_color = THEME['background']
    fig.outline_line_color = THEME['grid_color']
    
    fig.xgrid.grid_line_color = THEME['grid_color']
    fig.ygrid.grid_line_color = THEME['grid_color']
    fig.xgrid.grid_line_alpha = 0.3
    fig.ygrid.grid_line_alpha = 0.3
    
    fig.xaxis.axis_line_color = THEME['grid_color']
    fig.yaxis.axis_line_color = THEME['grid_color']
    fig.xaxis.major_tick_line_color = THEME['grid_color']
    fig.yaxis.major_tick_line_color = THEME['grid_color']
    fig.xaxis.minor_tick_line_color = None
    fig.yaxis.minor_tick_line_color = None
    
    fig.xaxis.major_label_text_color = THEME['text_color']
    fig.yaxis.major_label_text_color = THEME['text_color']
    fig.xaxis.axis_label_text_color = THEME['text_color']
    fig.yaxis.axis_label_text_color = THEME['text_color']
    
    if fig.title:
        fig.title.text_color = THEME['text_color']
        fig.title.text_font_size = '14pt'
        fig.title.text_font = 'Helvetica'
    
    if fig.legend:
        for legend in fig.legend:
            legend.background_fill_color = THEME['plot_bg']
            legend.background_fill_alpha = 0.8
            legend.border_line_color = THEME['grid_color']
            legend.label_text_color = THEME['text_color']
    
    return fig


# ============================================================================
# CHART CREATORS
# ============================================================================

def create_line_chart():
    """Create an interactive multi-line chart showing sales trends"""
    df = generate_sales_data(12)
    
    fig = figure(
        title="📈 Monthly Sales Trends by Product Category",
        x_axis_type='datetime',
        width=600,
        height=400,
        tools="pan,box_zoom,wheel_zoom,reset,save"
    )
    
    products = df['product'].unique()
    legend_items = []
    
    for i, product in enumerate(products):
        product_data = df[df['product'] == product].sort_values('date')
        source = ColumnDataSource(product_data)
        
        line = fig.line(
            x='date', y='sales',
            source=source,
            line_width=3,
            line_color=PALETTE[i % len(PALETTE)],
            alpha=0.9
        )
        
        circles = fig.scatter(
            x='date', y='sales',
            source=source,
            size=8,
            color=PALETTE[i % len(PALETTE)],
            alpha=0.8
        )
        
        legend_items.append(LegendItem(label=product, renderers=[line, circles]))
    
    # Add hover tool
    hover = HoverTool(
        tooltips=[
            ('Product', '@product'),
            ('Date', '@date{%B %Y}'),
            ('Sales', '$@sales{0,0}'),
            ('Units', '@units')
        ],
        formatters={'@date': 'datetime'}
    )
    fig.add_tools(hover)
    
    # Add legend
    legend = Legend(items=legend_items, location="top_left", click_policy="hide")
    fig.add_layout(legend, 'right')
    
    fig.xaxis.formatter = DatetimeTickFormatter(months='%b %Y')
    fig.yaxis.formatter = NumeralTickFormatter(format='$0,0')
    fig.xaxis.axis_label = "Month"
    fig.yaxis.axis_label = "Sales Revenue"
    
    return style_figure(fig)


def create_bar_chart():
    """Create horizontal bar chart for regional performance"""
    df = generate_regional_data()
    df = df.sort_values('revenue', ascending=True)
    
    source = ColumnDataSource(df)
    
    fig = figure(
        title="🌍 Revenue by Region",
        y_range=df['region'].tolist(),
        width=600,
        height=400,
        tools="pan,box_zoom,wheel_zoom,reset,save"
    )
    
    # Create gradient-like effect with bars
    bars = fig.hbar(
        y='region',
        right='revenue',
        source=source,
        height=0.6,
        color=factor_cmap('region', palette=PALETTE, factors=df['region'].tolist()),
        alpha=0.85,
        line_color=THEME['text_color'],
        line_width=1
    )
    
    # Add value labels
    for i, (region, revenue) in enumerate(zip(df['region'], df['revenue'])):
        fig.text(
            x=[revenue + 5000], y=[region],
            text=[f'${revenue:,.0f}'],
            text_color=THEME['text_color'],
            text_font_size='11px',
            text_baseline='middle'
        )
    
    hover = HoverTool(
        tooltips=[
            ('Region', '@region'),
            ('Revenue', '$@revenue{0,0}'),
            ('Growth', '@growth{0.0}%'),
            ('Customers', '@customers{0,0}')
        ]
    )
    fig.add_tools(hover)
    
    fig.xaxis.formatter = NumeralTickFormatter(format='$0,0')
    fig.xaxis.axis_label = "Revenue ($)"
    
    return style_figure(fig)


def create_scatter_plot():
    """Create interactive scatter plot with categories"""
    df = generate_scatter_data(150)
    
    source = ColumnDataSource(df)
    categories = df['category'].unique().tolist()
    
    fig = figure(
        title="🔮 Multi-dimensional Data Analysis",
        width=600,
        height=400,
        tools="pan,box_zoom,wheel_zoom,reset,save,lasso_select"
    )
    
    scatter = fig.scatter(
        x='x', y='y',
        source=source,
        size='size',
        color=factor_cmap('category', palette=PALETTE[:3], factors=categories),
        alpha=0.7,
        legend_field='category',
        line_color=THEME['text_color'],
        line_width=0.5
    )
    
    hover = HoverTool(
        tooltips=[
            ('Category', '@category'),
            ('X Value', '@x{0.0}'),
            ('Y Value', '@y{0.0}'),
            ('Size', '@size{0.0}'),
            ('Value', '@value{0.00}')
        ]
    )
    fig.add_tools(hover)
    
    fig.legend.location = "top_left"
    fig.legend.click_policy = "hide"
    fig.xaxis.axis_label = "Feature X"
    fig.yaxis.axis_label = "Feature Y"
    
    return style_figure(fig)


def create_area_chart():
    """Create stacked area chart"""
    df = generate_sales_data(12)
    
    # Pivot data for stacking
    pivot_df = df.pivot_table(index='date', columns='product', values='sales', aggfunc='sum')
    pivot_df = pivot_df.reset_index()
    
    fig = figure(
        title="📊 Cumulative Sales Distribution",
        x_axis_type='datetime',
        width=600,
        height=400,
        tools="pan,box_zoom,wheel_zoom,reset,save"
    )
    
    products = [col for col in pivot_df.columns if col != 'date']
    
    # Stack the areas
    bottom = np.zeros(len(pivot_df))
    
    for i, product in enumerate(products):
        top = bottom + pivot_df[product].values
        
        source = ColumnDataSource({
            'date': pivot_df['date'],
            'bottom': bottom,
            'top': top,
            'product': [product] * len(pivot_df)
        })
        
        fig.varea(
            x='date',
            y1='bottom',
            y2='top',
            source=source,
            fill_color=PALETTE[i % len(PALETTE)],
            fill_alpha=0.7,
            legend_label=product
        )
        
        bottom = top
    
    fig.legend.location = "top_left"
    fig.legend.click_policy = "hide"
    fig.xaxis.formatter = DatetimeTickFormatter(months='%b %Y')
    fig.yaxis.formatter = NumeralTickFormatter(format='$0,0')
    fig.xaxis.axis_label = "Month"
    fig.yaxis.axis_label = "Cumulative Sales"
    
    return style_figure(fig)


def create_donut_chart():
    """Create donut/pie chart for device distribution"""
    df = generate_pie_data()
    
    # Calculate mid angles for label positioning
    df['mid_angle'] = (df['start_angle'] + df['end_angle']) / 2
    
    source = ColumnDataSource(df)
    
    fig = figure(
        title="📱 Traffic by Device Type",
        width=500,
        height=400,
        tools="hover",
        tooltips="@category: @percentage{0.0}%",
        x_range=(-1.5, 1.5),
        y_range=(-1.5, 1.5)
    )
    
    # Create the donut chart
    fig.annular_wedge(
        x=0, y=0,
        inner_radius=0.4,
        outer_radius=0.9,
        start_angle='start_angle',
        end_angle='end_angle',
        color='color',
        source=source,
        alpha=0.9,
        line_color=THEME['background'],
        line_width=3
    )
    
    # Add labels
    for _, row in df.iterrows():
        angle = row['mid_angle']
        x = 0.65 * np.cos(angle)
        y = 0.65 * np.sin(angle)
        
        fig.text(
            x=[x], y=[y],
            text=[f"{row['percentage']:.0f}%"],
            text_color='white',
            text_font_size='12px',
            text_align='center',
            text_baseline='middle',
            text_font_style='bold'
        )
    
    # Add center text
    fig.text(
        x=[0], y=[0],
        text=['Total\nTraffic'],
        text_color=THEME['text_color'],
        text_font_size='14px',
        text_align='center',
        text_baseline='middle'
    )
    
    fig.axis.visible = False
    fig.grid.visible = False
    
    # Add legend manually
    for i, (_, row) in enumerate(df.iterrows()):
        fig.rect(
            x=[1.15], y=[0.7 - i * 0.25],
            width=0.1, height=0.12,
            color=row['color'],
            alpha=0.9
        )
        fig.text(
            x=[1.25], y=[0.7 - i * 0.25],
            text=[row['category']],
            text_color=THEME['text_color'],
            text_font_size='10px',
            text_baseline='middle'
        )
    
    return style_figure(fig)


def create_time_series_chart():
    """Create time series chart with moving average"""
    df = generate_time_series_data(90)
    source = ColumnDataSource(df)
    
    fig = figure(
        title="📉 Stock Price Analysis with Moving Average",
        x_axis_type='datetime',
        width=800,
        height=400,
        tools="pan,box_zoom,wheel_zoom,reset,save,crosshair"
    )
    
    # Add price line
    fig.line(
        x='date', y='price',
        source=source,
        line_width=2,
        color=THEME['accent_primary'],
        alpha=0.9,
        legend_label='Price'
    )
    
    # Add moving average
    fig.line(
        x='date', y='moving_avg',
        source=source,
        line_width=2,
        color=THEME['accent_tertiary'],
        line_dash='dashed',
        alpha=0.8,
        legend_label='7-Day MA'
    )
    
    # Add high-low range as area
    fig.varea(
        x='date',
        y1='low',
        y2='high',
        source=source,
        fill_color=THEME['accent_secondary'],
        fill_alpha=0.2,
        legend_label='High-Low Range'
    )
    
    hover = HoverTool(
        tooltips=[
            ('Date', '@date{%F}'),
            ('Price', '$@price{0.00}'),
            ('High', '$@high{0.00}'),
            ('Low', '$@low{0.00}'),
            ('7-Day MA', '$@moving_avg{0.00}'),
            ('Volume', '@volume{0,0}')
        ],
        formatters={'@date': 'datetime'},
        mode='vline'
    )
    fig.add_tools(hover)
    
    fig.legend.location = "top_left"
    fig.legend.click_policy = "hide"
    fig.xaxis.axis_label = "Date"
    fig.yaxis.axis_label = "Price ($)"
    fig.yaxis.formatter = NumeralTickFormatter(format='$0.00')
    
    return style_figure(fig)


def create_grouped_bar_chart():
    """Create grouped bar chart for team performance"""
    df = generate_performance_data()
    
    metrics = ['productivity', 'quality', 'efficiency']
    x = [(team, metric) for team in df['team'] for metric in metrics]
    
    # Create colors list matching the data
    colors = [PALETTE[0], PALETTE[1], PALETTE[2]] * len(df)
    
    data = {
        'x': x,
        'value': sum([[row['productivity'], row['quality'], row['efficiency']] 
                      for _, row in df.iterrows()], []),
        'color': colors
    }
    
    source = ColumnDataSource(data)
    
    from bokeh.models import FactorRange
    
    fig = figure(
        title="🏆 Team Performance Metrics",
        x_range=FactorRange(*x),
        width=900,
        height=400,
        tools="pan,box_zoom,wheel_zoom,reset,save"
    )
    
    fig.vbar(
        x='x',
        top='value',
        source=source,
        width=0.8,
        color='color',
        alpha=0.85,
        line_color=THEME['text_color'],
        line_width=0.5
    )
    
    # Add reference line at 85%
    span = Span(
        location=85,
        dimension='width',
        line_color=THEME['accent_quaternary'],
        line_dash='dashed',
        line_width=2
    )
    fig.add_layout(span)
    
    label = Label(
        x=0, y=87,
        text='Target: 85%',
        text_color=THEME['accent_quaternary'],
        text_font_size='10px'
    )
    fig.add_layout(label)
    
    fig.xaxis.major_label_orientation = 0.8
    fig.yaxis.axis_label = "Score (%)"
    fig.y_range.start = 0
    fig.y_range.end = 110
    
    # Add custom legend
    from bokeh.models import Legend, LegendItem
    legend_items = [
        LegendItem(label='Productivity', renderers=[]),
        LegendItem(label='Quality', renderers=[]),
        LegendItem(label='Efficiency', renderers=[])
    ]
    
    return style_figure(fig)


def create_dashboard_header():
    """Create the dashboard header with title and description"""
    header_html = """
    <div style="
        background: linear-gradient(135deg, #12121a 0%, #1a1a2e 50%, #12121a 100%);
        padding: 30px;
        border-radius: 16px;
        margin-bottom: 20px;
        border: 1px solid #2a2a3a;
        box-shadow: 0 10px 40px rgba(0, 0, 0, 0.4);
    ">
        <h1 style="
            color: #00d4aa;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 2.5em;
            margin: 0 0 10px 0;
            text-shadow: 0 0 30px rgba(0, 212, 170, 0.3);
            letter-spacing: -0.5px;
        ">
            ✨ Data Visualization Dashboard
        </h1>
        <p style="
            color: #a0a0a0;
            font-family: 'Segoe UI', Arial, sans-serif;
            font-size: 1.1em;
            margin: 0;
            line-height: 1.6;
        ">
            Interactive analytics powered by Bokeh • Explore trends, compare metrics, and discover insights
        </p>
        <div style="margin-top: 15px; display: flex; gap: 20px;">
            <span style="color: #00d4aa; font-size: 0.9em;">📊 6 Chart Types</span>
            <span style="color: #7c3aed; font-size: 0.9em;">🔍 Interactive Tools</span>
            <span style="color: #f59e0b; font-size: 0.9em;">📈 Real-time Analysis</span>
        </div>
    </div>
    """
    return Div(text=header_html, width=1200)


def create_kpi_cards():
    """Create KPI summary cards"""
    sales_df = generate_sales_data()
    regional_df = generate_regional_data()
    
    total_sales = sales_df['sales'].sum()
    total_customers = regional_df['customers'].sum()
    avg_satisfaction = regional_df['satisfaction'].mean()
    avg_growth = regional_df['growth'].mean()
    
    kpi_html = f"""
    <div style="display: flex; gap: 20px; margin-bottom: 25px;">
        <div style="
            flex: 1;
            background: linear-gradient(135deg, rgba(0, 212, 170, 0.1) 0%, rgba(0, 212, 170, 0.05) 100%);
            border: 1px solid rgba(0, 212, 170, 0.3);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        ">
            <div style="color: #a0a0a0; font-size: 0.9em; margin-bottom: 5px;">Total Revenue</div>
            <div style="color: #00d4aa; font-size: 2em; font-weight: bold;">${total_sales:,.0f}</div>
            <div style="color: #4ade80; font-size: 0.85em;">↑ 12.5% vs last year</div>
        </div>
        <div style="
            flex: 1;
            background: linear-gradient(135deg, rgba(124, 58, 237, 0.1) 0%, rgba(124, 58, 237, 0.05) 100%);
            border: 1px solid rgba(124, 58, 237, 0.3);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        ">
            <div style="color: #a0a0a0; font-size: 0.9em; margin-bottom: 5px;">Total Customers</div>
            <div style="color: #7c3aed; font-size: 2em; font-weight: bold;">{total_customers:,}</div>
            <div style="color: #a78bfa; font-size: 0.85em;">↑ 8.3% growth</div>
        </div>
        <div style="
            flex: 1;
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.1) 0%, rgba(245, 158, 11, 0.05) 100%);
            border: 1px solid rgba(245, 158, 11, 0.3);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        ">
            <div style="color: #a0a0a0; font-size: 0.9em; margin-bottom: 5px;">Avg. Satisfaction</div>
            <div style="color: #f59e0b; font-size: 2em; font-weight: bold;">{avg_satisfaction:.1f}/5.0</div>
            <div style="color: #fbbf24; font-size: 0.85em;">⭐ Excellent rating</div>
        </div>
        <div style="
            flex: 1;
            background: linear-gradient(135deg, rgba(236, 72, 153, 0.1) 0%, rgba(236, 72, 153, 0.05) 100%);
            border: 1px solid rgba(236, 72, 153, 0.3);
            border-radius: 12px;
            padding: 20px;
            text-align: center;
        ">
            <div style="color: #a0a0a0; font-size: 0.9em; margin-bottom: 5px;">Avg. Growth Rate</div>
            <div style="color: #ec4899; font-size: 2em; font-weight: bold;">{avg_growth:.1f}%</div>
            <div style="color: #f472b6; font-size: 0.85em;">↑ Strong performance</div>
        </div>
    </div>
    """
    return Div(text=kpi_html, width=1200)


def create_dashboard():
    """Assemble the complete dashboard"""
    # Create header and KPIs
    header = create_dashboard_header()
    kpis = create_kpi_cards()
    
    # Create all charts
    line_chart = create_line_chart()
    bar_chart = create_bar_chart()
    scatter_plot = create_scatter_plot()
    area_chart = create_area_chart()
    donut_chart = create_donut_chart()
    time_series = create_time_series_chart()
    grouped_bar = create_grouped_bar_chart()
    
    # Section dividers
    section1 = Div(text="""
        <h2 style="color: #e0e0e0; font-family: 'Segoe UI', Arial, sans-serif; 
                   border-bottom: 2px solid #2a2a3a; padding-bottom: 10px; margin: 30px 0 20px 0;">
            📊 Sales & Revenue Analytics
        </h2>
    """, width=1200)
    
    section2 = Div(text="""
        <h2 style="color: #e0e0e0; font-family: 'Segoe UI', Arial, sans-serif; 
                   border-bottom: 2px solid #2a2a3a; padding-bottom: 10px; margin: 30px 0 20px 0;">
            📈 Advanced Analytics & Insights
        </h2>
    """, width=1200)
    
    section3 = Div(text="""
        <h2 style="color: #e0e0e0; font-family: 'Segoe UI', Arial, sans-serif; 
                   border-bottom: 2px solid #2a2a3a; padding-bottom: 10px; margin: 30px 0 20px 0;">
            🎯 Performance Overview
        </h2>
    """, width=1200)
    
    # Footer
    footer = Div(text="""
        <div style="
            text-align: center;
            padding: 20px;
            margin-top: 30px;
            border-top: 1px solid #2a2a3a;
            color: #606060;
            font-size: 0.9em;
        ">
            Built with ❤️ using Bokeh Library • Data Visualization Dashboard © 2025
        </div>
    """, width=1200)
    
    # Assemble layout
    layout = column(
        header,
        kpis,
        section1,
        row(line_chart, bar_chart),
        section2,
        row(scatter_plot, donut_chart),
        time_series,
        section3,
        row(area_chart, grouped_bar),
        footer,
        sizing_mode='fixed'
    )
    
    return layout


# ============================================================================
# MAIN EXECUTION
# ============================================================================

# For running as a standalone HTML file
output_file(
    "dashboard.html",
    title="Data Visualization Dashboard - Bokeh"
)

# Create and display the dashboard
dashboard = create_dashboard()

# Add page background styling
page_css = Div(text="""
<style>
    body {
        background-color: #0a0a0f !important;
        margin: 0;
        padding: 20px;
    }
    .bk-root {
        background-color: #0a0a0f !important;
    }
</style>
""")

final_layout = column(page_css, dashboard)

# Show in browser
show(final_layout)

print("""
╔══════════════════════════════════════════════════════════════════╗
║     🎉 Dashboard Generated Successfully!                         ║
║                                                                  ║
║     The dashboard has been saved to 'dashboard.html'             ║
║     and should open automatically in your browser.               ║
║                                                                  ║
║     Features:                                                    ║
║     • Line Chart - Sales trends over time                        ║
║     • Bar Chart - Regional revenue comparison                    ║
║     • Scatter Plot - Multi-dimensional analysis                  ║
║     • Donut Chart - Device traffic distribution                  ║
║     • Area Chart - Cumulative sales distribution                 ║
║     • Time Series - Stock analysis with moving average           ║
║     • Grouped Bar - Team performance metrics                     ║
║                                                                  ║
║     Interactive Tools:                                           ║
║     • Pan, Zoom, Box Select, Lasso Select                        ║
║     • Hover tooltips with detailed information                   ║
║     • Click legend to hide/show data series                      ║
╚══════════════════════════════════════════════════════════════════╝
""")

