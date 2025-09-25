"""Various plotting functions to show the disclosure control features."""
from collections import defaultdict

import numpy as np
import polars as pl
from matplotlib import pyplot as plt
from metasyn.privacy import BasicPrivacy
from metasyn.registry import DistributionRegistry

from metasyncontrib.disclosure import DisclosurePrivacy


def plot_outliers(dist_type, distribution_name, series_size=50, n_outliers=1):
    """Create a plot of how outliers affect the resultant parameters.

    Parameters
    ----------
    dist_type
        Variable type, either continuous or discrete.
    distribution_name
        Name of the distribution, e.g. uniform, normal
    series_size, optional
        How big the series should be for showing the results, by default 50
    n_outliers, optional
        Number of outliers to be added to the default distribution, by default 1

    """
    # Create the distribution registry
    dist_registry = DistributionRegistry.parse(["builtin", "metasyn-disclosure"])
    disc_class = dist_registry.find_distribution(distribution_name, dist_type)
    disc_fit_class = dist_registry.find_fitter(distribution_name, dist_type,
                                               privacy=DisclosurePrivacy())
    disc_privacy = DisclosurePrivacy()

    # Find the base class of the disclosure distribution
    var_type = (disc_class.var_type if isinstance(disc_class.var_type, str)
                else disc_class.var_type[0])
    base_class = dist_registry.find_distribution(disc_class.name, var_type)
    base_fit_class = dist_registry.find_fitter(distribution_name, dist_type,
                                               privacy=BasicPrivacy())
    base_privacy = BasicPrivacy()
    # Get the default distribution of the base class
    dist = base_class.default_distribution(var_type)

    # Draw a series of random values
    series = pl.Series([dist.draw() for _ in range(series_size)])

    # Fit the distribution to the series
    clean_base_param = base_fit_class(base_privacy).fit(series).to_dict()["parameters"]
    clean_disc_param = disc_fit_class(disc_privacy).fit(series).to_dict()["parameters"]

    # Initialize dictionaries to store the parameters of the distributions
    base_param = defaultdict(lambda: [])
    disc_param = defaultdict(lambda: [])

    # Helper function to add parameters
    def _add(parameters, param, new_val):
        for key, val in param.items():
            parameters[key].append(val)
        parameters["new_val"].append(new_val)

    # Iterate over a range of values
    for new_val in np.linspace(-100, 100, 51):
        # Add a new value to the series
        new_series = series.extend_constant(new_val, n_outliers)

        # Fit the distributions to the new series
        base_dist = base_fit_class(base_privacy).fit(new_series)
        disc_dist = disc_fit_class(disc_privacy).fit(new_series)

        # Add the parameters of the fitted distributions to the dictionaries
        _add(base_param, base_dist.to_dict()["parameters"], new_val)
        _add(disc_param, disc_dist.to_dict()["parameters"], new_val)

    fs = 17
    plt.rcParams.update({"font.size": fs})

    fig, axes = plt.subplots(nrows=1, ncols=len(base_param)-1, figsize=(20, 10))
    # Plot the differences between the base and disclosure distributions for each value
    i_ax = 0
    for param in base_param:
        if param == "new_val":
            continue

        ax = axes if len(base_param) == 2 else axes[i_ax]
        # Create plot for the base distribution
        ax.plot(
            base_param["new_val"],
            np.array(base_param[param]) - clean_base_param[param],
            label="base",
        )

        # Create plot for the disclosure distribution
        ax.plot(
            disc_param["new_val"],
            np.array(disc_param[param]) - clean_disc_param[param],
            label="disclosure",
        )
        extras = "s" if n_outliers > 1 else ""
        # Set the title, labels and show the plot
        ax.set_title(f"{disc_class.__name__}: {param}")
        ax.set_ylabel(f"Difference between dist with and without outlier{extras}")
        ax.set_xlabel(f"Value of the outlier{extras}")
        ax.legend()
        i_ax += 1
    fig.show()
