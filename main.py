#import OpenAI Library and Authenticate with OpenAI Key
import openai
import subprocess
openai.api_key="OPEN_AI_KEY"
#define System Role
system_role="Extract entities and thier values as a key-value pair from the provided OCR text and seperate them by a new line."
system_role="Extract entities and values as a key-value pair from the text provided"

example_text="Invoicing Street Address Template.com City , ST ZIP Code BILL TO Name Address City , State ZIP Country Phone Email pp1 pp2 Pp3 P.O. # # / Taxable NOTES : Your Company Name looooo0000 ロ Phone Number , Web Address , etc. Sales Rep . Name Ship Date Description test item 1 for online invoicing test item 2 for onvoice invoicing template This template connects to an online SQL Server SHIP TO Name Address City , State ZIP Country Contact Ship Via Quantity 1 2 3 PST GST INVOICE THANK YOU FOR YOUR BUSINESS ! DATE : INVOICE # : Client # Terms Unit Price 3.00 4.00 5.50 SUBTOTAL 8.000 % 6.000 % SHIPPING & HANDLING TOTAL PAID TOTAL DUE Due Date Line Total 3.00 8.00 16.50 27.50 27.50 27.50"

example_entities="""
Company Name: Your Company Name 
Phone Number: looooo0000 
Web Address: Template.com 
Ship To Name: 
Address: 
City: 
State: 
Zip Code: 
Country: 
Contact:  
Quantity: 1 
Quantity: 2 
Quantity: 3  
Unit Price: 3.00 
Unit Price: 4.00 
Unit Price: 5.50 
Subtotal: 8.00 
Taxable: 
Line Total: 3.00 
Subtotal: 8.00 
Shipping & Handling: 6.00 
Total Paid: 27.50
Total Due: 27.50"""
process = subprocess.Popen(["python", "text.py"], stdout=subprocess.PIPE, universal_newlines=True)
ocr_generated_text = process.stdout.read()
#Get The Response
response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    messages=[
        {"role": "system", "content": system_role},
        {"role": "user", "content": example_text},
        {"role": "assistant", "content": example_entities},
        {"role": "user", "content": ocr_generated_text}
    ],
    temperature=0.2  # Adjust the temperature value as desired
)

#extracting content from the response object.
extracted_entities=response["choices"][0]["message"]["content"]
improved_output = ""
for line in extracted_entities.split("\n"):
    key_value = line.split(":", 1)
    if len(key_value) == 2:
        key, value = key_value
        improved_output += f"{key.strip()}: {value.strip()}\n"
    else:
        # Handling missing values or malformed lines
        improved_output += f"{line.strip()}\n"

print(improved_output)
