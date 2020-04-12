import argparse
import os
import platform as pla
import subprocess
from datetime import datetime

import pyfiglet

conf = {}


def ejecutar_comando(comando, outputDir):
    x = subprocess.getoutput(comando)
    guardar_salida(str(comando), x, outputDir)


def parseo_argumentos():
    parser = argparse.ArgumentParser("First Forensics Unified Program BETA 1.0 HackerOps-FCFM")
    parser.add_argument('-v', '--verbose', help='Despliega mensajes de error e informativos',
                        action='store_true', default=False)
    parser.add_argument('-oD', '--outputDir', help='Especificas el nombre del directorio de salida',
                        type=str, default="./Results - " + datetime.now().strftime("%d-%b-%Y-%H.%M.%S"), required=False)
    parser.add_argument('-wP', '--wifiPassword', help='Extraer las credenciales de wifi del equipo local',
                        action='store_true', required=False)
    parser.add_argument('-cmd', '--command',
                        help='Ruta del archivo json con la lista de comandos a ejecutar por sistema operativo',
                        type=str, default='./conf.json', required=False)
    parser.add_argument('-nA', '--notAdmin',
                        help='No ejecuta cualquier comando que sea catalogado con requerimientos administrador',
                        action='store_true', default=False, required=False)
    gl_args = parser.parse_args()
    global conf
    conf = gl_args
    imprimir_mensaje("Argumentos con exito")
    crear_directorio()


def imprimir_mensaje(msg):
    global conf
    if conf.verbose:
        print(msg)


def guardar_salida(comando, resultado, outputDir):
    with open(outputDir + '\\' + comando.replace("\\", "").replace("/", "").replace(".", "").replace("\"", "").replace(
            "'", "") + '.txt', 'w') as out:
        out.write(resultado)


#####################
# Referencia https://nitratine.net/blog/post/get-wifi-passwords-with-python/
#####################
def extraer_wifi(outputDir):
    if pla.system() == "Windows":
        result = "{:<30}| {}".format("SSID", "Password")
        netsh = subprocess.check_output(['netsh', 'wlan', 'show', 'profiles']).decode('utf-8',
                                                                                      errors="backslashreplace").split(
            '\n')
        profiles = [i.split(":")[1][1:-1] for i in netsh if ":" in i]
        for i in profiles:
            if i != "":
                try:
                    results = subprocess.check_output(['netsh', 'wlan', 'show', 'profile', i, 'key=clear']).decode(
                        'utf-8', errors="backslashreplace").split('\n')
                    results = [b.split(":")[1][1:-1] for b in results if ("clave" or "Key") in b]
                    result += "\n{:<30}| {}".format(i, results[0])
                except IndexError:
                    result += "\n{:<30}| {}".format(i, "")
                except:
                    print("[+] NETSH: Formato no encontrado en " + i)
        guardar_salida("netsh", result, outputDir)


def crear_directorio():
    global conf
    if not os.path.exists(conf.outputDir):
        os.mkdir(conf.outputDir)


def imprimir_banner():
    print(r"""                                                  

                                                       .@@@@@@,           
                                                (@@@@&&&&&@@@&&&          
                                                &&@@&@@@@@@@&&&&&&&&&.    
                                               %&&&@@@@@@@@@@&&&& &&@&&#  
                                             &&&&%&&&@&&&&&&%((,  @@@@&@  
                                             @&&&@,     #####@@@@@@@@@@   
             @@@@@&                             &&&@@@@@@@@@@@@@@@@@      
             @@@@@&           @@@@@@@@@@  @@@@@@&%%#((//   **///          
             @@@@@&         @@@@@@&,*@@   @@@@@@@@@@@@@@   @@@@@          
             @@@@@&        *@@@@#             .@@@@@       @@@@@          
             @@@@@&         @@@@@&            .@@@@@       @@@@@          
             @@@@@&          @@@@@@@@         .@@@@@       @@@@@          
             @@@@@&            *@@@@@@@@      .@@@@@       @@@@@          
             @@@@@&                @@@@@@     .@@@@@       @@@@@          
             @@@@@&                 @@@@@     .@@@@@       @@@@@          
             @@@@@@&&&&&&&  @&    @@@@@@      .@@@@@       @@@@@          
             @@@@@@@@@@@@@ &@@@@@@@@@@&       .@@@@@       @@@@@          
    
    ============================================================================
    ----------------------------------------------------------------------------
    :::::::::Licenciatura en Seguridad en Tecnologias de la Informacion:::::::::
    ----------------------------------------------------------------------------
    ============================================================================
        """)
    custom_fig = pyfiglet.Figlet(font='roman')
    print(custom_fig.renderText('FCFM - HackerOPS'))
