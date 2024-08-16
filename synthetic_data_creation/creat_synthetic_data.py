import pandas as pd
import copy

csv_file_path = r'C:\Users\User\Dropbox\study\Ydata\C0_projects\Data\synthetic_data\synthetic_data.csv'

def creat_data_stream():
    # Define the data
    data_streams=[
        {
            'ID': ['1'],
            'name':['CalDemo'],
            'Measure': ['Transactions_request_Amount', 'Transaction_Request_Count'],
            'Dimension': ['Segment', 'Source', 'Is_tourist', 'Status', 'Request_type', 'Payment_Method', 'Slack_mapping'],
            'Segment': ['Fashion', 'Gardening', 'Travel', 'Tech'],
            'Source': ['Bank', 'Mastercard', 'Shva', 'Visa'],
            'Is_tourist': [True, False],
            'Status': ['Approved', 'Declined'],
            'Request_type': ['Frontal', 'Online', 'Cash_withdraw', 'Contactless'],
            'Payment_Method': ['American', 'Visa', 'MasterCard', 'Diners', 'Trustly'],
        },
        {
            'ID': ['2'],
            'name': ['CustomerSupport'],
            'Measure': ['Customer_Satisfaction_Score', 'Response_Rate'],
            'Dimension': ['Customer_Segment', 'Contact_Channel', 'Issue_Resolved', 'Agent_ID'],
            'Customer_Segment': ['VIP', 'Regular', 'Occasional', 'First-time'],
            'Contact_Channel': ['Phone', 'Email', 'Chat', 'Social_Media'],
            'Issue_Resolved': [True, False],
            'Agent_ID': ['A001', 'A002', 'A003', 'A004']
        },
        {
            'ID': ['3'],
            'name': ['grocery'],
            'Measure': ['Daily_Sales_Volume', 'Inventory_Turnover_Rate'],
            'Dimension': ['Product_Category', 'Store_Location', 'Promotion_Applied', 'Season'],
            'Product_Category': ['Electronics', 'Clothing', 'Home_Goods', 'Groceries'],
            'Store_Location': ['North', 'South', 'East', 'West'],
            'Promotion_Applied': [True, False],
            'Season': ['Spring', 'Summer', 'Autumn', 'Winter']
        },
        {
            'ID': ['4'],
            'name': ['CustomerService'],
            'Measure': ['Average_Handling_Time', 'First_Call_Resolution'],
            'Dimension': ['Service_Type', 'Operator_ID', 'Peak_Hours', 'Customer_Type'],
            'Service_Type': ['Technical_Support', 'Customer_Inquiry', 'Billing_Issue', 'Account_Update'],
            'Operator_ID': ['OP001', 'OP002', 'OP003', 'OP004'],
            'Peak_Hours': ['Morning', 'Afternoon', 'Evening', 'Night'],
            'Customer_Type': ['Business', 'Personal']
        },
        {
            'ID': ['5'],
            'name': ['SalesData'],
            'Measure': ['Revenue', 'Units_Sold', 'Profit'],
            'Dimension': ['Product_Type', 'Region', 'Channel'],
            'Product_Type': ['Electronics', 'Apparel', 'Furniture', 'Food'],
            'Region': ['North', 'South', 'East', 'West'],
            'Channel': ['Online', 'Retail']
        },
        {
            'ID': ['6'],
            'name': ['EmployeePerformance'],
            'Measure': ['Sales_Target_Achieved', 'Customer_Satisfaction_Score', 'Absenteeism_Rate'],
            'Dimension': ['Department', 'Position', 'Tenure'],
            'Department': ['Sales', 'Marketing', 'HR', 'Finance'],
            'Position': ['Manager', 'Associate', 'Supervisor', 'Executive'],
            'Tenure': ['0-2_Years', '3-5_Years', '6-10_Years', '10+_Years']
        },
        {
            'ID': ['7'],
            'name': ['WebsiteTraffic'],
            'Measure': ['Page_Views', 'Unique_Visitors', 'Bounce_Rate'],
            'Dimension': ['Page_Type', 'Traffic_Source', 'Device_Type'],
            'Page_Type': ['Home', 'Product', 'Blog', 'Contact'],
            'Traffic_Source': ['Organic_Search', 'Social_Media', 'Referral', 'Direct'],
            'Device_Type': ['Desktop', 'Mobile', 'Tablet']
        },
        {
            'ID': ['8'],
            'name': ['SupplyChain'],
            'Measure': ['Inventory_Level', 'Order_Fulfillment_Time', 'Supplier_Performance'],
            'Dimension': ['Product_Category', 'Supplier', 'Warehouse'],
            'Product_Category': ['Electronics', 'Apparel', 'Furniture', 'Toys'],
            'Supplier': ['Amazon', 'Walmart', 'Target', 'BestBuy'],
            'Warehouse': ['Warehouse1', 'Warehouse2', 'Warehouse3', 'Warehouse4']
        },
        {
            'ID': ['9'],
            'name': ['HealthMetrics'],
            'Measure': ['Blood_Pressure', 'Heart_Rate', 'BMI', 'Blood_Sugar'],
            'Dimension': ['Age_Group', 'Gender', 'Health_Status'],
            'Age_Group': ['Under_30', '30-50', '50-70', 'Over_70'],
            'Gender': ['Male', 'Female'],
            'Health_Status': ['Healthy', 'Prehypertension', 'Hypertension']
        },
        {
            'ID': ['10'],
            'name': ['EnergyConsumption'],
            'Measure': ['Electricity_Consumption', 'Gas_Consumption', 'Water_Consumption'],
            'Dimension': ['Building_Type', 'Usage_Type', 'Time_Period'],
            'Building_Type': ['Residential', 'Commercial', 'Industrial'],
            'Usage_Type': ['Heating', 'Cooling', 'Lighting'],
            'Time_Period': ['Day', 'Week', 'Month', 'Year']
        }
    ]
    data_streams_dict = {d['ID'][0]: d for d in data_streams}
    return data_streams_dict

def creat_csv_for_data_stream(data_streams,csv_file_path):
    all_dfs = []
    number_of_ds = len(data_streams)
    # Loop through each data stream
    for id_key, data in data_streams.items():
        #lengths = [len(v) for v in data.values()]
        max_length = max(len(v) for v in data.values())  # Find the maximum length of lists in the data
        for key, value in data.items():
            # Calculate how many empty values need to be added
            insert = max_length - len(value)
            # Use None or an appropriate placeholder such as an empty string or '_'
            empty_values = [None] * insert  # Create a list of Nones or any other placeholder
            # Concatenate the original list with the list of placeholders
            data[key] = value + empty_values

        # Create a DataFrame
        df = pd.DataFrame(data)
        # Append the DataFrame to the list
        all_dfs.append(df)

        ## Add two rows of empty values between DataFrames
        #all_dfs.append(pd.DataFrame([[None] * len(df.columns)] * 2, columns=df.columns))
    # Save the concatenated DataFrame to a CSV file
    for ds_number in range(number_of_ds):
        df = all_dfs[ds_number]
        # Save the DataFrame to CSV
        if ds_number == 0:
            # If it's the first DataFrame, write to CSV without appending
            df.to_csv(csv_file_path, index=False)
        else:
            # If it's not the first DataFrame, append to CSV
            df.to_csv(csv_file_path, mode='a', index=False)

        # Add two rows of empty values between DataFrames
        with open(csv_file_path, 'a') as file:
            file.write('\n\n')

def main():
    data_streams = creat_data_stream()
    temp = copy.deepcopy(data_streams)
    creat_csv_for_data_stream(temp,csv_file_path)
    print('DONE data_streams')

#main()

