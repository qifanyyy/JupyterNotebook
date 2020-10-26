import sys


def validate_config_content(str_, dict_):
    if str_ not in dict_:
        print("Missing argument in config_content: " + str_)
        sys.exit()


def is_int(s):
    try:
        int(s)
        return True
    except ValueError:
        return False


def validate_config_lines(str_, k):


    if (":" in str_ and len(str_.split(":")) < 2) or ("=" in str_ and len(str_.split("=")) < 2):
        print("Cannot process key and value in config file, line: " + str(k))
        sys.exit()

    if ":" not in str_ and "=" not in str_ and len(str_.split()) < 2:
        print("Cannot process key and value in config file, line: " + str(k))
        sys.exit()

    if not any(is_int(x) for x in str_.split()) and \
            not any(is_int(x) for x in str_.split(":")) and \
            not any(is_int(x) for x in str_.split("=")):
        print("Line " + str_ + " is missing numerical (integer) value")
        sys.exit()

    if not any(isinstance(x, (str)) for x in str_.split()):
        print("Line " + str_ + " is missing key")
        sys.exit()


def validate_seq(str_, condition, id):
    if len(str_) > condition:
        print("Sequence too long! seq_" + id)
        sys.exit()


def import_config(filepath):
    config_content = {}
    k = 1

    with open(filepath) as fp:
        line = fp.readline().lower()
        validate_config_lines(line, k)

        while line:
            k += 1

            if "=" in line:
                config_content[line.split("=", 1)[0].strip()] = line.split("=", 1)[1].strip()
                line = fp.readline().lower()

            elif ":" in line:
                config_content[line.split(":", 1)[0].strip()] = line.split(":", 1)[1].strip()
                line = fp.readline().lower()

            else:
                config_content[line.split(" ", 1)[0].strip()] = line.split(" ", 1)[1].strip()
                line = fp.readline().lower()

            if line:
                validate_config_lines(line, k)

    validate_config_content('same', config_content)
    validate_config_content('diff', config_content)
    validate_config_content('gap', config_content)
    validate_config_content('max_seq_length', config_content)
    validate_config_content('max_number_paths', config_content)

    config_content = {k: config_content[k] for k in ['same', 'diff', 'gap', 'max_seq_length', 'max_number_paths']}

    return config_content


def import_sequences(seq_1_path, seq_2_path, cond):

    with open(seq_1_path, "r") as text_file:

        for line in text_file:
            if ">" in line:
                break

        seq_1 = text_file.read()

    with open(seq_2_path, "r") as text_file:

        for line in text_file:
            if ">" in line:
                break

        seq_2 = text_file.read()

    validate_seq(seq_1, cond, "1")
    validate_seq(seq_2, cond, "2")

    seq_1 = seq_1.replace('\n', '')
    seq_2 = seq_2.replace('\n', '')

    return seq_1, seq_2


def create_output(NW_table, path):
    print("Writing results to file..")

    with open(path, "w") as text_file:
        text_file.write("SCORE = " + str(NW_table.final_score))
        text_file.write("\n\n")
        text_file.write(NW_table.output)

