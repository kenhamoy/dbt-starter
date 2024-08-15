import json

"""
Generate a dbdiagram for dbdiagram.io from a dbt project, grouped by schema 
Usage:
  1. Run `dbt run`
  2. Run `dbt docs generate`
  2. Run `dbt_to_dbdiagram.py`
  3. Paste the output in https://dbdiagram.io/
"""

class Table:
    def __init__(self, name, schema, columns):
        self.name = name
        self.schema = schema
        self.columns = columns

    @classmethod
    def build(cls, data):
        table_name = data.get("metadata", {}).get("name")
        schema_name = data.get("metadata", {}).get("schema")
        return cls(
            table_name,
            schema_name, 
            [Column.build(table_name, name, details) for name, details in data.get("columns", {}).items()]
        )

class Column:
    def __init__(self, table_name, name, type_): 
        self.table_name = table_name
        self.name = name
        self.type = type_

    @classmethod
    def build(cls, table_name, name, details):
        return cls(table_name, name, details.get("type"))

def schema_fill(schema_dict, table):
    # Groups the tables by schema
    if table.schema in schema_dict.keys(): 
        schema_dict[table.schema].append(table.name)
    else: 
        schema_dict[table.schema] = [table.name]
    return  schema_dict

def out_table(table):
    # Produces the tables 
    out = f"TABLE {table.name} {{"
    columns = []
    for column in table.columns: 
        if '.' not in  column.name: 
            type = column.type
            if '<' in column.type: 
                type = type.split('<')[0]
            columns.append(f"{column.name} {type}") 
    out += "\n  " + "\n  ".join(columns) + "\n}"
    return out

def out_schema(schema): 
    # Produces the tableggroup, which is grouped by schema 
    out = f"TABLEGROUP {schema} {{"
    out += "\n  " + "\n  ".join(schema_dict[schema]) + "\n}"
    return out 

with open("../target/catalog.json", "r") as catalog_file:
    CATALOG = json.load(catalog_file)

schema_dict= {}
tables = [Table.build(data) for _key, data in CATALOG.get("nodes", {}).items()] 

for table in tables:
    schema_dict = schema_fill(schema_dict, table)
    print(out_table(table))
    print("")

for schema in schema_dict: 
    print(out_schema(schema))
    print("")