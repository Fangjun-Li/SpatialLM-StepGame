# 4 shot
standard_prompt = '''
Given an input about spatial relations among objects, build the linking chain between the two queried objets.

Input:
1. H is above S with a small gap between them. 2. S is positioned below I. 3. P is on the top side to I. What is the relation of the agent S to the agent P?
Answer: S -> I (use 2) -> P (use 3)

Input:
1. Q is to the right of O and is on the same horizontal plane. 2. Q is slightly off center to the top left and M is slightly off center to the bottom right. 3. X and E are next to each other with X on the top and E at the bottom. 4. O is sitting at the upper right position to E. 5. W is on the right side and below M. What is the relation of the agent W to the agent E?
Answer: W -> M (use 5) -> Q (use 2) -> O (use 1) -> E (use 4)

Input:
1. Y is placed at the lower right of F. 2. X is over there and Y is directly below it. 3. I is positioned in the lower left corner of Q. 4. A is north west of Q. 5. The object labeled N is positioned to the right of the object labeled W. 6. N and A are vertical and N is below A. 7. F presents right to O. 8. O is slightly off center to the top left and W is slightly off center to the bottom right. What is the relation of the agent Q to the agent X?
Answer: Q -> A (use 4) -> N (use 6) -> W (use 5) -> O (use 8) -> F (use 7) -> Y (use 1) -> X (use 2)

Input:
1. C is above R with a small gap between them. 2. The objects L and Q are over there. The object L is lower and slightly to the left of the object Q. 3. C is to the upper left of J. 4. J is to the right of E. 5. T and A are next to each other with T on the top and A at the bottom. 6. G is lower right of N. 7. G is south east of A. 8. L is slightly off center to the top left and Y is slightly off center to the bottom right. 9. R is to the top right of Q. 10. If Y is the center of a clock face, T is located between 7 and 8. What is the relation of the agent G to the agent Q?
Answer: G -> A (use 7) -> T (use 5) -> Y (use 10) -> L (use 8) -> Q (use 2)


Input:
{input}
'''

# 4-shot
cot_prompt = '''Given an input about spatial relations among objects, build the linking chain between the two queried objets.

Input:
1. H is above S with a small gap between them. 2. S is positioned below I. 3. P is on the top side to I. What is the relation of the agent S to the agent P?
Steps:
chain: S ->, target: P, unused: 1. H-S, 2. S-I, 3. P-I.
chain: S -> I (use 2) ->, target: P, unused: 1. H-S, 3. P-I.
chain: I -> P (use 3) ->, target: P, unused: 1. H-S.
Answer: S -> I (use 2) -> P (use 3)

Input:
1. Q is to the right of O and is on the same horizontal plane. 2. Q is slightly off center to the top left and M is slightly off center to the bottom right. 3. X and E are next to each other with X on the top and E at the bottom. 4. O is sitting at the upper right position to E. 5. W is on the right side and below M. What is the relation of the agent W to the agent E?
Steps:
chain: W ->, target: E, unused: 1. Q-O, 2. Q-M, 3. X-E, 4. O-E, 5. W-M.
chain: W -> M (use 5) ->, target: E, unused: 1. Q-O, 2. Q-M, 3. X-E, 4. O-E.
chain: M -> Q (use 2) ->, target: E, unused: 1. Q-O, 3. X-E, 4. O-E.
chain: Q -> O (use 1) ->, target: E, unused: 3. X-E, 4. O-E.
chain: O -> E (use 4) ->, target: E, unused: 3. X-E.
Answer: W -> M (use 5) -> Q (use 2) -> O (use 1) -> E (use 4)

Input:
1. Y is placed at the lower right of F. 2. X is over there and Y is directly below it. 3. I is positioned in the lower left corner of Q. 4. A is north west of Q. 5. The object labeled N is positioned to the right of the object labeled W. 6. N and A are vertical and N is below A. 7. F presents right to O. 8. O is slightly off center to the top left and W is slightly off center to the bottom right. What is the relation of the agent Q to the agent X?
Steps:
chain: Q ->, target: X, unused: 1. Y-F, 2. X-Y, 3. I-Q, 4. A-Q, 5. N-W, 6. N-A, 7. F-O, 8. O-W.
chain: Q -> A (use 4) ->, target: X, unused: 1. Y-F, 2. X-Y, 3. I-Q, 5. N-W, 6. N-A, 7. F-O, 8. O-W.
chain: A -> N (use 6) ->, target: X, unused: 1. Y-F, 2. X-Y, 3. I-Q, 5. N-W, 7. F-O, 8. O-W.
chain: N -> W (use 5) ->, target: X, unused: 1. Y-F, 2. X-Y, 3. I-Q, 7. F-O, 8. O-W.
chain: W -> O (use 8) ->, target: X, unused: 1. Y-F, 2. X-Y, 3. I-Q, 7. F-O.
chain: O -> F (use 7) ->, target: X, unused: 1. Y-F, 2. X-Y, 3. I-Q.
chain: F -> Y (use 1) ->, target: X, unused: 2. X-Y, 3. I-Q.
chain: Y -> X (use 2) ->, target: X, unused: 3. I-Q.
Answer: Q -> A (use 4) -> N (use 6) -> W (use 5) -> O (use 8) -> F (use 7) -> Y (use 1) -> X (use 2)

Input:
1. C is above R with a small gap between them. 2. The objects L and Q are over there. The object L is lower and slightly to the left of the object Q. 3. C is to the upper left of J. 4. J is to the right of E. 5. T and A are next to each other with T on the top and A at the bottom. 6. G is lower right of N. 7. G is south east of A. 8. L is slightly off center to the top left and Y is slightly off center to the bottom right. 9. R is to the top right of Q. 10. If Y is the center of a clock face, T is located between 7 and 8. What is the relation of the agent G to the agent Q?
Steps:
chain: G ->, target: Q, unused: 1. C-R, 2. L-Q, 3. C-J, 4. J-E, 5. T-A, 6. G-N, 7. G-A, 8. L-Y, 9. R-Q, 10. Y-T.
chain: G -> A (use 7) ->, target: Q, unused: 1. C-R, 2. L-Q, 3. C-J, 4. J-E, 5. T-A, 6. G-N, 8. L-Y, 9. R-Q, 10. Y-T.
chain: A -> T (use 5) ->, target: Q, unused: 1. C-R, 2. L-Q, 3. C-J, 4. J-E, 6. G-N, 8. L-Y, 9. R-Q, 10. Y-T.
chain: T -> Y (use 10) ->, target: Q, unused: 1. C-R, 2. L-Q, 3. C-J, 4. J-E, 6. G-N, 8. L-Y, 9. R-Q.
chain: Y -> L (use 8) ->, target: Q, unused: 1. C-R, 2. L-Q, 3. C-J, 4. J-E, 6. G-N, 9. R-Q.
chain: L -> Q (use 2) ->, target: Q, unused: 1. C-R, 3. C-J, 4. J-E, 6. G-N, 9. R-Q.
Answer: G -> A (use 7) -> T (use 5) -> Y (use 10) -> L (use 8) -> Q (use 2)

Input:
{input}
'''

# 4-shot
propose_first_step_prompt = ''' 
Provided with a sequence of statements that define the spatial relationships among various objects, your task is to detail the subsequent actions. This includes initiating the chain of connections, identifying the target object, and enumerating all links between objects from the statements.

Input: 1. H is above S with a small gap between them. 2. S is positioned below I. 3. P is on the top side to I. What is the relation of the agent S to the agent P?
Possible next steps:
chain: S ->, target: P, unused: 1. H-S, 2. S-I, 3. P-I.

Input: 1. Q is to the right of O and is on the same horizontal plane. 2. Q is slightly off center to the top left and M is slightly off center to the bottom right. 3. X and E are next to each other with X on the top and E at the bottom. 4. O is sitting at the upper right position to E. 5. W is on the right side and below M. What is the relation of the agent W to the agent E?
Possible next steps:
chain: W ->, target: E, unused: 1. Q-O, 2. Q-M, 3. X-E, 4. O-E, 5. W-M.

Input: 1. Y is placed at the lower right of F. 2. X is over there and Y is directly below it. 3. I is positioned in the lower left corner of Q. 4. A is north west of Q. 5. The object labeled N is positioned to the right of the object labeled W. 6. N and A are vertical and N is below A. 7. F presents right to O. 8. O is slightly off center to the top left and W is slightly off center to the bottom right. What is the relation of the agent Q to the agent X?
Possible next steps:
chain: Q ->, target: X, unused: 1. Y-F, 2. X-Y, 3. I-Q, 4. A-Q, 5. N-W, 6. N-A, 7. F-O, 8. O-W.

Input: 1. C is above R with a small gap between them. 2. The objects L and Q are over there. The object L is lower and slightly to the left of the object Q. 3. C is to the upper left of J. 4. J is to the right of E. 5. T and A are next to each other with T on the top and A at the bottom. 6. G is lower right of N. 7. G is south east of A. 8. L is slightly off center to the top left and Y is slightly off center to the bottom right. 9. R is to the top right of Q. 10. If Y is the center of a clock face, T is located between 7 and 8. What is the relation of the agent G to the agent Q?
Possible next steps:
chain: G ->, target: Q, unused: 1. C-R, 2. L-Q, 3. C-J, 4. J-E, 5. T-A, 6. G-N, 7. G-A, 8. L-Y, 9. R-Q, 10. Y-T.

Input: {input}
Possible next steps:
'''


# 3-shot
propose_prompt = ''' Use relations listed in unused relations to enumerate all potential expansions of the chain by considering unused relations that exhibit a direct link to the last object within the chain.

Input: chain: G ->, target: Q, unused: 1. C-R, 2. L-Q, 3. C-J, 4. J-E, 5. T-A, 6. G-N, 7. G-A, 8. L-Y, 9. R-Q, 10. Y-T.
Possible next steps:
The last object within the chain is G, and the unused relations 6. G-N and 7. G-A include G. 
relation  chain: G -> N (use 6) ->, target: Q, unused: 1. C-R, 2. L-Q, 3. C-J, 4. J-E, 5. T-A, 7. G-A, 8. L-Y, 9. R-Q, 10. Y-T.
chain: G -> A (use 7) ->, target: Q, unused: 1. C-R, 2. L-Q, 3. C-J, 4. J-E, 5. T-A, 6. G-N, 8. L-Y, 9. R-Q, 10. Y-T.

Input: chain: Q -> A (use 4) ->, target: X, unused: 1. Y-F, 2. X-Y, 3. I-Q, 5. N-W, 6. N-A, 7. F-O, 8. O-W.
Possible next steps:
The last object within the chain is A, and the unused relation 6. N-A includes A. 
chain: A -> N (use 6) ->, target: X, unused: 1. Y-F, 2. X-Y, 3. I-Q, 5. N-W, 7. F-O, 8. O-W.

Input: chain: A -> N (use 6) ->, target: X, unused: 1. U-W, 2. R-D, 3. Z-I, 4. Z-P, 5. P-R, 6. I-V, 7. N-D, 8. X-Z, 9. Y-V, 10. H-Y, 11. V-X.
Possible next steps:
The last object within the chain is N, and the unused relation 7. N-D includes N. 
chain: N -> D (use 7) ->, target: X, unused: 1. U-W, 2. R-D, 3. Z-I, 4. Z-P, 5. P-R, 6. I-V, 8. X-Z, 9. Y-V, 10. H-Y, 11. V-X.

Input: {input}
Possible next steps:
'''

#3-shot
value_prompt = ''' Evaluate whether the chain can reach the target (sure/likely/impossible). If the chain has already reached the target, it's 'sure'. If the unused relations include the current object, it's 'likely'. If there are no unused relations that include the current object, it's 'impossible'.

chain: F ->, target: X, unused: 1. Y-F, 2. X-Y, 3. I-Q, 4. A-Q, 5. N-W, 6. N-A, 7. F-O, 8. O-W.
The current object is F, there are unused relations that include F (1. Y-F, 7. F-O).
likely

chain: L -> Q (use 2) ->, target: Q, unused: 1. C-R, 3. C-J, 4. J-E, 7. G-A, 8. L-Y, 9. R-Q.
The chain already reaches the target object Q.
sure

chain: G -> N (use 6) ->, target: Q, unused: 1. C-R, 2. L-Q, 3. C-J, 4. J-E, 5. T-A, 8. L-Y, 9. R-Q, 10. Y-T.
The current object is N, and there are no unused relations that include N.
impossible

{input}
'''

value_last_step_prompt = '''Evaluate whether the answer is correct. Given an input and an answer, give a judgement (sure/impossible) whether the answer is correct, i.e. it uses each unused relation correctly and reach the target.

Input: chain: Z ->, target: C, unused: 1. C-M, 2. Z-Y, 3. Z-M, 4. Y-G.
Answer: Z -> M (use 3) -> C (use 1)
Judge: sure

Input: chain: N ->, target: X, unused: 1. Y-V, 2. R-D, 3. V-X, 4. Z-P, 5. N-D, 6. P-R, 7. X-Z.
Answer: N -> D (use 5) -> R (use 2) -> P (use 6) -> Z (use 4) -> X (use 7)
Judge: sure

Input: chain: R ->, target: L, unused: 1. P-Z, 2. C-T, 3. R-M, 4. B-Z, 5. L-A, 6. M-O, 7. R-P, 8. O-A, 9. B-C.
Answer: R -> M (use 3) -> O (use 6) -> A (use 8) -> L (use 5)
Judge: sure

Input: chain: W ->, target: E, unused: 1. Q-O, 2. Q-M, 3. X-E, 4. O-E, 5. W-M.
Answer: W -> M (use 5) -> E (use 3)
Judge: impossible

Input: chain: Q ->, target: X, unused: 1. Y-F, 2. X-Y, 3. I-Q, 4. A-Q, 5. N-W, 6. N-A, 7. F-O, 8. O-W.
Answer: Q -> Y (use 2) -> X (use 2)
Judge: impossible

Input: chain: G ->, target: Q, unused: 1. C-R, 2. L-Q, 3. C-J, 4. J-E, 5. T-A, 6. G-N, 7. G-A, 8. L-Y, 9. R-Q, 10. Y-T.
Answer: G -> N (use 6)
Judge: impossible

Input: {input}
Answer: {answer}
Judge:'''

# 4 shot
cot_following_prompt = '''
Given an input about spatial relations among objects, build the linking chain between the two queried objets.

Input:
1. H is above S with a small gap between them. 2. S is positioned below I. 3. P is on the top side to I. What is the relation of the agent S to the agent P?
Linking chain: S -> I (use 2) -> P (use 3)

Input:
1. Q is to the right of O and is on the same horizontal plane. 2. Q is slightly off center to the top left and M is slightly off center to the bottom right. 3. X and E are next to each other with X on the top and E at the bottom. 4. O is sitting at the upper right position to E. 5. W is on the right side and below M. What is the relation of the agent W to the agent E?
Linking chain: W -> M (use 5) -> Q (use 2) -> O (use 1) -> E (use 4)

Input:
1. Y is placed at the lower right of F. 2. X is over there and Y is directly below it. 3. I is positioned in the lower left corner of Q. 4. A is north west of Q. 5. The object labeled N is positioned to the right of the object labeled W. 6. N and A are vertical and N is below A. 7. F presents right to O. 8. O is slightly off center to the top left and W is slightly off center to the bottom right. What is the relation of the agent Q to the agent X?
Linking chain: Q -> A (use 4) -> N (use 6) -> W (use 5) -> O (use 8) -> F (use 7) -> Y (use 1) -> X (use 2)

Input:
1. C is above R with a small gap between them. 2. The objects L and Q are over there. The object L is lower and slightly to the left of the object Q. 3. C is to the upper left of J. 4. J is to the right of E. 5. T and A are next to each other with T on the top and A at the bottom. 6. G is lower right of N. 7. G is south east of A. 8. L is slightly off center to the top left and Y is slightly off center to the bottom right. 9. R is to the top right of Q. 10. If Y is the center of a clock face, T is located between 7 and 8. What is the relation of the agent G to the agent Q?
Linking chain: G -> A (use 7) -> T (use 5) -> Y (use 10) -> L (use 8) -> Q (use 2)

Input:
{input}
'''
