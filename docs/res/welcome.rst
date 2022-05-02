Introduction
===================

Welcome to napari-cellseg-annotator !
--------------------------------------------

Here you will find instructions on how to use the program.
If the installation was successful, you'll see the napari-cellseg-annotator plugin
in the Plugins section of napari.

This plugin is intended for the review of labeled cell volumes [#]_ from mice whole-brain samples
imaged by mesoSPIM microscopy [#]_ , and for training and using segmentation models from the MONAI project [#]_, or
any custom model written in Pytorch.

From here you can access the guides on the several modules available for your tasks, such as :

* Review : :ref:`loader_module_guide`
* Inference: :ref:`inference_module_guide`
* Training : :ref:`training_module_guide`
* Cropping utility (3D) : :ref:`cropping_module_guide`
* Advanced : Defining custom models directly in the plugin (WIP) : :ref:`custom_model_guide`


Requirements
--------------------------------------------

.. important::
    A **CUDA-capable GPU** is not needed but **very strongly recommended**, especially for training.

Requires manual installation of pytorch and some optional dependencies of MONAI.

* For Pytorch, please see `PyTorch's website`_ for installation instructions, with or without CUDA depending on your hardware.

* If you get errors from MONAI regarding missing readers, please see `MONAI's optional dependencies`_ page for instructions on getting the readers required by your images.

.. _MONAI's optional dependencies: https://docs.monai.io/en/stable/installation.html#installing-the-recommended-dependencies
.. _PyTorch's website: https://pytorch.org/get-started/locally/

Installation
--------------------------------------------

You can install `napari-cellseg-annotator` via [pip]:

    ``pip install napari-cellseg-annotator``

For local installation, please run:

    ``pip install -e .``



Usage
--------------------------------------------

To use the plugin, please run:

    ``napari``

Then go into Plugins > napari-cellseg-annotator, and choose which tool to use.

- **Review**: This module allows you to review your labels, from predictions or manual labeling, and correct them if needed. It then saves the status of each file in a csv, for easier monitoring.
- **Infer**: This module allows you to use pre-trained segmentation algorithms on volumes to automatically label cells.
- **Train**:  This module allows you to train segmentation algorithms from labeled volumes.
- **Crop utility**: This module allows you to crop your volumes and labels dynamically, by selecting a fixed size volume and moving it around the image.





.. rubric:: References

.. [#] Mapping mesoscale axonal projections in the mouse brain using a 3D convolutional network, Friedmann et al., 2020 ( https://pnas.org/cgi/doi/10.1073/pnas.1918465117 )
.. [#] The mesoSPIM initiative: open-source light-sheet microscopes for imaging cleared tissue, Voigt et al., 2019 ( https://doi.org/10.1038/s41592-019-0554-0 )
.. [#] MONAI Project website ( https://monai.io/ )
