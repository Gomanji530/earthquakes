from datetime import date
import matplotlib.pyplot as plt
import requests
import numpy as np
from collections import defaultdict


def get_data():
    """Retrieve earthquake data from USGS API."""
    try:
        response = requests.get(
            "https://earthquake.usgs.gov/fdsnws/event/1/query.geojson",
            params={
                'starttime': "2000-01-01",
                "maxlatitude": "58.723",
                "minlatitude": "50.008",
                "maxlongitude": "1.67",
                "minlongitude": "-9.756",
                "minmagnitude": "1",
                "endtime": "2018-10-11",
                "orderby": "time-asc"}
        )
        
        response.raise_for_status()
        return response.json()
    except requests.RequestException:
        print("Using sample data (API request failed)")
        return create_sample_data()


def create_sample_data():
    """Generate sample earthquake data for testing."""
    import random
    from datetime import datetime, timedelta
    
    features = []
    base_date = datetime(2000, 1, 1)
    end_date = datetime(2018, 10, 11)
    days_range = (end_date - base_date).days
    
    for i in range(1000):
        random_days = random.randint(0, days_range)
        earthquake_time = base_date + timedelta(days=random_days)
        timestamp = int(earthquake_time.timestamp() * 1000)
        magnitude = round(random.uniform(1.0, 6.0), 1)
        
        features.append({
            'properties': {
                'time': timestamp,
                'mag': magnitude,
                'place': f"Sample Location {i}"
            }
        })
    
    return {'features': features}


def get_year(earthquake):
    """Extract the year from earthquake timestamp."""
    timestamp = earthquake['properties']['time']
    return date.fromtimestamp(timestamp / 1000).year


def get_magnitude(earthquake):
    """Retrieve earthquake magnitude."""
    return earthquake['properties']['mag']


def get_annual_statistics(earthquakes):
    """Calculate annual earthquake counts and average magnitudes."""
    quakes_per_year = defaultdict(int)
    magnitudes_per_year = defaultdict(list)
    
    for quake in earthquakes:
        try:
            year = get_year(quake)
            magnitude = get_magnitude(quake)
            quakes_per_year[year] += 1
            magnitudes_per_year[year].append(magnitude)
        except (KeyError, TypeError):
            continue
    
    # Calculate average magnitudes
    avg_magnitudes = {
        year: np.mean(magnitudes) 
        for year, magnitudes in magnitudes_per_year.items()
    }
    
    return dict(quakes_per_year), avg_magnitudes


def plot_earthquake_frequency(quakes_per_year):
    """Plot number of earthquakes per year."""
    years = sorted(quakes_per_year.keys())
    counts = [quakes_per_year[year] for year in years]
    
    plt.figure(figsize=(12, 6))
    bars = plt.bar(years, counts, color='skyblue', edgecolor='navy', alpha=0.7)
    
    plt.title('Earthquakes per Year (2000-2018)', fontsize=14, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Number of Earthquakes')
    plt.grid(axis='y', alpha=0.3)
    plt.xticks(years, rotation=45)
    
    # Add value labels on bars
    for bar, count in zip(bars, counts):
        plt.text(bar.get_x() + bar.get_width()/2., bar.get_height() + 0.5,
                f'{count}', ha='center', va='bottom', fontsize=9)
    
    plt.tight_layout()
    plt.savefig('earthquakes_per_year.png', dpi=300, bbox_inches='tight')
    plt.show()


def plot_average_magnitude(avg_magnitudes):
    """Plot average earthquake magnitude per year."""
    years = sorted(avg_magnitudes.keys())
    magnitudes = [avg_magnitudes[year] for year in years]
    
    plt.figure(figsize=(12, 6))
    plt.plot(years, magnitudes, marker='o', linewidth=2, color='coral')
    
    plt.title('Average Earthquake Magnitude per Year', fontsize=14, fontweight='bold')
    plt.xlabel('Year')
    plt.ylabel('Average Magnitude')
    plt.grid(True, alpha=0.3)
    plt.xticks(years, rotation=45)
    
    # Add value annotations
    for year, mag in zip(years, magnitudes):
        plt.annotate(f'{mag:.2f}', (year, mag), 
                    xytext=(0, 8), textcoords='offset points',
                    ha='center', fontsize=8)
    
    plt.tight_layout()
    plt.savefig('average_magnitude.png', dpi=300, bbox_inches='tight')
    plt.show()


def print_summary(quakes_per_year, avg_magnitudes):
    """Print data summary statistics."""
    total_quakes = sum(quakes_per_year.values())
    years = sorted(quakes_per_year.keys())
    
    print("=== EARTHQUAKE DATA SUMMARY ===")
    print(f"Time period: {years[0]} - {years[-1]}")
    print(f"Total earthquakes: {total_quakes}")
    print(f"Years covered: {len(years)}")
    print(f"Average earthquakes per year: {total_quakes/len(years):.1f}")
    
    max_year = max(quakes_per_year, key=quakes_per_year.get)
    min_year = min(quakes_per_year, key=quakes_per_year.get)
    print(f"Most active year: {max_year} ({quakes_per_year[max_year]} quakes)")
    print(f"Least active year: {min_year} ({quakes_per_year[min_year]} quakes)")


# Main execution
if __name__ == "__main__":
    # Load data
    data = get_data()
    earthquakes = data['features']
    
    # Calculate statistics
    quakes_per_year, avg_magnitudes = get_annual_statistics(earthquakes)
    
    # Print summary
    print_summary(quakes_per_year, avg_magnitudes)
    
    # Generate plots
    plot_earthquake_frequency(quakes_per_year)
    plot_average_magnitude(avg_magnitudes)