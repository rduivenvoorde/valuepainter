from PyQt5.QtWidgets import QAction, QLineEdit, QComboBox

from qgis.gui import QgsMapLayerComboBox, QgsFieldComboBox, QgsMapToolIdentifyFeature

from qgis.core import QgsMapLayerProxyModel, QgsVectorLayer, QgsValueMapFieldFormatter




class ValuePainter:

    def __init__(self, iface):
        self.iface = iface
        self.old_map_tool = self.iface.mapCanvas().mapTool()


    def initGui(self):
        self.toolbar = self.iface.addToolBar("Value Painter")

        self.action_paint = QAction('Paint!', self.iface.mainWindow())
        self.action_paint.setCheckable(True)
        self.toolbar.addAction(self.action_paint)

        self.paint_tool = QgsMapToolIdentifyFeature(self.iface.mapCanvas())
        self.paint_tool.setAction(self.action_paint)

        self.layer_picker = QgsMapLayerComboBox()
        self.layer_picker.setFilters(QgsMapLayerProxyModel.VectorLayer)
        self.layer_picker_action = self.toolbar.addWidget(self.layer_picker)

        self.field_picker = QgsFieldComboBox()
        self.field_picker_action = self.toolbar.addWidget(self.field_picker)

        self.editor_widget = None
        self.editor_widget_action = None

        self.paint_tool.featureIdentified.connect(self.featureIdentified)
        self.action_paint.triggered.connect(self.togglePaintTool)
        self.layer_picker.layerChanged.connect(self.updateFieldPicker)
        self.field_picker.fieldChanged.connect(self.updateEditorWidget)


    def unload(self):
        self.paint_tool.featureIdentified.disconnect(self.featureIdentified)
        self.layer_picker.layerChanged.disconnect(self.updateFieldPicker)
        self.field_picker.fieldChanged.disconnect(self.updateEditorWidget)
        self.action_paint.triggered.disconnect(self.togglePaintTool)

        if self.editor_widget_action is not None:
            self.toolbar.removeAction(self.editor_widget_action)
        self.toolbar.removeAction(self.field_picker_action)
        self.toolbar.removeAction(self.layer_picker_action)
        self.toolbar.removeAction(self.action_paint)
        del self.action_paint
        del self.toolbar


    def updateFieldPicker(self):
        if isinstance(self.layer_picker.currentLayer(), QgsVectorLayer):
            self.paint_tool.setLayer(self.layer_picker.currentLayer())
            self.field_picker.setLayer(self.layer_picker.currentLayer())
        else:
            self.paint_tool.setLayer(None)
            self.field_picker.setLayer(None)


    def updateEditorWidget(self):
        layer = self.layer_picker.currentLayer()
        field_name = self.field_picker.currentField()
        field_index = layer.fields().indexFromName(field_name)
        #print(layer, field_name, field_index)

        ews = layer.editorWidgetSetup(field_index)
        #print(ews.type(), ews.config())

        self.editor_widget = self.getWidget(ews)
        #print(self.editor_widget)

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
                for key in item:
                    if item[key] == QgsValueMapFieldFormatter.NULL_VALUE:
                        value = None
                    else:
                        value = item[key]
                    result.addItem(key, value)

        if ews.type() == 'TextEdit':
            result = QLineEdit()

        return result


    def togglePaintTool(self):
        #print('paint mode:', self.action_paint.isChecked())
        self.iface.mapCanvas().setMapTool(self.paint_tool)


    def updateCurrentLayer(self):
        layer is self.iface.activeLayer()


    def featureIdentified(self, feat):
        layer = self.iface.activeLayer()
        if layer == self.layer_picker.currentLayer():
            #print('same layer')
            if layer.isEditable():
                field_name = self.field_picker.currentField()
                field_index = layer.fields().lookupField(field_name)
                value = self.getEditorWidgetValue()
                feat.setAttribute(field_index, value)
                layer.updateFeature(feat)
                layer.triggerRepaint()
            else:
                pass
                #print('layer not editable')


    def getEditorWidgetValue(self):
        widget = self.editor_widget
        if isinstance(widget, QComboBox):
            return widget.currentData()
        elif isinstance(widget, QLineEdit):
            return widget.text()
        return None
