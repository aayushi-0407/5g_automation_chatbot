#!/bin/bash

CONFIG_FILE="generated_config.yaml"
METRICS_FILE="/var/lib/prometheus/node-exporter/ueransim.prom"
LOG_DIR="./logs"

# Ensure yq and log directory are available
mkdir -p $LOG_DIR

# Extract values from the YAML config using yq
GNB_COUNT=$(yq e '.gNBs' "$CONFIG_FILE")
UE_COUNT=$(yq e '.UEs' "$CONFIG_FILE")

# Create Prometheus metrics file
echo "# HELP ueransim_gnb_total Number of gNBs deployed" > $METRICS_FILE
echo "# TYPE ueransim_gnb_total gauge" >> $METRICS_FILE
echo "ueransim_gnb_total $GNB_COUNT" >> $METRICS_FILE

echo "# HELP ueransim_ue_total Number of UEs deployed" >> $METRICS_FILE
echo "# TYPE ueransim_ue_total gauge" >> $METRICS_FILE
echo "ueransim_ue_total $UE_COUNT" >> $METRICS_FILE

# Optional init (if you want registration data too)
echo "# HELP ueransim_ue_registration_success UE registration successes" >> $METRICS_FILE
echo "# TYPE ueransim_ue_registration_success gauge" >> $METRICS_FILE
echo "ueransim_ue_registration_success 0" >> $METRICS_FILE

echo "# HELP ueransim_ue_registration_failure UE registration failures" >> $METRICS_FILE
echo "# TYPE ueransim_ue_registration_failure gauge" >> $METRICS_FILE
echo "ueransim_ue_registration_failure 0" >> $METRICS_FILE

echo "✅ UERANSIM deployment metrics updated."

# Deploy gNB and UEs, capturing logs
echo "📡 Deploying $GNB_COUNT gNBs and $UE_COUNT UEs using UERANSIM..."
for ((i=1; i<=GNB_COUNT; i++)); do
    echo "✅ gNB $i started."
    ./UERANSIM/build/nr-gnb -c ./UERANSIM/configs/gnb$i.yaml > "$LOG_DIR/gnb_$i.log" 2>&1 &
done

for ((i=1; i<=UE_COUNT; i++)); do
    echo "✅ UE $i started."
    ./UERANSIM/build/nr-ue -c ./UERANSIM/configs/ue$i.yaml > "$LOG_DIR/ue_$i.log" 2>&1 &
done

