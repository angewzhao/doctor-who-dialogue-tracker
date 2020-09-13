# doctor-who-dialogue-tracker

This webscrapes all of the doctors' dialogue in Doctor Who. Given a quote, this calculates which incarnation of the doctor is most likely and least likely to have spoken that quote. 

Calculating the probabilities:
The quote is represented as a multinomial random variable. 

The probability to calculate is this: P(Doctor | quote). Using Baye's theorem, this becomes [P(quote | Doctor)P(Doctor)]/P(quote). Assume that P(Doctor)  = 1/13, since there are 13 doctors, not including the War Doctor. Additionally, the goal is not to find the exact probability but to find who is most likely to have said the quote. 

Therefore, say if one is comparing doctors 10 and 11, and one hopes that Doctor 10 said, "I don't want to go", [P(quote | Doctor)P(Doctor 10)]/P(quote) > [P(quote | Doctor)P(Doctor 11)]/P(quote). This simplifies to {[P(quote | Doctor)P(Doctor 10)]/P(quote)} / {[P(quote | Doctor)P(Doctor 11)]/P(quote)} > 1.

This simplifies to: P(quote | Doctor 10) / P(quote | Doctor 11) > 1. 

Here, we use Doctor 10 as a specific example. 

P(quote | Doctor 10) = [ n! / ( n1! * n2! * ... nk! ) ] * ( p1n1 * p2n2 * . . . * pknk), where n  = number of trials (or words in quote), n1 to nK = (number of times a unique word appeared), and p1 to pk = the probability that Doctor 10 said that word. 

p1 to pk are taken to be the frequencies of the words that Doctor 10 may or may not have said. These frequencies will be treated as probabilities since this uses a frequentist definition of probability. These are calculated by webscraping all of the words Doctor 10 has said in the Doctor Who TV series and calculating the counts of the words divided by the number of total words Doctor 10 said. If a word in the quote appears that Doctor 10 has never said before, like "mangosteen", then the frequency will be given as 1*10e-8. 

P(quote | Doctor 10) / P(quote | Doctor 11) > 1 now becomes Doctor 10's [ n! / ( n1! * n2! * ... nk! ) ] * ( p1n1 * p2n2 * . . . * pknk) > Doctor 11's [ n! / ( n1! * n2! * ... nk! ) ] * ( p1n1 * p2n2 * . . . * pknk) > 1. 

This simplifies to: Doctor 10's ( p1n1 * p2n2 * . . . * pknk) / Doctor 11's ( p1n1 * p2n2 * . . . * pknk) > 1. This [ n! / ( n1! * n2! * ... nk! ) is redundant because this concerns the quote given.

But since these probabilies are tiny, take the log to avoid floating point underflow. 

So the final equation calculated becomes: log(Doctor 10's ( p1n1 * p2n2 * . . . * pknk) / Doctor 11's ( p1n1 * p2n2 * . . . * pknk) > 1) = log(Doctor 10's ( p1n1 * p2n2 * . . . * pknk) - log(Doctor 11's ( p1n1 * p2n2 * . . . * pknk) > 0) = log(Doctor 10's ( p1n1 * p2n2 * . . . * pknk) > log(Doctor 11's ( p1n1 * p2n2 * . . . * pknk)).

This finally simplifies into: Doctor 10's(n1*log(p1) + ...nk * log(pk)) > Doctor 11's(n1*log(p1) + ...nk * log(pk)).

Order the resulting probabilities, and you get most likely to least likely. This method also explains why there is no specific probability given for each Doctor, but can accurately rank each of the doctors. 
