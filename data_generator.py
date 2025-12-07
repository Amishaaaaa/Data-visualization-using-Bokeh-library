"""
Sample Data Generator Module
Generates realistic sample data for the visualization dashboard
"""

import numpy as np
import pandas as pd
from datetime import datetime, timedelta


def generate_sales_data(months: int = 12) -> pd.DataFrame:
    """Generate monthly sales data for multiple products"""
    np.random.seed(42)
    
    products = ['Electronics', 'Clothing', 'Food & Beverages', 'Home & Garden', 'Sports']
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=months * 30),
        periods=months,
        freq='ME'
    )
    
    data = []
    for product in products:
        base_sales = np.random.randint(10000, 50000)
        trend = np.linspace(0, np.random.randint(-5000, 10000), months)
        seasonality = 5000 * np.sin(np.linspace(0, 2 * np.pi, months))
        noise = np.random.normal(0, 2000, months)
        
        sales = base_sales + trend + seasonality + noise
        sales = np.maximum(sales, 1000)  # Ensure positive sales
        
        for i, date in enumerate(dates):
            data.append({
                'date': date,
                'product': product,
                'sales': int(sales[i]),
                'units': int(sales[i] / np.random.randint(20, 100))
            })
    
    return pd.DataFrame(data)


def generate_regional_data() -> pd.DataFrame:
    """Generate sales data by region"""
    np.random.seed(42)
    
    regions = ['North America', 'Europe', 'Asia Pacific', 'Latin America', 'Middle East']
    
    data = {
        'region': regions,
        'revenue': np.random.randint(100000, 500000, len(regions)),
        'growth': np.random.uniform(-5, 25, len(regions)),
        'customers': np.random.randint(1000, 10000, len(regions)),
        'satisfaction': np.random.uniform(3.5, 5.0, len(regions))
    }
    
    return pd.DataFrame(data)


def generate_performance_data() -> pd.DataFrame:
    """Generate employee/team performance metrics"""
    np.random.seed(42)
    
    teams = ['Engineering', 'Sales', 'Marketing', 'Operations', 'Support', 'HR']
    
    data = {
        'team': teams,
        'productivity': np.random.uniform(70, 100, len(teams)),
        'quality': np.random.uniform(80, 99, len(teams)),
        'efficiency': np.random.uniform(65, 95, len(teams)),
        'headcount': np.random.randint(10, 100, len(teams))
    }
    
    return pd.DataFrame(data)


def generate_time_series_data(days: int = 90) -> pd.DataFrame:
    """Generate time series data for stock-like visualization"""
    np.random.seed(42)
    
    dates = pd.date_range(
        start=datetime.now() - timedelta(days=days),
        periods=days,
        freq='D'
    )
    
    # Generate random walk for stock-like data
    price = 100
    prices = [price]
    
    for _ in range(days - 1):
        change = np.random.normal(0, 2)
        price = max(price + change, 10)
        prices.append(price)
    
    prices = np.array(prices)
    volumes = np.random.randint(100000, 1000000, days)
    
    return pd.DataFrame({
        'date': dates,
        'price': prices,
        'volume': volumes,
        'high': prices + np.random.uniform(0, 5, days),
        'low': prices - np.random.uniform(0, 5, days),
        'moving_avg': pd.Series(prices).rolling(window=7).mean()
    })


def generate_scatter_data(n_points: int = 100) -> pd.DataFrame:
    """Generate scatter plot data with clusters"""
    np.random.seed(42)
    
    categories = ['Category A', 'Category B', 'Category C']
    data = []
    
    centers = [(30, 40), (60, 70), (80, 30)]
    
    for i, (category, center) in enumerate(zip(categories, centers)):
        x = np.random.normal(center[0], 10, n_points // 3)
        y = np.random.normal(center[1], 10, n_points // 3)
        size = np.random.uniform(5, 20, n_points // 3)
        
        for j in range(len(x)):
            data.append({
                'x': x[j],
                'y': y[j],
                'size': size[j],
                'category': category,
                'value': x[j] * y[j] / 100
            })
    
    return pd.DataFrame(data)


def generate_pie_data() -> pd.DataFrame:
    """Generate data for pie/donut charts"""
    np.random.seed(42)
    
    categories = ['Desktop', 'Mobile', 'Tablet', 'Smart TV', 'Other']
    values = np.array([45, 35, 12, 5, 3])
    
    # Calculate angles for pie chart
    total = sum(values)
    percentages = values / total * 100
    
    angles = values / total * 2 * np.pi
    cumulative = np.cumsum(angles)
    start_angles = np.concatenate([[0], cumulative[:-1]])
    end_angles = cumulative
    
    colors = ['#3498db', '#e74c3c', '#2ecc71', '#f39c12', '#9b59b6']
    
    return pd.DataFrame({
        'category': categories,
        'value': values,
        'percentage': percentages,
        'start_angle': start_angles,
        'end_angle': end_angles,
        'color': colors
    })


if __name__ == "__main__":
    # Test data generation
    print("Sales Data:")
    print(generate_sales_data().head())
    print("\nRegional Data:")
    print(generate_regional_data())
    print("\nPerformance Data:")
    print(generate_performance_data())
    print("\nTime Series Data:")
    print(generate_time_series_data().head())
    print("\nScatter Data:")
    print(generate_scatter_data().head())
    print("\nPie Data:")
    print(generate_pie_data())

