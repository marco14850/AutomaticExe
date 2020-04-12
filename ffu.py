#
# Author: HackerOps FCFM
# 2020
# Version BETA 1.0
#
#
import json
import logging
import multiprocessing
import platform as pla
import sys
import time

import ffc

# Tools to download
# Winpmem:
# Url: https://github.com/Velocidex/c-aff4,INK https://github.com/Velocidex/c-aff4/releases
#
#
sistema = {'Linux': ['Linux', 'linux', 'LINUX', 'l', 'L'],
           'Darwin': ['Mac', 'mac', 'MAC', 'MAC-OS', "mac-os", 'm', 'M'],
           'Windows': ['Windows', 'windows', 'w', 'W', 'WINDOWS']
           }

if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG, format='[+] %(asctime)s-%(levelname)s: %(message)s')
    comandos = {}
    startTime = time.time()
    try:
        ffc.parseo_argumentos()
    except Exception as ex:
        logging.error("Fallo en parseo de argumentos \n" + str(type(ex)) + "\n" + str(ex.args))
        sys.exit("Error en argumentos")
    try:
        with open(ffc.conf.command, 'r') as cmd:
            comandos = json.load(cmd)
        print(comandos)
    except Exception as ex:
        logging.error("Fallo archivo de comandos a ejecutar: \n" + str(type(ex)) + "\n" + str(ex.args))
        sys.exit("Erron en archivo  de comandos .json")
    ffc.imprimir_banner()
    process = []
    for i in comandos["Comandos"]:
        if any(element in sistema[pla.system()] for element in i["OS"]):
            # TODO bypass admin rights
            if not (ffc.conf.notAdmin and i["admin"]):
                process.append(
                    multiprocessing.Process(target=ffc.ejecutar_comando, args=(i["cmd"], ffc.conf.outputDir,)))
    ffc.imprimir_mensaje("Procesos agregados a la cola")
    if ffc.conf.wifiPassword:
        process.append(multiprocessing.Process(target=ffc.extraer_wifi, args=(ffc.conf.outputDir,)))
    for p in process:
        p.start()
    for p in process:
        try:
            p.join()
        except Exception as ex:
            logging.error("Fallo en la ejecucion \n" + str(type(ex)) + "\n" + str(ex.args))
    endTime = time.time()
    duration = endTime - startTime
    logging.info("Sistema operativo " + pla.system() + " Version: " + pla.version())
    logging.info("Tiempo de ejecucion: " + str(duration))
    logging.info("El programa se ejecuto con exito")
