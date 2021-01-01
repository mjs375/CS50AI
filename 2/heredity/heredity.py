# Usage: $ python heredity.py [data.csv]

import csv
import itertools
import os
import sys

#--GJB2 Gene probabilities DICT{}:
PROBS = {

    #--Unconditional probabilities for having gene (if we know nothing about person's parents, i.e. distribution in general population)
    "gene": {
        2: 0.01, # 2 copies (of hearing impairment version)
        1: 0.03, # 1 copy
        0: 0.96 # 0 copies (96% chance in gen. pop.)
    },

    #--Yes/No person expresses impairment based on gene
    "trait": {

        # Probability of trait given two copies of gene
        2: {
            True: 0.65,
            False: 0.35
        },

        # Probability of trait given one copy of gene
        1: {
            True: 0.56,
            False: 0.44
        },

        # Probability of trait given no gene
        0: {
            True: 0.01,
            False: 0.99
        }
    },

    # Mutation probability (1% chance of mutating)
    "mutation": 0.01
}


def main():

    # Check for proper usage
    if len(sys.argv) != 2:
        sys.exit("Usage: python heredity.py data.csv")
    #--Load the population data into a people DICT{}:
    people = load_data(sys.argv[1])

    # Keep track of gene and trait probabilities for each person
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
            # dict = {x for x in people} # except X is a big process...!
    }

    # Loop over all sets of people who might have the trait
    names = set(people)
    for have_trait in powerset(names):

        # Check if current set of people violates known information
        fails_evidence = any(
            (people[person]["trait"] is not None and
             people[person]["trait"] != (person in have_trait))
            for person in names
        )
        if fails_evidence:
            continue

        # Loop over all sets of people who might have the gene
        for one_gene in powerset(names):
            for two_genes in powerset(names - one_gene):
                # Update probabilities with new joint probability
                p = joint_probability(people, one_gene, two_genes, have_trait)
                update(probabilities, one_gene, two_genes, have_trait, p)

    # Ensure probabilities sum to 1
    normalize(probabilities)

    # Print results
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
    Helper function for joint_probability.
    """
    #--Get that person's num copies of gene from parameter variables:
    if person in one_gene:
        #print(f"{person} 1 gene")
        return 1
    elif person in two_genes:
        #print(f"{person} 2 genes")
        return 2
    else: # zero_genes:
        #print(f"{person} 0 genes")
        return 0

def inherit(parent_genes, if_inherited):
    """
    Given num of parent genes + if gene is inherited, calc probability of inheritance from this parent (mutations, &c.)
    """
    #--no genes, only have mutation prob:
    if parent_genes == 0:
        if if_inherited:
            return PROBS['mutation'] # e.g. 0.01
        else: # not if_inherited:
            return 1 - PROBS['mutation'] # e.g. 0.99

    #--parent has 1 gene, 50% chance of passing on:
    elif parent_genes == 1:
        return 0.5

    #--parent has 2 genes:
    elif parent_genes == 2:
        if if_inherited:
            return 1 - PROBS['mutation']
        else:
            return PROBS['mutation']



def joint_probability(people, one_gene, two_genes, have_trait):
    """
    Compute and return a joint probability (multiple events!).

    The probability returned should be the probability that
        * everyone in set `one_gene` has one copy of the gene, and
        * everyone in set `two_genes` has two copies of the gene, and
        * everyone not in `one_gene` or `two_gene` does not have the gene, and
        * everyone in set `have_trait` has the trait, and
        * everyone not in set` have_trait` does not have the trait.
    """
    #--Initialize probability, to be modified...
    probability = 1


    #--Loop all people in pop. data:
    for person in people:
        #--Individual person's probability:
        #Xprobability = 1.0
        #--Get that person's num copies of gene from parameter variables:
        gene_num = gene_count(person, one_gene, two_genes)
        #
        #--Get whether that person has trait exhibited or not (T/F):
        has_trait = person in have_trait


        #--Unconditional Probability for person IF NO parent data:
        if people[person]['father'] is None and people[person]['mother'] is None:
            #print(f"Unconditional Probability for {person}:",PROBS['gene'][gene_num], f"% chance has that {gene_num} genes and", PROBS['trait'][gene_num][has_trait], f"% chance  {has_trait} trait with genes.")
            probability *= PROBS['trait'][gene_num][has_trait] * PROBS['gene'][gene_num]
        #
        #
        #--Conditional Probability for person IF a child (parent data):
        else:
            #--Get mom & dad:
            mom = people[person]['mother']
            dad = people[person]['father']
            #--Get mom & dad 's num of genes
            mom_genes = gene_count(mom, one_gene, two_genes)
            dad_genes = gene_count(dad, one_gene, two_genes)



            #--Child has 1 way to inherit 0 copies (not mom AND not dad):
            if gene_num == 0:
                prob_mom = inherit(mom_genes, False)
                prob_dad = inherit(dad_genes, False)
                #
                probability *= prob_mom * prob_dad

            #--Child has 2 ways to inherit 1 copy (mom not dad OR dad not mom):
            elif gene_num == 1:
                prob_mom1 = inherit(mom_genes, False)
                prob_mom2 = inherit(mom_genes, True)
                prob_dad1 = inherit(dad_genes, False)
                prob_dad2 = inherit(dad_genes, True)
                #
                probability *= ((prob_mom1 * prob_dad2) + (prob_mom2 * prob_dad1))

            #--Child has 1 way to inherit 2 copies (mom AND dad):
            elif gene_num == 2: # genes_num == 2:
                prob_mom = inherit(mom_genes, True)
                prob_dad = inherit(mom_genes, True)
                #
                probability *= prob_mom * prob_dad

            #
            #--Probability of [child]person having the trait with their genes:
            probability *= PROBS['trait'][gene_num][has_trait]

        #--Add person's probability to JOINT PROB variable:
        #probability *= Xprobability
        #--End of loop round 'person':
        #print(f">>> {person}'s probability:", Xprobability)
        #
    #
    #--Calculations over, get JOINT probability:
    #print("\n>>> JOINT Probability:", probability, "\n")
    return probability
    #raise NotImplementedError















def update(probabilities, one_gene, two_genes, have_trait, p):
    """
    Add to `probabilities` a new joint probability `p`.
    Each person should have their "gene" and "trait" distributions updated.
    Which value for each distribution is updated depends on whether
    the person is in `have_gene` and `have_trait`, respectively.
    """
    # p => the joint probability of this round of situations
    #--Loop over family to update
    for person in probabilities:

        #--How many genes does 'person' have? (which key to update):
        gene_num = gene_count(person, one_gene, two_genes)
        #
        #--Does 'person' have trait expressed? (which key to update):
        has_trait = person in have_trait

        #--Update the trait/gene probability distributions:
        probabilities[person]["gene"][gene_num] += p
        probabilities[person]["trait"][has_trait] += p

    #return nothing, just updating
    #raise NotImplementedError



def normalize(probabilities):
    """
    Update `probabilities` such that each probability distribution
    is normalized (i.e., sums to 1, with relative proportions the same).
    """
    #print(probabilities)
    #--Loop over family in dataset:
    for person in probabilities:

        #--Get trait/gene probs|values sums:
        sum_trait = sum(probabilities[person]['trait'].values())
        sum_gene = sum(probabilities[person]['gene'].values())

        #-- Normalize by getting proportions (divide part by whole):
        for trait in probabilities[person]['trait']:
            probabilities[person]['trait'][trait] /= sum_trait
        for gene in probabilities[person]['gene']:
            probabilities[person]['gene'][gene] /= sum_gene
    # return nothing, just an update
    # raise NotImplementedError











if __name__ == "__main__":
    os.system('reset')
    main()
