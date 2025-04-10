# src/transform.py
from datetime import datetime

# src/transform.py
from datetime import datetime

def transform_data(laureates):
    transformed_laureates = []
    invalid_dates = []  # To track problematic entries
    
    for laureate in laureates:
        # Handle born date
        born_date = laureate.get('born')
        if born_date and born_date != "0000-00-00":
            try:
                born_date = datetime.strptime(born_date, "%Y-%m-%d")
            except ValueError as e:
                print(f"Invalid born date '{born_date}' for laureate ID {laureate.get('id')}: {e}")
                invalid_dates.append({'id': laureate.get('id'), 'field': 'born', 'value': born_date})
                born_date = None  # Set to None if invalid
        else:
            born_date = None
        
        # Handle died date
        died_date = laureate.get('died')
        if died_date == "0000-00-00":
            died_date = None
        elif died_date:
            try:
                died_date = datetime.strptime(died_date, "%Y-%m-%d")
            except ValueError as e:
                print(f"Invalid died date '{died_date}' for laureate ID {laureate.get('id')}: {e}")
                invalid_dates.append({'id': laureate.get('id'), 'field': 'died', 'value': died_date})
                died_date = None

        # Transform prizes
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

        # Create transformed document
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
    if invalid_dates:
        print(f"Encountered {len(invalid_dates)} invalid dates: {invalid_dates}")
    return transformed_laureates