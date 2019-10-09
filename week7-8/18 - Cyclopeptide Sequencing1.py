'''
CyclopeptideSequencing(Spectrum)
        candidate_peptides ← a set containing only the empty peptide
        FinalPeptides ← empty list of strings
        while candidate_peptides is nonempty
            candidate_peptides ← Expand(candidate_peptides)
            for each peptide Peptide in candidate_peptides
                if Mass(Peptide) = ParentMass(Spectrum)
                    if Cyclospectrum(Peptide) = Spectrum and Peptide is not in ﻿FinalPeptides
                        append Peptide to FinalPeptides
                    remove Peptide from candidate_peptides
                else if Peptide is not consistent with Spectrum
                    remove Peptide from candidate_peptides
        return FinalPeptides
'''


def cyclopeptide_sequencing(spectrum):
    candidate_peptides = ['']
    final_peptides = []
    while candidate_peptides:
        candidate_peptides = expand(candidate_peptides)
        minus = []
        for i in range(len(candidate_peptides)):
            peptide = candidate_peptides[i]
            if get_peptide_mass(peptide) == max(spectrum):
                if cyclic_spectrum(peptide, amino_acid_mass_table) == spectrum:
                    final_peptides.append(peptide)
                    minus.append(peptide)
            elif not consistent(peptide, spectrum):
                minus.append(peptide)
        for i in range(len(minus)):
            candidate_peptides.remove(minus[i])

    mass_final_peptide = []
    for peptide in final_peptides:
        mass_peptides = []
        for i in range(len(peptide)):
            mass_peptides.append(amino_acid_mass_table[peptide[i]])
        mass_final_peptide.append('-'.join(str(i) for i in mass_peptides))
    return ' '.join(str(i) for i in mass_final_peptide)


def expand(peptides):
    new_peptides = []
    for peptide in peptides:
        for key in amino_acid_mass_table:
            new_peptides.append(peptide + key)
    return new_peptides


def get_peptide_mass(peptide):
    mass = 0
    for i in range(len(peptide)):
        mass += amino_acid_mass_table[peptide[i]]
    return mass


def linear_spectrum(peptide):
    prefix_mass = [0 for i in range(len(peptide) + 1)]
    for i in range(len(peptide)):
        prefix_mass[i + 1] = prefix_mass[i] + amino_acid_mass_table[peptide[i]]
    lin_spectrum = []
    for i in range(len(peptide)):
        for j in range(i + 1, len(peptide) + 1):
            lin_spectrum.append(prefix_mass[j] - prefix_mass[i])
    lin_spectrum.append(0)
    lin_spectrum = sorted(lin_spectrum)
    return lin_spectrum


def cyclic_spectrum(peptide, amino_acid_mass_table):
    prefix_mass = [0 for i in range(len(peptide) + 1)]
    for i in range(len(peptide)):
        prefix_mass[i + 1] = prefix_mass[i] + amino_acid_mass_table[peptide[i]]
    peptideMass = prefix_mass[len(peptide)]
    cycl_spectrum = []
    for i in range(len(peptide)):
        for j in range(i + 1, len(peptide) + 1):
            cycl_spectrum.append(prefix_mass[j] - prefix_mass[i])
            if i > 0 and j < len(peptide):
                cycl_spectrum.append(peptideMass - (prefix_mass[j] - prefix_mass[i]))
    cycl_spectrum.append(0)
    cycl_spectrum = sorted(cycl_spectrum)
    return cycl_spectrum


def consistent(peptide, spectrum):
    lin_spectrum = linear_spectrum(peptide)
    for s in lin_spectrum:
        if lin_spectrum.count(s) > spectrum.count(s):
            return False
    return True


if __name__ == '__main__':
    spectrum = list(map(int, open('cyclopeptide_sequencing.txt').readline().split()))
    # print(spectrum)
    amino_acid_mass_table = {'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103, 'I': 113, 'L': 113,
                             'N': 114, 'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137, 'F': 147, 'R': 156,
                             'Y': 163, 'W': 186}
    amino = list(amino_acid_mass_table.keys())
    amino_mass = list(amino_acid_mass_table.values())
    print(cyclopeptide_sequencing(spectrum))
