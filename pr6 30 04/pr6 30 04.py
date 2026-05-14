from itertools import combinations


VARIABLE_NAMES = ("A", "B", "C", "D")


def gray_codes(bits_count):
    if bits_count == 0:
        return [""]
    if bits_count == 1:
        return ["0", "1"]
    previous = gray_codes(bits_count - 1)
    return ["0" + code for code in previous] + ["1" + code for code in reversed(previous)]


def parse_row_values(raw_line, expected_length):
    cleaned = raw_line.replace(",", " ").strip()
    if not cleaned:
        raise ValueError("Строка не может быть пустой.")

    if " " not in cleaned and len(cleaned) == expected_length:
        values = list(cleaned)
    else:
        values = cleaned.split()

    normalized = [value.lower() for value in values]
    if len(normalized) != expected_length:
        raise ValueError(f"Нужно ввести ровно {expected_length} значений.")

    for value in normalized:
        if value not in {"0", "1"}:
            raise ValueError("Допустимые символы: 0, 1.")
    return normalized


def bits_to_index(bits):
    return int(bits, 2)


def index_to_pattern(index, width):
    return tuple(format(index, f"0{width}b"))


def combine_patterns(left, right):
    difference_count = 0
    result = []

    for left_bit, right_bit in zip(left, right):
        if left_bit == right_bit:
            result.append(left_bit)
            continue
        if left_bit == "-" or right_bit == "-":
            return None
        difference_count += 1
        result.append("-")
        if difference_count > 1:
            return None

    if difference_count != 1:
        return None
    return tuple(result)


def find_prime_implicants(terms, variables_count):
    current_level = {index_to_pattern(term, variables_count) for term in terms}
    prime_implicants = set()

    while current_level:
        used = set()
        next_level = set()
        current_list = sorted(current_level)

        for index, left in enumerate(current_list):
            for right in current_list[index + 1:]:
                combined = combine_patterns(left, right)
                if combined is not None:
                    used.add(left)
                    used.add(right)
                    next_level.add(combined)

        prime_implicants.update(pattern for pattern in current_level if pattern not in used)
        current_level = next_level

    return sorted(prime_implicants)


def pattern_covers_term(pattern, term):
    bits = format(term, f"0{len(pattern)}b")
    return all(pattern_bit == "-" or pattern_bit == bit for pattern_bit, bit in zip(pattern, bits))


def implicant_literals_count(pattern):
    return sum(bit != "-" for bit in pattern)


def choose_minimal_cover(prime_implicants, required_terms):
    coverage = {
        term: [index for index, pattern in enumerate(prime_implicants) if pattern_covers_term(pattern, term)]
        for term in required_terms
    }

    selected = set()
    for indexes in coverage.values():
        if len(indexes) == 1:
            selected.add(indexes[0])

    uncovered = set(required_terms)
    for index in selected:
        uncovered -= {term for term in uncovered if pattern_covers_term(prime_implicants[index], term)}

    if not uncovered:
        return sorted(selected)

    remaining = [
        index
        for index, pattern in enumerate(prime_implicants)
        if index not in selected and any(pattern_covers_term(pattern, term) for term in uncovered)
    ]

    best_combo = None
    best_score = None

    for size in range(len(remaining) + 1):
        found_at_this_size = False
        for combo in combinations(remaining, size):
            covered = set()
            for index in combo:
                covered.update(term for term in uncovered if pattern_covers_term(prime_implicants[index], term))
            if covered != uncovered:
                continue

            found_at_this_size = True
            total_literals = sum(implicant_literals_count(prime_implicants[index]) for index in combo)
            lexical_key = tuple("".join(prime_implicants[index]) for index in combo)
            score = (size, total_literals, lexical_key)
            if best_score is None or score < best_score:
                best_score = score
                best_combo = combo

        if found_at_this_size:
            break

    if best_combo is None:
        raise RuntimeError("Не удалось покрыть все наборы функции.")

    return sorted(selected | set(best_combo))


def minimize_terms(required_terms, variables_count):
    if not required_terms:
        return []

    prime_implicants = find_prime_implicants(sorted(set(required_terms)), variables_count)
    indexes = choose_minimal_cover(prime_implicants, sorted(required_terms))
    return [prime_implicants[index] for index in indexes]


def index_to_minterm(index, variable_names):
    bits = format(index, f"0{len(variable_names)}b")
    literals = [variable if bit == "1" else f"!{variable}" for variable, bit in zip(variable_names, bits)]
    return "(" + " & ".join(literals) + ")"


def index_to_maxterm(index, variable_names):
    bits = format(index, f"0{len(variable_names)}b")
    literals = [variable if bit == "0" else f"!{variable}" for variable, bit in zip(variable_names, bits)]
    return "(" + " || ".join(literals) + ")"


def join_dnf(terms):
    return " || ".join(terms) if terms else "0"


def join_cnf(clauses):
    return " & ".join(clauses) if clauses else "1"


def build_map(num_vars):
    row_bits = num_vars // 2
    col_bits = num_vars - row_bits
    row_codes = gray_codes(row_bits)
    col_codes = gray_codes(col_bits)
    row_vars = VARIABLE_NAMES[:row_bits]
    col_vars = VARIABLE_NAMES[row_bits:num_vars]

    print("Введите значения карты Карно в порядке серого кода.")
    print(f"Строки ({', '.join(row_vars) if row_vars else '-'}): {' '.join(row_codes)}")
    print(f"Столбцы ({', '.join(col_vars) if col_vars else '-'}): {' '.join(col_codes)}")
    print("Допустимые значения ячеек: 0, 1")

    ones = []
    zeros = []

    for row_code in row_codes:
        while True:
            row_name = row_code if row_code else "-"
            raw_line = input(f"Значения для строки {row_name}: ")
            try:
                values = parse_row_values(raw_line, len(col_codes))
                break
            except ValueError as error:
                print(f"Ошибка: {error}")

        for col_code, value in zip(col_codes, values):
            assignment_bits = row_code + col_code
            index = bits_to_index(assignment_bits)
            if value == "1":
                ones.append(index)
            else:
                zeros.append(index)

    return row_codes, col_codes, row_vars, col_vars, sorted(ones), sorted(zeros)


def print_result(title, expression):
    print(f"{title}: {expression}")


def main():
    while True:
        try:
            num_vars = int(input("Введите количество переменных (2-4): ").strip())
        except ValueError:
            print("Ошибка: нужно ввести целое число.")
            continue

        if 2 <= num_vars <= 4:
            break
        print("Ошибка: поддерживается только 2, 3 или 4 переменные.")

    variables = VARIABLE_NAMES[:num_vars]
    row_codes, col_codes, row_vars, col_vars, ones, zeros = build_map(num_vars)

    print()
    if ones:
        sdnf = join_dnf([index_to_minterm(index, variables) for index in ones])
    else:
        sdnf = "0"

    if zeros:
        sknf = join_cnf([index_to_maxterm(index, variables) for index in zeros])
    else:
        sknf = "1"

    print_result("СДНФ", sdnf)
    print_result("СКНФ", sknf)


if __name__ == "__main__":
    main()
