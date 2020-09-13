"""
This calculates word frequency usage for each doctor. Given a line of words, it will predict which doctor was most likely
to have spoken so.
"""
import os, re, math
from collections import Counter

EPSILON = 0.00000001


# Returns an int
def get_doctor_num(doctor_name):
    return int(re.findall('\d+', doctor_name)[0])


def create_word_probability_map(file_path):
    dialogue_text = open(file_path, 'r', encoding='utf-8')

    words = [line.split(',') for line in dialogue_text.readlines()]
    words = words[0]
    words.remove('')
    num_words = len(words)

    word_prob = Counter(words)

    for entry in word_prob:
        word_prob[entry] = word_prob[entry] / num_words

    dialogue_text.close()
    return word_prob


def create_doctor_prob_map(folder_root):
    word_prob_dict = {}

    for folder in os.listdir(folder_root):
        dialogue_path = folder_root + "\\" + folder + "\\" + folder + "_dialogue.txt"
        word_prob_dict[get_doctor_num(folder)] = create_word_probability_map(dialogue_path)

    return word_prob_dict


def create_input_word_count(line):

    word_list = re.split('[,?.!;()\s]', line.lower())
    word_list = list(filter(None, word_list))

    return Counter(word_list)


def get_word_prob(doctor_word_prob_dict, doctor_num, word):
    if word in doctor_word_prob_dict[doctor_num]:
        return doctor_word_prob_dict[doctor_num][word]
    return EPSILON


def get_log_quote_prob(input_word_count_map, doctor_word_prob_dict, doctor_num):
    log_prob = 0
    for word in input_word_count_map:
        input_word_count = input_word_count_map[word]
        p_i = get_word_prob(doctor_word_prob_dict, doctor_num, word)
        log_prob += input_word_count * math.log(p_i)

    return log_prob


def main():
    dialogue_root = 'C:\\Users\\angel\\GitHub\\doctor-who-dialogue-tracker\\data\\doctor_who_dialogue'

    # Store each doctor's word probability in a dictionary with a key and the value as the Counter object
    doctor_word_prob_dict = create_doctor_prob_map(dialogue_root)

    user_input = input("Enter quote here: ")
    input_word_count_map = create_input_word_count(user_input)

    doctor_prob = {}

    for doctor_num in range(1, 14):
        doctor_prob[doctor_num] = get_log_quote_prob(input_word_count_map, doctor_word_prob_dict, doctor_num)

    # Sort by most likely, then alphabetically:
    doctor_prob = sorted(doctor_prob.items(), key=lambda kv: (-kv[1], kv[0]))


    print("In order from most likely to least likely: ")
    for i in range(len(doctor_prob) - 1):
        print("Doctor " + str(doctor_prob[i][0]))

# When executed directly, then condition is true. If executed indirectly, like it's imported, then the if statement
# evaluates to false.
if __name__ == "__main__":
    main()