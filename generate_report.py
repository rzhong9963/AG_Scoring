import db_utils
from pathlib import Path
import logging
import csv
from csv2pdf import convert
# Explore this one in the future
#from fpdf import Template

divisions = ["M", "J", "S"]

# Create reports folder. Everything will be saved here, including player list
def generate_folder():
    directory_path = Path("reports")
    logging.basicConfig(level=logging.INFO)
    # Create results directory
    try:
        directory_path.mkdir()
        logging.info(f"Directory '{directory_path}' created successfully.")
    except FileExistsError:
        logging.info(f"Directory '{directory_path}' already exists.")
    except PermissionError:
        logging.INFO(f"Permission denied: Unable to create '{directory_path}'.")
    except Exception as e:
        logging.INFO(f"An error occurred: {e}")

# Generate CSV version of results. One file per division
def generate_csv():
    generate_folder()
    headers = ['ID', 'Name', 'On-Sets', 'Equations', 'LinguiSHTIK', 'Propaganda', 'Propaganda Scaled', 'Presidents',
               'Presidents Scaled', 'Current Events', 'Current Events Scaled', 'Theme', 'Theme Scaled', 'Overall']
    all_data = db_utils.all_info()
    middle_data = all_data[0]
    junior_data = all_data[1]
    senior_data = all_data[2]
    for d in divisions:
        match d:
            case "M":
                with open("reports/Middle_Results.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(middle_data)
            case "J":
                with open("reports/Junior_Results.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(junior_data)
            case "S":
                with open("reports/Senior_Results.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(senior_data)

# Export Player List as CSV only. One file per division
def player_list():
    generate_folder()
    divs = ["M", "J", "S"]
    headers = ['ID', 'Name']
    for d in divs:
        players = db_utils.get_players(d)
        match d:
            case "M":
                with open("reports/Middle_Players.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(players)
            case "J":
                with open("reports/Junior_Players.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(players)
            case "S":
                with open("reports/Senior_Players.csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(players)

# Generate single PDF of results separated by division - In a future version
# Convert CSV to PDF for now
def generate_pdf():
    generate_folder()
    generate_csv()
    convert('reports/Middle_Results.csv', 'reports/Middle_Results.pdf', orientation="L")
    convert('reports/Junior_Results.csv', 'reports/Junior_Results.pdf', orientation="L")
    convert('reports/Senior_Results.csv', 'reports/Senior_Results.pdf', orientation="L")
