# KNOWLEDGE: LECTURE 1

```Existing knowledge + logic => conclusions```
- **Knowledge-Based Agents**: *agents that reason by operating internal representations of knowledge (e.g. people or AI!), using some sort of algorithm. Example (sentences 4 & 5 are inferred from sentences 1-3):*
  - **```1. If if did NOT rain, Harry visited Hagrid today.```**
  - **```2. Harry visited Hagrid OR Dumbledore today, but not both.```**
  - **```3. Harry visited Dumbledore today.```**
    - *```4. Harry did not visit Hagrid.```*
    - *```5. It rained today.```*

- **Sentence**: *an assertion about the world in a knowledge representation language.*

### Propositional Logic
*based on **```propositions```**, statements about the world that are either ```True``` or ```False```*
- **Symbols**: ```P```, ```Q```, ```R``` are the letters commonly used.
- **Logical Connectives**: *logical symbols that connect propositional symbols in order to reason in a more complex way about the world.*
  - **Not (```¬```)**: *inverses the value of a proposition. E.g. ```P: 'It is raining'``` <> ```¬P: 'It is not raining.'```. Below is a __Truth Table__:*
  
| P | ¬P |
|--|----|
false | true
true | false

  - **And (```∧```)**: *when two propositions are connected by ```∧```, the resulting proposition ```P ∧ Q``` is ```true``` only when/if __both__ ```P``` and ```Q``` are true.*
  
| P | Q | P ∧ Q |
|---|---|-----|
false | false | false
false | true | false
true | false | false
true | true | true

  - **Or (```∨```)**: *```true``` as long as __either__ of its arguments is true. For ```P ∨ Q``` to be true, at least 1 of ```P``` or ```Q``` must be true.*
    - **Inclusive Or**: ```true``` if any of ```P```, ```Q```, or ```P ∧ Q``` is ```true```.
    - **Exclusive Or**: ```P ∨ Q``` is ```false``` if ```P ∧ Q``` is true. In other words, it __must__ be ```either/or```, __not__ ```both```. Symbol = ```⊕``` or ```XOR```.
    
  - **Implication (```→```)**: *represents a structure of ```if P, then Q```. E.g. 'P: It is raining', 'Q: I'm indoors' => ```(P → Q)``` means 'If it is raining, I'm indoors.'*
    - **Antecedent**: ```P```. (P is true if Q is true)
    - **Consequent**: ```Q```. (If Q is false, then P is also false).
    
| P | Q | P → Q |
|---|---|-------|
false | false | true
false | true | true
true | false | false
true | true | true

  - **Biconditional (```↔```)**: *(```IFF```) an ```implication``` in both directions. It means 'if and only if'. ```P ↔ Q``` is the same as ```P → Q``` __and__ ```Q → P``` taken together. I.e. 'if it is raining, then I'm indoors' __and__ 'if I'm indoors, then it is raining.' We can infer more from this than a simple implcation.*

| P | Q | P ↔ Q |
|---|---|-------|
false | false | true
false | true | false
true | false | false
true | true | true

- **Model**: *an assignment of a truth value to every proposition. Propositions are statements about the world that can either be true or false. However, knowledge about the world is represented in the truth values of these propositions. How many possible models (truth-value assignments) are there?: ```2^n``` (each variable can be either T/F).*
  - ```P```: 'It is raining' (__proposition__ that is either T/F, not real-world yet).
  - ```Q```: 'It is Tuesday'
    - ```{P=true,Q=false}``` (__model__ about a real scenario, with actual T/F values assigned).

- **Knowledge Base (KB)**: *a set of sentences known by a __knowledge-based agent__ (a person, AI). Form = propositional logic sentences that can be used to make additional inferences about the world.*

- **Entailment (```⊨```)**: *If ```α ⊨ β``` (α entails β), then in any world where α is true, β is true, too. If alpha is true, beta must also be true.*
  - if ```α```: 'It is a Tuesday in January'
  - ```β```: 'It is a Tuesday'
    - we know that ```α ⊨ β```. It is true that if it is a Tuesday in January, we also know it is a Tuesday.
    - Entailment is different from implication. Entailment is a relation that means that if all information in alpha is true, then all information in beta is true as well. Implication rather, is a logical connective between two propositions.

### Inference
```the process of deriving new sentences from known ones```

- **Model Checking algorithm**: *one way to infer new knowledge based on existing knowledge.*
  - To determine if ```KB ⊨ α``` (i.e. answer the question *can we conclude that ```α``` is true based on our knowledge base?*): 
    - 1. Enumerate all possible models
    - 2. If in *every* model where ```KB``` is ```true```, ```α``` is ```true``` also, then KB entails α (```KB  ⊨ α```).
"""
P   It is Tuesday.
Q   It is raining.
R   Harry will go for a run.

KB  (P ∧ ¬Q) → R (in words, P and not Q imply R) 
  - P (P is true) ¬Q (Q is false) 
Query: R (We want to know whether R is true or false; Does KB ⊨ R?)
"""
  - To answer the query using the Model Checking algorith, we enumerate all possible models:
  
| P | Q | R | KB |
|---|---|---|----|
false | false | false |
false | false | true | 
false | true | false | 
false | true | true |
true | false | false |
true | false | true |
true | true | false |
true | true | true |







