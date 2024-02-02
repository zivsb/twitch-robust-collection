# Use Ubuntu 18.04 as the base image
FROM ubuntu:18.04

# Update the package list and install necessary dependencies
RUN apt-get update && apt-get install -y \
    protobuf-compiler \
    libprotobuf-dev \
    autotools-dev \
    dh-autoreconf \
    iptables \
    pkg-config \
    dnsmasq-base \
    apache2-bin \
    debhelper \
    libssl-dev \
    ssl-cert \
    libxcb-present-dev \
    libcairo2-dev \
    libpango1.0-dev \
    git \
    iproute2 \
    apache2-dev \
    iputils-ping \
    python3 \
    python3-pip \
    wget \
    curl \
    unzip \ 
    ssh \
    tcpdump \
    sudo

# Set capabilities on tcpdump to allow packet capture without root privileges
RUN setcap 'CAP_NET_RAW+eip CAP_NET_ADMIN+eip' /usr/sbin/tcpdump

# Install Google Chrome
RUN wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
RUN apt install -y ./google-chrome-stable_current_amd64.deb

# Install Chrome WebDriver and set permissions
RUN mkdir -p /opt/chromedriver && \
    curl -sS -o /tmp/chromedriver_linux64.zip https://edgedl.me.gvt1.com/edgedl/chrome/chrome-for-testing/120.0.6099.109/linux64/chromedriver-linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver && \
    chmod -R +x /opt/chromedriver/chromedriver-linux64  && \
    ls /opt/chromedriver/chromedriver-linux64/chromedriver && \
    mv /opt/chromedriver/chromedriver-linux64/chromedriver /usr/local/bin/ && \
    rm /tmp/chromedriver_linux64.zip

# Install Selenium
RUN pip3 install selenium

# Clone Mahi-Mahi
RUN git clone https://github.com/ravinet/mahimahi

# Install Mahi-Mahi
WORKDIR /mahimahi
RUN ./autogen.sh && \
    ./configure && \
    make && \
    make install

# Create a non-root user
RUN useradd -m nonrootuser

# Switch back to root to change permissions of the script
USER root

# Copy and make the bash script executable
COPY ./run_script.sh /home/nonrootuser/twitch_stat_collector/run_script.sh
RUN chmod +x /home/nonrootuser/twitch_stat_collector/run_script.sh

# Change the ownership of the /home/nonrootuser/twitch_stat_collector directory
RUN chown -R nonrootuser:nonrootuser /home/nonrootuser/twitch_stat_collector

# Switch to nonrootuser
USER nonrootuser
WORKDIR /home/nonrootuser

RUN mkdir twitch_stat_collector/browser_scripts

# Add files
COPY ./script.py /home/nonrootuser/twitch_stat_collector
COPY ./ookla_test.py /home/nonrootuser/twitch_stat_collector
COPY ./get_url.py /home/nonrootuser/twitch_stat_collector
COPY ./browser_scripts/twitch_analyze.js /home/nonrootuser/twitch_stat_collector/browser_scripts
COPY ./10Mbps_trace /home/nonrootuser/twitch_stat_collector
COPY ./1Mbps_trace /home/nonrootuser/twitch_stat_collector
COPY ./5Mbps_trace /home/nonrootuser/twitch_stat_collector
COPY ./3Mbps_trace /home/nonrootuser/twitch_stat_collector
COPY ./README /home/nonrootuser/twitch_stat_collector
COPY ./browser_scripts/twitch_unmute.js /home/nonrootuser/twitch_stat_collector/browser_scripts
COPY ./browser_scripts/twitch_low_latency.js /home/nonrootuser/twitch_stat_collector/browser_scripts
COPY ./browser_scripts/twitch_normal_latency.js /home/nonrootuser/twitch_stat_collector/browser_scripts

# Set the working directory to where the scripts are
WORKDIR /home/nonrootuser/twitch_stat_collector



# Set the default command
# CMD ["./run_script.sh", "3"]
