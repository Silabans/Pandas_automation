import pandas as pd
import os
import yfinance as yf
import matplotlib.pyplot as plt

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
    
    def plot_column(self, column):
        if self.df is None or column not in self.df.columns:
            print("Invalid column.")

        data_to_plot = self.df[column].dropna()
        if data_to_plot.empty:
            print("There is no data to plot!")
            return
        
        plt.figure(figsize=(10, 6))
        plt.clf()
        if pd.api.types.is_numeric_dtype(data_to_plot):
            data_to_plot.hist(edgecolor='black')
        else:
            data_to_plot.value_counts().plot(kind='bar')
            plt.xticks(rotation=30)

        print(f"Generating a histogram for {column}...")
        title = column.replace("_", " ").capitalize()
        plt.title(f"Distribution of {title}")
        plt.ylabel("Frequency")
        plt.show()
        #plt.savefig(f'{column}_distribution_graph.png')


    def get_df(self):
        return self.df
        
    
    
processor = DataProcessor()
processor.load_data("Teen_Mental_Health_Dataset.csv")
processor.plot_column("sleep_hours")



    
        
