### Step 1: Update System and Install Basic Packages

Update your package lists:
```bash
sudo apt update
```

Install essential packages:
```bash
sudo apt install -y build-essential libssl-dev libffi-dev python3-dev python3-venv python3-pip
```
### Step 2: Create the User and Group

1. **Create the user group `projects`**:
```bash
sudo groupadd projects
```

2. **Create the user `bothousingagent`** with no home directory and no login shell:
```bash
sudo useradd -M -s /usr/sbin/nologin -g projects bothousingagent
```

### Step 3: Prepare the Deployment Directory

1. **Create the project directory** and set appropriate permissions:
```bash
sudo mkdir -p /opt/projects/BotHousingAgent
sudo chown -R bothousingagent:projects /opt/projects/BotHousingAgent
sudo chmod -R 775 /opt/projects/BotHousingAgent
```

### Step 4: Set Up the Python Environment

1. **Create the virtual environment** as `bothousingagent`:
```bash
sudo -u bothousingagent python3 -m venv /opt/projects/BotHousingAgent/resources/venvs/bot_housing_agent_venv
```

2. **Activate the virtual environment** and install your project in editable mode:
```bash
sudo -u bothousingagent /opt/projects/BotHousingAgent/resources/venvs/bot_housing_agent_venv/bin/pip install -e /opt/projects/BotHousingAgent
```

### Step 5: Configure systemd

1. **Create a systemd service file**:
```bash
sudo nano /etc/systemd/system/bothousingagent.service
```

2. **Add the following configuration** to the service file:
```ini
[Unit]
Description=Bot Housing Agent Service
After=network.target

[Service]
User=bothousingagent
Group=projects
WorkingDirectory=/opt/projects/BotHousingAgent
Environment="PATH=/opt/projects/BotHousingAgent/resources/venvs/bot_housing_agent_venv/bin"
ExecStart=/opt/projects/BotHousingAgent/resources/venvs/bot_housing_agent_venv/bin/bot_housing_agent

[Install]
WantedBy=multi-user.target
```
- **Description**: A short description of your service.
- **After**: Specifies the order of unit startup.
- **User** and **Group**: Specify the user and group under which the service will run.
- **WorkingDirectory**: The directory where your application is located.
- **Environment**: Specifies the environment variables, including the path to the virtual environment.
- **ExecStart**: The command to start your application.

3. **Reload systemd to recognize the new service**:
```bash
sudo systemctl daemon-reload
```

4. **Enable the service to start on boot**:
```bash
sudo systemctl enable bothousingagent.service
```

5. **Start the service**:
```bash
sudo systemctl start bothousingagent.service
```

6. **Check the status of the service**:
```bash
sudo systemctl status bothousingagent.service
```

### Step 6: Verify and Manage the Service

- **View logs**:
```bash
sudo journalctl -u bothousingagent.service
```

- **Restart the service**:
```bash
sudo systemctl restart bothousingagent.service
```

- **Stop the service**:
```bash
sudo systemctl stop bothousingagent.service
```

### Recap of Important Points

- **User and Group**: Created `bothousingagent` user in the `projects` group with no home and no login shell.
- **Project Directory**: Located at `/opt/projects/BotHousingAgent` with appropriate permissions.
- **Virtual Environment**: Created and activated under `/opt/projects/BotHousingAgent/resources/venvs/bot_housing_agent_venv`.
- **systemd Service**: Configured to run the bot using the `bot_housing_agent` command.