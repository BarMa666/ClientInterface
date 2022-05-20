FROM python:3.10
WORKDIR /usr/src/dashboard_creator
COPY . .
RUN /usr/local/bin/python -m pip install --upgrade pip
RUN pip install -r requirements.txt

CMD ["python", "dashboard_creator.py", "--template_path=templates/template.json", "--cfg_path=configs/config.ini"]