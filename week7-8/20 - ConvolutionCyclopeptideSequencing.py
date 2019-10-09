def get_spectral_convolution_dict(spectrum):
    spectrum = sorted(spectrum)
    convolution_dict = {}
    for i in range(len(spectrum) - 1):
        for j in range(i, len(spectrum)):
            mass = spectrum[j] - spectrum[i]
            if mass < 57 or mass > 200:
                continue
            if mass in convolution_dict:
                convolution_dict[mass] += 1
            else:
                convolution_dict[mass] = 1
    return convolution_dict


def get_top_m_elements(convolution_dict, m):
    convolution = [(key, val) for key, val in convolution_dict.items()]
    sorted_convolution = sorted(convolution, key=lambda entry: entry[1], reverse=True)
    trim_pos = m-1
    for trim_pos in range(m - 1, len(sorted_convolution) - 1):
        if sorted_convolution[trim_pos][1] > sorted_convolution[trim_pos + 1][1]:
            break
    return [i[0] for i in sorted_convolution[:trim_pos + 1]]


def expand(peptides, amino_acid_mass_list):
    new_peptides = []
    for peptide in peptides:
        for mass in amino_acid_mass_list:
            new_peptide = list(peptide)
            new_peptide.append(mass)
            new_peptides.append(new_peptide)
    return new_peptides


def get_parent_mass(spectrum):
    return spectrum[-1]


def make_score(peptide, spectrum):
    ls = cyclospectrum(peptide)
    cs = spectrum.copy()
    score = 0
    for c in ls:
        if c in cs:
            score += 1
            cs.remove(c)
    return score


def cyclospectrum(peptide):
    prefix_mass = [0]
    for i in range(len(peptide)):
        prefix_mass.append(prefix_mass[i]+peptide[i])

    theoretical_spectrum = [0]
    for i in range(len(prefix_mass) - 1):
        for j in range(i + 1, len(prefix_mass)):
            theoretical_spectrum.append(prefix_mass[j]-prefix_mass[i])
            if i > 0 and j < len(prefix_mass)-1:
                theoretical_spectrum.append(prefix_mass[-1] - (prefix_mass[j] - prefix_mass[i]))
    return sorted(theoretical_spectrum)



def linear_spectrum(peptide):
    prefix_mass = [0 for i in range(len(peptide) + 1)]
    for i in range(len(peptide)):
        prefix_mass[i + 1] = prefix_mass[i] + peptide[i]
    lin_spectrum = []
    for i in range(len(peptide)):
        for j in range(i + 1, len(peptide) + 1):
            lin_spectrum.append(prefix_mass[j] - prefix_mass[i])
    lin_spectrum.append(0)
    lin_spectrum = sorted(lin_spectrum)
    return lin_spectrum


def linearscore(peptide, spectrum):
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
            scores.append(linearscore(pep, spectrum))
        scores.sort(reverse=True)
        score_min = scores[N - 1]
        valid_pep = []
        for i, pep in enumerate(leaderboard):
            if linearscore(pep, spectrum) >= score_min:
                valid_pep.append(i)
        leaderboard_to_return = []
        for k in valid_pep:
            leaderboard_to_return.append(leaderboard[k])
    return leaderboard_to_return


def leaderboard_cyclopeptide_sequencing(spectrum, n, amino_acid_mass_list):
    leaderboard = [[]]
    leader_peptide = ''
    leader_peptidescore = 0
    while leaderboard:
        leaderboard = expand(leaderboard, amino_acid_mass_list)
        loop = list(leaderboard)
        for peptide in loop:
            mass = sum(peptide)
            parent_mass = get_parent_mass(spectrum)
            if mass == parent_mass:
                score = make_score(peptide, spectrum)
                if score > leader_peptidescore:
                    leader_peptide = peptide
                    leader_peptidescore = score
            elif mass > parent_mass:
                leaderboard.remove(peptide)
        leaderboard = trim(leaderboard, spectrum, n)
    return leader_peptide


def convolution_cyclopeptide_sequencing(m, n, spectrum):
    spectrum = sorted(spectrum)
    convolution_dict = get_spectral_convolution_dict(spectrum)
    top_amino_acid_mass = get_top_m_elements(convolution_dict, m)
    return leaderboard_cyclopeptide_sequencing(spectrum, n, top_amino_acid_mass)


if __name__ == '__main__':
    with open('convolution_cyclopeptide_sequencing.txt') as f:
        m = int(f.readline())
        n = int(f.readline())
        spectrum = list(map(int, f.readline().split()))
    print('-'.join([str(i) for i in convolution_cyclopeptide_sequencing(m, n, spectrum)]))