"""
Application Entry Point
"""


import argparse
from client_dropbox.dropbox_client import DropboxClient
from agent.agent_controller import AgentController
from logger.logger import Logger


# Output logger
logger = Logger()


# Init dropbox client
drive_token = "wLggQQNtFusAAAAAAAAAAe_7oFlkQIHLaQHFyimnoitrQgaViOA6z-EnOpvRKnb-"
drive_client = DropboxClient()
drive_client.init(drive_token)

# Start controller
agent_meter = AgentController(drive_client, logger)
agent_meter.start()
agent_meter.wait_for_finish()
agent_meter.stop()

# Cleanup dropbox client
drive_client.cleanup()
