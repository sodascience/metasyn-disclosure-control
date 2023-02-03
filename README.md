# Metasynth disclosure control

This is a plugin for the [MetaSynth](https://github.com/sodascience/metasynth) Python library.
While the base MetaSynth package protects against some privacy leakage, it doesn't completely
fix the issue. For example, the uniform distributions in the base package will simply find
the lowest and highest values in the dataset, and use those as the boundaries for the uniform
distribution. The minimum and maximum values can be very disclosive in some cases!

## Rule of Thumb

In this package we have implemented the "rule of thumb" as described in the
[European guidelines](https://ec.europa.eu/eurostat/cros/system/files/dwb_standalone-document_output-checking-guidelines.pdf)
for output checking. The main idea behind the rule of thumb is that it is on the safe side
of what you are allowed to disclose. If you follow the rule of thumb then the idea is that
the output should be considered privacy conserving, without the need for a specialist to determine this.

## Current status of the plugin

Currently, there the disclosure plugin is work in progress. For most of the distributions
the micro-aggregation technique is used. This technique pre-averages a sorted version of the data,
which then supplied to the original fitting mechanism. The idea is that during this pre-averaging
step, we ensure that the rule of thumb is followed, so that the fitting method doesn't need to do
anything in particular. While, from a statistical point of view, we are losing more information than
we probably need, it should ensure the safety of the data. 

Below we have summarized the status for each of the variable types:

### Discrete

It technically works, but a new micro-aggregation algorithm specifically for integers might yield
better and more consistent results. Currently are implemented:

- DiscreteUniform, UniqueKey, Poisson

### Continuous

No current issues, following are implemented:

- Uniform, TruncatedNormal, Normal, LogNormal, Exponential

### Datetime

Implemented:

- UniformDate, UniformTime, UniformDateTime

### String

Currently only Faker distribution is implemented (which doesn't do anything on its own,
since it's already not using the original data). The regex distribution should also be implemented at some point.

### Categorical

A safe version of the multinoulli distribution is implemented. There is still some discussion on what to do if the dominance
rule is violated.