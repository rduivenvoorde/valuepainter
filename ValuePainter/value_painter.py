from PyQt5.QtWidgets import QAction, QMessageBox, QLineEdit, QComboBox

from qgis.gui import QgsMapLayerComboBox, QgsFieldComboBox, QgsMapTool




class ValuePainter:

    def __init__(self, iface):
        self.iface = iface


    def initGui(self):
        self.toolbar = self.iface.addToolBar("Value Painter")
        print(self.toolbar)
        self.action = QAction('Paint!', self.iface.mainWindow())

        self.toolbar.addAction(self.action)
        self.action.triggered.connect(self.run)

        self.map_tool = QgsMapTool(self.iface.mapCanvas())
        print(self.map_tool)
        self.map_tool_action = self.toolbar.addWidget(self.map_tool)

        self.layer_picker = QgsMapLayerComboBox()
        self.layer_picker_action = self.toolbar.addWidget(self.layer_picker)

        self.field_picker = QgsFieldComboBox()
        self.field_picker_action = self.toolbar.addWidget(self.field_picker)

        self.editor_widget = None
        self.editor_widget_action = None

        self.layer_picker.layerChanged.connect(self.updateFieldPicker)
        self.field_picker.fieldChanged.connect(self.updateEditorWidget)


    def unload(self):
        self.layer_picker.layerChanged.disconnect(self.updateFieldPicker)
        self.field_picker.fieldChanged.disconnect(self.updateEditorWidget)
        self.action.triggered.disconnect(self.run)

        self.toolbar.removeAction(self.action)
        del self.action
        del self.toolbar


    def run(self):
        QMessageBox.information(None, 'Value Painter plugin', 'Do something useful here...')


    def updateFieldPicker(self):
        self.field_picker.setLayer(self.layer_picker.currentLayer())


    def updateEditorWidget(self):
        layer = self.layer_picker.currentLayer()
        field_name = self.field_picker.currentField()
        field_index = layer.fields().indexFromName(field_name)

        print(layer, field_name, field_index)

        ews = layer.editorWidgetSetup(field_index)
        print(ews.type(), ews.config())

        self.editor_widget = self.getWidget(ews)
        print(self.editor_widget)

        if self.editor_widget_action is not None:
            self.toolbar.removeAction(self.editor_widget_action)
        if self.editor_widget is None:
            self.editor_widget_action = None
        else:
            self.editor_widget_action = self.toolbar.addWidget(self.editor_widget)


    def getWidget(self, ews):
        result = None

        if ews.type() == 'ValueMap':
            result = QComboBox()
            map = ews.config()['map']
            for item in map:
                print(item)
                for key in item:
                    result.addItem(key, item[key])

        if ews.type() == 'TextEdit':
            result = QLineEdit()

        return result
