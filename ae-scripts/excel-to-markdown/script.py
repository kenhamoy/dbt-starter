# xlsx to md
import pandas as pd
from tabulate import tabulate

#Fill dataset and table 
def fill_down(table, column):
    table[column] = table[column].fillna(method="ffill")
    return table

#Build and clean table
def build_table(directory, file):
    data = pd.read_excel(directory+file, sheet_name="5 Transform", header=1)
    data=fill_down(data, "Table")
    data=fill_down(data, "Dataset")
    data=fill_down(data, "Table.1")
    data.replace({"isUsed?":{1:True,0:False},"UniqueKey?":{1:True,0:False}}, inplace=True)
    return data

def create_markdown_tables(data, out_directory):
    grouped=data.groupby('Dataset')

    # Iterate over the groups (datasets)
    for dataset, group_data in grouped:
        markdown_content = ''

        # Iterate over tables in dataset
        tables = group_data.groupby('Table.1')
        for table, table_data in tables:
            # Generate the Markdown table for the current dataset
            table_data.drop(["Table","Dataset","Table.1"], axis=1, inplace=True)
            table_data.dropna(subset=["Standardized Field"], inplace=True)
            markdown_table = tabulate(table_data, headers='keys', tablefmt='pipe', showindex=False)

            # Append the Markdown table to the content with dataset header and separator
            title = table.replace("_"," ").title()
            markdown_content += f'# {title}\n\n{markdown_table}\n\n---\n\n'
        
    # Write the Markdown content to a file
        with open(out_directory+dataset+'.md', 'w') as file:
            file.write(markdown_content)

def main():
  directory = input("Enter directory of file: ")
  file = input("Enter file name: ")
  out_directory = input("Enter directory of output file: ")
  if not directory.endswith('/'):
    directory=directory+'/'
  if out_directory.strip()=="":
    out_directory=directory
  elif not out_directory.endswith('/'):
    out_directory=out_directory+'/'

  if not file.endswith('.xlsx'):
     file += '.xlsx'
  
  dataset=build_table(directory, file)
  create_markdown_tables(dataset, out_directory)

if __name__ == "__main__":
   main()
