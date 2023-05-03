# KeckLFC
This is control package for Laser Frequency Comb in Keck Observatory

# Installation

- Step 1: Install Anaconda and prepare the environment

-- 1.1 Download and install Anaconda

It is highly recommended to use Anaconda to manage python packages.

Download and install Anaconda from https://www.anaconda.com/download/

Verify the installation by running `conda --version` in terminal.

-- 1.2 Create a new environment

Create a new environment for KeckLFC by running `conda create -n lfc` in terminal.

Activate the environment by running `conda activate lfc` in terminal.

- Step 2: Install required packages

-- 2.1 Install pyvisa

Run `conda install -c conda-forge pyvisa` in terminal.

-- 2.2 Install numpy, scipy, matplotlib

Run `conda install numpy scipy matplotlib` in terminal.

-- 2.3 Install mcculw (for USB-2408 DAQ)

Run `pip install mcculw` in terminal.

-- 2.4 Install wsapi (for Finisar WaveShaper)

Follow the instructions in https://ii-vi.com/use-64-bit-python-3-7-to-control-the-waveshaper-through-the-usb-port/ for connection guide






