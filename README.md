# Metasyn disclosure control
[![](https://img.shields.io/badge/metasyn-plugin-blue?logo=python&logoColor=white)](https://github.com/sodascience/metasyn)
[![Python package](https://github.com/sodascience/metasyn-disclosure-control/actions/workflows/python-package.yml/badge.svg)](https://github.com/sodascience/metasyn-disclosure-control/actions/workflows/python-package.yml)
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

A privacy plugin for [metasyn](https://github.com/sodascience/metasyn), based on statistical disclosure control (SDC) rules of thumb as found in the following documents:

- The [SDC handbook](https://securedatagroup.org/guides-and-resources/sdc-handbook/) of the Secure Data group in the UK
- The Data Without Boundaries document [Guidelines for output checking](https://wayback.archive-it.org/12090/*/https:/cros-legacy.ec.europa.eu/system/files/dwb_standalone-document_output-checking-guidelines.pdf) (pdf)
- Statistics Netherlands' output guidelines

Producing synthetic data with [metasyn](https://github.com/sodascience/metasyn) is already a great first step towards protecting privacy, but it doesn't adhere to official standards. For example, fitting a uniform distribution will disclose the lowest and highest values in the dataset, which may be a privacy issue in particularly sensitive data. This plugin solves these kinds of problems.

> Currently, the disclosure control plugin is work in progress. Especially in light of this, we disclaim
any responsibility as a result of using this plugin. 

## Installing the plugin

`metasyn-disclosure-control` is not yet on PyPi, so it needs to be installed directly using git. Through `pip` you can install the package with the following command:

 ```sh
 pip install git+https://github.com/sodascience/metasyn-disclosure-control.git
 ```

## Usage

Basic usage for our built-in titanic dataset is as follows:

```py
from metasyncontrib.disclosure import DisclosurePrivacy
from metasyncontrib.disclosure.string import DisclosureFaker

from metasyn import MetaFrame, VarSpec, demo_dataframe

df = demo_dataframe("titanic")

spec = [
    VarSpec(name="PassengerId", unique=True),
    VarSpec(name="Name", distribution=DisclosureFaker("name")),
]

mf = MetaFrame.fit_dataframe(
    df=df,
    var_specs=spec,
    privacy=DisclosurePrivacy(),
)

mf.synthesize(5)
```

```
shape: (5, 13)
┌─────────────┬────────────────────┬────────┬──────┬───┬────────────┬────────────┬─────────────────────┬────────┐
│ PassengerId ┆ Name               ┆ Sex    ┆ Age  ┆ … ┆ Birthday   ┆ Board time ┆ Married since       ┆ all_NA │
│ ---         ┆ ---                ┆ ---    ┆ ---  ┆   ┆ ---        ┆ ---        ┆ ---                 ┆ ---    │
│ i64         ┆ str                ┆ cat    ┆ i64  ┆   ┆ date       ┆ time       ┆ datetime[μs]        ┆ f32    │
╞═════════════╪════════════════════╪════════╪══════╪═══╪════════════╪════════════╪═════════════════════╪════════╡
│ 0           ┆ Benjamin Cox       ┆ female ┆ 27   ┆ … ┆ 1931-12-01 ┆ 14:33:06   ┆ 2022-07-30 02:16:37 ┆ null   │
│ 1           ┆ Mr. David Robinson ┆ female ┆ null ┆ … ┆ 1906-02-18 ┆ null       ┆ 2022-08-03 13:09:19 ┆ null   │
│ 2           ┆ Randy Mosley       ┆ male   ┆ 24   ┆ … ┆ 1933-01-06 ┆ 15:52:54   ┆ 2022-07-18 18:52:05 ┆ null   │
│ 3           ┆ Vincent Maddox     ┆ female ┆ 24   ┆ … ┆ 1937-02-10 ┆ 16:58:30   ┆ 2022-07-23 20:29:49 ┆ null   │
│ 4           ┆ Kristin Holland    ┆ male   ┆ 17   ┆ … ┆ 1939-12-09 ┆ 18:07:45   ┆ 2022-08-05 02:41:51 ┆ null   │
└─────────────┴────────────────────┴────────┴──────┴───┴────────────┴────────────┴─────────────────────┴────────┘
```


## Implementation details
The rules of thumb, roughly, are: 

- at least 10 units
- at least 10 degrees of freedom
- no group disclosure
- no dominance

For most distributions, we implemented micro-aggregation. This technique pre-averages a sorted version of the data, which then supplied to the original fitting mechanism. The idea is that during this pre-averaging step, we ensure that the rules of thumb are followed, so that the fitting method doesn't need to do anything in particular. While from a statistical point of view, we are losing more information than we probably need, it should ensure the safety of the data. 



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
This is a project by the [ODISSEI Social Data Science (SoDa)](https://odissei-data.nl/nl/soda/) team. Do you have questions, suggestions, or remarks on the technical implementation? File an issue in the issue tracker or feel free to contact [Raoul Schram](https://github.com/qubixes) or [Erik-Jan van Kesteren](https://github.com/vankesteren).

<img src="soda.png" alt="SoDa logo" width="250px"/> 
