name: Update Expenses Data

on:
  schedule:
    - cron: '0 12 * * *' # Se ejecuta diario a las 12:00 UTC (7:00 AM COL/PE)
  workflow_dispatch:      # Permite ejecutarlo manualmente con un botón

jobs:
  build:
    runs-on: ubuntu-latest
    steps:
      - name: Checkout repo content
        uses: actions/checkout@v3

      - name: Setup python
        uses: actions/setup-python@v4
        with:
          python-version: '3.9'

      - name: Install dependencies
        run: |
          pip install pandas gspread google-auth

      - name: Execute script
        env:
          GOOGLE_CREDENTIALS: ${{ secrets.GOOGLE_CREDENTIALS }}
        run: python main.py

      - name: Commit and push if changed
        run: |
          git config --global user.name 'github-actions[bot]'
          git config --global user.email 'github-actions[bot]@users.noreply.github.com'
          git add expenses_combined.csv
          git commit -m "Auto-update data" || exit 0
          git push
