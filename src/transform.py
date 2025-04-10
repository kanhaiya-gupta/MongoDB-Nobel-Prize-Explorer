# src/transform.py
from datetime import datetime

def transform_data(laureates):
    transformed_laureates = []
    
    for laureate in laureates:
        born_date = laureate.get('born')
        if born_date and born_date != "0000-00-00":
            born_date = datetime.strptime(born_date, "%Y-%m-%d")
        else:
            born_date = None
        
        died_date = laureate.get('died')
        if died_date == "0000-00-00":
            died_date = None
        elif died_date:
            died_date = datetime.strptime(died_date, "%Y-%m-%d")

        prizes = laureate.get('prizes', [])
        transformed_prizes = []
        for prize in prizes:
            year = int(prize.get('year', 0))
            age_at_award = year - born_date.year if born_date and year else None
            transformed_prizes.append({
                'year': year,
                'category': prize.get('category'),
                'share': int(prize.get('share', 1)),
                'motivation': prize.get('motivation'),
                'age_at_award': age_at_award
            })

        transformed_laureates.append({
            '_id': laureate.get('id'),
            'firstname': laureate.get('firstname'),
            'surname': laureate.get('surname'),
            'born': born_date.isoformat() if born_date else None,
            'died': died_date.isoformat() if died_date else None,
            'bornCountry': laureate.get('bornCountry'),
            'gender': laureate.get('gender'),
            'prizes': transformed_prizes,
            'total_prizes': len(transformed_prizes)
        })
    
    print(f"Transformed {len(transformed_laureates)} laureates.")
    return transformed_laureates