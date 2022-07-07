from typing import Optional
from typing import Union

from qtpy.QtCore import Qt
from qtpy.QtCore import QUrl
from qtpy.QtGui import QDesktopServices
from qtpy.QtWidgets import QCheckBox
from qtpy.QtWidgets import QComboBox
from qtpy.QtWidgets import QDoubleSpinBox
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QGridLayout
from qtpy.QtWidgets import QGroupBox
from qtpy.QtWidgets import QHBoxLayout
from qtpy.QtWidgets import QLabel
from qtpy.QtWidgets import QLayout
from qtpy.QtWidgets import QLineEdit
from qtpy.QtWidgets import QPushButton
from qtpy.QtWidgets import QScrollArea
from qtpy.QtWidgets import QSizePolicy
from qtpy.QtWidgets import QSpinBox
from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget

from napari_cellseg3d import utils

"""
User interface functions and aliases"""


###############
# aliases
LEFT_AL = Qt.AlignmentFlag.AlignLeft
"""Alias for Qt.AlignmentFlag.AlignLeft, to use in addWidget"""
RIGHT_AL = Qt.AlignmentFlag.AlignRight
"""Alias for Qt.AlignmentFlag.AlignRight, to use in addWidget"""
HCENTER_AL = Qt.AlignmentFlag.AlignHCenter
"""Alias for Qt.AlignmentFlag.AlignHCenter, to use in addWidget"""
CENTER_AL = Qt.AlignmentFlag.AlignCenter
"""Alias for Qt.AlignmentFlag.AlignCenter, to use in addWidget"""
ABS_AL = Qt.AlignmentFlag.AlignAbsolute
"""Alias for Qt.AlignmentFlag.AlignAbsolute, to use in addWidget"""
BOTT_AL = Qt.AlignmentFlag.AlignBottom
"""Alias for Qt.AlignmentFlag.AlignBottom, to use in addWidget"""
###############
# colors
dark_red = "#72071d"  # crimson red
default_cyan = "#8dd3c7"  # turquoise cyan (default matplotlib line color under dark background context)
napari_grey = "#262930"  # napari background color (grey)


def toggle_visibility(checkbox, widget):
    """Toggles the visibility of a widget based on the status of a checkbox.

    Args:
        checkbox: The QCheckbox that determines whether to show or not
        widget: The widget to hide or show
    """
    widget.setVisible(checkbox.isChecked())


class Button(QPushButton):
    """Class for a button with a title and connected to a function when clicked. Inherits from QPushButton.

    Args:
        title (str-like): title of the button. Defaults to None, if None no title is set
        func (callable): function to execute when button is clicked. Defaults to None, no binding is made if None
        parent (QWidget): parent QWidget to add button to. Defaults to None, no parent is set if None
        fixed (bool): if True, will set the size policy of the button to Fixed in h and w. Defaults to True.

    """

    def __init__(
        self,
        title: str = None,
        func: callable = None,
        parent: QWidget = None,
        fixed: bool = True,
    ):
        super().__init__(parent)
        if title is not None:
            self.setText(title)

        if func is not None:
            self.clicked.connect(func)

        if fixed:
            self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

    def visibility_condition(self, checkbox):
        toggle_visibility(checkbox, self)


class DropdownMenu(QComboBox):
    """Creates a dropdown menu with a title and adds specified entries to it"""

    def __init__(
        self,
        entries: Optional[list] = None,
        parent: Optional[QWidget] = None,
        label: Optional[str] = None,
        fixed: Optional[bool] = True,
    ):
        """Args:
        entries (array(str)): Entries to add to the dropdown menu. Defaults to None, no entries if None
        parent (QWidget): parent QWidget to add dropdown menu to. Defaults to None, no parent is set if None
        label (str) : if not None, creates a QLabel with the contents of 'label', and returns the label as well
        fixed (bool): if True, will set the size policy of the dropdown menu to Fixed in h and w. Defaults to True.
        """
        super().__init__(parent)
        self.label = None
        if entries is not None:
            self.addItems(entries)
        if label is not None:
            self.label = QLabel(label)
        if fixed:
            self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)


class CheckBox(QCheckBox):
    """Shortcut for creating QCheckBox with a title and a function"""

    def __init__(
        self,
        title: Optional[str] = None,
        func: Optional[callable] = None,
        parent: Optional[QWidget] = None,
        fixed: Optional[bool] = True,
    ):
        """
        Args:
            title (str-like): title of the checkbox. Defaults to None, if None no title is set
            func (callable): function to execute when checkbox is toggled. Defaults to None, no binding is made if None
            parent (QWidget): parent QWidget to add checkbox to. Defaults to None, no parent is set if None
            fixed (bool): if True, will set the size policy of the checkbox to Fixed in h and w. Defaults to True.
        """
        super().__init__(title, parent)
        if fixed:
            self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        if func is not None:
            self.toggled.connect(func)


class AnisotropyWidgets(QWidget):
    def __init__(self, parent, default_x=1, default_y=1, default_z=1):
        super().__init__(parent)

        self._layout = QVBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.container, self._boxes_layout = make_container(T=7, parent=parent)
        self.checkbox = make_checkbox(
            "Anisotropic data", self.toggle_display_aniso, parent
        )

        self.box_widgets = make_n_spinboxes(
            n=3, min=1.0, max=1000, default=1, step=0.5, double=True
        )
        self.box_widgets[0].setValue(default_x)
        self.box_widgets[1].setValue(default_y)
        self.box_widgets[2].setValue(default_z)

        for w in self.box_widgets:
            w.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.box_widgets_lbl = [
            make_label("Resolution in " + axis + " (microns) :", parent=parent)
            for axis in "xyz"
        ]

        ##################
        # tooltips
        self.checkbox.setToolTip(
            "If you have anisotropic data, you can scale data using your resolution in microns"
        )
        [w.setToolTip("Resolution in microns") for w in self.box_widgets]
        ##################

        self.build()

    def toggle_display_aniso(self):
        """Shows the choices for correcting anisotropy when viewing results depending on whether :py:attr:`self.checkbox` is checked"""
        toggle_visibility(self.checkbox, self.container)

    def build(self):
        [
            self._boxes_layout.addWidget(widget, alignment=HCENTER_AL)
            for widgets in zip(self.box_widgets_lbl, self.box_widgets)
            for widget in widgets
        ]
        # anisotropy
        self.container.setLayout(self._boxes_layout)
        self.container.setVisible(False)

        add_widgets(self._layout, [self.checkbox, self.container])
        self.setLayout(self._layout)

    def get_anisotropy_resolution_xyz(self, as_factors=True):
        """
        Args :
            as_factors: if True, returns zoom factors, otherwise returns the input resolution

        Returns : the resolution in microns for each of the three dimensions. ZYX order suitable for napari scale"""

        resolution = [w.value() for w in self.box_widgets]
        if as_factors:
            return self.anisotropy_zoom_factor(resolution)

        return resolution

    def get_anisotropy_resolution_zyx(self, as_factors=True):
        """
        Args :
            as_factors: if True, returns zoom factors, otherwise returns the input resolution

        Returns : the resolution in microns for each of the three dimensions. XYZ order suitable for MONAI"""
        resolution = [w.value() for w in self.box_widgets]
        if as_factors:
            resolution = self.anisotropy_zoom_factor(resolution)

        return [resolution[2], resolution[1], resolution[0]]

    def anisotropy_zoom_factor(self, aniso_res):
        """Computes a zoom factor to correct anisotropy, based on anisotropy resolutions

            Args:
                resolutions: array for resolution (float) in microns for each axis

        Returns: an array with the corresponding zoom factors for each axis (all values divided by min)

        """

        base = min(aniso_res)
        zoom_factors = [base / res for res in aniso_res]
        return zoom_factors

    def is_enabled(self):
        """Returns : whether anisotropy correction has been enabled or not"""
        return self.checkbox.isChecked()


class FilePathWidget(QWidget):
    """Widget to handle the choice of file paths for data throughout the plugin."""

    def __init__(
        self,
        description: str,
        file_function: callable,
        parent: Optional[QWidget] = None,
    ):
        """Creates a FilePathWidget with the following elements :"""
        super().__init__(parent)
        self._layout = QHBoxLayout()
        self._layout.setSpacing(0)
        self._layout.setContentsMargins(0, 0, 0, 0)

        self.text_field = QLineEdit(description, self)
        self.button = Button("Open", file_function, parent=self, fixed=True)

        self.text_field.setReadOnly(True)

    def build(self):

        add_widgets(self._layout, [self.text_field, self.button])
        self.setLayout(self._layout)

    def get_text_field(self):
        return self.text_field

    def get_button(self):
        return self.button


def add_blank(widget, layout=None):
    """
    Adds a space between consecutive buttons/labels in a layout when building a widget

    Args:
        widget (QWidget): widget to add blank in
        layout (QLayout): layout to add blank in

    Returns:
        QLabel : blank label
    """
    blank = QLabel("", widget)
    if layout is not None:
        layout.addWidget(blank, alignment=ABS_AL)
    return blank


def open_file_dialog(
    widget,
    possible_paths: list = [""],
    load_as_folder: bool = False,
    filetype: str = "Image file (*.tif *.tiff)",
):
    """Opens a window to choose a file directory using QFileDialog.

    Args:
        widget (QWidget): Widget to display file dialog in
        possible_paths (str): Paths that may have been chosen before, can be a string
        or an array of strings containing the paths
        load_as_folder (bool): Whether to open a folder or a single file. If True, will allow opening folder as a single file (2D stack interpreted as 3D)
        filetype (str): The description and file extension to load (format : ``"Description (*.example1 *.example2)"``). Default ``"Image file (*.tif *.tiff)"``

    """

    default_path = utils.parse_default_path(possible_paths)
    if not load_as_folder:
        f_name = QFileDialog.getOpenFileName(
            widget, "Choose file", default_path, filetype
        )
        return f_name
    else:
        print(default_path)
        filenames = QFileDialog.getExistingDirectory(
            widget, "Open directory", default_path
        )
        return filenames


def make_label(name, parent=None):  # TODO update to child class
    """Creates a QLabel

    Args:
        name: string with name
        parent: parent widget

    Returns: created label

    """
    if parent is not None:
        return QLabel(name, parent)
    else:
        return QLabel(name)


def make_scrollable(
    contained_layout, containing_widget, min_wh=None, max_wh=None, base_wh=None
):  # TODO convert to child class
    """Creates a QScrollArea and sets it up, then adds the contained_widget to it,
    and finally adds the scroll area in a layout and sets it to the contaning_widget


    Args:
        contained_layout (QLayout): the widget to be made scrollable
        containing_widget (QWidget): the widget to add the resulting scroll area in
        min_wh (array(int)): array of two ints for respectively the minimum width and minimum height of the scrollable area. Defaults to None, lets Qt decide if None
        max_wh (array(int)): array of two ints for respectively the maximum width and maximum height of the scrollable area. Defaults to None, lets Qt decide if None
        base_wh (array(int)): array of two ints for respectively the initial width and initial height of the scrollable area. Defaults to None, lets Qt decide if None
    """
    container_widget = QWidget()  # required to use QScrollArea.setWidget()
    container_widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Maximum)
    container_widget.setLayout(contained_layout)
    container_widget.adjustSize()
    # TODO : optimize the number of created objects ?
    scroll = QScrollArea()
    scroll.setWidget(container_widget)
    scroll.setWidgetResizable(True)
    scroll.setSizePolicy(
        QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
    )
    if base_wh is not None:
        scroll.setBaseSize(base_wh[0], base_wh[1])
    if max_wh is not None:
        scroll.setMaximumSize(max_wh[0], max_wh[1])
    if min_wh is not None:
        scroll.setMinimumSize(min_wh[0], min_wh[1])

    scroll.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOn)
    scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
    # scroll.adjustSize()

    layout = QVBoxLayout(containing_widget)
    # layout.setContentsMargins(0,0,1,1)
    layout.setSizeConstraint(QLayout.SetMinAndMaxSize)
    layout.addWidget(scroll)
    containing_widget.setLayout(layout)


def make_n_spinboxes(
    n=1,
    min=0,
    max=10,
    default=0,
    step=1,
    parent=None,
    double=False,
    fixed=True,
) -> Union[list, QWidget]:  # TODO: child class if possible ?
    """

    Args:
        n: number of spinboxes, defaults to 1
        min: min value, defaults to 0
        max: max value, defaults to 10
        default: default value, defaults to 0
        step : step value, defaults to 1
        parent: parent widget, defaults to None
        double (bool): if True, creates a QDoubleSpinBox rather than a QSpinBox
        fixed (bool): if True, sets the QSizePolicy of the spinbox to Fixed

    Returns:
            list: A list of n Q(Double)SpinBoxes with specified parameters. If only one box is made, returns the box itself instead
    """
    if double:
        box_type = QDoubleSpinBox
    else:
        box_type = QSpinBox
    boxes = []
    for i in range(n):
        if parent is not None:
            widget = box_type(parent)
        else:
            widget = box_type()
        widget.setMinimum(min)
        widget.setMaximum(max)
        widget.setSingleStep(step)
        widget.setValue(default)

        if fixed:
            widget.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        boxes.append(widget)
    if len(boxes) == 1:
        return boxes[0]
    return boxes


def add_to_group(title, widget, layout, L=7, T=20, R=7, B=11):
    """Adds a single widget to a layout as a named group with margins specified.

    Args:
        title: title of the group
        widget: widget to add in the group
        layout: layout to add the group in
        L: left margin (in pixels)
        T: top margin (in pixels)
        R: right margin (in pixels)
        B: bottom margin (in pixels)

    """
    group, layout_internal = make_group(title, L, T, R, B)
    layout_internal.addWidget(widget)
    group.setLayout(layout_internal)
    layout.addWidget(group)


def make_group(title, L=7, T=20, R=7, B=11, parent=None):  # TODO : child class
    """Creates a group widget and layout, with a header (`title`) and content margins for top/left/right/bottom `L, T, R, B` (in pixels)
    Group widget and layout returned will have a Fixed size policy.

    Args:
        title (str): Title of the group
        L (int): left margin
        T (int): top margin
        R (int): right margin
        B (int): bottom margin
        parent (QWidget) : parent widget. If None, no parent is set
    """
    if parent is None:
        group = QGroupBox(title)
    else:
        group = QGroupBox(title, parent=parent)
    group.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
    layout = QVBoxLayout()
    layout.setContentsMargins(L, T, R, B)
    layout.setSizeConstraint(QLayout.SetFixedSize)

    return group, layout


def make_container(
    L=0, T=0, R=1, B=11, vertical=True, parent=None
):  # TODO child class?
    """Creates a QWidget and a layout for the purpose of containing other modules, with a Fixed layout.

    Args:
        parent : parent widget. If None, no widget is set
        L (int): left margin of layout
        T (int): top margin of layout
        R (int): right margin of layout
        B (int): bottom margin of layout
        vertical (bool): if False, uses QHBoxLayout instead of QVboxLayout. Default: True

    Returns:
        QWidget : widget that contains the other widgets. Fixed size.
        QBoxLayout :  H/V Box layout to add contained widgets in. Fixed size.
    """
    if parent is None:
        container_widget = QWidget()
    else:
        container_widget = QWidget(parent)

    if vertical:
        container_layout = QVBoxLayout()
    else:
        container_layout = QHBoxLayout()
    container_layout.setContentsMargins(L, T, R, B)
    container_layout.setSizeConstraint(QLayout.SetFixedSize)

    return container_widget, container_layout


def make_combobox():  # TODO finish child class conversion
    """Creates a dropdown menu with a title and adds specified entries to it

    Args:
        entries (array(str)): Entries to add to the dropdown menu. Defaults to None, no entries if None
        parent (QWidget): parent QWidget to add dropdown menu to. Defaults to None, no parent is set if None
        label (str) : if not None, creates a QLabel with the contents of 'label', and returns the label as well
        fixed (bool): if True, will set the size policy of the dropdown menu to Fixed in h and w. Defaults to True.

    Returns:
        QComboBox : created dropdown menu
    """
    raise NotImplementedError


def add_widgets(layout, widgets, alignment=LEFT_AL):
    """Adds all widgets in the list to layout, with the specified alignment.
    If alignment is None, no alignment is set.
    Args:
        layout: layout to add widgets in
        widgets: list of QWidgets to add to layout
        alignment: any valid Qt.AlignmentFlag, see aliases at beginning of interface.py. If None, uses default of addWidget
    """
    if alignment is None:
        for w in widgets:
            layout.addWidget(w)
    else:
        for w in widgets:
            layout.addWidget(w, alignment=alignment)


def make_checkbox(  # TODO update calls to class
    title: str = None,
    func: callable = None,
    parent: QWidget = None,
    fixed: bool = True,
):
    """Creates a checkbox with a title and connects it to a function when clicked

    Args:
        title (str-like): title of the checkbox. Defaults to None, if None no title is set
        func (callable): function to execute when checkbox is toggled. Defaults to None, no binding is made if None
        parent (QWidget): parent QWidget to add checkbox to. Defaults to None, no parent is set if None
        fixed (bool): if True, will set the size policy of the checkbox to Fixed in h and w. Defaults to True.

    Returns:
        QCheckBox : created widget
    """

    return CheckBox(title, func, parent, fixed)


def combine_blocks(
    right_or_below,
    left_or_above,
    min_spacing=0,
    horizontal=True,
    l=11,
    t=3,
    r=11,
    b=11,
):
    """Combines two QWidget objects and puts them side by side (first on the left/top and second on the right/bottom depending on "horizontal")
       Weird argument names due the initial implementation of it.  # TODO maybe fix arg names

    Args:
        horizontal (bool): whether to stack widgets vertically (False) or horizontally (True)
        left_or_above (QWidget): First widget, to be added on the left/above of "second"
        right_or_below (QWidget): Second widget, to be displayed right/below of "first"
        min_spacing (int): Minimum spacing between the two widgets (from the start of label to the start of button)

    Returns:
        QWidget: new QWidget containing the merged widget and label
    """
    temp_widget = QWidget()
    temp_widget.setSizePolicy(
        QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding
    )

    temp_layout = QGridLayout()
    if horizontal:
        temp_widget.setSizePolicy(
            QSizePolicy.MinimumExpanding, QSizePolicy.Maximum
        )
        temp_layout.setColumnMinimumWidth(0, min_spacing)
        c1, c2, r1, r2 = 0, 1, 0, 0
        temp_layout.setContentsMargins(
            l, t, r, b
        )  # determines spacing between widgets
    else:
        temp_widget.setSizePolicy(
            QSizePolicy.Maximum, QSizePolicy.MinimumExpanding
        )
        temp_layout.setRowMinimumHeight(0, min_spacing)
        c1, c2, r1, r2 = 0, 0, 0, 1
        temp_layout.setContentsMargins(
            l, t, r, b
        )  # determines spacing between widgets
    # temp_layout.setColumnMinimumWidth(1,100)
    # temp_layout.setSizeConstraint(QLayout.SetMinAndMaxSize)

    temp_layout.addWidget(left_or_above, r1, c1)  # , alignment=LEFT_AL)
    # temp_layout.addStretch(100)
    temp_layout.addWidget(right_or_below, r2, c2)  # , alignment=LEFT_AL)
    temp_widget.setLayout(temp_layout)
    return temp_widget


def open_url(url):
    """Opens the url given as a string in OS default browser using :py:func:`QDesktopServices.openUrl`.

    Args:
        url (str): Url to be opened
    """
    QDesktopServices.openUrl(QUrl(url, QUrl.TolerantMode))
