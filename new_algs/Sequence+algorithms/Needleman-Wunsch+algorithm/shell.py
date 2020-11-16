# ----------------------------------------------------------------------------------------------------------------------

from util.font import *
from model.kband_aligment import *
from model.local_alignment import *
from model.semiglobaLineal_aligment import *
from model.globalLineal_alignment import *
from model.localLineal_alignment import *


# ----------------------------------------------------------------------------------------------------------------------

class Shell(object):

    # ------------------------------------------------------------------------------------------------------------------

    def __init__(self):

        self._gap = -2
        self._match = 1
        self._mismatch = -1
        self.last_result = None
        self.algoritms = self.get_algorithms()

    # ------------------------------------------------------------------------------------------------------------------

    def run(self):
        self.command_line()

    # ------------------------------------------------------------------------------------------------------------------

    def command_line(self):

        command = input(
            Font.BOLD + Font.DARKCYAN +
            "Ingrese un comando: " +
            Font.END + Font.END)

        try:
            self.exec_command(command)
        except Exception as e:
            self.manage_exception(e, command)

        self.command_line()

    # ------------------------------------------------------------------------------------------------------------------

    def get_algorithms(self):

        return {
            "global": GlobalAlignment,
            "semiglobal": SemiglobalAlignment,
            "local": LocalAlignment,
            "globallineal": GlobalLinealAlignment,
            "semigloballineal": SemiglobaLinealAlignment,
            "locallineal": LocalLinealAlignment,
            "kband": KBandAlignment
        }

    # ------------------------------------------------------------------------------------------------------------------

    def manage_exception(self, exception, command):

        print(Font.RED + "\nError: " + Font.END + str(exception))
        name = command.split(" ")[0]
        option = self.find_option(name)

        if option is not None:
            doc = input("¿Desea ver la documentación? [S/N]: ").lower()
            if doc == "s":
                print(Font.BLUE + self.exec_help(name) + Font.END)
            else:
                print("")

    # ------------------------------------------------------------------------------------------------------------------

    def exec_option(self, option_name, option_args):

        option = self.find_option(option_name)
        if type(option) == str or type(option) == int:
            return str(option)
        if option is not None:
            return str(option(option_args))
        else:
            raise Exception("Opción no disponible\n")

    # ------------------------------------------------------------------------------------------------------------------

    def exec_help(self, option_name):

        option = self.find_option(option_name)
        if option is not None:
            return option.__doc__
        raise Exception("Ayuda no disponible")

    # ------------------------------------------------------------------------------------------------------------------

    def find_option(self, option_name):

        options = dir(self)
        if options.__contains__(option_name):
            return getattr(self, option_name)
        elif self.algoritms.__contains__(option_name):
            return self.algoritms[option_name]
        return None

    # ------------------------------------------------------------------------------------------------------------------

    def exec_command(self, command):

        name = command.split(" ")[0]
        args = command.split(" ")[1::]
        return self.exec_option(name, args)

# ----------------------------------------------------------------------------------------------------------------------
