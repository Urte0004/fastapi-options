FROM python:3

WORKDIR /Users/murphy/option_pricing_senexp

COPY requirementsr.txt ./
RUN pip install --no-cache-dir -r requirementsr.txt

COPY . .
CMD ["main.py"]

