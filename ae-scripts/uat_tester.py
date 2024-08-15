import json 
import pandas as pd 
import os.path as path

def get_opposite_logic(expression):
    # This function gets the opposite logic. Ex. !=0 returns ==0
    expression = expression.strip()
    if expression.startswith('=='):
        return '!=' + expression[2:]
    elif expression.startswith('!='):
        return '==' + expression[2:]
    elif expression.startswith('<'):
        return '>=' + expression[1:]
    elif expression.startswith('>'):
        return '<=' + expression[1:]
    elif expression.startswith('<='):
        return '>' + expression[2:]
    elif expression.startswith('>='):
        return '<' + expression[2:]
    else:
        raise ValueError('Unsupported logic operator')

def model_define(i): 
    # This function supplies the schema, model, and columns 
    global models
    global repo
    model = i.split('.')[2]
    models.append(model)
    repo[model] = {'model_type': 'model', 'schema': '', 'table': '', 'columns': {}}
    repo[model]['schema'] = data_manifest['nodes'][i]['schema']
    repo[model]['table'] = data_manifest['nodes'][i]['alias']
    for j in data_manifest['nodes'][i]['columns'].keys(): 
        repo[model]['columns'][j] = {}

def source_define(i): 
    # This function supplies the schema, source, and columns 
    global models
    global repo

    model = "sources" + "." + data_manifest['sources'][i]['source_name'] + "." + data_manifest['sources'][i]['name'] #sources.raw_runn.allocations
    
    models.append(model)
    repo[model] = {'model_type': 'source', 'schema': '', 'table': '', 'columns': {}}
    repo[model]['schema'] = data_manifest['sources'][i]['source_name']
    repo[model]['table'] = data_manifest['sources'][i]['identifier']
    for j in data_manifest['sources'][i]['columns'].keys(): 
        repo[model]['columns'][j] = {}


def test_define(i): 
    # This function supplies the tests, compiled code, expected result, and optionally comments per test
    global repo
    global finder 
    if data_manifest['nodes'][i]['file_key_name'].split('.')[0] == "sources": 
        model = data_manifest['nodes'][i]['file_key_name'] + "."+ data_manifest['nodes'][i]['sources'][0][1]
    else:     
        model = data_manifest['nodes'][i]['file_key_name'].split('.')[1]
    column = data_manifest['nodes'][i]['column_name']
    repo[model]['columns'][column][i] = {'test_case': '', 'compiled': '', 'expected_results': '', 'output': '', 'status':'', 'comments': ''}
    repo[model]['columns'][column][i]['test_case'] = data_manifest['nodes'][i]['test_metadata']['name']
    repo[model]['columns'][column][i]['compiled'] = data_manifest['nodes'][i]['compiled_code'].strip()
    repo[model]['columns'][column][i]['expected_results'] = get_opposite_logic(data_manifest['nodes'][i]['config']['error_if'])
    finder[i] = [model, column]

def test_results(i): 
    # This function supplies the output and status per test 
    global repo
    model = finder[i['unique_id']][0]
    column = finder[i['unique_id']][1]
    repo[model]['columns'][column][i['unique_id']]['status']= i['status']
    if i['status'] == "error": 
         repo[model]['columns'][column][i['unique_id']]['output'] = i['message']
    else: 
        repo[model]['columns'][column][i['unique_id']]['output']= i['failures']
    

def populate_dict(): 
    # This function populates the dictionary with model details and test results 
    for i in data_manifest['nodes'].keys(): 
        if i.split('.')[0] == 'model': 
            model_define(i)
    for i in data_manifest['sources'].keys(): 
        if i.split('.')[0] == "source": 
            source_define(i)
    for i in data_manifest['nodes'].keys():
        if i.split('.')[0] == 'test': 
            test_define(i)
    for i in data_run_results['results']: 
        if i["unique_id"].startswith("test"): 
            test_results(i)
    
def dict_to_df(): 
    # This function converts the dictionary to a pandas dataframe
    df = pd.DataFrame(columns=['model_type','schema', 'table', 'test_case', 'query', 'expected_result', 'actual_result', 'status', 'comments'])
    for i in repo.keys(): 
        model_type = repo[i]['model_type']
        schema = repo[i]['schema']
        table = repo[i]['table']
        for k in repo[i]['columns'].keys(): 
            for l in repo[i]['columns'][k].keys(): 
                test_case= repo[i]['columns'][k][l]['test_case']
                compiled = repo[i]['columns'][k][l]['compiled']
                expected = repo[i]['columns'][k][l]['expected_results'] 
                output = repo[i]['columns'][k][l]['output']
                status = repo[i]['columns'][k][l]['status']
                comments = repo[i]['columns'][k][l]['comments']
                df.loc[len(df)] = {'model_type': model_type, 'schema':schema, 'table':table, 'test_case': test_case,'query': compiled, 'expected_result': expected, 'actual_result': output, 'status': status,'comments': comments}
    return df 

# Loading the json files 
run_results = open('../target/run_results.json') 
manifest = open('../target/manifest.json')
data_run_results = json.load(run_results)
data_manifest = json.load(manifest)

repo = {}
finder = {} 
models = [] 

populate_dict() # populates repo variable 
df = dict_to_df()

path_seed = path.abspath(path.join(__file__ ,'../..','seeds/uat.csv')) 
df.to_csv(path_seed,index=False)    # exports csv file under seeds folder 
print("Done")
