import pandas as pd
import os
import yfinance as yf

class DataProcessor:
    def __init__(self):
        self.df = None  

    def load_data(self, file_path):
        extension = os.path.splitext(file_path)[1].lower()

        try:
            if extension == ".csv":
                self.df = pd.read_csv(file_path)
            elif extension in [".xls", ".xlsx"]:
                self.df = pd.read_excel(file_path)
            elif extension == ".json":
                self.df = pd.read_json(file_path)
            else:
                return f"Unsupported file format: {extension}"
            return f"Successfully loaded {len(self.df)} rows and {len(self.df.columns)} columns."
        except Exception as e:
            return f"Error loading file: {e}"
        
    def clean_data(self, drop_threshold=0.5):
        if self.df is None:
            return "No data loaded."
        
        # remove duplicates
        initial_count = len(self.df)
        self.df.drop_duplicates(inplace=True)
        duplicates_removed = initial_count - len(self.df)

        # drops columns that are mostly empty (> 50%)
        limit = int(len(self.df) * drop_threshold)
        self.df = self.df.dropna(thresh=limit, axis=1)

        number_cols = self.df.select_dtypes(include=["number"]).columns
        if not number_cols.empty:
            self.df[number_cols] = self.df[number_cols].fillna(self.df[number_cols].mean())

        object_cols = self.df.select_dtypes(include=["object"]).columns
        if not object_cols.empty:
            self.df[object_cols] = self.df[object_cols].fillna("Unknown.")

        dropped_count = initial_count - duplicates_removed - len(self.df)

        return f"Cleaned! Removed {duplicates_removed} duplicates and dropped {dropped_count}"
    
    def summarize(self):
        """ Summarises the important features of the data. """
        if self.df is None:
            return "No data to summarise"
        
        summary = self.df.describe()
        return summary

    def frequency(self, column, groupby):
        grouped = self.df.groupby(groupby)
        return grouped[column].value_counts()
    
    def get_df(self):
        return self.df
        
    
    
processor = DataProcessor()
processor.load_data("Teen_Mental_Health_Dataset.csv")



    
        
