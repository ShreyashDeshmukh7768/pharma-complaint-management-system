from app.ai.extractor import extract_complaint_information

sample_text = """
Customer Name: John Doe
Customer Email: john@example.com
Company: ABC Pharma

Product Name: Paracetamol 500mg
Batch Number: BATCH001

Manufacturing Date: 2026-01-01
Expiry Date: 2028-01-01

Complaint:
Several tablets were broken inside the strip.

Received Date: 2026-07-27
"""

response = extract_complaint_information(sample_text)

print(response)