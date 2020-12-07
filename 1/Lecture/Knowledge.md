# KNOWLEDGE: LECTURE 1

```Existing knowledge + logic => conclusions```
- **Knowledge-Based Agents**: *agents that reason by operating internal representations of knowledge. Example:*
  - ```1. If if did NOT rain, Harry visited Hagrid today.```
  - ```2. Harry visited Hagrid OR Dumbledore today, but not both.```
  - ```3. Harry visited Dumbledore today.```
    - => Did it rain today? We can conclude:
  - ```4. Harry did not visit Hagrid.```
  - ```5. It rained today.```

- **Sentence**: *an assertion about the world in a knowledge representation language.*

### Propositional Logic
*based on **```propositions```**, statements about the world that are either ```True``` or ```False```*
- **Symbols**: ```P```, ```Q```, ```R``` are the letters commonly used.
- **Logical Connectives**: *logical symbols that connect propositional symbols in order to reason in a more complex way about the world.*
  - **Not (```¬```)**: *inverses the value of a proposition. E.g. ```P: 'It is raining'``` <> ```¬P: 'It is not raining.'```. Below is a __Truth Table__:*
  
P | ¬P
--|----
false | true
true | false
