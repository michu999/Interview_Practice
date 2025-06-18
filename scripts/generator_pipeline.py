import os

def read_lines(filepath):
    with open(filepath, 'r') as f:
        for line in f:
            yield line.strip().lower()

if __name__ == '__main__':
    # Stwórzmy duży plik testowy
    file_path = 'large_test_file.txt'
    if not os.path.exists(file_path):
        print(f"Tworzę plik testowy: {file_path}")
        with open(file_path, 'w') as f:
            for i in range(1_000_000):
                f.write(f"Log entry {i}: some random data here.\n")

#    for line in read_lines(file_path):
#        print(line)