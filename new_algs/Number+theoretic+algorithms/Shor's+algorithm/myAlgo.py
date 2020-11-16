from gateSet import *
import os
import sys


def run_test(args):
    if args.adder:
        para = args.adder
        test_adder(para[0], para[1], para[2], args)
    if args.phimod:
        para = args.phimod
        test_ccphiMOD(para[0], para[1], para[2], para[3], args)
    if args.cmult:
        para = args.cmult
        testCMULT(para[0], para[1], para[2], para[3], para[4], args)
    if args.cu:
        para = args.cu
        test_cu(para[0], para[1], para[2], para[3], args)
    if args.nor:
        para = args.nor
        if para[1] == 0:
            for i in range(2, para[0]):
                if math.gcd(i, para[0]) == 1:
                    shorNormal(para[0], i, args)
        else:
            shorNormal(para[0], para[1], args)
    if args.seq:
        para = args.seq
        shorSequential(para[0], para[1], args)


def test_adder_appro(a, b, n, appro, args):
    if args.log:
        if not os.path.exists('adder/log'):
            os.makedirs('adder/log')
        path = f'adder/log/a{a}_b{b}_n{n}.log'
        sys.stdout = open(path, 'w')
    qc = adder_appro(a, b, n, appro)
    print("="*40)
    print(
        f"Executing adder_appro with a={a}, b={b}, n={n}, appro_deg={appro}...")
    if args.draw:
        figdir = f'./adder_appro/qcfig'
        if not os.path.exists(figdir):
            os.makedirs(figdir)
        figpath = f'./adder_appro/qcfig/a{a}_b{b}_n{n}.png'
        if not os.path.isfile(figpath):
            circuit_drawer(qc, filename=figpath, output='mpl')
    res = sim.mySim(qc, args)
    res_lis = list(res)
    expect_res = a+b
    meas_lis = []
    for i in range(len(res_lis)):
        meas_lis.append(int(res_lis[i], 2))
    equal_flag = False
    if args.simulation:
        dir_name = args.simulation
        if len(res) != 1:
            raise Exception("The measurement result should be determinisitic!")
        print(f"Expect ans = {expect_res}, Measure res = {meas_lis[0]}")
        if expect_res == meas_lis[0]:
            equal_flag = True
    else:
        dir_name = 'real'
        for i in range(len(meas_lis)):
            print(f"Expect ans = {expect_res}, Measure res = {meas_lis[i]}")
            if meas_lis[i] == expect_res:
                equal_flag = True
    if equal_flag:
        print("Result correct! Adder success!")
    if args.output:
        dir = f'./adder_appro/result/{dir_name}'
        if not os.path.exists(dir):
            os.makedirs(dir)
        path = f'./adder_appro/result/{dir_name}/adder{a}_{b}_appro{appro}.png'
        plot_histogram(res, figsize=(10, 10),
                       title=f'adder{a}_{b}_appro{appro}').savefig(path)

    print("="*40)


def test_adder_em(a, b, n):
    qc = adder(a, b, n, 1)
    backend = qiskit.Aer.get_backend('qasm_simulator')
    rbackend = provider.get_backend('ibmq_cambridge')
    noise_model = NoiseModel.from_backend(rbackend, gate_error=False)
    job = qiskit.execute(meas_calibs, backend=backend,
                         shots=1000, noise_model=noise_model)
    cal_results = job.result()
    meas_fitter = CompleteMeasFitter(
        cal_results, state_labels, circlabel='mcal')
    meas_filter = meas_fitter.filter

    # Results with mitigation
    mitigated_results = meas_filter.apply(results)
    mitigated_counts = mitigated_results.get_counts(0)
    plot_histogram([noisy_counts, mitigated_counts],
                   legend=['noisy', 'mitigated'])


def test_adder(a, b, n, args):
    if args.log:
        if not os.path.exists('adder/log'):
            os.makedirs('adder/log')
        path = f'adder/log/a{a}_b{b}_n{n}.log'
        sys.stdout = open(path, 'w')
    qc = adder(a, b, n)

    # print("="*40)
    print('=========================')
    print(f"Executing adder with a={a}, b={b}, n={n}...")
    if args.draw:
        figdir = f'./adder/qcfig'
        if not os.path.exists(figdir):
            os.makedirs(figdir)
        figpath = f'./adder/qcfig/a{a}_b{b}_n{n}.png'
        if not os.path.isfile(figpath):
            circuit_drawer(qc, filename=figpath, output='mpl')
    res = sim.mySim(qc, args)
    res_lis = list(res)
    expect_res = a+b
    meas_lis = []
    for i in range(len(res_lis)):
        meas_lis.append(int(res_lis[i], 2))
    equal_flag = False
    if args.simulation:
        dir_name = args.simulation
        if len(res) != 1:
            raise Exception("The measurement result should be determinisitic!")
        print(f"Expect ans = {expect_res}, Measure res = {meas_lis[0]}")
        if expect_res == meas_lis[0]:
            equal_flag = True
    else:
        dir_name = 'real'
        for i in range(len(meas_lis)):
            print(f"Expect ans = {expect_res}, Measure res = {meas_lis[i]}")
            if meas_lis[i] == expect_res:
                equal_flag = True
    if equal_flag:
        print("Result correct! Adder success!")
    else:
        print("Result wrong! Adder failed!")
        if expect_res >= (2**n):
            print("Overflow occurs!")
    if args.output:
        dir = f'./adder/result/{dir_name}'
        if not os.path.exists(dir):
            os.makedirs(dir)
        path = f'./adder/result/{dir_name}/adder{a}_{b}.png'
        plot_histogram(res, figsize=(10, 10),
                       title=f'adder{a}_{b}').savefig(path)

    # print("="*40)
    print('=========================')


def test_ccphiMOD(n, b, a, N, args, print_qc=False, save_fig=False):
    print("-"*40)
    bitlen = n+1
    expect = (a+b) % N
    print(f'a={a}, b={b}, N={N}, (a+b)mod N={expect} (expect ans)')
    qr_ctrl = QuantumRegister(2, name='ctrl')
    qr_phi = QuantumRegister(bitlen, name='phi')
    qr_ancilla = QuantumRegister(1, name='ancilla')
    cr_phi = ClassicalRegister(bitlen-1, name='cr_phi')
    cr_ancilla = ClassicalRegister(1, name='cr_ancilla')
    qc = QuantumCircuit(qr_ctrl, qr_phi, qr_ancilla, cr_phi, cr_ancilla)
    gate = ccphiADDmodN(n=n, a=a, b=b, N=N,
                        print_qc=print_qc, save_fig=save_fig)

    qft = myQFT(bitlen, inverse=False)
    iqft = myQFT(bitlen, inverse=True)

    qc.x(qr_ctrl)
    b = b % N
    b_bin = '{n:0{bit}b}'.format(n=b, bit=bitlen)
    for i in range(bitlen):
        if b_bin[i] == '1':
            qc.x(qr_phi[i])
    qc.append(qft, qargs=qr_phi[:])
    qc.append(gate, qargs=qr_ctrl[:]+qr_phi[:]+qr_ancilla[:])
    qc.append(iqft, qargs=qr_phi[:])
    for i in range(bitlen-1):
        qc.measure(qr_phi[i+1], cr_phi[bitlen-i-2])
    qc.measure(qr_ancilla, cr_ancilla)

    if print_qc:
        print(qc)
    if save_fig:
        circuit_drawer(qc, scale=1.3, output='mpl',
                       filename='./report/ccphiaddmod.png', plot_barriers=False)
    res = sim.mySim(qc, args)
    if len(list(res)) != 1:
        raise Exception("Ans trivial")
    res_num = list(res)[0]
    meas_anc = res_num.split(" ")[0]
    meas_phi = res_num.split(" ")[1]
    if meas_anc == '0':
        print("Ancilla bit correct!")
    else:
        raise Exception("ancilla bit broken!")

    print(f"The expect result is {a}+{b} mod {N} = {expect}")
    print(f"The measurement result is {res_num}={int(meas_phi,2)}")
    if expect == int(meas_phi, 2):
        print("Measure = Expect, Correct!")
    else:
        raise Exception('wrong ans')
    print("-"*40)


def testCMULT(n, x, b, a, N, args, print_qc=False, save_fig=False):
    bitlen = n+1
    qr_c = QuantumRegister(1, name='c')
    qr_x = QuantumRegister(n, name='x')
    qr_b = QuantumRegister(bitlen, name='b')
    qr_ancilla = QuantumRegister(1, name='ancilla')
    cr_x = ClassicalRegister(n, name='cr_x')
    cr_b = ClassicalRegister(bitlen, name='cr_b')
    cr_ancilla = ClassicalRegister(1, name='cr_ancilla')
    qc = QuantumCircuit(qr_c, qr_x, qr_b, qr_ancilla, cr_x, cr_b, cr_ancilla)
    qc.x(qr_c)
    b = b % N
    x_bin = '{n:0{bit}b}'.format(n=x, bit=n)
    b_bin = '{n:0{bit}b}'.format(n=b, bit=bitlen)
    for i in range(n):
        if x_bin[i] == '1':
            qc.x(qr_x[i])
    for i in range(bitlen):
        if b_bin[i] == '1':
            qc.x(qr_b[i])
    gate = cmult_a_mod_N(n, a, b, N, False, True)
    qc.append(gate, qargs=qr_c[:]+qr_x[:]+qr_b[:]+qr_ancilla[:])

    for i in range(bitlen):
        qc.measure(qr_b[i], cr_b[bitlen-i-1])
    # circuit_drawer(qc,scale=0.8,filename='./report/cmult2.png',output='mpl')
    for i in range(n):
        qc.measure(qr_x[i], cr_x[n-i-1])
    if print_qc:
        print(qc)
    if save_fig:
        pass
        circuit_drawer(
            qc, scale=0.8, filename='./report/cmult2.png', output='mpl')

    res = sim.mySim(qc, args)
    res_num = list(res)[0]

    meas_x = res_num.split(" ")[2]
    meas_b = res_num.split(" ")[1]
    meas_ancilla = res_num.split(" ")[0]
    if meas_x == x_bin:
        print("The x remain the same! Correct!")
    else:
        raise Exception("x_change")
    if meas_ancilla == '0':
        print("Ancilla bit correct!")
    else:
        raise Exception("ancilla bit broken!")
    expect = (b+a*x) % N
    print(f"x={x}, b={b}, a={a}, N={N}, b+ax mod N={(b+a*x)%N} ")

    if expect == int(meas_b, 2):
        print("Expect = Measure = {0}".format(expect))
        print("Multiplier correct!")
    elif a*x+b >= 2**bitlen:
        print("Expect = Measure = {0}".format(expect))
        print("Overflow occurs! Multiplier error!")
    else:
        raise Exception("Multiplier wrong")


def CMULTexp_latex(n, x, b, a, N, args, print_qc=False, save_fig=False):
    bitlen = n+1
    qr_c = QuantumRegister(1, name='c')
    qr_x = QuantumRegister(n, name='x')
    qr_b = QuantumRegister(bitlen, name='b')
    qr_ancilla = QuantumRegister(1, name='ancilla')

    cr_b = ClassicalRegister(bitlen, name='cr_b')

    qc = QuantumCircuit(qr_c, qr_x, qr_b, qr_ancilla, cr_b)
    qc.x(qr_c)
    b = b % N
    x_bin = '{n:0{bit}b}'.format(n=x, bit=n)
    b_bin = '{n:0{bit}b}'.format(n=b, bit=bitlen)
    for i in range(n):
        if x_bin[i] == '1':
            qc.x(qr_x[i])
    for i in range(bitlen):
        if b_bin[i] == '1':
            qc.x(qr_b[i])
    gate = cmult_a_mod_N(n, a, b, N, False, True)
    qc.append(gate, qargs=qr_c[:]+qr_x[:]+qr_b[:]+qr_ancilla[:])

    for i in range(bitlen):
        qc.measure(qr_b[i], cr_b[bitlen-i-1])
    circuit_drawer(qc, scale=0.8, filename='./report/cmult3.png', output='mpl')


def test_cu(n, x, a, N, args):
    print(f'x={x},a={a},N={N},ax mod N = {(a*x)%N}')
    a = a % N
    bitlen = n+1
    qr_c = QuantumRegister(1, name='c')
    qr_x = QuantumRegister(n, name='x')
    qr_b_0 = QuantumRegister(bitlen, name='b0')
    qr_ancilla = QuantumRegister(1, name='ancilla')
    cr = ClassicalRegister(n, name='cr')
    qc = QuantumCircuit(qr_c, qr_x, qr_b_0, qr_ancilla, cr)
    qc.x(qr_c[0])
    x = x % N
    x_bin = '{n:0{bit}b}'.format(n=x, bit=n)
    for i in range(n):
        if x_bin[i] == '1':
            qc.x(qr_x[i])
    gate = cu_a(n, a, N, False, True)
    qc.append(gate, qargs=qr_c[:]+qr_x[:]+qr_b_0[:]+qr_ancilla[:])

    for i in range(n):
        qc.measure(qr_x[i], cr[n-1-i])
    circuit_drawer(qc, output='mpl', scale=0.8, filename='./report/cu.png')
    # print(qc)
    res = sim.mySim(qc, args)
    res_num = list(res)[0]

    expect = (a*x) % N

    if expect == int(res_num, 2):
        print("Expect = Measure = {0}".format(expect))
        print("CU correct!")
    else:
        raise Exception("CU wrong")


def check_cphiADD(num, qr, qc):
    binary = bin(int(num))[2:].zfill(4)

    for i in range(4):
        if binary[i] == '1':
            qc.x(qr[i+1])


def rangeTest_cMult(N):
    error_lis = []
    for i in range(1, 16):
        for j in range(1, 16):
            try:
                testCMULT(n=4, x=2, b=i, a=j, N=N, print_qc=True)
            except Exception as e:
                args = (4, 2, i, j, N, e)
                error_lis.append(args)
    with open('error_mul.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['n', 'x', 'b', 'a', 'N', 'errorType'])
        for i in error_lis:
            csv_out.writerow(i)


def rangeTest_ccphiMOD(N):
    error_lis = []
    wrong_lis = []
    ancilla_lis = []
    trivial_lis = []

    for i in range(1, 16):
        for j in range(1, 16):
            try:
                test_ccphiMOD(n=4, b=i, a=j, N=N,
                              print_qc=False, save_fig=False)
            except Exception as e:
                print(e)
                args = (5, i, j, N)
                if str(e) == 'wrong ans':
                    wrong_lis.append(args)
                elif str(e) == 'ancilla bit broken!':
                    ancilla_lis.append(args)
                elif str(e) == 'Ans trivial':
                    trivial_lis.append(args)
                else:
                    error_lis.append(args)
    # test_ccphiMOD(bitlen=5,b=1,a=9,N=9,print_qc=True,save_fig=True)
    with open('error.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['bitlen', 'b', 'a', 'N'])
        for row in error_lis:
            csv_out.writerow(row)
    with open('wrong.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['bitlen', 'b', 'a', 'N'])
        for row in wrong_lis:
            csv_out.writerow(row)
    with open('ancilla.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['bitlen', 'b', 'a', 'N'])
        for row in ancilla_lis:
            csv_out.writerow(row)
    with open('trivial.csv', 'w') as out:
        csv_out = csv.writer(out)
        csv_out.writerow(['bitlen', 'b', 'a', 'N'])
        for row in trivial_lis:
            csv_out.writerow(row)


def shorNormal_circuit(N, a, args):
    # check whether a, N is coprime
    if math.gcd(a, N) != 1:
        raise Exception("a,N are not coprime.")
    # circuit preparation
    n = math.ceil(math.log(N, 2))
    up = QuantumRegister(2*n, name='up')
    down = QuantumRegister(n, name='x')
    down_b = QuantumRegister(n+1, name='b')
    ancilla = QuantumRegister(1, name='ancilla')
    cr = ClassicalRegister(2*n, name='cr')
    qc = QuantumCircuit(up, down, down_b, ancilla, cr)
    # initialize
    qc.h(up)
    qc.x(down[n-1])
    # control-unitary gate application
    for i in range(0, 2*n):
        gate = cu_a(n, a**(2**i), N, print_qc=False)
        qc.append(gate, qargs=[up[i]]+down[:]+down_b[:]+ancilla[:])
    # rest circuit construction
    qftgate = myQFT(2*n, inverse=True)
    qc.append(qftgate, qargs=up)
    for i in range(0, 2*n):
        qc.measure(up[i], cr[2*n-1-i])
    return qc


def shorNormal(N, a, args=None):
    # check whether a, N is coprime
    if math.gcd(a, N) != 1:
        raise Exception("a,N are not coprime.")
    # circuit preparation
    n = math.ceil(math.log(N, 2))
    up = QuantumRegister(2*n, name='up')
    down = QuantumRegister(n, name='x')
    down_b = QuantumRegister(n+1, name='b')
    ancilla = QuantumRegister(1, name='ancilla')
    cr = ClassicalRegister(2*n, name='cr')
    qc = QuantumCircuit(up, down, down_b, ancilla, cr)
    # initialize
    qc.h(up)
    qc.x(down[n-1])
    # control-unitary gate application
    for i in range(0, 2*n):
        gate = cu_a(n, a**(2**i), N, print_qc=False)
        qc.append(gate, qargs=[up[i]]+down[:]+down_b[:]+ancilla[:])
    # rest circuit construction
    qftgate = myQFT(2*n, inverse=True)
    qc.append(qftgate, qargs=up)
    for i in range(0, 2*n):
        qc.measure(up[i], cr[2*n-1-i])
    # ===========================================================================
    # Result formation
    if args == None:
        return qc
    if args.draw:
        qcpath = f'./normal/circuit'
        if not os.path.exists(qcpath):
            os.makedirs(qcpath)
        circuit_drawer(qc, output='mpl',
                       filename=f'./normal/circuit/{N}_{a}.png', scale=0.6)
    if args.simcmp:
        sim.gpuSim(qc)
        sim.cpuSim(qc)
        return 

    res = sim.mySim(qc, args)

    lis = sim.sort_by_prob(res)
    if args.output:
        respath = f'./normal/result'
        if not os.path.exists(respath):
            os.makedirs(respath)
        plot_histogram(res, figsize=(10, 10), title=f'N={N} a={a} result(Nor)').savefig(
            respath+f'/{N}_{a}_res.png')
    path = f'./normal/result/{N}_{a}.csv'
    if os.path.exists(path):
        print("Overwriting the existing data....")
    with open(f'./normal/result/{N}_{a}.csv', 'w') as out:
        csv_out = csv.writer(out)
        for i in lis:
            csv_out.writerow(i)


def shorSequential_rev2(N, a):
    n = math.ceil(math.log(N, 2))
    ctrl = QuantumRegister(1, name='ctrl')
    down = QuantumRegister(n, name='x')
    down_b = QuantumRegister(n+1, name='b')
    ancilla = QuantumRegister(1, name='ancilla')
    cr = ClassicalRegister(2*n, name='cr')
    c_aux = ClassicalRegister(1, name='caux')
    qc = QuantumCircuit(ancilla, down_b, down, ctrl, cr, c_aux)
    qc.x(down[0])
    for i in range(2*n):
        qc.x(ctrl).c_if(c_aux, 1)
        neighbor_range = range(np.max([0, i - 2*n + 1]), 2*n - i - 1)
        qc.h(ctrl)
        gate = cu_a(n, a**(2**(2*n-1-i)), N)
        qc.append(gate, qargs=ctrl[:]+down[:]+down_b[:]+ancilla[:])
        qc.h(ctrl)
        qc.measure(ctrl, c_aux)
        qc.measure(ctrl, cr)
        if neighbor_range != range(0, 0):
            gate = myR2(i, neighbor_range, c_aux)
            qc.append(gate, qargs=ctrl[:])
    return qc


def shorSequential(N, a, args=None):
    n = math.ceil(math.log(N, 2))
    ctrl = QuantumRegister(1, name='ctrl')
    down = QuantumRegister(n, name='x')
    down_b = QuantumRegister(n+1, name='b')
    ancilla = QuantumRegister(1, name='ancilla')
    qc = QuantumCircuit(ctrl, down, down_b, ancilla)
    cr_lis = []
    for i in range(0, 2*n):
        cr = ClassicalRegister(1)
        qc.add_register(cr)
        cr_lis.append(cr)
    qc.x(down[n-1])
    for i in range(2*n):
        qc.x(ctrl).c_if(cr_lis[i], 1)
        neighbor_range = range(np.max([0, i - 2*n + 1]), 2*n - i - 1)
        qc.h(ctrl)
        gate = cu_a(n, a**(2**(2*n-1-i)), N)
        qc.append(gate, qargs=ctrl[:]+down[:]+down_b[:]+ancilla[:])
        qc.h(ctrl)
        # qc.measure(ctrl,i)
        qc.measure(ctrl, cr_lis[i])
        if neighbor_range != range(0, 0):
            gate = myR(i, neighbor_range, cr_lis)
            qc.append(gate, qargs=ctrl[:])
    if args == None:
        return qc
    if args.draw:
        qcpath = f'./sequential/circuit'
        if not os.path.exists(qcpath):
            os.makedirs(qcpath)
        circuit_drawer(qc, output='mpl',
                       filename=f'./sequential/circuit/{N}_{a}.png', scale=0.6)

    res = sim.mySim(qc, args)
    print(res)
    new_dict = {}

    for iter in list(res):
        tmp = iter
        tmp = tmp.replace(" ", "")
        new_dict[tmp] = res.pop(iter)
   # print(new_dict)
    lis = sim.sort_by_prob(new_dict)
    # print(lis)
    if args.output:
        respath = f'./sequential/result'
        if not os.path.exists(respath):
            os.makedirs(respath)
        plot_histogram(new_dict, figsize=(
            10, 10), title=f'N={N} a={a} result(Seq)').savefig(respath+f'/{N}_{a}_res.png')
    with open(f'./sequential/result/{N}_{a}.csv', 'w') as out:
        csv_out = csv.writer(out)
        for i in lis:
            csv_out.writerow(i)
