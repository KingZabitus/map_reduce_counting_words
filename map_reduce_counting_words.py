from collections import defaultdict
from pathlib import Path
from threading import Thread

def is_valid_file(file):
    return file.is_file() and file.name.endswith("txt")

def map(file: Path):
    if is_valid_file(file):
        words = file.read_text().replace('\n', ' ').split(' ')
        with Path('./output.tmp').open('a') as output_file:
            for word in words:
                output_file.write(f'{word}: "1"\n')

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

def reduce(word: str, occurrences: list[str]):
    occurrences_count = len(occurrences)
    print({'word': word, 'occurrences': occurrences_count})

if __name__ == '__main__':
    path = Path('./')
    files_on_path = path.glob('*')

    map_threads = []

    # Executa a função map em uma thread para cada arquivo
    for file in files_on_path:
        thread = Thread(target=map, args=(file,))
        thread.start()
        map_threads.append(thread)

    # Aguarda todas as threads do map terminarem antes de chamar a função reduce
    for thread in map_threads:
        thread.join()

    # Ordena o arquivo temporário e obtém a lista de ocorrências de palavras
    word_ocurrence_list = order_temp_file()

    reduce_threads = []

    # Executa a função em uma Thread para cada palavra junto de suas ocorrências
    for word_ocurrence in word_ocurrence_list:
        word = word_ocurrence.get('word')
        occurrences = word_ocurrence.get('occurrences')
        thread = Thread(target=reduce, args=(word, occurrences))
        thread.start()
        reduce_threads.append(thread)

    for thread in reduce_threads:
        thread.join()