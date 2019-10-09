"""
LeaderboardCyclopeptideSequencing(Spectrum, N)
    Leaderboard ← set containing only the empty peptide
    LeaderPeptide ← empty peptide
    while Leaderboard is non-empty
        Leaderboard ← Expand(Leaderboard)
        for each Peptide in Leaderboard
            if Mass(Peptide) = ParentMass(Spectrum)
                if Score(Peptide, Spectrum) > Score(LeaderPeptide, Spectrum)
                    LeaderPeptide ← Peptide
            else if Mass(Peptide) > ParentMass(Spectrum)
                remove Peptide from Leaderboard
        Leaderboard ← Trim(Leaderboard, Spectrum, N)
    output LeaderPeptide
"""


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

def get_parent_mass(spectrum):
    return spectrum[-1]


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


def linear_score(peptide, spectrum):
    ls = linear_spectrum(peptide)
    cs = spectrum.copy()
    score = 0
    for c in ls:
        if c in cs:
            score += 1
            cs.remove(c)
    return score


def trim(leaderboard, spectrum, N):
    scores = []
    if len(leaderboard) < N:
        leaderboard_to_return = leaderboard
    else:
        for pep in leaderboard:
            scores.append(linear_score(pep, spectrum))
        scores.sort(reverse=True)
        score_min = scores[N - 1]
        valid_pep = []
        for i, pep in enumerate(leaderboard):
            if linear_score(pep, spectrum) >= score_min:
                valid_pep.append(i)
        leaderboard_to_return = []
        for k in valid_pep:
            leaderboard_to_return.append(leaderboard[k])
    return leaderboard_to_return


def leaderboard_cyclopeptide_sequencing(spectrum, n):
    leaderboard = ['']
    leader_peptide = ''
    leader_peptide_score = 0
    while leaderboard:
        leaderboard = expand(leaderboard)
        loop = list(leaderboard)
        for peptide in loop:
            mass = get_peptide_mass(peptide)
            parent_mass = get_parent_mass(spectrum)
            if mass == parent_mass:
                score = linear_score(peptide, spectrum)
                if score > leader_peptide_score:
                    leader_peptide = peptide
                    leader_peptide_score = score
            elif mass > parent_mass:
                leaderboard.remove(peptide)
        leaderboard = trim(leaderboard, spectrum, n)
    return leader_peptide


def leaderboard_cyclopeptide(spectrum, n):
    leader_peptide = leaderboard_cyclopeptide_sequencing(spectrum, n)
    return [amino_acid_mass_table[amino_acid] for amino_acid in leader_peptide]


if __name__ == '__main__':
    amino_acid_mass_table = {'G': 57, 'A': 71, 'S': 87, 'P': 97, 'V': 99, 'T': 101, 'C': 103, 'I': 113, 'L': 113,
                             'N': 114, 'D': 115, 'K': 128, 'Q': 128, 'E': 129, 'M': 131, 'H': 137, 'F': 147, 'R': 156,
                             'Y': 163, 'W': 186}
    with open('leaderboard_cyclopeptide_sequencing.txt') as f:
        n = int(f.readline())
        spectrum = list(map(int, f.readline().split()))
    leader_peptide = leaderboard_cyclopeptide_sequencing(spectrum, n)
    leader_peptide_mass = []
    for i in leader_peptide:
        leader_peptide_mass.append(amino_acid_mass_table[i])
    print('-'.join([str(i) for i in leader_peptide_mass]))
# 71-101-99-128-163-186-128-113-147-113-131-87-115-131