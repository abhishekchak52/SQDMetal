# SQDMetal

Tools to aid in simulating and fabricating superconducting quantum devices. The tools are an extension of [Qiskit-Metal](https://github.com/Qiskit/qiskit-metal) to provide additional support for:

- Extra components with more flexible user-friendly options (see [gallery](https://nbviewer.org/github/sqdlab/SQDMetal/blob/main/docs/User/Comps_All.ipynb))
- Visualising and simulating effects of shadow evaporation techniques used to fabricate qubits
- RF and DC simulations using **COMSOL** (including calculation of capacitance matrices, inductance ~~matrices~~ and RF s-parameters)
- RF and DC simulations using cluster-friendly **AWS PALACE** (including **meshing via either COMSOL or Gmsh**)
- GDS export and manipulation techniques to help with fabrication setup for multi-die wafers, arrayed structures, and more

There are two classes of documentation provided for this stack:

- [User documentation](docs/User/Readme.md)
- [Developer documentation](docs/Developer/Readme.md)

## Installation instructions

[![Pixi Badge](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/prefix-dev/pixi/main/assets/badge/v0.json)](https://pixi.sh)

We use Pixi for dependency management. Pixi fits unto existing `conda`-based workflows but leverages the `rattler` crate, a highly-performant spiritual successor to `mamba` written in Rust. 

The following instructions will set up the development environment, including Qiskit Metal and Jupyter. The commands assume a POSIX terminal, but the equivalent Windows CMD/PowerShell commands should be substituted appropriately.



```bash
# First, clone this repository
git clone https://github.com/sqdlab/SQDMetal.git 

# Change directory to project root
cd ./SQDMetal

# Install the default environment
pixi install 
```
This will install Qiskit Metal, SQDMetal, Jupyter and some other dependencies into the `default` virtual environment. To open a shell prompt inside this environment (the equivalent of `conda activate ...`), run the following command in a terminal window:

```bash
pixi shell
```


