# Specifies base image
FROM python:3.11.6-slim-bookworm
# Install nmap and traceroute
RUN apt-get update && \
    apt-get install -y nmap mtr
# Set working directory inside container to /app (subsequent commands are executed here)
WORKDIR /app
# Copies requirements.txt file from host system into current directory (./) in the image
COPY ./requirements.txt /app/requirements.txt
# Upgrades pip if needed
RUN /usr/local/bin/python3 -m pip install --upgrade pip
# Installs packages from requirements.txt
RUN pip3 install -r requirements.txt
# Clean APT cache and remove lists
RUN apt-get clean && \
    rm -rf /var/lib/apt/lists/*
# Informs docker that container will listen on this port, and makes it accessible outside container
EXPOSE 8501
# Copies all files and directories from the host machine's current directory to the /app for the image
COPY . /app
# This tells Docker to execute 'streamlit run' which starts the Streamlit server
ENTRYPOINT ["streamlit", "run"]
# Specifies default command to be executed when the container starts
CMD ["Home.py"]