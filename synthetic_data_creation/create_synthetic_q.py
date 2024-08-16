import pandas as pd

csv_file_path = r'C:\Users\User\Dropbox\study\Ydata\C0_projects\Data\synthetic_data\synthetic_queries.csv'

# Define the queries
def creat_queries():

    queries = [
        {'idx':0 , 'Query': 'Monitor for a significant increase in transaction amounts from tourists making online payments.', 'ID': 'CalDemo', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Is_tourist', 'Request_type'], 'Measure': 'Transactions_request_Amount'},
        {'idx':1 , 'Query': 'Alert for sharp declines in transaction counts for contactless payments in the tech segment.', 'ID': 'CalDemo', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Segment', 'Request_type'], 'Measure': 'Transaction_Request_Count'},
        {'idx':2 , 'Query': 'Monitor for unexpected spikes in declined transactions through Visa in the gardening segment.', 'ID': 'CalDemo', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Segment', 'Payment_Method', 'Status'], 'Measure': 'Transaction_Request_Count'},
        {'idx':3 , 'Query': 'Alert for a significant drop in transaction amounts from non-tourists using MasterCard in fashion.', 'ID': 'CalDemo', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Is_tourist', 'Segment', 'Payment_Method'], 'Measure': 'Transactions_request_Amount'},
        {'idx':4 , 'Query': 'Monitor sharp increases in approved transactions from Shva in the travel segment.', 'ID': 'CalDemo', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Source', 'Segment', 'Status'], 'Measure': 'Transaction_Request_Count'},
        {'idx':5 , 'Query': 'Alert if there is no transaction data for cash withdrawals by tourists using Diners.', 'ID': 'CalDemo', 'Alert_Type': 'no data', 'Direction': 'both', 'Dimensions': ['Is_tourist', 'Request_type', 'Payment_Method'], 'Measure': 'Transaction_Request_Count'},
        {'idx':6 , 'Query': 'Monitor for consistent transaction counts from Bank sources across all segments, indicating static behavior.', 'ID': 'CalDemo', 'Alert_Type': 'static', 'Direction': 'both', 'Dimensions': ['Source'], 'Measure': 'Transaction_Request_Count'},
        {'idx':7 , 'Query': 'Alert for unusual increases in transaction amounts via contactless payments from non-tourists in the fashion segment.', 'ID': 'CalDemo', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Is_tourist', 'Segment', 'Request_type'], 'Measure': 'Transactions_request_Amount'},
        {'idx':8 , 'Query': 'Monitor a sudden drop in approved transaction counts through Visa in the gardening segment.', 'ID': 'CalDemo', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Segment', 'Payment_Method', 'Status'], 'Measure': 'Transaction_Request_Count'},
        {'idx':9 , 'Query': 'Alert for spikes in declined transactions through MasterCard in the travel segment, potentially indicating security issues.', 'ID': 'CalDemo', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Segment', 'Payment_Method', 'Status'], 'Measure': 'Transaction_Request_Count'},

        {'idx':10 , 'Query': 'Monitor significant decrease in customer satisfaction scores for VIP customers via phone.', 'ID': 'CustomerSupport', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Customer_Segment', 'Contact_Channel'], 'Measure': 'Customer_Satisfaction_Score'},
        {'idx':11 , 'Query': 'Alert for sudden increases in response rates through email communications.', 'ID': 'CustomerSupport', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Contact_Channel'], 'Measure': 'Response_Rate'},
        {'idx':12 , 'Query': 'Alert if response rates for VIP customers suddenly drop significantly.', 'ID': 'CustomerSupport', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Customer_Segment'], 'Measure': 'Response_Rate'},
        {'idx':13 , 'Query': 'Monitor for significant increases in customer satisfaction when handled by specific agents.', 'ID': 'CustomerSupport', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Agent_ID'], 'Measure': 'Customer_Satisfaction_Score'},
        {'idx':14 , 'Query': 'Alert if customer satisfaction scores drop when specific issues are resolved by certain agents.', 'ID': 'CustomerSupport', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Agent_ID', 'Issue_Resolved'], 'Measure': 'Customer_Satisfaction_Score'},
        {'idx':15 , 'Query': 'Monitor for sharp increase in response rates when issues are resolved via social media.', 'ID': 'CustomerSupport', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Contact_Channel', 'Issue_Resolved'], 'Measure': 'Response_Rate'},
        {'idx':16 , 'Query': 'Alert for unexpected spikes in customer satisfaction from regular customers using chat.', 'ID': 'CustomerSupport', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Customer_Segment', 'Contact_Channel'], 'Measure': 'Customer_Satisfaction_Score'},
        {'idx':17 , 'Query': 'Monitor drop in response rates during peak times indicating potential system overload.', 'ID': 'CustomerSupport', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Peak_Hours'], 'Measure': 'Response_Rate'},
        {'idx':18 , 'Query': 'Alert for no data on customer satisfaction scores for first-time customers handled by specific agents.', 'ID': 'CustomerSupport', 'Alert_Type': 'no data', 'Direction': 'both', 'Dimensions': ['Customer_Segment', 'Agent_ID'], 'Measure': 'Customer_Satisfaction_Score'},
        {'idx':19 , 'Query': 'Monitor if issue resolution does not alter the customer satisfaction score, suggesting ineffective resolutions.', 'ID': 'CustomerSupport', 'Alert_Type': 'static', 'Direction': 'both', 'Dimensions': ['Issue_Resolved'], 'Measure': 'Customer_Satisfaction_Score'},

        {'idx':20 , 'Query': 'Monitor spikes in daily sales volume of groceries during the summer.', 'ID': 'grocery', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Product_Category', 'Season'], 'Measure': 'Daily_Sales_Volume'},
        {'idx':21 , 'Query': 'Monitor a decrease in inventory turnover in Northern stores, suggesting decreased efficiency.', 'ID': 'grocery', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Store_Location'], 'Measure': 'Inventory_Turnover_Rate'},
        {'idx':22 , 'Query': 'Monitor a rise in inventory turnover during the autumn season across all categories.', 'ID': 'grocery', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Season'], 'Measure': 'Inventory_Turnover_Rate'},
        {'idx':23 , 'Query': 'Alert for unexpected decreases in daily sales volume of clothing during spring.', 'ID': 'grocery', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Product_Category', 'Season'], 'Measure': 'Daily_Sales_Volume'},
        {'idx':24 , 'Query': 'Monitor significant fluctuations in sales volume for home goods during promotional periods.', 'ID': 'grocery', 'Alert_Type': 'anomaly', 'Direction': 'both', 'Dimensions': ['Product_Category', 'Promotion_Applied'], 'Measure': 'Daily_Sales_Volume'},
        {'idx':25 , 'Query': 'Alert for sharp increases in inventory turnover rates at stores in the West, potentially indicating effective promotions.', 'ID': 'grocery', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Store_Location', 'Promotion_Applied'], 'Measure': 'Inventory_Turnover_Rate'},
        {'idx':26 , 'Query': 'Alert for no sales data on electronics during winter, indicating potential supply issues.', 'ID': 'grocery', 'Alert_Type': 'no data', 'Direction': 'both', 'Dimensions': ['Product_Category', 'Season'], 'Measure': 'Daily_Sales_Volume'},
        {'idx':27 , 'Query': 'Alert if daily sales volume for groceries does not fluctuate with seasonal changes, indicating ineffective market strategies.', 'ID': 'grocery', 'Alert_Type': 'static', 'Direction': 'both', 'Dimensions': ['Product_Category', 'Season'], 'Measure': 'Daily_Sales_Volume'},
        {'idx':28 , 'Query': 'Monitor unexpected dips in daily sales of electronics in Eastern stores, suggesting distribution issues.', 'ID': 'grocery', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Product_Category', 'Store_Location'], 'Measure': 'Daily_Sales_Volume'},
        {'idx':29 , 'Query': 'Alert for significant increases in sales during non-promotional periods for clothing, suggesting unexpected consumer interest.', 'ID': 'grocery', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Product_Category', 'Promotion_Applied'], 'Measure': 'Daily_Sales_Volume'},

        {'idx':30 , 'Query': 'Monitor significant increases in average handling time for billing issues.', 'ID': 'CustomerService', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Service_Type', 'Operator_ID'], 'Measure': 'Average_Handling_Time'},
        {'idx':31 , 'Query': 'Alert for a sharp rise in first call resolution during evening shifts.', 'ID': 'CustomerService', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Peak_Hours'], 'Measure': 'First_Call_Resolution'},
        {'idx':32 , 'Query': 'Alert if theres a notable decrease in average handling time for customer inquiries.', 'ID': 'CustomerService', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Service_Type'], 'Measure': 'Average_Handling_Time'},
        {'idx':33 , 'Query': 'Monitor for significant drops in first call resolutions for technical support queries.', 'ID': 'CustomerService', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Service_Type'], 'Measure': 'First_Call_Resolution'},
        {'idx':34 , 'Query': 'Alert for unexpected spikes in handling times during peak hours by specific operators.', 'ID': 'CustomerService', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Peak_Hours', 'Operator_ID'], 'Measure': 'Average_Handling_Time'},
        {'idx':35 , 'Query': 'Monitor average handling time consistency for account updates, suggesting efficient training.', 'ID': 'CustomerService', 'Alert_Type': 'static', 'Direction': 'both', 'Dimensions': ['Service_Type'], 'Measure': 'Average_Handling_Time'},
        {'idx':36 , 'Query': 'Alert for no data on first call resolution for billing issues handled by new operators.', 'ID': 'CustomerService', 'Alert_Type': 'no data', 'Direction': 'both', 'Dimensions': ['Service_Type', 'Operator_ID'], 'Measure': 'First_Call_Resolution'},
        {'idx':37 , 'Query': 'Monitor for drops in average handling time after implementing new CRM software.', 'ID': 'CustomerService', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Technology'], 'Measure': 'Average_Handling_Time'},
        {'idx':38 , 'Query': 'Alert for spikes in first call resolution for personal customer types, indicating improved service.', 'ID': 'CustomerService', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Customer_Type'], 'Measure': 'First_Call_Resolution'},
        {'idx':39 , 'Query': 'Monitor if technical support issues see an increase in resolution speed during morning hours.', 'ID': 'CustomerService', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Service_Type', 'Peak_Hours'], 'Measure': 'First_Call_Resolution'},

        {'idx':40 , 'Query': 'Monitor spikes in revenue from online electronics sales in the East region.', 'ID': 'SalesData', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Product_Type', 'Region', 'Channel'], 'Measure': 'Revenue'},
        {'idx':41 , 'Query': 'Alert for sudden drops in units sold for apparel in retail stores in the South.', 'ID': 'SalesData', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Product_Type', 'Region', 'Channel'], 'Measure': 'Units_Sold'},
        {'idx':42 , 'Query': 'Monitor profit margins for furniture sales, looking for significant anomalies in the West.', 'ID': 'SalesData', 'Alert_Type': 'anomaly', 'Direction': 'both', 'Dimensions': ['Product_Type', 'Region'], 'Measure': 'Profit'},
        {'idx':43 , 'Query': 'Alert for no change in revenue from food products sold online, suggesting market saturation.', 'ID': 'SalesData', 'Alert_Type': 'static', 'Direction': 'both', 'Dimensions': ['Product_Type', 'Channel'], 'Measure': 'Revenue'},
        {'idx':44 , 'Query': 'Alert for no data on profit for new electronics product lines in northern regions.', 'ID': 'SalesData', 'Alert_Type': 'no data', 'Direction': 'both', 'Dimensions': ['Product_Type', 'Region'], 'Measure': 'Profit'},
        {'idx':45 , 'Query': 'Monitor unexpected increases in units sold for apparel during non-promotional periods.', 'ID': 'SalesData', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Product_Type', 'Channel'], 'Measure': 'Units_Sold'},
        {'idx':46 , 'Query': 'Alert for significant dips in revenue during expected high-sales periods for furniture.', 'ID': 'SalesData', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Product_Type', 'Season'], 'Measure': 'Revenue'},
        {'idx':47 , 'Query': 'Monitor unexpected rises in profit from retail food sales in eastern regions.', 'ID': 'SalesData', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Product_Type', 'Region', 'Channel'], 'Measure': 'Profit'},
        {'idx':48 , 'Query': 'Monitor consistent sales figures for electronics across all channels, indicating stable demand.', 'ID': 'SalesData', 'Alert_Type': 'static', 'Direction': 'both', 'Dimensions': ['Product_Type', 'Channel'], 'Measure': 'Units_Sold'},
        {'idx':49 , 'Query': 'Alert for sharp increases in units sold for furniture in the commercial channel, indicating a successful marketing campaign.', 'ID': 'SalesData', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Product_Type', 'Channel'], 'Measure': 'Units_Sold'},

        {'idx':50 , 'Query': 'Monitor sales target achievement anomalies among managers in the Sales department.', 'ID': 'EmployeePerformance', 'Alert_Type': 'anomaly', 'Direction': 'both', 'Dimensions': ['Department', 'Position'], 'Measure': 'Sales_Target_Achieved'},
        {'idx':51 , 'Query': 'Alert for sudden drops in customer satisfaction scores among HR executives.', 'ID': 'EmployeePerformance', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Department', 'Position'], 'Measure': 'Customer_Satisfaction_Score'},
        {'idx':52 , 'Query': 'Monitor absenteeism rates in the Finance department for trends indicating employee dissatisfaction.', 'ID': 'EmployeePerformance', 'Alert_Type': 'anomaly', 'Direction': 'both', 'Dimensions': ['Department'], 'Measure': 'Absenteeism_Rate'},
        {'idx':53 , 'Query': 'Alert for consistent customer satisfaction scores in Marketing, suggesting effective training.', 'ID': 'EmployeePerformance', 'Alert_Type': 'static', 'Direction': 'both', 'Dimensions': ['Department'], 'Measure': 'Customer_Satisfaction_Score'},
        {'idx':54 , 'Query': 'Alert for no data on sales target achievement for newly promoted supervisors in Sales.', 'ID': 'EmployeePerformance', 'Alert_Type': 'no data', 'Direction': 'both', 'Dimensions': ['Department', 'Position'], 'Measure': 'Sales_Target_Achieved'},
        {'idx':55 , 'Query': 'Monitor for significant increases in customer satisfaction scores for associates with over 10 years of tenure.', 'ID': 'EmployeePerformance', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Tenure', 'Position'], 'Measure': 'Customer_Satisfaction_Score'},
        {'idx':56 , 'Query': 'Alert for sharp decreases in absenteeism rates following a change in HR policies.', 'ID': 'EmployeePerformance', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Department'], 'Measure': 'Absenteeism_Rate'},
        {'idx':57 , 'Query': 'Monitor sudden increases in sales target achievements during high-sales seasons by Marketing managers.', 'ID': 'EmployeePerformance', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Department', 'Season'], 'Measure': 'Sales_Target_Achieved'},
        {'idx':58 , 'Query': 'Alert for unexpected spikes in absenteeism rates among new hires in Finance.', 'ID': 'EmployeePerformance', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Department', 'Tenure'], 'Measure': 'Absenteeism_Rate'},
        {'idx':59 , 'Query': 'Monitor consistent high performance in sales target achievement across all departments.', 'ID': 'EmployeePerformance', 'Alert_Type': 'static', 'Direction': 'both', 'Dimensions': ['Department'], 'Measure': 'Sales_Target_Achieved'},

        {'idx':60 , 'Query': 'Monitor for unexpected spikes in page views on product pages via social media referrals.', 'ID': 'WebsiteTraffic', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Page_Type', 'Traffic_Source'], 'Measure': 'Page_Views'},
        {'idx':61 , 'Query': 'Alert for significant drops in unique visitors from direct traffic to the homepage.', 'ID': 'WebsiteTraffic', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Page_Type', 'Traffic_Source'], 'Measure': 'Unique_Visitors'},
        {'idx':62 , 'Query': 'Monitor bounce rates for blogs sourced from organic search to identify engagement issues.', 'ID': 'WebsiteTraffic', 'Alert_Type': 'anomaly', 'Direction': 'both', 'Dimensions': ['Page_Type', 'Traffic_Source'], 'Measure': 'Bounce_Rate'},
        {'idx':63 , 'Query': 'Alert for no data on page views from referral traffic to the contact page, indicating potential tracking issues.', 'ID': 'WebsiteTraffic', 'Alert_Type': 'no data', 'Direction': 'both', 'Dimensions': ['Page_Type', 'Traffic_Source'], 'Measure': 'Page_Views'},
        {'idx':64 , 'Query': 'Monitor consistent traffic patterns on mobile devices, suggesting steady user engagement.', 'ID': 'WebsiteTraffic', 'Alert_Type': 'static', 'Direction': 'both', 'Dimensions': ['Device_Type'], 'Measure': 'Unique_Visitors'},
        {'idx':65 , 'Query': 'Alert for spikes in bounce rates during promotional campaigns on product pages.', 'ID': 'WebsiteTraffic', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Page_Type', 'Season'], 'Measure': 'Bounce_Rate'},
        {'idx':66 , 'Query': 'Monitor for drops in unique visitors to blog pages during seasonal events.', 'ID': 'WebsiteTraffic', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Page_Type', 'Season'], 'Measure': 'Unique_Visitors'},
        {'idx':67 , 'Query': 'Alert for sudden increases in page views on product pages from tablet devices.', 'ID': 'WebsiteTraffic', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Page_Type', 'Device_Type'], 'Measure': 'Page_Views'},
        {'idx':68 , 'Query': 'Monitor for unexpected decreases in traffic from social media to blog pages.', 'ID': 'WebsiteTraffic', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Page_Type', 'Traffic_Source'], 'Measure': 'Unique_Visitors'},
        {'idx':69 , 'Query': 'Alert for a sharp rise in page views during non-peak hours, suggesting effective off-peak promotions.', 'ID': 'WebsiteTraffic', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Peak_Hours'], 'Measure': 'Page_Views'},

        {'idx':70 , 'Query': 'Monitor inventory levels for electronics from Amazon to prevent overstocking.', 'ID': 'SupplyChain', 'Alert_Type': 'anomaly', 'Direction': 'both', 'Dimensions': ['Product_Category', 'Supplier'], 'Measure': 'Inventory_Level'},
        {'idx':71 , 'Query': 'Alert for critical lows in inventory levels of apparel at Warehouse2, indicating potential supply issues.', 'ID': 'SupplyChain', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Product_Category', 'Warehouse'], 'Measure': 'Inventory_Level'},
        {'idx':72 , 'Query': 'Monitor order fulfillment times for furniture from Walmart to ensure supplier performance.', 'ID': 'SupplyChain', 'Alert_Type': 'anomaly', 'Direction': 'both', 'Dimensions': ['Product_Category', 'Supplier'], 'Measure': 'Order_Fulfillment_Time'},
        {'idx':73 , 'Query': 'Alert for no data on supplier performance for toys from Target, indicating potential reporting issues.', 'ID': 'SupplyChain', 'Alert_Type': 'no data', 'Direction': 'both', 'Dimensions': ['Product_Category', 'Supplier'], 'Measure': 'Supplier_Performance'},
        {'idx':74 , 'Query': 'Monitor consistent inventory levels for electronics, suggesting effective restocking processes.', 'ID': 'SupplyChain', 'Alert_Type': 'static', 'Direction': 'both', 'Dimensions': ['Product_Category'], 'Measure': 'Inventory_Level'},
        {'idx':75 , 'Query': 'Alert for sudden increases in order fulfillment times for electronics from BestBuy.', 'ID': 'SupplyChain', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Product_Category', 'Supplier'], 'Measure': 'Order_Fulfillment_Time'},
        {'idx':76 , 'Query': 'Monitor drops in supplier performance ratings for apparel, indicating issues with Walmart.', 'ID': 'SupplyChain', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Product_Category', 'Supplier'], 'Measure': 'Supplier_Performance'},
        {'idx':77 , 'Query': 'Alert for unexpected highs in inventory levels of toys during the holiday season.', 'ID': 'SupplyChain', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Product_Category', 'Season'], 'Measure': 'Inventory_Level'},
        {'idx':78 , 'Query': 'Monitor for sharp drops in order fulfillment times for furniture items in all warehouses.', 'ID': 'SupplyChain', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Product_Category', 'Warehouse'], 'Measure': 'Order_Fulfillment_Time'},
        {'idx':79 , 'Query': 'Alert for spikes in inventory levels of furniture post-holiday season, suggesting unsold stock.', 'ID': 'SupplyChain', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Product_Category', 'Season'], 'Measure': 'Inventory_Level'},

        {'idx':80 , 'Query': 'Monitor unexpected rises in blood pressure in the 30-50 age group.', 'ID': 'HealthMetrics', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Age_Group'], 'Measure': 'Blood_Pressure'},
        {'idx':81 , 'Query': 'Alert for significant drops in heart rate among individuals over 70, indicating potential health risks.', 'ID': 'HealthMetrics', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Age_Group'], 'Measure': 'Heart_Rate'},
        {'idx':82 , 'Query': 'Monitor for changes in BMI that could indicate health issues in the male population.', 'ID': 'HealthMetrics', 'Alert_Type': 'anomaly', 'Direction': 'both', 'Dimensions': ['Gender'], 'Measure': 'BMI'},
        {'idx':83 , 'Query': 'Alert for no changes in blood sugar levels among prehypertensive patients, suggesting ineffective treatments.', 'ID': 'HealthMetrics', 'Alert_Type': 'static', 'Direction': 'both', 'Dimensions': ['Health_Status'], 'Measure': 'Blood_Sugar'},
        {'idx':84 , 'Query': 'Alert for no data on heart rate for females in the under-30 group, indicating missing health screenings.', 'ID': 'HealthMetrics', 'Alert_Type': 'no data', 'Direction': 'both', 'Dimensions': ['Age_Group', 'Gender'], 'Measure': 'Heart_Rate'},
        {'idx':85 , 'Query': 'Monitor sudden increases in BMI among the elderly, suggesting potential health concerns.', 'ID': 'HealthMetrics', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Age_Group'], 'Measure': 'BMI'},
        {'idx':86 , 'Query': 'Alert for drops in blood pressure among hypertensive patients, indicating effective medication.', 'ID': 'HealthMetrics', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Health_Status'], 'Measure': 'Blood_Pressure'},
        {'idx':87 , 'Query': 'Monitor sharp rises in blood sugar levels in the 50-70 age group during winter.', 'ID': 'HealthMetrics', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Age_Group', 'Season'], 'Measure': 'Blood_Sugar'},
        {'idx':88 , 'Query': 'Alert for increases in heart rate that could signify stress or potential health issues in females.', 'ID': 'HealthMetrics', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Gender'], 'Measure': 'Heart_Rate'},
        {'idx':89 , 'Query': 'Monitor for consistent blood pressure levels in healthy individuals, suggesting effective health management.', 'ID': 'HealthMetrics', 'Alert_Type': 'static', 'Direction': 'both', 'Dimensions': ['Health_Status'], 'Measure': 'Blood_Pressure'},

        {'idx':90 , 'Query': 'Monitor for spikes in electricity consumption in commercial buildings during peak hours.', 'ID': 'EnergyConsumption', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Building_Type', 'Usage_Type', 'Time_Period'], 'Measure': 'Electricity_Consumption'},
        {'idx':91 , 'Query': 'Alert for unexpected drops in gas consumption in industrial buildings, suggesting operational issues.', 'ID': 'EnergyConsumption', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Building_Type', 'Usage_Type'], 'Measure': 'Gas_Consumption'},
        {'idx':92 , 'Query': 'Monitor water consumption in residential buildings during the summer to manage resource use effectively.', 'ID': 'EnergyConsumption', 'Alert_Type': 'anomaly', 'Direction': 'both', 'Dimensions': ['Building_Type', 'Season'], 'Measure': 'Water_Consumption'},
        {'idx':93 , 'Query': 'Alert for no data on gas consumption during the winter in commercial buildings, indicating metering issues.', 'ID': 'EnergyConsumption', 'Alert_Type': 'no data', 'Direction': 'both', 'Dimensions': ['Building_Type', 'Season'], 'Measure': 'Gas_Consumption'},
        {'idx':94 , 'Query': 'Monitor consistent electricity usage in residential areas during the night, suggesting energy efficiency.', 'ID': 'EnergyConsumption', 'Alert_Type': 'static', 'Direction': 'both', 'Dimensions': ['Building_Type', 'Time_Period'], 'Measure': 'Electricity_Consumption'},
        {'idx':95 , 'Query': 'Alert for significant increases in water consumption in commercial buildings during non-peak times, possibly indicating leaks.', 'ID': 'EnergyConsumption', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Building_Type', 'Time_Period'], 'Measure': 'Water_Consumption'},
        {'idx':96 , 'Query': 'Monitor decreases in electricity consumption in industrial buildings, potentially indicating less production activity.', 'ID': 'EnergyConsumption', 'Alert_Type': 'anomaly', 'Direction': 'down', 'Dimensions': ['Building_Type', 'Usage_Type'], 'Measure': 'Electricity_Consumption'},
        {'idx':97 , 'Query': 'Alert for unexpected increases in gas consumption during non-heating periods in residential buildings.', 'ID': 'EnergyConsumption', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Building_Type', 'Usage_Type', 'Season'], 'Measure': 'Gas_Consumption'},
        {'idx':98 , 'Query': 'Monitor for sudden rises in water consumption in industrial settings, which could suggest inefficiencies or leaks.', 'ID': 'EnergyConsumption', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Building_Type', 'Usage_Type'], 'Measure': 'Water_Consumption'},
        {'idx':99, 'Query': 'Alert for spikes in electricity usage in commercial settings during weekends, potentially due to unauthorized use.', 'ID': 'EnergyConsumption', 'Alert_Type': 'anomaly', 'Direction': 'up', 'Dimensions': ['Building_Type', 'Time_Period'], 'Measure': 'Electricity_Consumption'},
    ]
    return queries

def creat_csv_for_queries(csv_file_path):
    queries = creat_queries()
    # Convert the queries to a DataFrame
    queries_df = pd.DataFrame(queries)

    # Save the DataFrame to CSV
    queries_df.to_csv(csv_file_path, index=False)
    print('DONE')

#creat_csv_for_queries(csv_file_path)

if 0:
    # this is the chat GPT prompt for futer use
    data_stream_example = """ID: 'CalDemo'
Measures: ['Transactions_request_Amount', 'Transaction_Request_Count']
Dimensions: ['Segment', 'Source', 'Is_tourist', 'Status', 'Request_type', 'Payment_Method', 'Slack_mapping']
Segment: ['Fashion', 'Gardening', 'Travel', 'Tech']
Source: ['Bank', 'Mastercard', 'Shva', 'Visa']
Is_tourist: [True, False]
Status: ['Approved', 'Declined']
Request_type: ['Frontal', 'Online', 'Cash_withdraw', 'Contactless']
Payment_Method: ['American', 'Visa', 'MasterCard', 'Diners', 'Trustly']"""

    system_promt = """Start with a dataset like data_stream_example with the following structure: Define alert queries according to the following specifications:
Each query should have an Query, ID, an Alert_Type, a Direction, Dimensions, and a Measure.
The Alert_Type can only be one of the following: 'anomaly', 'static', or 'no data'.
Each query should be associated with one of the provided measures from the dataset.
Each query should be associated with one or more of the provided dimensions from the dataset.
The Direction can be 'down', 'up', or 'both', indicating the direction of the anomaly.
Ensure to provide specific values for each query based on your requirements.
#in need 10 queries and they should includes : 8 anomalies 1 no data and 1 static
in need 2 queries and they should all be Alert_Type= 'static'
note: static means that the Measure craose some static pre-definde threshold
Optionally, provide a descriptive query statement for each alert query to clarify its purpose i need 10 queries."""

    queries_examples = """queries = [
    {
        'Query': 'Alert me when there is a decrease in transactions below 1000, focusing on their transaction request type and payment source together.',
        'ID': 'CalDemo',
        'Alert_Type': 'static',
        'Direction': 'down',
        'Dimensions': ['Request_type', 'Payment_Method'],
        'Measure': 'Transaction_Request_Count'
    }
    queries_examples = """queries = [
    {
        'Query': 'Alert me when there is a noticeable decrease in transactions, focusing on their transaction request type and payment source together.',
        'ID': 'CalDemo',
        'Alert_Type': 'anomaly',
        'Direction': 'down',
        'Dimensions': ['Request_type', 'Payment_Method'],
        'Measure': 'Transaction_Request_Count'
    }
    ]
    """


