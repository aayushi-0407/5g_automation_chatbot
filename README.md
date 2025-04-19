# 📡 5G Network Automation Chatbot Project 
**Team Members:**  
- Aayushi Singh (202251001)  
- Priyanka Dhurvey (202251104)  
- Tisha Yadav (202251144)  
- Anjali Lodhi (202252306)
  
The project titled "Development of an AI-Powered Chatbot for 5G Network Automation" aims to simplify and automate the configuration of 5G network components like gNBs, UEs, and monitoring tools. Using AI and natural language processing, the chatbot will interpret user inputs and generate YAML configuration files, reducing manual effort and errors.The Mistral model used  will further enhance the chatbot’s language understanding capabilities.

Key integrations include OpenAirInterface (OAI), UERANSIM, and Grafana for real-time validation and monitoring.

> "Deploy 2 gNBs and 5 UEs with monitoring."

It then:
- Parses the input using Hugging Face model (mistral)
- Generates a `config.yaml` file
- Deploys gNBs and UEs via UERANSIM
- Exports metrics to Prometheus
- Visualizes data in Grafana

---

## 🧩 Components

- **FastAPI chatbot backend**
- **UERANSIM** – 5G simulation for gNBs and UEs
- **Prometheus** – for metrics collection
- **Node Exporter** – with `textfile_collector` for exposing gNB/UE counts
- **Grafana** – for visualization dashboards
- **Hugging Face MODEL** – for NLP parsing of instructions

---

## ✅ Requirements

Install:

- Python 3.8+
- UERANSIM
- Prometheus
- Grafana
- Node Exporter
- `yq` for YAML parsing

---

## 🚀 Setup Instructions

### 1. Clone and Setup Project

```bash
1. git clone https://github.com/aayushi-0407/5g_automation_chatbot.git
 cd 5g_automation_chatbot/5g_chatbot
python3 -m venv venv
source venv/bin/activate
2. pip install -r requirements.txt --break-system-packages

3.Set Hugging Face Token
Create a .env file:

echo "HUGGINGFACEHUB_API_TOKEN=your_token_here" > .env
4. Install yq for YAML parsing
sudo snap install yq

5.Set up Node Exporter
wget https://github.com/prometheus/node_exporter/releases/download/v1.8.1/node_exporter-1.8.1.linux-amd64.tar.gz
tar -xvzf node_exporter-1.8.1.linux-amd64.tar.gz
sudo mv node_exporter-1.8.1.linux-amd64/node_exporter /usr/local/bin/

# Setup metrics folder
sudo mkdir -p /var/lib/node_exporter/textfile_collector
sudo chown -R $USER:$USER /var/lib/node_exporter


6.setup Prometheus
wget https://github.com/prometheus/prometheus/releases/download/v2.52.0/prometheus-2.52.0.linux-amd64.tar.gz
tar -xzf prometheus-2.52.0.linux-amd64.tar.gz
cd prometheus-2.52.0.linux-amd64



7.Install and start grafana
sudo apt install -y grafana
sudo systemctl enable grafana-server
sudo systemctl start grafana-server
```
Steps to run the code :
```bash
1.Activate venv
source venv/bin/activate
2.start node exporter
node_exporter --collector.textfile.directory=/var/lib/node_exporter/textfile_collector &

3.Restart the prometheus
sudo systemctl restart prometheus

4.Restart the grafana
sudo systemctl restart grafana-server

5.Run the Backend
python 5g_chatbot.py

6.Give user input
curl -X POST "http://localhost:8000/chatbot" \
-H "Content-Type: application/json" \
-d '{"user_input": "Deploy 2 gNBs and 5 UEs with monitoring."}'

7.Deploy ueransim
sudo ./deploy_ueransim.
```
You can see the visualisation at http://localhost:3000



