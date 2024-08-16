from globals import advanced_logic

# =============================================================================
# data stream ID
system_prompt_ds_ID_single = """This request contains the dictionary of existing user's data streams.
Every stream has id, name, measure names where measure is business metric and dimensions which are features of metrics.
Select a datastream that corresponds to user's request.
User wants to create an 'Alert' instance that will inform about anomalies in measure filtered according to dimensions.
You must select the stream that contains requested metrics and features.
Respond can't be empty. Data Streams: """

system_prompt_ds_id = """User wants to create an 'Alert' instance that will inform about anomalies in measure.
Measure is a timeseries of business metric in data stream.
Every data stream has id, name, measures and dimensions. Dimensions are features of measures.
Given the dictionary of existing user's data streams, select data stream that is the most relevant to the user query.
If the query is ambiguous and it is not clear what data stream to choose you must return two most relevant data streams.
Together with the data stream id you must return detected_ambiguous flag and estimated probability score between 0 and 10 for data stream to be chosen.
Sum of scores must be equal to 10. 
Make decision using step by step reasoning. 
ATTENTION: output must contain only data stream ids, detected_ambiguous flag, and estimated scores 
Respond can't be empty.
Data Streams:
'''json
"""

if advanced_logic:
    system_prompt_ds_ID = system_prompt_ds_id
else:
    system_prompt_ds_ID = system_prompt_ds_ID_single

pyd_description_ds_ID = "Select a datastream id from the fixed list."
pyd_instruction_ds_ID = "The values are restricted to the entries present in the dataset."

# =============================================================================
# direction
pyd_description_direction = """Direction of anomaly."
Here are examples of query and correct answer.
example #1: query = "Monitor sharp increases in approved transactions count" answer = "up"
example #2: query = "Alert if theres a notable decrease in average handling time for customer inquiries" answer = "down"
example #3: query = "Monitor significant fluctuations in sales volume for home goods during promotional periods" answer = "both"
example #4: query = "Alert me when the inventory of electronic goods exceeds the value of 1000 units" answer = "up"
"""
# =============================================================================
# measure
pyd_description_measure = "Select a measure from the fixed list."
pyd_instruction_measure = "The values are restricted to the entries present in the datastream."
pyd_instruction_measure_ambiguous = """If the query is ambiguous and it is not clear what measure to choose you must return list of most relevant measures.
Together with the measures you must return reasoning explanation, detected_ambiguous flag and list of estimated probability scores between 0 and 10 for each measure to be chosen.
Sum of scores must be equal to 10.
Make decision using step by step reasoning.
ATTENTION: If the query is ambiguous you MUST return several measures
"""
if advanced_logic:
    pyd_instruction_measure = pyd_instruction_measure + pyd_instruction_measure_ambiguous
else:
    pyd_instruction_measure = pyd_instruction_measure

# =============================================================================
# dimension
pyd_description_dimensions = """Dimensions are features of measure.
Here are examples of query, sample of dimension values, reasoning and correct answer.
###
query = 'Alert for significant increases in water consumption in commercial buildings during non-peak times, possibly indicating leaks'
sample = {'Building_Type': ['Residential', 'Commercial', 'Industrial'], 'Usage_Type': ['Heating', 'Cooling', 'Lighting'], 'Time_Period': ['Day', 'Week', 'Month', 'Year']}
reasoning = User mentioned commercial buildings and 'Commercial' is the value under 'Building_Type' dimension. User wants to monitor measures during non-peak times, that is why 'Time_Period' Dimension could also be relevant.
answer = ['Building_Type', 'Time_Period']
###
query = 'Alert me when the sales target achieved by sales managers with 0-2 years tenure falls below 70%'
sample = {'Department': ['Sales', 'Marketing', 'HR', 'Finance'], 'Position': ['Manager', 'Associate', 'Supervisor', 'Executive'], 'Tenure': ['0-2_Years', '3-5_Years', '6-10_Years', '10+_Years']}
reasoning = 'User mentioned managers, where manager is the values from 'Position' Dimensions. Also sales managers were specificly mentioned, which makes 'Department' Dimension also relevant because it contains 'Sales'. User specified tenure from 0 to 2 years, therefore 'Tenure' Dimension must be added to the list of dimensions.
answer = ['Department', 'Position', 'Tenure']
###
query = 'Alert when time spent on development is significantly lower than usual.'
sample = {'Project_Type': ['Development', 'Research', 'Marketing', 'Maintenance'], 'Task_Type': ['Research', 'Development', 'Testing', 'Deployment'], 'Budget_Source': ['Commercial', 'Credit', 'Direct Funding']}
reasoning = The query specifically mentions development, which is a value under both 'Project_Type' and 'Task_type' dimensions. Therefore both Project_Type and Task_Type must be returned.
answer = ['Project_Type', 'Task_Type']
"""

pyd_instruction_dimensions_simple = """Given sample of dimension values select dimensions from the fixed list.
Make decision using step by step reasoning and take into account values of dimensions from the sample.
If no dimension can be extracted from query then return all dimensions."""

pyd_instruction_dimensions = """Given sample of dimension values return list of relevant dimensions.
If the query does not specify any particular dimension return all dimensions."""

pyd_instruction_dimensions_ambiguous = """If the measure could logically involve multiple dimensions, you must return several most relevant dimensions.
Ensure to iterate thrice over every dimension value from the sample to determine all potentially relevant dimensions.
Consider all dimensions that could logically relate to the user query and sample data, and provide reasoning for each selected dimension.
Together with the dimensions you must return reasoning explanation, detected_ambiguous flag and list of estimated probability scores between 0 and 10 for each dimension to be chosen.
Sum of scores must be equal to 10."""

if advanced_logic:
    pyd_instruction_dimensions = pyd_instruction_dimensions + pyd_instruction_dimensions_ambiguous
else:
    pyd_instruction_dimensions = pyd_instruction_dimensions_simple
# =============================================================================
# type
pyd_description_type = """
Alert type is based on the behavior of the measure:
- 'Anomaly' indicates any spike or drop in the measure.
- 'Static' denotes when a specific static value or percentage is crossed or reached.
- 'No Data' signifies when the data stream receives no data from the source.
 Here are examples of query and correct answer:
### 
query = "Alert me when the transaction request count drops significantly"
answer = "anomaly"
###
query = "Alert me when the daily sales volume for electronics falls below 500 units"
answer = "static"
###
query = "Alert me about missing data for sales volume"
answer = "no data"
"""

# =============================================================================
# _title
pyd_description_title = """Title for an Alert based on user query in format <Drop or Spike or Anomaly> in <Measure Name> by {{<Dimension Name 1>},{<Dimension Name 2 if any>}...}.
Don't include symbols '<' and '>' but include symbols '{' and '}'  
Example:  Drop in Transaction Count by {{Request_type}}, {{Source}}"""

# =============================================================================
# general
general_system_prompt = """User wants to create an 'Alert' instance that will inform about anomalies in measure.
Measure is a timeseries of business metric in data stream.
You are given user query and data stream schema. Data stream schema contains name of measures, dimensions and sample.
Measure may has several dimensions and can be aggregated by them. Sample contains existing dimension values.
Extract alert title, alert type, alert direction, the most relevant measure and dimensions according to the response model."""

system_prompt_ambiguous = """
If the query is ambiguous and it is not clear what measure to choose you must return list of two most relevant measures.
If the measure could logically involve multiple dimensions, you must return several most relevant dimensions.
Ensure to iterate thrice over every dimension value from the sample to determine all potentially relevant dimensions.
Consider all dimensions that could logically relate to the user query and sample data, and provide reasoning for each selected dimension.
"""

if advanced_logic:
    general_system_prompt = general_system_prompt + system_prompt_ambiguous

pyd_description_ambiguous = 'detected_ambiguous flag can be True or False. True: if more than one value can be selected. False: if only one value can be selected'

customized_pydentic = """The output should be formatted as a JSON instance that conforms to the JSON schema.
Here is the output schema:"""

all_prompts = {"system_prompt_ds_ID": system_prompt_ds_ID,
               "pyd_description_ds_ID": pyd_description_ds_ID,
               "pyd_instruction_ds_ID": pyd_instruction_ds_ID,
               "pyd_description_measure": pyd_description_measure,
               "pyd_instruction_measure": pyd_instruction_measure,
               "pyd_description_dimensions": pyd_description_dimensions,
               "pyd_instruction_dimensions": pyd_instruction_dimensions,
               "pyd_description_title": pyd_description_title,
               "pyd_description_type": pyd_description_type,
               "general_system_prompt": general_system_prompt,
               "customized_pydentic": customized_pydentic,
               "pyd_description_ambiguous": pyd_description_ambiguous,
               "pyd_description_direction": pyd_description_direction}