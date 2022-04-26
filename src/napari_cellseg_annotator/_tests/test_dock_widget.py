import os
from pathlib import Path

from tifffile import imread

from napari_cellseg_annotator.plugin_dock import Datamanager


def test_prepare(make_napari_viewer):
    path_to_csv = os.path.dirname(os.path.realpath(__file__)) + "/res"
    path_image = os.path.dirname(os.path.realpath(__file__)) + "/res/test.tif"
    image = imread(path_image)
    viewer = make_napari_viewer()
    viewer.add_image(image)
    widget = Datamanager(viewer)

    widget.prepare(path_to_csv, ".tif", "", False, False)

    assert widget.filetype == ".tif"
    assert widget.as_folder == False
    assert Path(widget.csv_path) == Path(os.path.dirname(os.path.realpath(__file__)) + "/res/_train0.csv")
