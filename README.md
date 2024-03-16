# Take a picture of receipts and use data in receipts to track spending
## Steps:
1. Take a picture of the receipt and upload to some cloud tool
2. Create pipeline to read data from receipt and store in data warehouse
3. Create report to track spending by category

## To train a text extracting model:
1. Label receipts with a unique id number
2. Take picture and store in G drive
3. Enter receipt information (price, business, date) in a G drive sheet
4. Use Python to associate data from g sheet with an image
5. Train on associated data

## Tools:
- python
- orchestrator like Prefect
- camera
- cloud storage
- image to text library
- data warehouse
- dbt for modelling
- terraform for infra
- docker for containers
- VM or local machine for execution
- reporting tool like Looker or even a custom build in Python for HTML