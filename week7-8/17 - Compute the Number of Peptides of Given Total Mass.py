def count_peptide(m):
    count = 0
    for i in amino:
        if (m - amino_dict[i]) in mass_dict.keys():
            count += mass_dict[(m - amino_dict[i])]
        elif m - amino_dict[i] < 0:
            break
        elif m - amino_dict[i] == 0:
            count += 1
            return count
        elif m - amino_dict[i] > 0:
            count += count_peptide(m - amino_dict[i])
    mass_dict[m] = count
    # print(count)
    return count


if __name__ == '__main__':
    m = int("".join(open('counting_peptides.txt')))
    amino_dict = {'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103, 'I': 113, \
                  'N': 114, 'D': 115, 'K': 128, 'E': 129, 'M': 131, \
                  'H': 137, 'F': 147, 'R': 156, 'Y': 163, 'W': 186}
    amino = list(amino_dict.keys())
    amino_mass = list(amino_dict.values())
    mass_dict = {}
    ans_num = count_peptide(m)
    # print(mass_dict)
    print(ans_num)
