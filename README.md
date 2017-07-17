
# Using (Google) Neural Machine Translation for chess movements inference

Somedays ago a free version of the source code of the GNMT (Google Neural Machine Translation) was release in: https://github.com/tensorflow/nmt
by Thang Luong, Eugene Brevdo, Rui Zhao

<p align="center">
<img width="48%" src="nmt/g3doc/img/seq2seq.jpg" />
<br>

# Introduction

Sequence-to-sequence (seq2seq) models
([Sutskever et al., 2014](https://papers.nips.cc/paper/5346-sequence-to-sequence-learning-with-neural-networks.pdf),
[Cho et al., 2014](http://emnlp2014.org/papers/pdf/EMNLP2014179.pdf)) have
enjoyed great success in a variety of tasks such as machine translation, speech
recognition, and text summarization.

I've used the release of this seq2seq to show the power of this model. Using a vocabulary with just de numbers and letters
(the symbols) used for the chess algebraic notation, I could learn a model to infer the movement I human would do given
a table state.

The supervised learning uses source-target of the form:

Source:
rnq1kb1r/pp11ppp1/11p11n11/1111111p/11111111/11111NPb/PPPP1P1P/RNBQR1KB b

Target:
Bg4

The source is the state of the board, and the target the movement a human would do in this situation.

´´´
In this way the source vocabulary was:
w
/
1
p
r
n
b
q
k
P
R
N
B
Q
K
´´´

´´´
and the target vocabulary:
p
r
n
b
q
k
P
R
N
B
Q
K
x
+
O
-
1
2
3
4
5
6
7
8
a
c
d
e
f
g
h
=
´´´

# Results

Using a NMT + GNMT attention (2 layers) I was able to reach a good result with:

eval dev: perplexity 2.83
eval test: perplexity 3.07
global training step 72100 lr 0.868126 step-time 0.51s wps 9.57K ppl 2.76 bleu 20.64

This result means that, given a board state whatsoever, the model can predict in a seq2seq way a valid (and usually human)
chess movement.


