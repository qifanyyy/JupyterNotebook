from QuantumCircuits import QuantumPrograms
from qiskit import QuantumProgram
from QConfig import QConfig
import PrintUtils
import subprocess
import os

def print_available_programs(programs):
    PrintUtils.printHeader("Available programs:")
    i = 1
    for progname in programs.keys():
        PrintUtils.printInfo(f"  {i}. {progname}: {programs[progname]}")
        i += 1

def getParams():
    programs = QuantumPrograms.PROGRAMS

    backend = 'local_qasm_simulator'
    shots = 1024
    timeout = 120
    program = None

    engine = QuantumProgram()

    def tryParseInt(value):
        try:
            return int(value)
        except:
            return None
    
    print_available_programs(programs)
    program = input("Select a program to run, or type 'exit' to quit.\n> ").strip()
    progNum = tryParseInt(program)
    while program not in programs and program != "exit":
        if progNum is not None:
            if progNum > len(programs):
                PrintUtils.printErr(f"Invalid program '{progNum}'")
            else:
                program = list(programs.keys())[progNum - 1]
                break
        else:
            PrintUtils.printErr(f"Invalid program '{program}'")
        print_available_programs(programs)
        program = input("Run which program?\n> ").strip()
        progNum = tryParseInt(program)
    return QuantumPrograms(engine, QConfig(backend, shots, timeout, program))

def setup_experiment(args):
    if args is None:
        return getParams()
    else:
        programs = QuantumPrograms.PROGRAMS

        apiToken = None
        backend = None
        shots = None
        timeout = None
        program = None

        # get API token
        if args.apitoken is None:
            try:
                apiToken = open("./.qiskit_api_token", "r").read()
            except:
                apiToken = input("Enter your IBM Quantum Experience API token: \n> ")
        else: 
            apiToken = args.apitoken
        
        engine = QuantumProgram()
        engine.set_api(apiToken, 'https://quantumexperience.ng.bluemix.net/api')

        # get backend
        backends = get_backend_dict(engine.available_backends())
        if args.backend is None:
            PrintUtils.printHeader("Available backends:")
            for key, value in backends.items():
                PrintUtils.printInfo(f"  {key}: {value}")
            backend = get_backend(backends[int(input("Run on which backend?\n> "))], backends)
        else:
            if args.backend in backends.values():
                backend = args.backend
            elif int(args.backend) in backends.keys():
                backend = backends[int(args.backend)]
            else: 
                raise ValueError(f"Invalid backend: '{args.backend}'")
        
        # set shots default value
        if args.shots is None:
            shots = 1024
        else:
            shots = int(args.shots)
        
        # set timeout default value
        if args.timeout is None:
            timeout = 120
        else:
            timeout = int(args.timeout)

        # validate program
        if args.program is None:
            print_available_programs(programs)
            program = input("Run which program?\n> ")
            while program not in programs:
                PrintUtils.printErr(f"Invalid program '{program}'")
                print_available_programs(programs)
                program = input("Run which program?\n> ")
        else:
            if args.program not in programs.keys():
                raise ValueError(f"Invalid program '{args.program}'")
            else:
                program = args.program
        
        return QuantumPrograms(engine, QConfig(backend, shots, timeout, program))

def get_backend_dict(backends):
    dict = {}
    i = 1
    # ensure simulators are at top of list
    for b in backends:
        if "simulator" in b:
            dict[i] = b
            i += 1
    for b in backends:
        if "simulator" not in b:
            dict[i] = b
            i += 1
    return dict

def build_backend_dict(backends):
    dict = {1: "local_qasm_simulator"}
    i = 2
    # ensure simulators are at top of list
    for b in backends:
        if "simulator" in b["name"]:
            dict[i] = b["name"]
            i += 1
    for b in backends:
        if "simulator" not in b["name"]:
            dict[i] = b["name"]
            i += 1
    return dict

def get_backend(i, available_backends):
    backend = None
    if i in available_backends.keys():
        return available_backends[i]
    elif str(i) in available_backends.keys():
        return available_backends[str(i)]
    elif str(i) in available_backends.values():
        return str(i)
    else:
        PrintUtils.printErr(f"Invalid backend '{backend}', using default simulator...")
        return next(iter(available_backends.values())) # first value in dict

def request_input_file():
    files = [i for i in os.listdir(".") if i.endswith(".qasm")]
    PrintUtils.printHeader("QASM files found in current directory: ")
    for i in files:
        PrintUtils.printInfo(f"    ./{i}")
    file = subprocess.check_output('read -e -p "Enter path to QASM file to run: \n> " var ; echo $var',shell=True).rstrip()
    return file