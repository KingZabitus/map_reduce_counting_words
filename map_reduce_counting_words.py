from collections import defaultdict
from pathlib import Path
from threading import Thread

# Verifica se n]ao é um diretório e se a extensão do arquivo é txt
def is_valid_file(file):
    return file.is_file() and file.name.endswith("txt")

def map(file: Path):
    if is_valid_file(file):
        words = file.read_text().replace('\n', ' ').split(' ')
        with Path('./output.tmp').open('a') as file:
            for word in words:
                file.write(f'{word}: "1"\n')

def order_temp_file():
    temp_file = Path('./output.tmp')
    words = temp_file.read_text().split('\n')

    word_ocurrence_dict = defaultdict(list)

    for line in words:
        word = line.split(' ')[0].replace(':', '')
        if word:
            word_ocurrence_dict[word].append('1')

    word_ocurrence_list = [{"word": word, "occurrences": occurrences} for word, occurrences in word_ocurrence_dict.items()]

    return word_ocurrence_list

def reduce():
    ...

if __name__ == '__main__':
    path = Path('./')
    files_on_path = path.glob('*')

    threads = []

    for file in files_on_path:
        thread = Thread(target=map, args=(file,))
        thread.start()
        threads.append(thread)

    # Aguarda que todas as threads terminem antes de chamar a função reduce()
    for thread in threads:
        thread.join()

    word_ocurrence_list = order_temp_file()

    print(*word_ocurrence_list, sep='\n')

    reduce()