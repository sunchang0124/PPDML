FROM python:3.7

RUN pip install requests pandas numpy
RUN touch /input.txt
RUN touch /output.txt

COPY run.py /run.py

CMD ["python", "run.py"]