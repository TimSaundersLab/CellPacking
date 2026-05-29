# CellPacking

![image](https://user-images.githubusercontent.com/17041165/203357182-08c978cd-5a90-4862-85a2-b9a0f6d5d124.png)


This is a flat monolayer simulation package for the article: 
### Curvature-induced cell rearrangements in biological tissues

Yuting Lou<sup>1</sup>, Jean-Francois Rupprecht<sup>1,2</sup>, Sophie Theis<sup>3</sup>, Tetsuya Hiraiwa<sup>1</sup>, and Timothy E Saunders<sup>1,3</sup>

[link to the article](https://journals.aps.org/prl/abstract/10.1103/PhysRevLett.130.108401)

& 

### Stress anisotropy in axisymmetric 3D active curved structures

Yuting Lou<sup>1</sup>, Sophie Theis<sup>3</sup>, Jean-Francois Rupprecht<sup>1,2</sup>, Timothy E Saunders<sup>1,3</sup>, and Tetsuya Hiraiwa<sup>1</sup>

[link to the article]()


<sup>1</sup>Mechanobiology Institute, National University of Singapore  
<sup>2</sup>Aix Marseille Université, Université de Toulon, CNRS,  
Centre de Physique Théorique, Turing Centre for Living Systems, Marseille, France  
<sup>3</sup>Warwick Medical School, University of Warwick, Coventry, United Kingdom


## Installation
This package is based on the [`tyssue`](https://tyssue.readthedocs.org) library and its dependencies It recquires a specific version of tyssue that you can find here : [tyssue](https://github.com/sophietheis/tyssue/tree/standardisation). 

The recommanded installation route is to use the `conda` package manager. You can get a `conda` distribution for your OS at https://www.anaconda.com/download . Make sure to choose a python 3.6 version. Once you have installed conda, you can install tyssue with:

```bash
$ conda install -c conda-forge tyssue
```

You can then download and install CellPacking from github:

- with git:

```bash
$ git clone https://github.com/TimSaundersLab/CellPacking.git
$ cd CellPacking
$ python setup.py install
```

- or by downloading https://github.com/TimSaundersLab/CellPacking/archive/master.zip ,  uncompressing the archive and running `python setup.py install` in the root directory.


## Run simulation
Simulation can be run using notebook found in `notebooks/PRL` or `notebooks/PRE` folders. 


To generate simulation about anisotropic stress and in plane shape index (Fig1B), you can use the following notebook: [`notebooks/PRE/Simu_Stress_SI.ipynb`](https://github.com/TimSaundersLab/CellPacking/blob/main/notebooks/PRE/Simu_Stress_SI.ipynb)

To generate simulation about Compression/Extension (Fig1C), you can use the following notebook: [`notebooks/PRE/Simu_Extension_Compression.ipynb`](https://github.com/TimSaundersLab/CellPacking/blob/main/notebooks/PRE/Simu_Extension_Compression.pynb)

To generate simulation from the PRL paper, you can use the following notebook: [`notebooks/PRL/Simulations_Main.ipynb`](https://github.com/TimSaundersLab/CellPacking/blob/main/notebooks/PRL/Simulations_Main.ipynb)



## Licence

This work is free software, published under the MPLv2 licence, see LICENCE for details.


&copy; The article authors -- all rights reserved
