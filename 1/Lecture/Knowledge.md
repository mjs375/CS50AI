# KNOWLEDGE

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
  - P (P is true), ¬Q (Q is false) 
Query: R (We want to know whether R is true or false; Does KB ⊨ R?)
"""
  - To answer the query using the Model Checking algorith, we enumerate all possible models (P, Q, R cols); *then go through every model and check whether it is true given our __Knowledge Base__:*
    - We know P is true in our KB. *Thus we can say that the KB is false in all models where P is not true.*
    - We know that Q is false in our KB. *Thus we can say that the KB is false in all models where Q is true.*
    - Finally, we are left with 2 models (both have P true and Q false, but either R is true or false). *Due to ```(P ∧ ¬Q) → R``` being our Knowledge Base (KB), we know that R is true when P is true and Q is false. 
    - Finally, there is only 1 model where our KB is true; R is also true. By entailment, if R is true in all models where the KB is true, then ```KB ⊨ R```.*
  
| P | Q | R | KB |
|---|---|---|----|
false | false | false | *false*
false | false | true | *false*
false | true | false | *false*
false | true | true | *false*
true | false | false | *false*
true | false | true | **true**
true | true | false | *false*
true | true | true | *false*

### Knowledge & Logic in Code
```python
# Create new classes, each having a name, or a symbol, representing each proposition.
rain = Symbol("rain")  # It is raining.
hagrid = Symbol("hagrid")  # Harry visited Hagrid
dumbledore = Symbol("dumbledore")  # Harry visited Dumbledore

# Save sentences into the KB
knowledge = And(  # Starting from the "And" logical connective, because each proposition represents knowledge that we know to be true.

    Implication(Not(rain), hagrid),  # ¬(It is raining) → (Harry visited Hagrid)

    Or(hagrid, dumbledore),  # (Harry visited Hagrid) ∨ (Harry visited Dumbledore).

    Not(And(hagrid, dumbledore)),  # ¬(Harry visited Hagrid ∧ Harry visited Dumbledore) i.e. Harry did not visit both Hagrid and Dumbledore.

    dumbledore  # Harry visited Dumbledore. Note that while previous propositions contained multiple symbols with connectors, this is a proposition consisting of one symbol. This means that we take as a fact that, in this KB, Harry visited Dumbledore.
    )
```
- To run the __Model Checking algorithm__,  the following info is needed:
  - __Knowledge Base__: used to draw inferences.
  - A __query__: proposition that we are interested in whether it is entailed by the KB or not.
  - __Symbols__: a list of all the symbols ('atomic propositions') used (here, ```rain```, ```hagrid```, ```dumbledore```).
  - __Model__: an assignment of true/false values to symbols.
- The __model checking algorithm__ itself looks like this:
```python
def check_all(knowledge, query, symbols, model):

    # If model has an assignment for each symbol
    # (The logic below might be a little confusing: we start with a list of symbols. The function is recursive, and every time it calls itself it pops one symbol from the symbols list and generates models from it. Thus, when the symbols list is empty, we know that we finished generating models with every possible truth assignment of symbols.)
    if not symbols:

        # If knowledge base is true in model, then query must also be true
        if knowledge.evaluate(model):
            return query.evaluate(model)
        return True
    else:

        # Choose one of the remaining unused symbols
        remaining = symbols.copy()
        p = remaining.pop()

        # Create a model where the symbol is true
        model_true = model.copy()
        model_true[p] = True

        # Create a model where the symbol is false
        model_false = mode.copy()
        model_false[p] = False

        # Ensure entailment holds in both models
        return(check_all(knowledge, query, remaining, model_true) and check_all(knowledge, query, remaining, model_false))
```




