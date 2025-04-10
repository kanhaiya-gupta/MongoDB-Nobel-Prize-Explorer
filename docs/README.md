# Nobel Laureates ETL Pipeline

This project builds an **Extract, Transform, Load (ETL)** pipeline to process Nobel Prize data from the MongoDB "nobel" database, which includes "laureates" and "prizes" collections. It extracts data using the connected client (client.nobel), transforms it by standardizing dates and calculating ages at award time, and loads the results into a new "laureates_transformed" collection. Leveraging MongoDB’s NoSQL flexibility, the pipeline handles dynamic schemas to streamline data processing. The final step generates a visualization of laureates by country based on the transformed data. All code and outputs are crafted to align with the project’s analytical goals.

## Project Structure

```
nobel_etl/
├── src/                  # Core Python modules
│   ├── __init__.py       # Package initialization
│   ├── config.py         # Configuration settings
│   ├── database.py       # MongoDB connection and extraction
│   ├── transform.py      # Data transformation logic
│   ├── load.py           # Data loading into MongoDB
│   └── visualization.py  # Visualization generation
├── tests/                # Unit tests
│   ├── __init__.py
│   ├── test_database.py
│   ├── test_transform.py
│   ├── test_load.py
│   └── test_visualization.py
├── data/                 # Data storage
│   └── README.md         # Instructions for data files
├── docs/                 # Documentation
│   ├── README.md         # Additional project docs
│   └── requirements.txt  # Dependencies
├── main.py               # Entry point for the ETL pipeline
├── README.md             # This file
└── LICENSE               # MIT License
```

## Features
- **Extract**: Retrieves laureate data from the `nobel.laureates` collection in MongoDB.
- **Transform**: Standardizes dates, calculates age at award time, and enriches prize data.
- **Load**: Stores transformed data into `nobel.laureates_transformed`.
- **Visualization**: Generates a bar chart of the top 10 countries by laureate count, saved as `laureates_by_country.png`.
- **Comparison**: Compares the number of laureates vs. prizes to determine a true statement.
- **Modular Design**: Separates concerns into distinct modules with a configurable setup.
- **Testing**: Includes unit tests for each component.

## Prerequisites
- **Python 3.8+**: Ensure Python is installed on your system.
- **MongoDB**: A local MongoDB instance running on `localhost:27017` (default port).
- **Dependencies**: Listed in `docs/requirements.txt`.

## Setup Instructions

### 1. Install MongoDB
- Download and install MongoDB Community Server from [MongoDB Download Center](https://www.mongodb.com/try/download/community).
- Start MongoDB:
  - On Windows (if installed as a service): It should start automatically; check `services.msc`.
  - Manually: Run `mongod` from the MongoDB `bin` directory (e.g., `C:\Program Files\MongoDB\Server\8.0\bin`).

### 2. Clone the Repository
```bash
git clone <repository-url>
cd nobel_etl
```

### 3. Install Dependencies
```bash
pip install -r docs/requirements.txt
```
This installs `pymongo` for MongoDB interaction and `matplotlib` for visualization.

### 4. Prepare Data
- Ensure your Nobel Prize data is loaded into the `nobel` database:
  - If you have a `laureates.json` file, place it in the `data/` directory and load it into MongoDB manually (see below) or extend `database.py` to handle this.
  - Example manual load:
    ```python
    from pymongo import MongoClient
    import json
    client = MongoClient('mongodb://localhost:27017/')
    db = client['nobel']
    with open('data/laureates.json', 'r') as f:
        data = json.load(f)
        db.laureates.insert_many(data)
    client.close()
    ```

## Usage

### Running the ETL Pipeline
1. Ensure MongoDB is running.
2. Execute the main script:
   ```bash
   python main.py
   ```
3. Expected Output:
   - Connection confirmation.
   - Number of extracted, transformed, and loaded laureates.
   - Comparison of laureates vs. prizes.
   - A file `laureates_by_country.png` in the root directory.

### Running Tests
```bash
python -m unittest discover tests
```
This runs all unit tests to verify functionality. Note: Tests assume a running MongoDB instance with data in `nobel.laureates`.

## Configuration
Edit `src/config.py` to customize:
- `MONGODB_URI`: Change if your MongoDB instance is not on `localhost:27017`.
- `DATABASE_NAME`: Set to a different database if needed.
- `TARGET_COLLECTION`: Rename the output collection.
- `VISUALIZATION_OUTPUT`: Change the visualization file name/path.

## Sample Data
The pipeline expects data in the `nobel.laureates` collection with a structure like:
```json
{
  "id": "2",
  "firstname": "Hendrik Antoon",
  "surname": "Lorentz",
  "born": "1853-07-18",
  "died": "1928-02-04",
  "bornCountry": "the Netherlands",
  "gender": "male",
  "prizes": [
    {
      "year": "1902",
      "category": "physics",
      "share": "2",
      "motivation": "..."
    }
  ]
}
```

## Extending the Pipeline
- **Add Data Loading**: Modify `database.py` to load `laureates.json` from `data/`.
- **More Visualizations**: Update `visualization.py` for additional charts (e.g., prizes by category).
- **Error Handling**: Add try-except blocks for robustness.
- **CLI Options**: Use `argparse` in `main.py` for runtime configuration.

## License
This project is licensed under the MIT License. See the `LICENSE` file for details.

## Contributing
Feel free to submit issues or pull requests to enhance the pipeline. See `docs/README.md` for more details.

## Contact
For questions, reach out to [Your Name/Email] or open an issue on the repository.
```

---

### Notes
- **Placement**: Save this as `README.md` in the root directory (`nobel_etl/`).
- **Customization**: Replace `<repository-url>` and `[Your Name/Email]` with your actual details if hosting this on GitHub or similar.
- **Data Loading**: I included a manual loading example since your `laureates.json` isn’t automatically loaded yet. If you want this integrated, I can update `database.py` and `main.py`.
- **Tests**: The README notes that tests require MongoDB and data—consider mocking for CI environments if needed.

This README should give anyone a clear path to set up and run your project. Let me know if you’d like to adjust anything!
