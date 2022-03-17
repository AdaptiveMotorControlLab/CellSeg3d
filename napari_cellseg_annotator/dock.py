import os
import shutil
from pathlib import Path

import pandas as pd
from qtpy.QtWidgets import (
    QWidget,
    QPushButton,
    QHBoxLayout,
    QVBoxLayout,
)

GUI_MAXIMUM_WIDTH = 225
GUI_MAXIMUM_HEIGHT = 350
GUI_MINIMUM_HEIGHT = 300


"""
dock.py
====================================
Definition of Datamanager widget, for saving labels status in csv file
"""


class Datamanager(QWidget):
    """A widget with a single checkbox that allows to store the status of
    a slice in csv file (checked/not checked)

    """

    def __init__(self, parent: "napari.viewer.Viewer", *args, **kwargs):
        """Creates the datamanager widget in the specified viewer window.

        Args:
            parent (napari.viewer.Viewer): napair Viewer for the widget to be displayed in"""

        # TODO : use of args ?
        super(Datamanager, self).__init__(*args, **kwargs)

        layout = QVBoxLayout()
        self.viewer = parent
        """napari.viewer.Viewer: viewer in which the widget is displayed"""

        # add some buttons
        self.button = QPushButton("1", self)
        self.button.clicked.connect(self.button_func)

        io_panel = QWidget()
        io_layout = QHBoxLayout()
        io_layout.addWidget(self.button)
        io_panel.setLayout(io_layout)
        io_panel.setMaximumWidth(GUI_MAXIMUM_WIDTH)
        layout.addWidget(io_panel)

        # set the layout
        # layout.setAlignment(Qt.AlignTop)
        # layout.setSpacing(4)

        self.setLayout(layout)
        # self.setMaximumHeight(GUI_MAXIMUM_HEIGHT)
        # self.setMaximumWidth(GUI_MAXIMUM_WIDTH)

        self.df = ""
        self.csv_path = ""
        self.slice_num = 0
        self.filetype = ""
        self.image_dims = self.viewer.layers[0].data.shape

    def prepare(self, label_dir, filetype, model_type, checkbox):
        """Initialize the Datamanager, which loads the csv file and updates it
        with the index of the current slice.

        Args:
        label_dir (str): label path
        filetype (str) : file extension
        model_type (str): model type
        checkbox (bool): create new dataset or not
        """
        self.filetype = filetype
        self.df, self.csv_path = self.load_csv(label_dir, model_type, checkbox)

        print(self.csv_path, checkbox)
        # print(self.viewer.dims.current_step[0])
        self.update(self.viewer.dims.current_step[0])

    def load_csv(self, label_dir, model_type, checkbox):
        """
        Loads newest csv or create new csv

        Args:
            label_dir (str): label path
            model_type (str):model type
            checkbox ( bool ): create new dataset or not

        Returns:
            (pandas.DataFrame, str) dataframe、csv path
        """
        csvs = sorted(list(Path(label_dir).glob(f"{model_type}*.csv")))
        if len(csvs) == 0:
            df, csv_path = self.create(
                label_dir, model_type
            )  # df,  train_data_dir, ...
        else:
            csv_path = str(csvs[-1])
            df = pd.read_csv(csv_path, index_col=0)
            if checkbox is True:
                csv_path = (
                    csv_path.split("_train")[0]
                    + "_train"
                    + str(
                        int(os.path.splitext(csv_path.split("_train")[1])[0])
                        + 1
                    )
                    + ".csv"
                )  # adds 1 to current csv name number
                df.to_csv(csv_path)
            else:
                pass
        return df, csv_path

    def create(self, label_dir, model_type):
        """
        Create a new dataframe and save the csv
        Args:
          label_dir (str): label path
          model_type (str): model type
        Returns:
         (pandas.DataFrame, str): dataframe, csv path
        """

        if self.filetype == ".png":
            labels = sorted(
                list(
                    path.name
                    for path in Path(label_dir).glob("./*" + self.filetype)
                )
            )
        elif self.filetype == ".tif":
            path = list(Path(label_dir).glob("./*.tif"))
            # print(self.image_dims[0])
            print(path[0].name)
            filename = path[0].name
            labels = [str(filename) for i in range(self.image_dims[0])]

        else:
            print("Error: filetype should be assigned on launch")

        df = pd.DataFrame(
            {"filename": labels, "train": ["Not Checked"] * len(labels)}
        )
        csv_path = os.path.join(label_dir, f"{model_type}_train0.csv")
        df.to_csv(csv_path)
        return df, csv_path

    def update(self, slice_num):
        """Updates the Datamanager with the index of the current slice, and updates
        the text with the status contained in the csv (e.g. checked/not checked).

        Args:
            slice_num (int): index of the current slice

        """
        self.slice_num = slice_num
        # print(self.df)
        self.button.setText(
            self.df.at[self.df.index[self.slice_num], "train"]
        )  # puts  button values at value of 1st csv item

    def button_func(self):  # updates csv every time you press button...
        if self.button.text() == "Not Checked":
            self.button.setText("Checked")
            self.df.at[self.df.index[self.slice_num], "train"] = "Checked"
            self.df.to_csv(self.csv_path)
        else:
            self.button.setText("Not Checked")
            self.df.at[self.df.index[self.slice_num], "train"] = "Not Checked"
            self.df.to_csv(self.csv_path)

    def move_data(self):
        shutil.copy(
            self.df.at[self.df.index[self.slice_num], "filename"],
            self.train_data_dir,
        )

    def delete_data(self):
        os.remove(
            os.path.join(
                self.train_data_dir,
                os.path.basename(
                    self.df.at[self.df.index[self.slice_num], "filename"]
                ),
            )
        )

    def check_all_data_and_mod(self):
        for i in range(len(self.df)):
            if self.df.at[self.df.index[i], "train"] == "Checked":
                try:
                    shutil.copy(
                        self.df.at[self.df.index[i], "filename"],
                        self.train_data_dir,
                    )
                except:
                    pass
            else:
                try:
                    os.remove(
                        os.path.join(
                            self.train_data_dir,
                            os.path.basename(
                                self.df.at[self.df.index[i], "filename"]
                            ),
                        )
                    )
                except:
                    pass
