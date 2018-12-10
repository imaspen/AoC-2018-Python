__author__ = "Aspen Thompson"
__date__ = "2018-12-02"


def part_one(strings):
    repetitions = [0, 0]
    for string in strings:
        count = {}
        for char in string:
            count[char] = count.get(char, 0) + 1

        if 2 in count.values():
            repetitions[0] += 1
        if 3 in count.values():
            repetitions[1] += 1

    return repetitions[0] * repetitions[1]


def part_two(strings):
    strings_len = len(strings)
    string_len = len(strings[0])

    for i in range(strings_len):
        string = strings[i]

        for j in range(i + 1, strings_len):
            test = strings[j]
            differences = 0
            return_string = ""

            for k in range(string_len):
                if string[k] == test[k]:
                    return_string += string[k]
                else:
                    differences += 1
                    if differences > 1:
                        break

            if differences < 2:
                return return_string
