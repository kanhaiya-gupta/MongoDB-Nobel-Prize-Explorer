#!/bin/bash


# Create directory structure
mkdir -p src tests data docs

# Create files in src/
touch src/__init__.py
touch src/config.py
touch src/database.py
touch src/transform.py
touch src/load.py
touch src/visualization.py

# Create files in tests/
touch tests/__init__.py
touch tests/test_database.py
touch tests/test_transform.py
touch tests/test_load.py
touch tests/test_visualization.py

# Create data directory and README
touch data/README.md
echo "# Data Directory" > data/README.md
echo "This directory is for storing sample data or outputs (e.g., CSVs, PNGs)." >> data/README.md

# Create docs directory and files
touch docs/README.md
touch docs/requirements.txt

# Populate docs/README.md with basic content
cat <<EOL > docs/README.md
# Census Data Explorer

A Python project to explore and analyze census data from a database.

## Setup
1. Install dependencies: \`pip install -r docs/requirements.txt\`
2. Configure the database connection in \`src/config.py\`.
3. Run the pipeline: \`python main.py\`

## Features
- Connect to the database.
- Extract, Transform, and Load (ETL) census data.
- Generate analysis and visualizations.
EOL

# Populate docs/requirements.txt with basic dependencies
cat <<EOL > docs/requirements.txt
sqlalchemy
psycopg2-binary
pandas
matplotlib
EOL

# Create root-level files
touch main.py
touch .gitignore
touch LICENSE


EOL

# Populate .gitignore with common Python ignores
cat <<EOL > .gitignore
__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
venv/
*.egg-info/
dist/
build/
*.log
*.csv
*.png
EOL

# Populate LICENSE with a simple MIT License
cat <<EOL > LICENSE
MIT License

Copyright (c) 2025 [Your Name]

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
EOL



echo "Project structure created successfully!"
