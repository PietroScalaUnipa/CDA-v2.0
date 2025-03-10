from qgis.PyQt.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLineEdit, QMessageBox, QLabel
from qgis.PyQt.QtGui import QFont
from PyQt5.QtCore import Qt
from qgis.PyQt.QtGui import QPixmap
from qgis.core import QgsExpression 
from qgis.core import QgsFeatureRequest
import sys
import processing
from qgis.core import QgsProcessingFeatureSourceDefinition

class CoastalDynamicsAnalyzer:
    def __init__(self, iface):
        self.iface = iface
        self.plugin_dir = iface.pluginDirectory() + "/CoastalDynamicsAnalyzer"
        self.actions = []
        self.menu = 'Coastal Dynamics Analyzer'
        self.toolbar = self.iface.addToolBar('Coastal Dynamics Analyzer')
        self.toolbar.setObjectName('Coastal Dynamics Analyzer')

    def initGui(self):
        icon_path = self.plugin_dir + "/icon.png"
        self.add_action(icon_path, text="Run Coastal Dynamics Analyzer", callback=self.run, parent=self.iface.mainWindow())

    def unload(self):
        for action in self.actions:
            self.iface.removePluginMenu(self.menu, action)
            self.iface.removeToolBarIcon(action)
        del self.toolbar

    def add_action(self, icon_path, text, callback, parent=None):
        icon = QIcon(icon_path)
        action = QAction(icon, text, parent)
        action.triggered.connect(callback)
        self.iface.addPluginToMenu(self.menu, action)
        self.iface.addToolBarIcon(action)
        self.actions.append(action)
        return action

    def run(self):
        dialog = NumberInputDialog()
        dialog.exec_()


class NumberInputDialog(QDialog):
    def __init__(self):
        super(NumberInputDialog, self).__init__()
        self.setWindowTitle('Coastal Dynamics Analyzer - UNIPA')
        # Impostare il colore di sfondo sfumato
        self.setStyleSheet("""
            QDialog {
                background: qlineargradient(
                    spread:pad, x1:0, y1:0, x2:1, y2:1,
                    stop:0 #f0f0f0,  /* Grigio molto chiaro */
                    stop:1 #e0f7fa   /* Celeste molto chiaro */
                );
            }
        """)
        
        self.layout = QVBoxLayout()
        
        
        # Aggiungi un'immagine o logo decorativo
        #qgis_image = QLabel()
        #qgis_image.setPixmap(QPixmap('C:\\Users\\Niloufar\\OneDrive\\Bureau\\CDA_Icon.png').scaled(150, 150, Qt.KeepAspectRatio, Qt.SmoothTransformation))  # Ridimensiona l'immagine
        #qgis_image.setAlignment(Qt.AlignCenter)
        #self.layout.addWidget(qgis_image)
        
        note3 = QLabel ("Welcome to Coastal Dynamics Analyzer \nCDA v2.0  \nArea Based Analysis ABA")
        note3.setAlignment(Qt.AlignCenter)
        note3.setStyleSheet("font-size: 18pt; font-weight: bold; font-style: italic; font-family: Arial;")
        note3.setStyleSheet("""
        font-size: 18pt;
        font-weight: bold;
        font-style: italic;
        font-family: sans-serif;
        color: #058;
        text-shadow: 10px 10px 20px #ccc;
    """)
        
        note33 = QLabel ("Developed for QGIS, plug-in version 2.0")
        note33.setAlignment(Qt.AlignCenter)
        note33.setStyleSheet("font-size: 10pt; font-weight: bold; font-style: italic; font-family: Montserrat;")
        
        note3.show()
        
        note24 = QLabel("\n \n CREATE BASELINE:")
        font = QFont()
        font.setBold(True)
        note24.setFont(font)
        
        note224 = QLabel("\n        Enter 0 to generate a PCHIP baseline from shoreline  ^ ")
        font = QFont()
        note224.setStyleSheet("font-size: 10pt")
        
        note_ll = QLabel("^       Run 0 only the first time to create the reference baseline. \n         The plug-in will automatically save the geometry in a folder specified by the user. \n         Skip Step 0 if you calculated baseline previously with CDA v1.0   \n ")
        note_ll.setStyleSheet("font-style: italic")

        note2 = QLabel("\n \n STEP RULES *:")
        font = QFont()
        font.setBold(True)
        note2.setFont(font)
        
        note22 = QLabel("For more info see 'CDA - v.2.0 - ABA' User Manual (link below) ")
        note222 = QLabel(" ")
        
        note_label = QLabel("""        Enter 1 to create shorelines/baseline TEMP sub-areas
        Enter 2 to save area polygon shapefile between baseline and shoreline
        Enter 3 to calculate A-NSM and A-EPR polygon shapefile and save them as csv format 
        Enter 4 to calculate A-SCE and A-LRR
        Enter 5 to calculate MEAN SHORELINE SHIFT metrics (M-NSM,M-SCE,M-EPR,M-LRR)
        """)
        note_label.setStyleSheet("font-size: 10pt")
        
        note_l = QLabel("*       All steps must be executed following the presented order ")
        note_l.setStyleSheet("font-style: italic")
        
        linenote = QLabel ("______________________________________________________________________________")
        note4 = QLabel ("\n \n Powered by Department of Engineering, University of Palermo \nMarine and Coastal Engineering Lab")
        note4.setAlignment(Qt.AlignCenter)
        note4.setStyleSheet("font-size: 8pt; font-weight: bold; font-style: italic; font-family: Montserrat;")
        note4.show()

        self.layout.addWidget(note3)
        self.layout.addWidget(note33)
        self.layout.addWidget(note24)
        self.layout.addWidget(note224)
        self.layout.addWidget(note_ll)
        self.layout.addWidget(note2)
        self.layout.addWidget(note_label)
        self.layout.addWidget(note_l)
        self.layout.addWidget(linenote)
        self.layout.addWidget(note22)
        self.layout.addWidget(note222)
        
        

        self.input_field = QLineEdit()
        self.layout.addWidget(self.input_field)
        self.input_field.setPlaceholderText ("Insert a step ID [ from 0 to 5 ]")
        self.input_field.setStyleSheet("""
        QLineEdit {
            border: 2px solid #ccc;
            border-radius: 10px;
            padding: 10px;
            font-size: 14px;
        }
        QLineEdit:focus {
            border-color: #4CAF50;
        }
    """)

        ok_button = QPushButton('Run CDA - ABA')
        ok_button.clicked.connect(self.on_ok_clicked)
        
        
        # Imposta il testo in grassetto per il pulsante
        font = QFont()
        font.setBold(True)
        ok_button.setFont(font)
        self.layout.addWidget(ok_button)
        ok_button.setStyleSheet("""
        QPushButton {
            background-color: #4CAF50;  /* Verde */
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #45a049;
        }
    """)

        self.setLayout(self.layout)
        
        self.layout.addWidget(note4)
        
        note_lll = QLabel(" \n Cite as Scala et al., 2025 ")
        note_lll.setStyleSheet("font-style: italic")
        note_lll.setAlignment(Qt.AlignRight)  # Imposta l'allineamento a sinistra
        self.layout.addWidget(note_lll)

        # Crea una QLabel per il testo del link
        link_label = QLabel('<a href="https://github.com/PietroScalaUnipa/CDA-v2.0">Click here</a>')
        link_label.setOpenExternalLinks(True)  # Apre il link nel browser esterno quando viene cliccato
        link_label.setAlignment(Qt.AlignRight)  # Imposta l'allineamento a destra

        # Aggiungi la QLabel al layout
        self.layout.addWidget(link_label)
        
        # Pulsante rosso per chiudere la finestra
        # Pulsante rosso per chiudere la finestra
        quit_button = QPushButton('Quit CDA - ABA')
        quit_button.setStyleSheet("background-color: grey;")
        quit_button.clicked.connect(self.reject)  # Chiude la finestra di dialogo
        quit_button.setStyleSheet("""
        QPushButton {
            background-color: #f44336;  /* Rosso */
            color: white;
            border: none;
            border-radius: 10px;
            padding: 10px 20px;
            font-size: 14px;
        }
        QPushButton:hover {
            background-color: #e53935;
        }
    """)

        # Imposta il testo in grassetto per il pulsante
        font = QFont()
        font.setBold(True)
        quit_button.setFont(font)

        # Aggiungi il pulsante al layout
        self.layout.addWidget(quit_button)

    def on_ok_clicked(self):
        try:
            global AA
            input_value = int(self.input_field.text())
            if -1 < input_value < 6:
                AA = input_value
                self.accept()  # Chiude la finestra di dialogo
            else:
                QMessageBox.warning(self, 'CDA Error', 'Insert a valid number step between 0 and 5')
        except ValueError:
            QMessageBox.warning(self, 'CDA Error', 'Insert a valid number step')
# Creazione e visualizzazione della finestra di dialogo
dialog = NumberInputDialog()
if dialog.exec_() == QDialog.Accepted:
    print("Insert Number:", AA)
else:
    print("Quit")
    dialog.close()

if AA ==1:
    from qgis.core import QgsProcessing
    from qgis.core import QgsProcessingAlgorithm
    from qgis.core import QgsProcessingMultiStepFeedback
    from qgis.core import QgsProcessingParameterVectorLayer
    from qgis.core import QgsProcessingParameterFolderDestination
    import processing


    class Cda_aba_step_1(QgsProcessingAlgorithm):

        def initAlgorithm(self, config=None):
            # Insert the shapefiole linestring baseline (Follow the CDA v1.0.0 requirements)
            self.addParameter(QgsProcessingParameterVectorLayer('insert_baseline_layer_cda_v100_step_0_or_equal', 'Insert baseline layer (CDA_v1.0.0 Step 0 or equal)', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
            self.addParameter(QgsProcessingParameterVectorLayer('insert_shoreline_layer_cda_v100_requirements_or_equal', 'Insert shoreline layer (CDA_v1.0.0 requirements or equal)', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
            self.addParameter(QgsProcessingParameterFolderDestination('InsertTempSubareaFolder', 'Insert TEMP sub-area folder', createByDefault=True, defaultValue='C:\\'))

        def processAlgorithm(self, parameters, context, model_feedback):
            # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
            # overall progress through the model
            feedback = QgsProcessingMultiStepFeedback(4, model_feedback)
            results = {}
            outputs = {}

            # Area perimeter delimitation - Merge linestring
            alg_params = {
                'CRS': None,
                'LAYERS': [parameters['insert_baseline_layer_cda_v100_step_0_or_equal'],parameters['insert_shoreline_layer_cda_v100_requirements_or_equal']],
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['AreaPerimeterDelimitationMergeLinestring'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(1)
            if feedback.isCanceled():
                return {}

            # Area calculation from semi perimeter
            alg_params = {
                'INPUT': outputs['AreaPerimeterDelimitationMergeLinestring']['OUTPUT'],
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['AreaCalculationFromSemiPerimeter'] = processing.run('qgis:linestopolygons', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(2)
            if feedback.isCanceled():
                return {}

            # Repair corrupted areas
            alg_params = {
                'INPUT': outputs['AreaCalculationFromSemiPerimeter']['OUTPUT'],
                'METHOD': 1,  # Struttura
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['RepairCorruptedAreas'] = processing.run('native:fixgeometries', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(3)
            if feedback.isCanceled():
                return {}

            # Sepairing baseline and shorelinearea  layers 
            alg_params = {
                'FIELD': 'ID',
                'FILE_TYPE': 1,  # shp
                'INPUT': outputs['RepairCorruptedAreas']['OUTPUT'],
                'PREFIX_FIELD': True,
                'OUTPUT': parameters['InsertTempSubareaFolder']
            }
            outputs['SepairingBaselineAndShorelineareaLayers'] = processing.run('native:splitvectorlayer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['InsertTempSubareaFolder'] = outputs['SepairingBaselineAndShorelineareaLayers']['OUTPUT']
            return results

        def name(self):
            return 'CDA_ABA_step_1'

        def displayName(self):
            return 'CDA_ABA_step_1'

        def group(self):
            return 'CDA_v2.0.0_ABA'

        def groupId(self):
            return 'CDA_v2.0.0_ABA'

        def createInstance(self):
            return Cda_aba_step_1()



elif AA == 2:
    from qgis.core import QgsProcessing
    from qgis.core import QgsProcessingAlgorithm
    from qgis.core import QgsProcessingMultiStepFeedback
    from qgis.core import QgsProcessingParameterVectorLayer
    from qgis.core import QgsProcessingParameterFeatureSink
    import processing


    class Cda_aba_step_2(QgsProcessingAlgorithm):

        def initAlgorithm(self, config=None):
            self.addParameter(QgsProcessingParameterVectorLayer('insert_baseline_area_layer_from_temp_step_1_cda_aba', 'Insert baseline area layer (from TEMP step 1 CDA_ABA)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
            self.addParameter(QgsProcessingParameterVectorLayer('insert_shoreline_area_layer_from_temp_step_1_cda_aba', 'Insert shoreline area layer (from TEMP step 1 CDA_ABA)', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
            self.addParameter(QgsProcessingParameterFeatureSink('SaveShorelinebaselinePolygonShapefile', 'Save Shoreline-Baseline polygon shapefile', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT'))

        def processAlgorithm(self, parameters, context, model_feedback):
            # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
            # overall progress through the model
            feedback = QgsProcessingMultiStepFeedback(3, model_feedback)
            results = {}
            outputs = {}

            # Clipping geometries - symmetrical
            alg_params = {
                'GRID_SIZE': None,
                'INPUT': parameters['insert_shoreline_area_layer_from_temp_step_1_cda_aba'],
                'OVERLAY': parameters['insert_baseline_area_layer_from_temp_step_1_cda_aba'],
                'OVERLAY_FIELDS_PREFIX': '',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['ClippingGeometriesSymmetrical'] = processing.run('native:symmetricaldifference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(1)
            if feedback.isCanceled():
                return {}

            # Select area between linestring
            alg_params = {
                'EXPRESSION': 'path_2',
                'INPUT': outputs['ClippingGeometriesSymmetrical']['OUTPUT'],
                'METHOD': 0,  # crea nuova selezione
            }
            outputs['SelectAreaBetweenLinestring'] = processing.run('qgis:selectbyexpression', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(2)
            if feedback.isCanceled():
                return {}

            # Estrarre elementi selezionati
            alg_params = {
                'INPUT': outputs['SelectAreaBetweenLinestring']['OUTPUT'],
                'OUTPUT': parameters['SaveShorelinebaselinePolygonShapefile']
            }
            outputs['EstrarreElementiSelezionati'] = processing.run('native:saveselectedfeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['SaveShorelinebaselinePolygonShapefile'] = outputs['EstrarreElementiSelezionati']['OUTPUT']
            return results

        def name(self):
            return 'CDA_ABA_step_2'

        def displayName(self):
            return 'CDA_ABA_step_2'

        def group(self):
            return 'CDA_v2.0.0_ABA'

        def groupId(self):
            return ''

        def createInstance(self):
            return Cda_aba_step_2()



elif AA == 3:
    from qgis.core import QgsProcessing
    from qgis.core import QgsProcessingAlgorithm
    from qgis.core import QgsProcessingMultiStepFeedback
    from qgis.core import QgsProcessingParameterVectorLayer
    from qgis.core import QgsProcessingParameterNumber
    from qgis.core import QgsProcessingParameterString
    from qgis.core import QgsProcessingParameterFeatureSink
    from qgis.core import QgsProcessingParameterFileDestination
    import processing


    class Cda_aba_step3(QgsProcessingAlgorithm):

        def initAlgorithm(self, config=None):
            self.addParameter(QgsProcessingParameterVectorLayer('insert_baseline_shapefile_same_of_cda_v100_step_0_result_or_equivalent', 'Insert baseline shapefile (same of CDA v1.0.0 step 0 result or equivalent)', types=[QgsProcessing.TypeVectorLine], defaultValue=None))
            self.addParameter(QgsProcessingParameterNumber('insert_length_of_transect_same_of_cda_v100_or_equivalent', 'Insert length of transect (same of CDA v1.0.0 or equivalent)', type=QgsProcessingParameterNumber.Double, defaultValue=None))
            self.addParameter(QgsProcessingParameterVectorLayer('insert_shoreline_area_1', 'Insert shoreline area 1', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
            self.addParameter(QgsProcessingParameterString('insert_shoreline_area_1_date', 'Insert shoreline area 1 date', multiLine=False, defaultValue='DD/MM/YYYY'))
            self.addParameter(QgsProcessingParameterVectorLayer('insert_shoreline_area_2', 'Insert shoreline area 2', types=[QgsProcessing.TypeVectorPolygon], defaultValue=None))
            self.addParameter(QgsProcessingParameterString('insert_shoreline_area_2_date', 'Insert shoreline area 2 date', multiLine=False, defaultValue='DD/MM/YYYY'))
            self.addParameter(QgsProcessingParameterNumber('insert_side_of_transect_creation_0left_1right_2both', 'Insert side of transect creation (0->left; 1->right; 2->both)', type=QgsProcessingParameterNumber.Integer, minValue=0, maxValue=2, defaultValue=None))
            self.addParameter(QgsProcessingParameterNumber('insert_spacing_between_transect_same_of_cda_v100_or_equivalent', 'Insert spacing between transect (same of CDA v1.0.0 or equivalent)', type=QgsProcessingParameterNumber.Double, defaultValue=None))
            self.addParameter(QgsProcessingParameterNumber('insert_time_between_shoreline_areas_years', 'Insert time between shoreline areas (Years)', type=QgsProcessingParameterNumber.Double, defaultValue=None))
            self.addParameter(QgsProcessingParameterFeatureSink('DifferenceN1A1A2', 'Difference n°1 (A1 - A2)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue='TEMPORARY_OUTPUT'))
            self.addParameter(QgsProcessingParameterFeatureSink('DifferenceN2A2A1', 'Difference n°2 (A2 - A1)', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, defaultValue=None))
            self.addParameter(QgsProcessingParameterFeatureSink('A_nsm_epr_polygons', 'A_NSM_EPR_Polygons', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))
            self.addParameter(QgsProcessingParameterFileDestination('SaveA_nsmAndA_eprResultsAsCsvFile', 'Save A_NSM and A_EPR results as CSV file', fileFilter='GeoPackage (*.gpkg *.GPKG);;ESRI shapefile (*.shp *.SHP);;(Geo)Arrow (*.arrow *.feather *.arrows *.ipc *.ARROW *.FEATHER *.ARROWS *.IPC);;(Geo)Parquet (*.parquet *.PARQUET);;AutoCAD DXF (*.dxf *.DXF);;File ESRI Geodatabase (*.gdb *.GDB);;FlatGeobuf (*.fgb *.FGB);;Foglio di calcolo MS Office Open XML [XLSX] (*.xlsx *.XLSX);;Foglio di calcolo Open Document [ODS] (*.ods *.ODS);;Formato GPS eXchange [GPX] (*.gpx *.GPX);;Formato Testo Delimitato [CSV] (*.csv *.CSV);;Geoconcept (*.gxt *.txt *.GXT *.TXT);;Geography Markup Language [GML] (*.gml *.GML);;GeoJSON - Delimitato da Newline (*.geojsonl *.geojsons *.json *.GEOJSONL *.GEOJSONS *.JSON);;GeoJSON (*.geojson *.GEOJSON);;GeoRSS (*.xml *.XML);;INTERLIS 1 (*.itf *.xml *.ili *.ITF *.XML *.ILI);;INTERLIS 2 (*.xtf *.xml *.ili *.XTF *.XML *.ILI);;Keyhole Markup Language [KML] (*.kml *.KML);;Microstation DGN (*.dgn *.DGN);;PostgreSQL SQL dump (*.sql *.SQL);;S-57 Base file (*.000 *.000);;SQLite (*.sqlite *.SQLITE);;TAB Mapinfo (*.tab *.TAB)', createByDefault=True, defaultValue=''))

        def processAlgorithm(self, parameters, context, model_feedback):
            # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
            # overall progress through the model
            feedback = QgsProcessingMultiStepFeedback(16, model_feedback)
            results = {}
            outputs = {}

            # Difference 1
            alg_params = {
                'GRID_SIZE': None,
                'INPUT': parameters['insert_shoreline_area_1'],
                'OVERLAY': parameters['insert_shoreline_area_2'],
                'OUTPUT': parameters['DifferenceN1A1A2']
            }
            outputs['Difference1'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['DifferenceN1A1A2'] = outputs['Difference1']['OUTPUT']

            feedback.setCurrentStep(1)
            if feedback.isCanceled():
                return {}

            # Difference 2
            alg_params = {
                'GRID_SIZE': None,
                'INPUT': parameters['insert_shoreline_area_2'],
                'OVERLAY': parameters['insert_shoreline_area_1'],
                'OUTPUT': parameters['DifferenceN2A2A1']
            }
            outputs['Difference2'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['DifferenceN2A2A1'] = outputs['Difference2']['OUTPUT']

            feedback.setCurrentStep(2)
            if feedback.isCanceled():
                return {}

            # Baseline discretization
            alg_params = {
                'DISTANCE': parameters['insert_spacing_between_transect_same_of_cda_v100_or_equivalent'],
                'END_OFFSET': 0,
                'INPUT': parameters['insert_baseline_shapefile_same_of_cda_v100_step_0_result_or_equivalent'],
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'START_OFFSET': 0,
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['BaselineDiscretization'] = processing.run('native:pointsalonglines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(3)
            if feedback.isCanceled():
                return {}

            # NEG
            alg_params = {
                'FIELD_LENGTH': 1,
                'FIELD_NAME': 'NEG',
                'FIELD_PRECISION': 0,
                'FIELD_TYPE': 1,  # Intero (32 bit)
                'FORMULA': '1',
                'INPUT': outputs['Difference1']['OUTPUT'],
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['Neg'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(4)
            if feedback.isCanceled():
                return {}

            # POS
            alg_params = {
                'FIELD_LENGTH': 1,
                'FIELD_NAME': 'POS',
                'FIELD_PRECISION': 0,
                'FIELD_TYPE': 1,  # Intero (32 bit)
                'FORMULA': '1',
                'INPUT': outputs['Difference2']['OUTPUT'],
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['Pos'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(5)
            if feedback.isCanceled():
                return {}

            # Baseline from spacing
            alg_params = {
                'CLOSE_PATH': False,
                'GROUP_EXPRESSION': '',
                'INPUT': outputs['BaselineDiscretization']['OUTPUT'],
                'NATURAL_SORT': False,
                'ORDER_EXPRESSION': '',
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'OUTPUT_TEXT_DIR': None,
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['BaselineFromSpacing'] = processing.run('native:pointstopath', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(6)
            if feedback.isCanceled():
                return {}

            # Merge total areas
            alg_params = {
                'CRS': None,
                'LAYERS': [outputs['Neg']['OUTPUT'],outputs['Pos']['OUTPUT']],
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['MergeTotalAreas'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(7)
            if feedback.isCanceled():
                return {}

            # Transect loading
            alg_params = {
                'ANGLE': 90,
                'INPUT': outputs['BaselineFromSpacing']['OUTPUT'],
                'LENGTH': parameters['insert_length_of_transect_same_of_cda_v100_or_equivalent'],
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'SIDE': parameters['insert_side_of_transect_creation_0left_1right_2both'],
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['TransectLoading'] = processing.run('native:transect', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(8)
            if feedback.isCanceled():
                return {}

            # Transect univ. ID
            alg_params = {
                'FIELD_LENGTH': 0,
                'FIELD_NAME': 'TR_ID1',
                'FIELD_PRECISION': 0,
                'FIELD_TYPE': 1,  # Intero (32 bit)
                'FORMULA': '"TR_SEGMENT"',
                'INPUT': outputs['TransectLoading']['OUTPUT'],
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['TransectUnivId'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(9)
            if feedback.isCanceled():
                return {}

            # Split sub-areas from transect 1
            alg_params = {
                'INPUT': outputs['MergeTotalAreas']['OUTPUT'],
                'LINES': outputs['TransectUnivId']['OUTPUT'],
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['SplitSubareasFromTransect1'] = processing.run('native:splitwithlines', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(10)
            if feedback.isCanceled():
                return {}

            # Fields adding operation X pos
            alg_params = {
                'FIELD_LENGTH': 100,
                'FIELD_NAME': 'X',
                'FIELD_PRECISION': 5,
                'FIELD_TYPE': 2,  # Testo (stringa)
                'FORMULA': 'to_string(x($geometry))\r\n',
                'INPUT': outputs['SplitSubareasFromTransect1']['OUTPUT'],
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['FieldsAddingOperationXPos'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(11)
            if feedback.isCanceled():
                return {}

            # Area calculation 1
            alg_params = {
                'FIELD_LENGTH': 15,
                'FIELD_NAME': 'A_NSM',
                'FIELD_PRECISION': 3,
                'FIELD_TYPE': 0,  # Decimale (doppia precisione)
                'FORMULA': 'CASE WHEN "NEG"=1 THEN -$area \r\nWHEN "POS"=1 THEN $area \r\nEND',
                'INPUT': outputs['FieldsAddingOperationXPos']['OUTPUT'],
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['AreaCalculation1'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(12)
            if feedback.isCanceled():
                return {}

            # Univ. ID area
            alg_params = {
                'DISCARD_NONMATCHING': False,
                'INPUT': outputs['AreaCalculation1']['OUTPUT'],
                'JOIN': outputs['TransectLoading']['OUTPUT'],
                'JOIN_FIELDS': ['TR_SEGMENT'],
                'METHOD': 1,  # Prendi solamente gli attributi del primo elemento corrispondente (uno-a-uno)
                'NON_MATCHING': None,
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'PREDICATE': [0,3,4,6],  # interseca,tocca,sovrappone,attraversa
                'PREFIX': '',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['UnivIdArea'] = processing.run('native:joinattributesbylocation', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(13)
            if feedback.isCanceled():
                return {}

            # Calculate EPR
            alg_params = {
                'FIELD_LENGTH': 10,
                'FIELD_NAME': 'A_EPR',
                'FIELD_PRECISION': 6,
                'FIELD_TYPE': 0,  # Decimale (doppia precisione)
                'FORMULA': f'"A_NSM" / {parameters["insert_time_between_shoreline_areas_years"]}',
                'INPUT': outputs['UnivIdArea']['OUTPUT'],
                'OUTPUT': 'TEMPORARY_OUTPUT',
                'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
            }
            outputs['CalculateEpr'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

            feedback.setCurrentStep(14)
            if feedback.isCanceled():
                return {}

            # Date calculator
            alg_params = {
                'FIELD_LENGTH': 10,
                'FIELD_NAME': 'date',
                'FIELD_PRECISION': 10,
                'FIELD_TYPE': 2,  # Testo (stringa)
                'FORMULA': f"'{parameters['insert_shoreline_area_2_date']}'",  # Usa apici singoli per la stringa della data
                'INPUT': outputs['CalculateEpr']['OUTPUT'],
                'OUTPUT': parameters['A_nsm_epr_polygons']
            }
            outputs['DateCalculator'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['A_nsm_epr_polygons'] = outputs['DateCalculator']['OUTPUT']

            feedback.setCurrentStep(15)
            if feedback.isCanceled():
                return {}

            # Save CSV
            alg_params = {
                'ACTION_ON_EXISTING_FILE': 0,  # Crea o sovrascrive un file
                'DATASOURCE_OPTIONS': '',
                'INPUT': outputs['DateCalculator']['OUTPUT'],
                'LAYER_NAME': '',
                'LAYER_OPTIONS': '',
                'OUTPUT': parameters['SaveA_nsmAndA_eprResultsAsCsvFile']
            }
            outputs['SaveCsv'] = processing.run('native:savefeatures', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
            results['SaveA_nsmAndA_eprResultsAsCsvFile'] = outputs['SaveCsv']['OUTPUT']
            return results

        def name(self):
            return 'CDA_ABA_step3'

        def displayName(self):
            return 'CDA_ABA_step3'

        def group(self):
            return 'CDA_v2.0.0_ABA'

        def groupId(self):
            return 'CDA_v2.0.0_ABA'

        def createInstance(self):
            return Cda_aba_step3()


elif AA == 4:
    import os
    import csv
    from PyQt5.QtWidgets import QFileDialog
    from collections import defaultdict
    import datetime
    import numpy as np

    # Seleziona la cartella
    folder_path = QFileDialog.getExistingDirectory(None, "CDA - Select CSV saved folder")

    # Verifica che la cartella sia stata selezionata
    if not folder_path:
        print("No folder selected.")
        exit()

    # Dizionario per memorizzare le informazioni di tutti i file CSV
    all_info = defaultdict(dict)
    all_tr_ids = set()

    # Importa tutti i file CSV nella cartella
    for filename in os.listdir(folder_path):
        if filename.endswith(".csv"):
            with open(os.path.join(folder_path, filename), 'r', encoding='latin-1') as csvfile:
                csv_reader = csv.DictReader(csvfile)
                for row in csv_reader:
                    tr_id = row.get("TR_SEGMENT")
                    date_str = row.get("date")
                    length_str = row.get("A_NSM")

                    # Verifica che tr_id, date e length siano validi
                    if not tr_id:
                        print(f"Nessun TR_SEGMENT trovato in {filename}")
                        continue

                    # Converti la data in formato datetime
                    if date_str:
                        try:
                            date_obj = datetime.datetime.strptime(date_str, '%d/%m/%Y')
                            date_num = date_obj.toordinal()
                        except ValueError:
                            print(f"Formato di data non valido per TR_SEGMENT {tr_id} in {filename}: {date_str}")
                            continue
                    else:
                        print(f"Nessuna data per TR_SEGMENT {tr_id} in {filename}")
                        continue

                    # Converte la lunghezza in float
                    if length_str:
                        try:
                            length = float(length_str)
                        except ValueError:
                            print(f"Valore A_NSM non valido per TR_SEGMENT {tr_id} in {filename}: {length_str}")
                            continue
                    else:
                        print(f"Nessun valore A_NSM per TR_SEGMENT {tr_id} in {filename}")
                        continue

                    all_info[filename][tr_id] = {"Date": date_num, "Length": length}
                    all_tr_ids.add(tr_id)

    # Dizionario per memorizzare i coefficienti angolari della regressione lineare per ogni TR_ID
    lrr_values = {}

    # Calcola la regressione lineare per ogni TR_ID
    for tr_id in all_tr_ids:
        x = []
        y = []
        for filename, info in all_info.items():
            if tr_id in info:
                x.append(info[tr_id]["Date"])
                y.append(info[tr_id]["Length"])
        if x and y:  # Assicurati che ci siano dati prima di continuare
            x = np.array(x)
            y = np.array(y)

            # Calcola i coefficienti della regressione lineare
            mean_x = np.mean(x)
            mean_y = np.mean(y)
            num = np.sum((x - mean_x) * (y - mean_y))
            den = np.sum((x - mean_x) ** 2)
            if den != 0:
                lrr_values[tr_id] = num / den
            else:
                lrr_values[tr_id] = 0  # Assegna un valore di default in caso di divisione per zero

    # Calcola il valore minimo della colonna "length" per ogni riga
    max_length_per_row = {}
    max_length_date_per_row = {}
    for tr_id in all_tr_ids:
        max_length_info = min((info[tr_id]["Length"], info[tr_id]["Date"]) for info in all_info.values() if tr_id in info)
        max_length_per_row[tr_id] = max_length_info[0]
        max_length_date_per_row[tr_id] = max_length_info[1]

    # Ordina gli ID
    sorted_tr_ids = sorted(all_tr_ids, key=lambda x: int(x) if x.isdigit() else float('inf'))

    # Scrivi le informazioni in un unico file
    output_file = os.path.join(folder_path, "info_all.csv")
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ["TR_SEGMENT"] + [f"{filename}_Date" for filename in sorted(all_info.keys())] + [f"{filename}_Length" for filename in sorted(all_info.keys())] + ["SCE", "date_SCE", "LRR"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Scrivi le informazioni per ogni ID
        for tr_id in sorted_tr_ids:
            row_data = {"TR_SEGMENT": tr_id}
            for filename, info in all_info.items():
                if tr_id in info:
                    date_obj = datetime.datetime.fromordinal(info[tr_id]["Date"])
                    row_data[f"{filename}_Date"] = date_obj.strftime('%d/%m/%Y')
                    row_data[f"{filename}_Length"] = info[tr_id]["Length"]
                else:
                    row_data[f"{filename}_Date"] = "null"
                    row_data[f"{filename}_Length"] = "null"

            # Aggiungi le colonne SCE, date_SCE e LRR
            if tr_id in lrr_values:
                row_data["LRR"] = lrr_values[tr_id]
            else:
                row_data["LRR"] = "null"

            # Converti il numero rappresentativo della data_SCE in un oggetto data
            date_SCE_obj = datetime.datetime.fromordinal(max_length_date_per_row[tr_id])
            # Salva la data_SCE nel formato DD/MM/YYYY
            row_data["date_SCE"] = date_SCE_obj.strftime('%d/%m/%Y')

            # Aggiungi le colonne SCE
            row_data["SCE"] = max_length_per_row[tr_id]

            writer.writerow(row_data)

    print("Operazione completata. Il file 'info_all.csv' è stato creato nella cartella selezionata.")

# here elif 5

elif AA == 5:
    from PyQt5.QtWidgets import QFileDialog, QInputDialog
    import os
    import pandas as pd
    import random

    # Funzione per selezionare una cartella
    def select_folder():
        folder = QFileDialog.getExistingDirectory(None, "Select csv Folder")
        return folder

    # Funzione per inserire un valore numerico
    def input_dcr():
        dcr, ok = QInputDialog.getDouble(None, "Input Dialog", "Insert space between transect - last area:")
        if ok:
            return dcr
        else:
            return None

    # Funzione per elaborare i file CSV e salvarli come nuovi file
    def process_csv_files(folder, dcr):
        # Lista di tutti i file CSV nella cartella
        csv_files = [f for f in os.listdir(folder) if f.endswith('.csv')]

        for csv_file in csv_files:
            file_path = os.path.join(folder, csv_file)
            
            # Carica il file CSV come DataFrame Pandas
            df = pd.read_csv(file_path)
            
            # Nuovo nome per il file CSV modificato
            new_file_name = os.path.splitext(csv_file)[0] + '_modified.csv'
            new_file_path = os.path.join(folder, new_file_name)

            # Genera un valore casuale per ogni riga e applica a tutte le colonne interessate
            for index, row in df.iterrows():
                dcr_randomized = dcr + random.uniform(-0.5, 0.5)
                
                # Se è il file 'info_all.csv', processa SCE e LRR
                if csv_file == 'info_all.csv':
                    if 'SCE' in df.columns and 'LRR' in df.columns:
                        df.at[index, 'M_SCE'] = row['SCE'] / dcr_randomized
                        df.at[index, 'M_LRR'] = row['LRR'] / dcr_randomized
                # Per gli altri file, processa A_NSM e A_EPR
                else:
                    if 'A_NSM' in df.columns and 'A_EPR' in df.columns:
                        df.at[index, 'M_NSM'] = row['A_NSM'] / dcr_randomized
                        df.at[index, 'M_EPR'] = row['A_EPR'] / dcr_randomized
            
            # Salva il nuovo file CSV senza sovrascrivere l'originale
            df.to_csv(new_file_path, index=False)
            
    # Avvio del processo
    folder = select_folder()  # Seleziona la cartella
    if folder:
        dcr = input_dcr()  # Inserisci il valore numerico
        if dcr:
            process_csv_files(folder, dcr)  # Elabora i file CSV

    

elif AA == 0:
    from qgis.PyQt.QtWidgets import QFileDialog, QLineEdit, QDialog, QVBoxLayout, QPushButton, QApplication
    from qgis.PyQt.QtCore import QDir
    from qgis.core import (
        QgsVectorLayer,
        QgsFields,
        QgsField,
        QgsFeature,
        QgsGeometry,
        QgsVectorFileWriter,
        QgsPointXY,
        QgsWkbTypes,
    )
    from PyQt5.QtCore import QVariant
    from PyQt5.QtCore import QFile
    from scipy.interpolate import CubicSpline
    from qgis.core import QgsProject


    # Apri una finestra di dialogo per selezionare la cartella di input per la baseline
    infolder_baseline = QFileDialog.getExistingDirectory(None, 'CDA - Select the baseline input folder', QDir.homePath())

    # Apri una finestra di dialogo per selezionare la cartella di input per le linee di riva
    infolder_shoreline = QFileDialog.getExistingDirectory(None, 'CDA - Select the shoreline input folder', QDir.homePath())

    # Apri una finestra di dialogo per selezionare la cartella di output per la baseline
    outfolder_baseline = QFileDialog.getExistingDirectory(None, 'CDA - Select the baseline output folder', QDir.homePath())

    outfolder_transects = QFileDialog.getExistingDirectory(None, 'CDA - Select the TEMP materials output folder', QDir.homePath())

    infolder_baseline += QDir.separator()
    infolder_shoreline += QDir.separator()
    outfolder_baseline += QDir.separator()
    outfolder_transects += QDir.separator()

    # Verifica se l'utente ha annullato la selezione di una cartella
    if infolder_baseline == '' or infolder_shoreline == '' or outfolder_baseline == '':
        print('Selection of the cancelled folder. The programme will be terminated.')
        exit()

    # --------------------------------------- PARAMETRI --------------------------------------------------------------
    dialog = QDialog()
    layout = QVBoxLayout()
    dialog.setLayout(layout)

    line_edits = []
    prompt = ['Enter distance between transect:', 'Enter length of transect:']
    for text in prompt:
        line_edit = QLineEdit()
        line_edit.setPlaceholderText(text)
        layout.addWidget(line_edit)
        line_edits.append(line_edit)

    button = QPushButton('INPUT DONE')
    layout.addWidget(button)

    button.clicked.connect(dialog.accept)
    dialog.exec_()

    a = float(line_edits[0].text())
    b = float(line_edits[1].text())

    dist_trans = a  # Definizione di dist_trans
    length_trans = b  # Definizione di length_trans

    # --------------------------------------- PART 1 --------------------------------------------------------------
    # lettura base line
    for file_path in QDir(infolder_baseline).entryList(['*.shp']):
        base_in = QgsVectorLayer(infolder_baseline + file_path, '', 'ogr')

    base_in_features = base_in.getFeatures()
    for feature in base_in_features:
        base_geometry = feature.geometry()

    # ricampionare base line in vertici equidistanti
    dx = 1
    sampling = round(base_geometry.length() / dist_trans) + 1
    n_transects = round((base_geometry.length()) / dist_trans)
    with open(outfolder_transects + 'n_transects.txt', 'w') as f:
        f.write(str(n_transects))

    # Ottenere i vertici della geometria della linea di base
    unique_points = base_geometry.vertices()
    coordinates = [(pt.x(), pt.y()) for pt in unique_points]

    # Rimuovere i punti duplicati lungo l'asse x
    unique_coordinates = []
    seen_x = set()  # Usiamo un set per memorizzare le coordinate X già viste

    for coord in coordinates:
        x, y = coord  # Assegna la coordinata X e Y dalla tupla coord
        if x not in seen_x:
            unique_coordinates.append(coord)
            seen_x.add(x)

    # Ordinare le coordinate in base all'asse X
    sorted_coordinates = sorted(unique_coordinates, key=lambda coord: coord[0])

    # Dividere le coordinate ordinate in tuple separate di X e Y
    unique_X, unique_Y = zip(*sorted_coordinates)


    # Definisci il numero di punti su cui eseguire la spline
    num_points = sampling  # Modifica questo valore a tuo piacimento

    # Calcola il passo tra i punti x
    step = (max(unique_X) - min(unique_X)) / (num_points - 1)

    # Genera un array di punti x equidistanti nell'intervallo da x_min a x_max
    x_values = [min(unique_X) + i * step for i in range(num_points)]

    spline = CubicSpline(unique_X, unique_Y)

    # Calcola i corrispondenti valori di y utilizzando la spline
    y_values = spline(x_values)

    # Crea i punti interpolati lungo la base utilizzando le coordinate x e y
    interpolated_points = [QgsPointXY(x, y) for x, y in zip(x_values, y_values)]


    # --------------------------------------- NEW base line struct -------------------------------------
    baseline = QgsVectorLayer('LineString', 'baseline', 'memory')
    baseline_fields = QgsFields()
    baseline_fields.append(QgsField('ID', QVariant.Int))
    baseline_fields.append(QgsField('X', QVariant.Double))
    baseline_fields.append(QgsField('Y', QVariant.Double))
    baseline_provider = baseline.dataProvider()
    baseline_provider.addAttributes(baseline_fields)
    baseline.updateFields()

    # Creazione delle feature
    features = []
    for i, pt in enumerate(interpolated_points):
        # Crea una nuova feature
        feature = QgsFeature(baseline_fields)
        # Imposta gli attributi per questa feature
        feature.setAttribute('ID', i)
        feature.setAttribute('X', pt.x())
        feature.setAttribute('Y', pt.y())
        # Imposta la geometria per questa feature
        feature.setGeometry(QgsGeometry.fromPolylineXY(interpolated_points))
        # Aggiungi la feature alla lista delle feature
        features.append(feature)

        #print(f"Feature {i}: ID={i}, X={pt.x()}, Y={pt.y()}")  # Aggiunto per il debug

    # Lunghezza del provider dei dati prima dell'aggiunta delle feature
    length_before_adding_features = baseline_provider.featureCount()

    # Aggiunta delle feature al data provider del layer baseline
    baseline_provider.addFeatures(features)
    # Aggiornamento dei limiti del layer
    baseline.updateExtents() 

    # Lunghezza del provider dei dati dopo l'aggiunta delle feature
    length_after_adding_features = baseline_provider.featureCount()

    ######################################
    ###############
    ###########
    # Calcola la lunghezza della linea
    baseline_length = base_geometry.length()

    # Calcola Irregularity come rapporto tra lunghezza della linea e il numero di transetti
    irregularity = baseline_length / n_transects/100

    # Calcola la media delle differenze tra tutte le posizioni Y dei punti interpolati
    y_differences = [abs(y_values[i+1] - y_values[i]) for i in range(len(y_values) - 1)]
    mean_y_difference = sum(y_differences) / len(y_differences)

    # Calcola Roughness come prodotto tra Irregularity e la media delle differenze Y
    roughness = irregularity * mean_y_difference/2

    # Scrivi i risultati nel file di output
    with open(outfolder_transects + 'n_transects.txt', 'w') as f:
        f.write(f"Number of transects: {n_transects}\n")
        f.write(f"Irregularity: {irregularity}\n")
        f.write(f"Roughness: {roughness}\n")

        # Aggiungi un campo "JOIN" al layer baseline
        baseline_provider.addAttributes([QgsField("JOIN", QVariant.Int)])
        baseline.updateFields()
        baseline.updateExtents()
######################################
    ###############
    ###########
    
    # Imposta tutti i valori del campo "JOIN" su 1 per ogni feature
    for feature in baseline.getFeatures():
        baseline.dataProvider().changeAttributeValues({feature.id(): {baseline.fields().indexFromName("JOIN"): 1}})

    # Esegui il dissolvi basato sul campo "JOIN"
    dissolved_baseline = processing.run("native:dissolve", {
        'INPUT': baseline,
        'FIELD': ['JOIN'],  # Campo su cui eseguire il dissolvi
        'OUTPUT': 'memory:'
    })['OUTPUT']

    
    # Rimuovi eventuali caratteri di escape dalla fine del percorso della directory
    outfolder_baseline = outfolder_baseline.rstrip("\\")
    
    # Salva la geometria del layer dissolto
    dissolved_output_shapefile = outfolder_baseline + '/dissolved_baseline.shp'
    QgsVectorFileWriter.writeAsVectorFormat(dissolved_baseline, dissolved_output_shapefile, 'UTF-8', baseline.crs(), 'ESRI Shapefile')
    

    # Specifica il percorso completo del file shapefile
    output_shapefile = outfolder_baseline + '/baseline.shp'

    # Scrivi il layer baseline su disco come shapefile
    QgsVectorFileWriter.writeAsVectorFormat(baseline, output_shapefile, 'UTF-8', baseline.crs(), 'ESRI Shapefile')

    # Copia il file di proiezione
    QFile.copy(infolder_baseline + 'baseline.prj', outfolder_baseline + 'baseline.prj')
    # Copia il file di proiezione
    QFile.copy(infolder_baseline + 'baseline.prj', outfolder_baseline + 'dissolved_baseline.prj')

    # Caricare il risultato baseline nella TOC
    project_instance = QgsProject.instance()
    baseline_layer = QgsVectorLayer(output_shapefile, 'Baseline', 'ogr')

else:
    pass
    
###from PyQt5.QtWidgets import QMessageBox

# Dopo che il tuo script è stato eseguito con successo
###QMessageBox.information(None, " CDA ", "Processing done! \nClose this window and the next one \nAll the processes ended correctly!")