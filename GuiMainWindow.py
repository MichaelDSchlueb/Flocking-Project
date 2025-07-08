import sys
import os

from GuiFlockingArea import GuiFlockingArea
from Vector2d import Vector2d

from PySide6.QtWidgets import *
from PySide6.QtCore import * # type: ignore
from PySide6.QtUiTools import QUiLoader


class GuiMainWindow(QWidget):
    def __init__(self):
        super(GuiMainWindow, self).__init__()

        #self.load_ui()

        # Create flocking area widget
        self.flockingAreaWidget = GuiFlockingArea()


        # Create animation timer and set its callback
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.callback_timerUpdated)
        self.timer.start(50)

        flockLayout = QVBoxLayout()
        flockLayout.addWidget(self.flockingAreaWidget)
        frame = QFrame()
        frame.setLayout(flockLayout)
        frame.setMinimumSize(200,300)

        # Create controls
        spacerItem = QSpacerItem(1,1, QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.speedLBL        = QLabel("Speed")
        self.avoidLBL        = QLabel("Avoid")
        self.alignLBL        = QLabel("Align")
        self.approLBL        = QLabel("Approach")
        self.numPreyLBL      = QLabel("Num Prey:")
        self.numPredatorsLBL = QLabel(" Num Predators:")
        self.numObstaclesLBL = QLabel(" Num Obstacles:")
        mainLayout           = QVBoxLayout()
        speedLayout          = QVBoxLayout()
        avoidLayout          = QVBoxLayout()
        alignLayout          = QVBoxLayout()
        approLayout          = QVBoxLayout()
        labelsLayout         = QHBoxLayout()
        controlsLayout       = QHBoxLayout()
        buttonLayout         = QHBoxLayout()
        self.numPreyLE       = QLineEdit()
        self.numPredatorsLE  = QLineEdit()
        self.numObstaclesLE  = QLineEdit()
        self.runPB           = QPushButton("Go")
        self.resetPB         = QPushButton("Reset")
        self.addObstaclePB   = QPushButton("Add Obstacle")
        self.remObstaclePB   = QPushButton("Remove Obstacles")
        self.addPredatorPB   = QPushButton("Add Predator")
        self.addPreyPB       = QPushButton("Add Prey")
        self.remPredatorPB   = QPushButton("Remove Predators")
        self.testPB          = QPushButton("Test")
        self.feelersCB       = QCheckBox("Look-Ahead Vectors")
        self.speedSL         = QSlider()
        self.avoidSL         = QSlider()
        self.alignSL         = QSlider()
        self.approSL         = QSlider()
        self.speedSL.setOrientation(Qt.Orientation.Vertical)
        mainLayout.addWidget(frame)

        speedLayout.addWidget(self.speedSL)
        speedLayout.addWidget(self.speedLBL)
        avoidLayout.addWidget(self.avoidSL)
        avoidLayout.addWidget(self.avoidLBL)
        alignLayout.addWidget(self.alignSL)
        alignLayout.addWidget(self.alignLBL)
        approLayout.addWidget(self.approSL)
        approLayout.addWidget(self.approLBL)

        controlsLayout.addSpacerItem(spacerItem)
        controlsLayout.addLayout(speedLayout)
        controlsLayout.addSpacerItem(spacerItem)
        controlsLayout.addLayout(avoidLayout)
        controlsLayout.addSpacerItem(spacerItem)
        controlsLayout.addLayout(alignLayout)
        controlsLayout.addSpacerItem(spacerItem)
        controlsLayout.addLayout(approLayout)
        controlsLayout.addSpacerItem(spacerItem)

        buttonLayout.addWidget(self.runPB)
        buttonLayout.addWidget(self.addPreyPB)
        buttonLayout.addWidget(self.addObstaclePB)
        buttonLayout.addWidget(self.remObstaclePB)
        buttonLayout.addWidget(self.addPredatorPB)
        buttonLayout.addWidget(self.remPredatorPB)
        buttonLayout.addWidget(self.resetPB)
        buttonLayout.addWidget(self.testPB)
        self.testPB.hide()

        labelsLayout.addWidget(self.numPreyLBL)
        labelsLayout.addWidget(self.numPreyLE)
        labelsLayout.addWidget(self.numPredatorsLBL)
        labelsLayout.addWidget(self.numPredatorsLE)
        labelsLayout.addWidget(self.numObstaclesLBL)
        labelsLayout.addWidget(self.numObstaclesLE)
        labelsLayout.addSpacerItem(spacerItem)
        labelsLayout.addWidget(self.feelersCB)

        mainLayout.addLayout(labelsLayout)
        mainLayout.addLayout(controlsLayout)
        mainLayout.addLayout(buttonLayout)

        self.numPreyLE.setMaximumWidth(40)
        self.numPredatorsLE.setFixedWidth(30)
        self.numObstaclesLE.setFixedWidth(30)
        self.numPreyLE.setAlignment(Qt.AlignRight)
        self.numPredatorsLE.setAlignment(Qt.AlignRight)
        self.numObstaclesLE.setAlignment(Qt.AlignRight)
        self.numPreyLE.setReadOnly(True)
        self.numPredatorsLE.setReadOnly(True)
        self.numObstaclesLE.setReadOnly(True)
        self.testPB.setFixedWidth(50)

        self.setLayout(mainLayout)

        # Set stretch for layout members
        mainLayout.setStretch(0,1)
        mainLayout.setStretch(1,0)
        mainLayout.setStretch(2,0)

        #
        # Create connections for the controls here...
        self.runPB.clicked.connect(self.callback_run)
        self.addPreyPB.clicked.connect(self.callback_addPrey)
        self.addObstaclePB.clicked.connect(self.callback_addObstacle)
        self.remObstaclePB.clicked.connect(self.callback_removeObstacles)
        self.addPredatorPB.clicked.connect(self.callback_addPredator)
        self.remPredatorPB.clicked.connect(self.callback_removePredators)
        self.resetPB.clicked.connect(self.callback_resetWidgets)
        self.speedSL.valueChanged.connect(self.callback_speedChanged)
        self.feelersCB.stateChanged.connect(self.callback_feelersCB)
        self.avoidSL.valueChanged.connect(self.callback_avoidChanged)
        self.alignSL.valueChanged.connect(self.callback_alignChanged)
        self.approSL.valueChanged.connect(self.callback_approachChanged)

        # Setup the sizing policy for the GUI
        sizePolicy = QSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        sizePolicy.setVerticalStretch(1)
        self.flockingAreaWidget.setSizePolicy(sizePolicy)
        self.flockingAreaWidget.initialize()

        # Setup some tooltips
        self.feelersCB.setToolTip("Show each prey agent's \"ahead\" vector")
        self.testPB.setToolTip("Create 1 prey agent and 1 obstacle")
        self.speedSL.setToolTip("Change the current speed of the simulation")
        self.avoidSL.setToolTip("Change how much the prey agents avoid each other")
        self.alignSL.setToolTip("Change how the prey agents align their neighbors")
        self.approSL.setToolTip("Change how the prey agents approach each other")
        self.runPB.setToolTip("Click to begin and end the simulation")
        self.addPreyPB.setToolTip("Add prey to the simulation")
        self.addObstaclePB.setToolTip("Add an obstacle in the path of the prey agents")
        self.remObstaclePB.setToolTip("Remove an obstacle from the path of the prey agents")
        self.addPredatorPB.setToolTip("Add a predator to the simulation")
        self.remPredatorPB.setToolTip("Remove a predator from the simulation")
        self.resetPB.setToolTip("Reset the sliders")

        self.callback_resetWidgets()

        # Set main window attributes
        self.flockingAreaWidget.setBrush(Qt.BrushStyle.SolidPattern)
        self.setWindowTitle("Flocking - Michael Schlueb")
        self.flockingAreaWidget.callback_reset()

    def load_ui(self):
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        print("path: ", path)

        ui_file = QFile(path)
        if not ui_file.open(QIODevice.ReadOnly):
            print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
            sys.exit(-1)
        loader = QUiLoader()
        print(5)
        loader.load(ui_file)
        print(6)
        ui_file.close()
        """
        print(1)
        loader = QUiLoader()
        print(2)
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        print("path: ", path)
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()
        """

    def removeAll(self):
        self.flockingAreaWidget.removePrey()
        self.callback_removePredators()
        self.callback_removeObstacles()

    def updateObstaclesLE(self, numObstacles):
        self.numObstaclesLE.setText(str(numObstacles))

    def updatePredatorLE(self, numPredators):
        self.numPredatorsLE.setText(str(numPredators))

    def updatePreyLE(self, numPrey):
        self.numPreyLE.setText(str(numPrey))

    # --- callbacks ---

    def callback_addPredator(self):
        self.updatePredatorLE(self.flockingAreaWidget.createPredators(1))

    def callback_addPrey(self):
        self.updatePreyLE(self.flockingAreaWidget.createPrey(10))

    def callback_addObstacle(self):
        self.updateObstaclesLE(self.flockingAreaWidget.createObstacles(1))

    def callback_avoidChanged(self, value):
        self.flockingAreaWidget.setWeightAvoid(value/100.0)

    def callback_alignChanged(self, value):
        self.flockingAreaWidget.setWeightAlign(value/100.0)

    def callback_approachChanged(self, value):
        self.flockingAreaWidget.setWeightApproach(value/100.0)

    def callback_createJustOneObstacle(self):
        self.flockingAreaWidget.setNumObstacles(1)

    def callback_createOneAgent(self):
        self.flockingAreaWidget.setNumAgents(1)

    def callback_feelersCB(self, state):
        self.flockingAreaWidget.showFeelers(Qt.CheckState(state)==Qt.Checked)

    def callback_removeObstacles(self):
        self.flockingAreaWidget.removeObstacles()
        self.updateObstaclesLE(0)

    def callback_removePredators(self):
        self.flockingAreaWidget.removePredators()
        self.updatePredatorLE(0)

    def callback_resetWidgets(self):
        self.speedSL.setValue(50)
        self.avoidSL.setValue(int(100*(4/8.0)))
        self.alignSL.setValue(int(100*(3/8.0)))
        self.approSL.setValue(int(100*(1/8.0)))
        self.removeAll()
        self.updatePreyLE(self.flockingAreaWidget.createPrey(100))

    def callback_run(self):
        if (self.runPB.text() == "Stop"):
            self.runPB.setText("Go")
        else:
            self.runPB.setText("Stop")
        self.flockingAreaWidget.callback_stop()

        numPrey      = self.flockingAreaWidget.getNumPrey()
        numPredators = self.flockingAreaWidget.getNumPredators()
        numObstacles = self.flockingAreaWidget.getNumObstacles()

        self.updatePreyLE(numPrey)
        self.updatePredatorLE(numPredators)
        self.updateObstaclesLE(numObstacles)

    def callback_speedChanged(self, value):
        self.timer.setInterval(100-value)


    def callback_test(self):
        self.removeAll()
        self.updatePreyLE(self.flockingAreaWidget.createPrey(1))
        self.updateObstaclesLE(self.flockingAreaWidget.createTestObstacle())

    def callback_timerUpdated(self):
        self.flockingAreaWidget.update()
