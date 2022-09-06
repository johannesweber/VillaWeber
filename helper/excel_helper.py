from msilib.schema import tables
from helper.configuration import Configuration
from openpyxl import load_workbook
import pandas as pd


class ExcelHelper:

    def __init__(self) -> None:
        self.configuration = Configuration('villaweber')
        self.configuration.load()
        self.path = self.configuration.ga_excel_path

    def read_excel(self, sheetName, table = None) -> pd.DataFrame:
        wb = load_workbook(self.path)
        sheet = wb[sheetName]
        tables = []

        for entry, data_boundary in sheet.tables.items():
            #parse the data within the ref boundary

            data = sheet[data_boundary]
            #extract the data 
            #the inner list comprehension gets the values for each cell in the table
            content = [[cell.value for cell in ent] 
                        for ent in data
                      ]
            
            header = content[0]
            rest = content[1:]

            df = pd.DataFrame(rest, columns = header)
            tables.append(df)
            if table is not None and table is entry:
                break
        return tables
