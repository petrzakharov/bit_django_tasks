from input import tariff_info


def main(data, indent, dictionary):
    for element in data:
        if element == 'children':
            indent += 1
            main(data[element], indent, False)
        elif isinstance(element, dict):
            main(element, indent, True)
        elif isinstance(element, str):
            print('\t' * indent, element, '\n')
            if dictionary:
                main(data[element], indent, True)


if __name__ == '__main__':
    main(tariff_info, 0, True)
