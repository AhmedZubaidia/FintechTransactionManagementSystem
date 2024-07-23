FROM  python:3.9

WORKDIR /fintechTransactionMangmentSystem

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY . ./fintechTransactionMangmentSystem

CMD ["python", "fintechTransactionMangmentSystem/run.py"]

