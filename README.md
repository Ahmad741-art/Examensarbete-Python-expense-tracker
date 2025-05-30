Expense Tracker – Python CLI-applikation för budgethantering

Expense Tracker är ett terminalbaserat program som låter dig registrera, hantera och analysera dina inkomster och utgifter. Projektet är utvecklat som ett skolprojekt i syfte att öva på Python, databashantering med SQLite och datavisualisering med matplotlib.



Syfte och mål

Målet med projektet är att skapa ett enkelt verktyg för personlig budgethantering, med funktioner för att:

- Lägga till och spara inkomster/utgifter
- Filtrera transaktioner efter datum eller kategori
- Visa summeringar och statistik
- Skapa diagram över utgiftskategorier

Projektet är en del av kursmomentet och syftar till att uppnå VG-nivå enligt kursens bedömningskriterier.



 Tekniker och bibliotek

- Python 3.10+
- SQLite – lokal databas
- matplotlib – visualisering av data
- argparse – hantering av CLI-kommandon
- Git – versionshantering via GitHub



Installation och användning

Så här gör du om du vill använda eller testa projektet på din egen dator:

1. Kopiera projektet från GitHub (klona)

Öppna din terminal (eller Git Bash på Windows) och skriv:

```bash
git clone https://github.com/ditt-användarnamn/expense-tracker.git
cd expense-tracker

2. (Valfritt) Skapa ett virtuellt Python-miljö
Det här hjälper till att hålla paket och versioner organiserade:

python -m venv venv
# För macOS/Linux
source venv/bin/activate

# För Windows
venv\Scripts\activate

3. Installera alla nödvändiga bibliotek

Använd requirements.txt för att installera rätt paket: pip install -r requirements.txt

4. Starta programmet

Kör huvudfilen med: python main.py
Nu är du redo att börja lägga till transaktioner, visa statistik eller skapa diagram!


