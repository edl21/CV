FROM blang/latex:ctanfull

# Install Python and pip
RUN apt-get update && apt-get install -y python3 python3-pip

# Install Jinja2
RUN pip3 install jinja2

WORKDIR /data