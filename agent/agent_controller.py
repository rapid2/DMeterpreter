"""
Agent controller
"""


import threading
from agent.agent_meterpreter import AgentMeterpreter


class AgentController:
    def __init__(self, dive_client, logger):
        self._dive_client = dive_client
        self._logger = logger
        self._working = False
        self._meterpreter_thread = None
        self._meterpreter = AgentMeterpreter(logger)
        self._active_agent_id = ""
        
    def start(self):
        if self._working:
            return True

        self._working = True
        self._meterpreter_thread = threading.Thread(target=self._worker)
        self._meterpreter_thread.start()

    def stop(self):
        self._working = False
        if self._meterpreter_thread:
            if self._meterpreter_thread.is_alive():
                self._meterpreter_thread.join()
                
    def wait_for_finish(self):
        if self._working and self._meterpreter_thread:
            if self._meterpreter_thread.is_alive():
                self._meterpreter_thread.join()

    def _worker(self):
            while self._working:
                if self._active_agent_id:
                    _input = input(f"{self._active_agent_id}> ")
                else:
                    _input = input("> ")
                if len(_input) == 0:
                    continue
                # Parse command
                name, args = self.parse_input(_input)
                # Handle command
                if name == "list":
                    agent_names = self._get_agent_names()
                    for index in range(len(agent_names)):
                        name = agent_names[index]
                        self._logger.log_message(f"{index + 1}. {name}")
                elif name == "select":
                    if args.get(0):
                        self._active_agent_id = args[0]
                        self._meterpreter.init(self._dive_client, args[0])
                    else:
                        self._logger.log_message("Invalid agent specified")
                elif name == "restart_agents":
                    self._restart_agents()
                elif name == "help":
                    self._log_help()
                elif name == "list_agent_commands":
                    self._log_agent_help()
                elif name == "exit":
                    if self._active_agent_id:
                        self._meterpreter.cleanup()
                        self._active_agent_id = ""
                    else:
                        self._working = False
                elif self._active_agent_id:
                    self._meterpreter.run_command(name, args)
                else:
                    self._logger.log_message("Invalid command specified")

    def parse_input(self, _input):
        index = _input.find(" ")
        first_argument = ""
        if index > 0:
            name = _input[0:index].strip()
            first_argument = _input[index:].strip()
        else:
            name = _input.strip()
        if first_argument.startswith("'"):
            first_argument = first_argument[1:]
            if first_argument.endswith("'"):
                first_argument = first_argument[:-1]
        elif first_argument.startswith('"'):
            first_argument = first_argument[1:]
            if first_argument.endswith('"'):
                first_argument = first_argument[:-1]
        args = {0: first_argument}
        return name, args

    def _get_agent_names(self):
        return self._dive_client.list_dir("")

    def _restart_agents(self):
        agent_names = self._get_agent_names()
        for name in agent_names:
            self._logger.log_message(f"Restarting: {name}")
            self._dive_client.remove("/" + name)

    def _log_help(self):
        self._logger.log_message("list                - lists all agents")
        self._logger.log_message("select              - selects agent")
        self._logger.log_message("restart_agents      - restarts agents")
        self._logger.log_message("list_agent_commands - prints agent commands")
        self._logger.log_message("help                - prints this message")
        self._logger.log_message("exit                - exit current agent or program")

    def _log_agent_help(self):
        names = self._meterpreter.get_command_names()
        for name in names:
            self._logger.log_message(name)
