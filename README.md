# Bioinformatics-Algorithms
Authors:

• Pavel Pevzner (University of California, San Diego)

• Phillip E. C. Compeau (University of California, San Diego)

Resources:

• bioinformaticsalgorithms.com – Lecture Videos

• Stepik.org – Interactive Text

• Rosalind.info – Programming Exercises


# 1 - Clump Finding Problem
Given integers L and t, a string Pattern forms an (L, t)-clump inside a (larger) string Genome if there is an interval of Genome of length L in which Pattern appears at least t times. For example, TGCA forms a (25,3)-clump in the following Genome: gatcagcataagggtcccTGCAATGCATGACAAGCCTGCAgttgttttac.

Clump Finding Problem
Find patterns forming clumps in a string.

Given: A string Genome, and integers k, L, and t.

Return: All distinct k-mers forming (L, t)-clumps in Genome.
