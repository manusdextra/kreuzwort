class Word:
    def __init__(self, letters):
        self.letters = letters
        self.hint = ""  # definition to be added
        self.named_nodes = dict()
        self.nodes = list()

    def __repr__(self):
        return f"'{self.letters}'"

    def __iter__(self):
        return iter(self.letters)


class Wordlist:
    def __init__(self, words):
        self.items = [Word(item) for item in words]
        self.alphabet = self.find_all_letters()
        self.items = self.analyse(self.items)
        self.best_choices = self.rank_words()

    def __iter__(self):
        return iter(self.items)

    def find_all_letters(self):
        alphabet = dict()
        for item in self.items:
            for letter in item.letters:
                if letter in alphabet.keys():
                    alphabet[letter] += 1
                else:
                    alphabet[letter] = 1
        # print(alphabet)
        return alphabet

    def analyse(self, items):
        # find common letters
        for item in items:
            for i in range(0, len(item.letters)):
                if item.letters[i] not in self.alphabet.keys():
                    continue
                if self.alphabet[item.letters[i]] == 1:
                    continue
                else:
                    item.named_nodes[i] = item.letters[i]

        # throw out letters that only occur in the same word
        for item in items:
            for index, letter in item.named_nodes.items():
                if self.alphabet[letter] == item.letters.count(letter):
                    item.named_nodes[index] = 0

            # this seems to be necessary because you can't delete entries while looping over a dict
            item.named_nodes = {
                key: val for key, val in item.named_nodes.items() if val != 0
            }

            # this is done for convenience, I don't know if it actually will be useful in the future
            item.nodes = list(item.named_nodes.keys())
        return items

    def rank_words(self):
        return sorted(self.items, key=lambda x: len(x.nodes), reverse=True)
