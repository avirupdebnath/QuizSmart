The Adaptive Learning Platform accepts discrimination, difficulty and guessing-bias from the teacher/admin along with the question text and options and passes it to the fuzzifier block which accepts these three indices (difficulty, discrimination and guessing-bias) as input and returns an aggregated normalized index as output which is then stored discreetly along-with the question text in the database. This stored parameter is a normalized estimation of the difficulty level of the question as is further used to map a student’s ability to a particular question of a given difficulty. 
While designing the normalization process inside the fuzzifier, it was kept in mind the fact that a teacher might be biased to a particular question as well, to make it look too hard or too easy, thus, making it appear in a quiz only rarely (i.e. only when a student performs unrealistically well or unrealistically poorly). For example, if a question has difficulty=10, discrimination=10 and bias=10 (on a scale of 10), quantitatively, it should translate to a question that is so hard that no student should be able to answer it. But that should never be the case because then the question would serve no purpose. Thus, the algorithm assumes that there would be a few students who might have advanced knowledge to even answer that question. So, the aggregated normalized parameter observed in such a case was only 8.33 and not 10. Similarly, if difficulty=0, discrimination=0 and bias=0, it correlates to a question that is so easy that no student can answer it incorrectly. Again, such an argument is unrealistic. There might be a few students who might fail to understand the question properly or might select the wrong answer in a hurry!  So, the aggregated normalized parameter returned for such a scenario was observed to be 1.66 and not 0.
The aggregating aspect of the fuzzy membership functions has been formulated in such a way that they have a centralizing tendency and reduces the scope of either extremities, to enable a student to attempt a little harder question (than what ability might suggest) when he has been answering a lot of questions correctly and also conversely provide the student with an easier question (than his ability might suggest) when he attempts a lot of questions wrongly to keep up with a student’s confidence level during the test.
