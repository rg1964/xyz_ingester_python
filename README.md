# xyz_ingester_python
<!-- TABLE OF CONTENTS -->
## Table of Contents

* [About the Project](#about-the-project)
* [Getting Started](#getting-started)
  * [Prerequisites](#prerequisites)
  * [Installation](#installation)
* [Usage](#usage)
* [Contributing](#contributing)
* [License](#license)
* [Contact](#contact)
* [Acknowledgements](#acknowledgements)



<!-- ABOUT THE PROJECT -->
## About The Project
This is an implementation of an ingester to transform a Python pandas dataframe into the PIF format.  
It includes a function [xyz_converter.py](https://github.com/rg1964/xyz_ingester_python/blob/master/2_xyz_converter.py) that takes in a Python pandas dataframe and outputs a PIF file.
The test uses data from [QM9](https://figshare.com/articles/Data_for_6095_constitutional_isomers_of_C7H10O2/1057646).
This is a relatively large data set, and one ca use only a representative subset of this data for illustration purposes.
The main journal article that describes this data set (and the data file structure) can be found [here](https://www.nature.com/articles/sdata201422).

## Getting Started

These instructions will give an overview on the components of the project and how to run it.

### Prerequisites

This project has been developed with Python 3.7.3, and the following packages are used by the different components:

* os
* requests
* tarfile
* shutil
* random
* argparse
* pypif and pypif.obj
* citrination_client
* string

### Installing

A step by step series of examples that tell you how to get a development env running

Say what the step will be

```
Give the example
```

And repeat

```
until finished
```

End with an example of getting some data out of the system or using it for a little demo

## Running the tests

Explain how to run the automated tests for this system

### Break down into end to end tests

Explain what these tests test and why

```
Give an example
```

### And coding style tests

Explain what these tests test and why

```
Give an example
```

## Deployment

Add additional notes about how to deploy this on a live system

## Built With

* [Dropwizard](http://www.dropwizard.io/1.0.2/docs/) - The web framework used
* [Maven](https://maven.apache.org/) - Dependency Management
* [ROME](https://rometools.github.io/rome/) - Used to generate RSS Feeds

## Contributing

Please read [CONTRIBUTING.md](https://gist.github.com/PurpleBooth/b24679402957c63ec426) for details on our code of conduct, and the process for submitting pull requests to us.

## Versioning

We use [SemVer](http://semver.org/) for versioning. For the versions available, see the [tags on this repository](https://github.com/your/project/tags). 

## Authors

* **Billie Thompson** - *Initial work* - [PurpleBooth](https://github.com/PurpleBooth)

See also the list of [contributors](https://github.com/your/project/contributors) who participated in this project.

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details

## Acknowledgments

* Hat tip to anyone whose code was used
* Inspiration
* etc
