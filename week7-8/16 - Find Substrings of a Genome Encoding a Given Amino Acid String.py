def peptide_encoding_problem(dna, peptide):
    sequence = []
    protein_length = len(peptide)
    for i in range(len(dna) - 3 * protein_length + 1):
        if protein_translation(dna_rna(dna[i:i + protein_length * 3])) == peptide \
                or protein_translation(dna_rna(reverse_sequence(dna[i:i + protein_length * 3]))) == peptide:
            sequence.append(dna[i:i + protein_length * 3])
    return sequence


def protein_translation(rna):
    protein = ""
    for i in range(0, len(rna), 3):
        if rna_codons[rna[i:i + 3]]:
            protein += rna_codons[rna[i:i + 3]]
        else:
            return protein
    return protein


def dna_rna(dna):
    return dna.replace('T', 'U')


def reverse_sequence(seq):
    result = ''
    for i in seq:
        if i == 'A':
            result += 'T'
        elif i == 'C':
            result += 'G'
        elif i == 'G':
            result += 'C'
        elif i == 'T':
            result += 'A'
    return result[::-1]


if __name__ == '__main__':
    data = "".join(open('peptide_encoding.txt')).split()
    # print(data)
    rna_codons = dict()
    with open('codon_table.txt') as f:
        for i in f:
            i = i.split()
            if len(i) > 1:
                rna_codons[i[0]] = i[1]
            else:
                rna_codons[i[0]] = []
    # print(rna_codons)
    for i in peptide_encoding_problem(data[0], data[1]):
        print(i)


