FROM python:2.7
COPY . /src
CMD ["python", "/src/gspread-test.py"]
