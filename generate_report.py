import db_utils
from pathlib import Path
import logging
import csv

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
    all_data_unfiltered = []
    all_data = []
    middle_data = all_data[0]
    junior_data = all_data[1]
    senior_data = all_data[2]
    for d in divisions:
        match d:
            case "M":
                with open("Middle_Results,csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(middle_data)
            case "J":
                with open("Junior_Results,csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(junior_data)
            case "S":
                with open("Senior_Results,csv", 'w', newline='') as file:
                    writer = csv.writer(file)
                    writer.writerow(headers)
                    writer.writerows(senior_data)

# Export Player List as CSV. One file per division
def player_list():
    pass

# Generate single PDF of results separated by division
def generate_pdf():
    generate_folder()