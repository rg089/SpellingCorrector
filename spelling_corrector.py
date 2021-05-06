import re
from tokenizer import sentence_tokenizer
from mbleven import compare
# from spellcorrector import spell_corrector

class SpellingCorrector:
    freq_word = {}
    freq_bigram = {}
    total_uni = 0
    total_bi = 0
    wordlist = set()

    def __init__(self, method=0, ignore_capitalized=True):
        self.method = method
        self.ignore_capitalized = ignore_capitalized
        self.keep_regex = "\w+"
        self.alphabet = "".join([chr(i) for i in range(65, 91)]+[chr(i) for i in range(97, 123)])
        SpellingCorrector.fill_frequency()

    def fill_frequency():
        if SpellingCorrector.total_uni != 0:
            return
        l1 = open("frequency_dictionary_en_82_765.txt", "r").read().splitlines()
        l2 = open("frequency_bigramdictionary_en_243_342.txt", "r").read().splitlines()
        t1 = 0; t2 = 0
        for i in l1:
            word, count = i.split(); count = int(count);
            SpellingCorrector.wordlist.add(word)
            SpellingCorrector.freq_word[word] = count
            t1 += count
        for i in l2:
            word1, word2, count = i.split(); count = int(count)
            SpellingCorrector.wordlist.add(word1); SpellingCorrector.wordlist.add(word2)
            SpellingCorrector.freq_bigram[(word1, word2)] = count
            t2 += count
        SpellingCorrector.total_uni = t1; SpellingCorrector.total_bi = t2

    def most_probable_word(self, word_dist, previous_word):
        max_prob = 0
        recommendation = ""
        current_dist = -1
        for word, dist in word_dist:
            if previous_word != "":
                prob = SpellingCorrector.freq_bigram.get((previous_word, word), 0) / SpellingCorrector.total_bi
            else:
                prob = SpellingCorrector.freq_word.get(word, 0) / SpellingCorrector.total_uni
            if dist==2 and current_dist==1:
                if prob - max_prob > 0.005:
                    max_prob = prob; recommendation = word; current_dist = dist
            else:
                if prob > max_prob:
                    max_prob = prob; recommendation = word; current_dist = dist
        return recommendation

    def chose_word(self, previous_word, word_dist):
        recommendation = self.most_probable_word(word_dist, previous_word)
        if recommendation == "" and previous_word != "":
            recommendation = self.most_probable_word(word_dist, "")
        return recommendation

    def correct_word(self, incorrect_word, previous_word):
        word_dist = []
        for possible_word in SpellingCorrector.wordlist:
            dist = compare(incorrect_word, possible_word, transpose=True)
            if dist != -1:
                word_dist.append((possible_word, dist))
        word_dist.sort(key=lambda x: x[1])
        word = self.chose_word(previous_word, word_dist)
        if word == "":
            return incorrect_word
        return word

    def correct_sentence(self, sentence):
        last_index = len(sentence)
        if sentence[-1] not in ".!?":
            punctuation = ""
        else:
            punctuation = sentence[-1]
            last_index = -1
        words = sentence[:last_index].split()
        for i in range(len(words)):
            word = words[i]
            if word[-1] in ",#":
                word_end = word[-1]
                word = word[:-1]
            else:
                word_end = ""
            capital = False
            if word.isalpha() and word.lower() not in SpellingCorrector.wordlist and (self.ignore_capitalized and ord(word[0])>90 or not self.ignore_capitalized):
                if ord(word[0]) <= 90:
                    capital = True
                incorrect = word.lower()
                if i==0:
                    previous_word = ""
                else:
                    previous_word = words[i-1].lower()
                correct = self.correct_word(incorrect, previous_word)
                if capital:
                    correct = correct.capitalize()
                words[i] = correct+word_end
        return " ".join(words)+punctuation

    def correct_text(self, text):
        # if self.method == 1:
        #     return spell_corrector(input_term = text)
        sentences = sentence_tokenizer(text)
        text = " ".join([self.correct_sentence(sentence) for sentence in sentences])
        text = re.sub("\s+", " ", text)
        return text


sp_check = SpellingCorrector(ignore_capitalized=False)
print(sp_check.correct_text("Hllo, I pronise that I will not bresk the silence again!"))
