FROM datasharing/base

COPY preprocessed_dataFile_A.csv preprocessed_dataFile_A.csv 
COPY communication_A1.py communication_A1.py
COPY input_shared.json input_shared.json
COPY input_internal.json input_internal.json

CMD ["python", "communication_A1.py"]