import pickle
import tensorflow as tf
import numpy as np

from model import NPI

from card_matching import CardPatternMatchingCore
from config_card_matching import CONFIG, PROGRAM_SET
from environment_card_matching import ScratchPad, get_args


MOVE_PID, WRITE_PID = 0, 1
W_PTRS = {0: "OUT", 1: "CARRY"}
PTRS = {0: "CARD1_PTR", 1: "CARD2_PTR", 2: "OUT_PTR"}
R_L = {0: "LEFT", 1: "RIGHT"}
LOG_PATH = "Card Pattern Matching/"
CKPT_PATH = "Card Pattern Matching/card_pattern_matching_model.ckpt"
TEST_PATH = "Card Pattern Matching/card_pattern_matching_test.pik"


def evaluate_card_pattern_matching():
    """
    Load NPI Model from Checkpoint, and initialize REPL, for interactive carry-addition.
    """
    # Load Data
    with open(TEST_PATH, 'rb') as f:
        data = pickle.load(f)

    # Initialize Card Pattern Matching Core
    print ('Initializing Card Pattern Matching Core!')
    core = CardPatternMatchingCore()

    # Initialize NPI Model
    npi = NPI(core, CONFIG, LOG_PATH)

    with tf.Session() as sess:
        # Restore from Checkpoint
        saver = tf.train.Saver()
        saver.restore(sess, CKPT_PATH)

        # Run REPL
        repl(sess, npi, data)

def repl(session, npi, data):
    while True:
        inpt = input('Enter Two Numbers, or Hit Enter for Random Pair: ')

        # if inpt == "":
        #     x, y, _ = data[np.random.randint(len(data))]

        # else:
        #     x, y = map(int, inpt.split())

        x, y, _ = data[np.random.randint(len(data))]

        # Reset NPI States
        print ()
        npi.reset_state()

        # Setup Environment
        scratch = ScratchPad(x, y)
        prog_name, prog_id, arg, term = 'CMP', 2, [], False

        cont = 'c'
        while cont == 'c' or cont == 'C':
            # Print Step Output
            if prog_id == MOVE_PID:
                a0, a1 = PTRS.get(arg[0], "OOPS!"), R_L[arg[1]]
                a_str = "[%s, %s]" % (str(a0), str(a1))
            elif prog_id == WRITE_PID:
                a0, a1 = W_PTRS[arg[0]], arg[1]
                a_str = "[%s, %s]" % (str(a0), str(a1))
            else:
                a_str = "[]"

            print ('Step: %s, Arguments: %s, Terminate: %s' % (prog_name, a_str, str(term)))
            print ('CARD 1: %s, CARD 2: %s, OUT: %s' % (scratch._card1_ptr[1],
                                                              scratch._card2_ptr[1],
                                                              scratch._out_ptr[1]))

            # Update Environment if MOVE or WRITE
            if prog_id == MOVE_PID or prog_id == WRITE_PID:
                scratch.execute(prog_id, arg)

            # Print Environment
            scratch.pretty_print()

            # Get Environment, Argument Vectors
            env_in, arg_in, prog_in = [scratch.get_env()], [get_args(arg, arg_in=True)], [[prog_id]]
            t, n_p, n_args = session.run([npi.terminate, npi.program_distribution, npi.arguments],
                                         feed_dict={npi.env_in: env_in, npi.arg_in: arg_in,
                                                    npi.prg_in: prog_in})

            if np.argmax(t) == 1:
                print ('Step: %s, Arguments: %s, Terminate: %s' % (prog_name, a_str, str(True)))
                print ('CARD 1: %s, CARD 2: %s, OUT: %s' % (scratch._card1_ptr[1],
                                                                  scratch._card2_ptr[1],
                                                                  scratch._out_ptr[1]))
                # Update Environment if MOVE or WRITE
                if prog_id == MOVE_PID or prog_id == WRITE_PID:
                    scratch.execute(prog_id, arg)

                # Print Environment
                scratch.pretty_print()

                output = int("".join(map(str, map(int, scratch[3]))))
                print ("Model Output: %s + %s = %s" % (str(x), str(y), str(output)))
                print ("Correct Out : %s + %s = %s" % (str(x), str(y), str(x + y)))
                print ("Correct!" if output == (x + y) else "Incorrect!")
                break

            else:
                prog_id = np.argmax(n_p)
                prog_name = PROGRAM_SET[prog_id][0]
                if prog_id == MOVE_PID or prog_id == WRITE_PID:
                    arg = [np.argmax(n_args[0]), np.argmax(n_args[1])]
                else:
                    arg = []
                term = False

            cont = 'c'
            # cont = input('Continue? ')