# Probabilistic Analysis and Randomized Algorithms

## The hiring problem

**Assistants**:
- HR agency to hire a new office assistant
- You must have always someone hired
- You want the best possible candidates
- If you hire someone you must fire another

**Costs**:
- Cost to interview
- Cost to hire
  - includes cost to fire current assistant + hiring fee paid to agency
- Ch >> Ci (cost to hire is significantly greater than cost of interview)

**Goal**:
Determine what the price of this strategy will be

### AlgorithmFor `n` candidates, if you hire `m` of them, the cost is:

```
O (n*ci + m ch)
```

- The first part is a fixed cost
- We focus on analyzing the second hiring cost part
  - It depends on the order in which you interview the candidates
- **Commom paradigm**: need to find the TODO

### Probabilistic analysis

- Most commonly, to analyse the running time of an algorithm
- Sometimes we analyse other quantities, such as:
  - The hiring cost in the HIRE-ASSISTANT procedure
  - Which depends on the input distribution

### Randomized algorithms

- To use probabilistic analysis, we need info on the input distribution
- And also be able to model it computationally

### Change of scenario

- The HR agency sends a list of `n` candidates in advance
- Making it possible to interview a random candidate each day, not following the order given by the HR

### Randomized algorithms (2)

- Atomic expected value is: 1*(Probability of the value) + 0*(Probability of not being the value).
- For the expectability of the value if we try it `n` times, we get the sum of the expected value for each of the possible values it can assume (0..n).

The expected hiring cost of RANDOMIZED-HIRE-ASSISTANT is:
```
O(ch * ln n)
```

The solution is to randomly permutate the array of candidates in the start of the hiring process.
