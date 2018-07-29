
# coding: utf-8

"""predict.

Usage:
    predict <corpus_file>

Options:
    -h --help            Show this screen.
"""

# TODO : use shelves to store ngrams dict
# Refacto to Predict class

import os
import sys
import re
import collections

from docopt import docopt

from read_text import readText

ngrams_dir = os.path.join(os.path.dirname(__file__), 'ngrams')
os.makedirs(ngrams_dir, mode=0o755, exist_ok=True)


def clearLine(line):
    line = re.sub(r"[^\w\s]", ' ', line)
    line = re.sub(r'\s+', ' ', line)
    return line.lower()


def unigrams(infile, outfile='unigrams.txt'):
    print('Calcul des unigrammes...', end='', flush=True)
    unigrams = {}
    try:
        with open(infile, 'r', encoding="utf-8") as fic:
            for line in fic:
                for word in clearLine(line).split(' '):
                    if word != '':
                        if word in unigrams:
                            unigrams[word] += 1
                        else:
                            unigrams[word] = 1
    except Exception as e:
        print('\nUne erreur est survenue lors de la lecture de', infile)
        print(e)
        exit(1)

    try:
        with open(os.path.join(ngrams_dir, outfile), 'w', encoding="utf-8") as fic:
            unigrams = collections.OrderedDict(sorted(unigrams.items(), key=lambda elt: elt[1], reverse=True))
            for word in unigrams:
                fic.write(word + ' ' + str(unigrams[word]) + '\n')
    except Exception as e:
        print('\nUne erreur est survenue lors de l\'écriture de', outfile)
        print(e)
        exit(1)

    print(' Ok')


def generate_ngrams(infile, n, outfile=''):
    if n < 2:
        print('Fonction generate_ngrams() : Valeur minimale de n : 2')
        exit(3)
    if outfile == '':
        outfile = str(n) + '_grams.txt'
    print('Calcul des %s-grammes...', n, end='', flush=True)
    ngrams = {}
    try:
        with open(infile, 'r', encoding="utf-8") as fic:
            for line in fic:
                words = clearLine(line).split(' ')
                words = [elt for elt in words if elt != '']
                words = [' '.join(name) for name in zip(*[words[i:] for i in range(n)])]
                for word in words:
                    if word in ngrams:
                        ngrams[word] += 1
                    else:
                        ngrams[word] = 1

    except Exception as e:
        print('\nUne erreur est survenue lors de la lecture de', infile)
        print(e)
        exit(1)

    try:
        with open(os.path.join(ngrams_dir, outfile), 'w', encoding="utf-8") as fic:
            ngrams = list(ngrams.items())
            ngrams.sort(key=lambda elt: elt[1], reverse=True)
            for word, val in ngrams:
                fic.write(word + ' ' + str(val) + '\n')
    except Exception as e:
        print('\nUne erreur est survenue lors de l\'écriture de', outfile)
        print(e)
        exit(1)

    print(' Ok')


def generate_stats(infile):
    print('Lecture du ficher des n-grammes', end='', flush=True)
    ngrams = {}
    try:
        with open(os.path.join(ngrams_dir, infile), 'r', encoding="utf-8") as fic:
            for line in fic:
                words = line.split(' ')
                value = int(words.pop())
                next_word = words.pop()
                key = ' '.join(words)
                if key in ngrams:
                    ngrams[key][next_word] = value
                else:
                    ngrams[key] = {next_word: value}
    except Exception as e:
        print('\nUne erreur est survenue lors de la lecture de', infile)
        print(e)
        exit(1)

    for words in ngrams:
        n = 0
        for next_word in ngrams[words]:
            n += ngrams[words][next_word]
        ngrams[words] = [(next_word, round(ngrams[words][next_word] / n, 3)) for next_word in ngrams[words]]
        ngrams[words].sort(key=lambda elt: elt[1], reverse=True)

    print(' Ok')
    return ngrams


def predict(stats, term, threshold):
    result = []
    if term in stats:
        for words, value in stats[term]:
            if value > threshold:
                result.append((words, value))
    if result == []:
        return [('', 1)]
    else:
        return result


def main():
    arguments = docopt(__doc__, version='predict 0.1')
    corpus_file = arguments['<corpus_file>']

    unigrams(corpus_file)
    generate_ngrams(corpus_file, 2)
    ngrams = generate_stats('2_grams.txt')
    prediction = predict(ngrams, 'son', 0.05)

    readText('Pour le mot, "son", je prédit les mots suivants :')
    for val, pourc in prediction:
        print('son {} ({})'.format(val, pourc))
        readText('son {}'.format(val))

    generate_ngrams(corpus_file, 3)
    ngrams = generate_stats('3_grams.txt')
    prediction_2 = predict(ngrams, 'de la', 0.05)
    readText('Pour le mot, "de la", je prédit les mots suivants :')
    for val, pourc in prediction_2:
        print('de la {} ({})'.format(val, pourc))
        readText('de la {}'.format(val))


if __name__ == '__main__':
    main()
