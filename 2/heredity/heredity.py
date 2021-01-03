# Usage: $ python heredity.py data/[family#.csv]

import csv
import itertools
import os
import sys

"""
GJB2 Gene probabilities calculator.
CS50 AI w/ Python [Harvard]
"""

#--General population probabilities for GJB2, a gene that can cause hearing impairment:
PROBS = {

    #--Unconditional probabilities for having gene (if we know nothing about parents, i.e. distribution in general population):
    "gene": {
        2: 0.01, # 2 copies (of hearing impairment version)
        1: 0.03, # 1 copy
        0: 0.96 # 0 copies (96% in gen. pop.)
    },

    #--True/False if person EXPRESSES impairment based on gene nums:
    "trait": {

        #--Probability of trait given two copies of gene
        2: {
            True: 0.65, # likeliest to express with 2 copies of gene...
            False: 0.35 # even with 2 copies, not assured to have hearing impairment...
        },

        #--Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        #--Probability of trait given no gene
        0: {
            True: 0.01, # highly unlikely to express if 0 genes...
            False: 0.99
        }
    },

    #--Mutation probability (1% chance of parent's gene mutated when passed on )
    "mutation": 0.01
}






def main():

    #--Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    #--Load csv data into a dictionary:
    people = load_data(sys.argv[1])

    #--Keep track of gene and trait probabilities for each person (blank to start, will update each round):
    probabilities = {
        person: {
            "gene": {
                2: 0,
                1: 0,
                0: 0
            },
            "trait": {
                True: 0,
                False: 0
            }
        }
        for person in people # DICT comprehension
            # dict = {person{...} for person in people}
    }

    #--Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        #--Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        #--Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                #--Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    #--Ensure probabilities sum to 1
    normalize(probabilities)

    #--Print results
    for person in people:
        print(f"{person}:")
        for field in probabilities[person]:
            print(f"  {field.capitalize()}:")
            for value in probabilities[person][field]:
                p = probabilities[person][field][value]
                print(f"    {value}: {p:.4f}")


def load_data(filename):
    """
    Load gene and trait data from a file into a dictionary.
    File assumed to be a CSV containing fields name, mother, father, trait.
    mother, father must both be blank, or both be valid names in the CSV.
    trait should be 0 or 1 if trait is known, blank otherwise.
    """
    data = dict()
    with open(filename) as f:
        reader = csv.DictReader(f)
        for row in reader:
            name = row["name"]
            data[name] = {
                "name": name,
                "mother": row["mother"] or None,
                "father": row["father"] or None,
                "trait": (True if row["trait"] == "1" else
                          False if row["trait"] == "0" else None)
            }
    return data


def powerset(s):
    """
    Return a list of all possible subsets of set s.
    """
    s = list(s)
    return [
        set(s) for s in itertools.chain.from_iterable(
            itertools.combinations(s, r) for r in range(len(s) + 1)
        )
    ]


def gene_count(person, one_gene, two_genes):
    """
    Matches person in one_gene, two_genes, or (no list) to an actual number.
    """
    if person in one_gene:
        return 1
    elif person in two_genes:
        return 2
    else:
        return 0
#
#
#
def inherit(parent_genes, inherit):
    """
    Returns probability of inheritance for child from specific parent.
    """
    #--No genes, can only mutate to have gene or not:
    if parent_genes == 0:
        if inherit: #--trait is expressed:
            return PROBS["mutation"]
        else: #--trait is not expressed:
            return 1 - PROBS["mutation"]
    #
    #--50/50 shot of passing on if 1 gene in parent:
    elif parent_genes == 1:
        return 0.5 # always 50/50 %
    #
    #--Parent has 2 genes, almost definitely will pass on (minus small mutation prob. rate):
    elif parent_genes == 2:
        if inherit:
            return 1 - PROBS["mutation"]
        else:
            return PROBS["mutation"]




def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability.
    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    #--Initialize probability for this 'round' (specific situation), to be modified...
    probability = 1.0

    #--Loop all people in pop. data:
    for person in people:
        #
        #--Get Person's number of genes
        gene_num = gene_count(person, one_gene, two_genes)
        #
        #--Get whether that Person has trait exhibited or not:
        if person in have_trait: # check list
            has_trait = True # hearing impairment expressed
        else:
            has_trait = False # no hearing impairment
        #
        #--Parent data (check, could be None):
        mom = people[person]['mother']
        dad = people[person]['father']


        #--Unconditional probability: for person IF NOT parent data:
        if dad is None and mom is None:
            probability *= PROBS["trait"][gene_num][has_trait] * PROBS["gene"][gene_num]
        #
        #               O R :
        #
        #--Conditional probability: for person IF parent data available (child):
        else:
            #--Get mom & dad's num of genes:
            mom_genes = gene_count(mom, one_gene, two_genes)
            dad_genes = gene_count(dad, one_gene, two_genes)

            #
            # Child gets probability from ONE of the following paths:
            #

            #--Child has 0 copies, 1 way to get (not mom AND not dad)
            if gene_num == 0:
                probability *= inherit(mom_genes, False) * inherit(dad_genes, False)

            #--Child has 1 copy, 2 ways to get (mom not dad, OR dad not mom):
            elif gene_num == 1:
                probability *= inherit(mom_genes, True) * inherit(dad_genes, False) + inherit(mom_genes, False) * inherit(dad_genes, True)

            #--Child has 2 copies, 1 way to get (mom AND dad):
            elif gene_num == 2:
                probability *= inherit(mom_genes, True) * inherit(dad_genes, True)

            #--Lastly, the probability of child having the trait expressed or not with their given genes:
            probability *= PROBS["trait"][gene_num][has_trait]
    #
    #
    #print(f">>>>>>> {probability}")
    return probability


def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # p => the joint probability of this last round of situations:

    #--Loop over family to update:
    for person in probabilities:
        #--How many genes does person have?
        gene_num = gene_count(person, one_gene, two_genes)
        #
        #--Does person have trait expressed or not?
        if person in have_trait:
            has_trait = True
        else:
            has_trait = False
        #
        #--Update the trait & gene probability distributions:
        probabilities[person]["gene"][gene_num] += p
        probabilities[person]["trait"][has_trait] += p

    # (return nothing, just an update function)
    # raise NotImplementedError


def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    #--Loop over family in dataset one last time to normalize prob values:
    for person in probabilities:

        #--Get sums of trait/gene probabilities:
        sum_gene = sum(probabilities[person]["gene"].values())
        sum_trait = sum(probabilities[person]["trait"].values())
        #
        #--Normalize by getting proportion of each (divide part by whole to get a decimal):
        for trait in probabilities[person]["trait"]:
            probabilities[person]["trait"][trait] /= sum_trait
        #
        for gene in probabilities[person]["gene"]:
            probabilities[person]["gene"][gene] /= sum_gene
    #
    # return nothing, just an update
    # raise NotImplementedError


# # # # # # # # # # # # # # # #
                              #
if __name__ == "__main__":    #
    os.system('reset')        #
    main()                    #
                              #
# # # # # # # # # # # # # # # #


#
