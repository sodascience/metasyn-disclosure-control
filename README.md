# Metasyn disclosure control

A privacy plugin for [metasyn](https://github.com/sodascience/metasyn), based on statistical disclosure control (SDC) rules as found in the following documents:

- The [SDC handbook](https://securedatagroup.org/guides-and-resources/sdc-handbook/) of the Secure Data group in the UK
- The Data Without Boundaries document [Guidelines for output checking](https://wayback.archive-it.org/12090/*/https:/cros-legacy.ec.europa.eu/system/files/dwb_standalone-document_output-checking-guidelines.pdf) (pdf)
- Statistics Netherlands' output guidelines


While the base metasyn package is generally good at protecting privacy, it doesn't adhere to any standard level of privacy. For example, the uniform distributions in the base package will simply find the lowest and highest values in the dataset, and use those as the boundaries for the uniform distribution. In some cases the minimum and maximum values can be disclosive. That is why we have built this plugin that implements the disclosure control standard.

## Usage

The most basic usage is as follows:

```py
import polars as pl
from metasyn import MetaFrame
from metasyncontrib.disclosure import DisclosurePrivacy

df = pl.read_csv("your_data.csv")
mf = MetaFrame.fit_dataframe(
    df=df, 
    dist_providers=["builtin", "metasyn-disclosure"],
    privacy=DisclosurePrivacy()
)
mf.synthesize()
```


## Current status of the plugin

Currently, there the disclosure plugin is work in progress. Especially in light of this, we disclaim
any responsibility as a result of using this plugin. For most of the distributions
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

Currently only Faker distribution is implemented (which is the same as the metasyn base package,
since the distribution is not fit to any data). The regex distribution is currently not implemented.

### Categorical

A safe version of the multinoulli distribution is implemented. There is still some discussion on what to do if the dominance
rule is violated.


<!-- CONTRIBUTING -->
## Contributing
You can contribute to this metasyn plugin by giving feedback in the "Issues" tab, or by creating a pull request.

To create a pull request:
1. Fork the Project
2. Create your Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit your Changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the Branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request


<!-- CONTACT -->
## Contact
**Metasyn-disclosure** is a project by the [ODISSEI Social Data Science (SoDa)](https://odissei-data.nl/nl/soda/) team.
Do you have questions, suggestions, or remarks on the technical implementation? File an issue in the issue tracker or feel free to contact [Raoul Schram](https://github.com/qubixes) or [Erik-Jan van Kesteren](https://github.com/vankesteren).

<img src="soda.png" alt="SoDa logo" width="250px"/> 
