FROM datasharing/base

COPY preprocessed_dataFile_B.csv preprocessed_dataFile_B.csv 
COPY final_B.py final_B.py
COPY input_shared.json input_shared.json
COPY input_internal.json input_internal.json

CMD ["python", "final_B.py"]