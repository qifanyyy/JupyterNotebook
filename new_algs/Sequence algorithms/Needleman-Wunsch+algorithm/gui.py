# ----------------------------------------------------------------------------------------------------------------------

import os

from shell import *
from util.bye import *
from util.file import *
from util.timem import *


# ----------------------------------------------------------------------------------------------------------------------


class GUI(Shell):

    # ------------------------------------------------------------------------------------------------------------------

    def run(self):

        print(Font.BOLD + Font.DARKCYAN + "\nOpciones disponibles: " + Font.END + Font.END)
        print("alineamiento, tablas, optimo, listar, val")
        print("match, mismatch, gap, recursos, ayuda, salir \n")

        print(Font.BOLD + Font.DARKCYAN +
              "Para mostrar información detallada "
              "sobre cada opción anteponga la palabra 'ayuda' " +
              Font.END + Font.END)

        print("Ejemplo: >> ayuda alineamiento \n")

        super().run()

    # ------------------------------------------------------------------------------------------------------------------

    def alineamiento(self, args):

        """
        Realiza un alineamiento entre dos hileras con el algoritmo indicado.
        Las hileras pueden ser escritas manualmente o puede especificarse por medio de archivos.
        Sintaxis: alineamiento [global|semiglobal|local|kband] [texto_1|arhivo_1] [texto_2|arhivo_2] ?lineal
        Ejemplos:
            1. alineamiento global AAGCTGGT ACCCTTCGG
            2. alineamiento local AGTCGTCC archivo.txt
            3. alineamiento global archivo.txt otro_archivo.txt lineal
        """

        if len(args) != 3 and len(args) != 4:
            raise Exception("Cantidad incorrecta de argumentos.")

        v_text = open_file(args[1]) if os.path.isfile(args[1]) else args[1]
        h_text = open_file(args[2]) if os.path.isfile(args[2]) else args[2]
        alignment = self.find_option(args[0] + " lineal" if len(args) == 4 else args[0])

        if args[0] == "kband":
            kvalue = int(input("Ingrese un valor para k: "))
            self.last_result = alignment(v_text, h_text, self._match, self._mismatch, self._gap, kvalue)
        else:
            self.last_result = alignment(v_text, h_text, self._match, self._mismatch, self._gap)

        self.optimo(args)

        tab = input("¿Desea ver la tabla generada? [S/N]: ").lower()
        if tab == "s":
            proc = input("¿Mostrar procedimiento en la tabla [S/N]: ").lower()
            if proc == "s":
                self.tablas("flechas")
            else:
                self.tablas(args)
        else:
            print("")

    # ------------------------------------------------------------------------------------------------------------------

    def tablas(self, args):

        """
        Muestra las estructuras internas de trabajo, es decir, los calculos realizados dentro de las tablas.
        Si se específica la palabra flechas, la tabla se mostrará con el procedimiento realizado sobre la misma.
        Sintaxis: tablas ?flechas
        Ejemplos:
            1. tablas
            2. tablas flechas
        """

        print("\n" + Font.BOLD + Font.PURPLE + "Tabla obtenida" + Font.END + Font.END)

        if self.last_result is not None:
            self.last_result.show_arrows = args.__contains__("flechas")
            print(self.last_result)
        else:
            print("Sin calcular\n")

    # ------------------------------------------------------------------------------------------------------------------

    def optimo(self, args):

        """
        Muestra el valor óptimo alcanzado y el resultado óptimo del alineamiento.
        """

        print("\n" + Font.BOLD + Font.PURPLE + "Valor óptimo: " + Font.END + Font.END)
        if self.last_result is not None:
            print("valor: " + self.last_result.calc_score().astype(str) + "\n")
        else:
            print("valor: 0 \n")

        print(Font.BOLD + Font.PURPLE + "Alineamiento obtenido: " + Font.END + Font.END)
        if self.last_result is not None:
            string_1, string_2 = self.last_result.reconstruction()
            print(string_1)
            print(string_2 + "\n")
        else:
            print("alineamiento: Sin calcular \n")

    # ------------------------------------------------------------------------------------------------------------------

    def listar(self, args):

        """
        Lista todos los algoritmos implementados en el programa.
        """

        print("\n" + Font.BOLD + Font.PURPLE + "Algoritmos implementados" + Font.END + Font.END)
        algorithms = list(self.algoritms.keys())
        for i in range(len(algorithms)):
            print(str(i) + ". " + str(algorithms[i]))
        print("")

    # ------------------------------------------------------------------------------------------------------------------

    def val(self, args):

        """
        Muestra el valor actual de los pesos.
        """

        print("\n" + Font.BOLD + Font.PURPLE + "Valor actual de los pesos" + Font.END + Font.END)
        print("match: " + str(self._match))
        print("mismatch: " + str(self._mismatch))
        print("gap: " + str(self._gap) + "\n")

    # ------------------------------------------------------------------------------------------------------------------

    def match(self, args):

        """
        Función para mostrar el valor actual de match o establecer un nuevo valor de match si viene
        como parámetro del comando.
        Sintaxis: match ?nuevo_valor
        """

        self.config(["match"] + args)

    # ------------------------------------------------------------------------------------------------------------------

    def mismatch(self, args):

        """
        Función para mostrar el valor actual de mismatch o establecer un nuevo valor de mismatch si viene
        como parámetro del comando.
        Sintaxis: mismatch ?nuevo_valor
        """

        self.config(["mismatch"] + args)

    # ------------------------------------------------------------------------------------------------------------------

    def gap(self, args):

        """
        Función para mostrar el valor actual de gap o establecer un nuevo valor de gap si viene
        como parámetro del comando.
        Sintaxis: gap ?nuevo_valor
        """

        self.config(["gap"] + args)

    # ------------------------------------------------------------------------------------------------------------------

    def config(self, args):

        """
        Muestra la configuración actual del sistema. Puede usarse para mostrar un valor en específico
        o establecer un nuevo valor si viene como parámetro del comando.
        Sintaxis: config ?[ gap | match | mismatch ] ?nuevo_valor
        Ejemplos:
            1. config
            2. config match
            3. config mismatch -2
        """

        if len(args) == 0:
            self.val(args)

        else:

            if len(args) == 2:
                exec("self._" + args[0] + " = " + args[1])

            print("\n" + Font.BOLD + Font.PURPLE + "Valor actual" + Font.END + Font.END)
            eval("print('" + args[0] + ": ' + " + "str(self._" + args[0] + ") + '\\n' )")

    # ------------------------------------------------------------------------------------------------------------------

    def ayuda(self, args):

        """
        Muestra la ayuda para una función o un conjunto de estas.
        Sintaxis: ayuda [ funcion_1, funcion_2, ... funcion_N ]
        Ejemplos;
            1. ayuda
            2. ayuda alineamiento
            3. ayuda alineamiento listar
        """

        if len(args) == 0:
            self.ayuda(["alineamiento"])

        for arg in args:
            print(Font.BLUE + self.exec_help(arg) + Font.END)

    # ------------------------------------------------------------------------------------------------------------------

    def salir(self, args):

        """
        Se termina la ejecución del programa. Se muestra la cantidad de recursos utilizados durante la ejecución y la
        información de los autores.
        """

        self.recursos(["total"])
        print(bye)
        print(info)
        sys.exit(0)

    # ------------------------------------------------------------------------------------------------------------------

    def recursos(self, args):

        """
        Muestra el consumo actual de memoria y de tiempo. Si se especifíca la palabra 'totales' se mostrará la sumatoria
        de recursos utilizados durante la ejecución de lo contrario se mostrará el consumo del último algoritmo usado.
        """

        print("\n" + Font.BOLD + Font.PURPLE +
              "Recursos utilizados" +
              Font.END + Font.END)

        print("tiempo: %.10f segundos" % Timem.last_time)
        print("memoria: %s bytes\n" % str(Timem.last_memory_usage))

        if args.__contains__("totales"):

            print(Font.BOLD + Font.PURPLE +
                  "Sumatoria de recursos utilizados durante la ejecución" +
                  Font.END + Font.END)

            print("tiempo: %.10f segundos" % (time() - Timem.start_time))
            print("memoria: %s bytes \n" % str(Timem.total_memory_usage))

# ----------------------------------------------------------------------------------------------------------------------

if __name__ == "__main__":
    gui = GUI()
    gui.run()

# ----------------------------------------------------------------------------------------------------------------------

