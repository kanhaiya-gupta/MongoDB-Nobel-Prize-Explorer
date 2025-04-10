# src/visualization.py
import matplotlib.pyplot as plt
from src.config import Config

def visualize_laureates_by_country(collection):
    pipeline = [
        {'$group': {'_id': '$bornCountry', 'count': {'$sum': 1}}},
        {'$sort': {'count': -1}},
        {'$limit': 10}
    ]
    results = list(collection.aggregate(pipeline))
    
    countries = [r['_id'] if r['_id'] else 'Unknown' for r in results]
    counts = [r['count'] for r in results]
    
    plt.figure(figsize=(10, 6))
    plt.bar(countries, counts, color='skyblue')
    plt.title('Top 10 Countries by Number of Nobel Laureates')
    plt.xlabel('Country')
    plt.ylabel('Number of Laureates')
    plt.xticks(rotation=45, ha='right')
    plt.tight_layout()
    plt.savefig(Config.VISUALIZATION_OUTPUT)
    print(f"Visualization saved as '{Config.VISUALIZATION_OUTPUT}'.")
    plt.close()