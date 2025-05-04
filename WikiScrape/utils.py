import sys

def get_arguments():
    try:
        seed_file = sys.argv[1]
        max_files = sys.argv[2]
        max_depth = sys.argv[3]
        output_dir = sys.argv[4]
    except IndexError as e:
        print("Missing arguments!")
        exit(1)
    return (seed_file, max_files, max_depth, output_dir)

def read_seed_urls(filename):
    with open(filename, 'r') as file:
        return [line.strip() for line in file]

def split_list(list, count):
    a, b = divmod(len(list), count)
    return [list[i * a + min(i, b):(i + 1) * a + min(i + 1, b)] for i in range(count)]
