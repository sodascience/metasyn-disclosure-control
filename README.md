# Metasyn disclosure control
[![](https://img.shields.io/badge/metasyn-plugin-blue?logo=python&logoColor=white)](https://github.com/sodascience/metasyn)
[![Python package](https://github.com/sodascience/metasyn-disclosure-control/actions/workflows/python-package.yml/badge.svg)](https://github.com/sodascience/metasyn-disclosure-control/actions/workflows/python-package.yml)
[![Project Status: WIP – Initial development is in progress, but there has not yet been a stable, usable release suitable for the public.](https://www.repostatus.org/badges/latest/wip.svg)](https://www.repostatus.org/#wip)

A privacy plugin for [metasyn](https://github.com/sodascience/metasyn), based on statistical disclosure control (SDC) rules of thumb as found in the following documents:

- The [SDC handbook](https://securedatagroup.org/guides-and-resources/sdc-handbook/) of the Secure Data group in the UK
- The EU-funded Data Without Boundaries document on [Guidelines for output checking](https://wayback.archive-it.org/12090/*/https:/cros-legacy.ec.europa.eu/system/files/dwb_standalone-document_output-checking-guidelines.pdf) (pdf)
- Statistics Netherlands' statistical disclosure control guidelines for microdata output

> [!NOTE]
> Disclaimer: although this plugin is written according to disclosure control guidelines (and we seek input from their authors), we are not officially affiliated with any of the organisations above. 

Producing synthetic data with [metasyn](https://github.com/sodascience/metasyn) is already a great first step towards protecting privacy, but it doesn't adhere to official standards. For example, fitting a uniform distribution will disclose the lowest and highest values in the dataset, which may be a privacy issue in particularly sensitive data. This plugin solves these kinds of problems.

> [!WARNING]
> This plugin does not eliminate the need to check the output of metasyn; you cannot assume that the output is completely free of privacy sensitive information or that it will adhere to the SDC rules completely. For example, one of the SDC rules states that There should not be any groups with more than 90% of the items in that group. This will be checked by the disclosure control plugin. However, sometimes groups could be sensibly aggregated (for example different cancer types into a cancer diagnosis) so that the group disclosure rule is violated. This examplifies the need for a human to manually check the output. We disclaim any responsibility as a result of using this plugin.

## Installing the plugin

To install the package with pip, run the following:
```sh
pip install metasyn-disclosure
```

For the development, installed the package directly through git with the following command:

 ```sh
 pip install git+https://github.com/sodascience/metasyn-disclosure-control.git
 ```

## Usage

Basic usage for our built-in titanic dataset is as follows:

```py
from metasyncontrib.disclosure import DisclosurePrivacy
from metasyn.distribution import FakerDistribution

from metasyn import MetaFrame, VarSpec, demo_dataframe

df = demo_dataframe("titanic")

spec = [
    VarSpec(name="PassengerId", unique=True),
    VarSpec(name="Name", distribution=FakerDistribution("name")),
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
