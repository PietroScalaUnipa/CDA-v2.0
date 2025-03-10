# 📌 CDA-v2.0 - Coastal Dynamics Analyzer  

The **Coastal Dynamics Analyzer (CDA)** is a powerful QGIS plugin designed to automate **Shoreline Change Analysis (SCA)** with enhanced accuracy and speed.  

The latest version, **CDA-v2.0**, introduces **Area-Based Analysis (ABA)**, offering a more comprehensive approach to shoreline evolution studies.  

![image](https://github.com/user-attachments/assets/eea51907-1827-4244-bc73-cf7aeadac78f)


## 🚀 Features  

 ✅ Automatic **Shoreline Change Analysis (SCA)**  
 ✅ New **Area-Based Analysis (ABA)** for enhanced accuracy  
 ✅ Seamless integration with **QGIS**  
 ✅ User-friendly interface for efficient analysis  
 ✅ Support for multiple shoreline datasets  

## 📥 Installation  

To install **CDA-v2.0** in **QGIS**, follow these steps:  
1.	Download the CDA plugin v. 2.0 ZIP file.
2.	Open QGIS.
3.	Go to the Plugins menu and select Manage and Install Plugins.
4.	Click on the Install from ZIP tab.
5.	Browse and select the downloaded ZIP file.
6.	Click Install Plugin.
2. Running the Plugin

To run the CDA plugin v. 2.0, you will need to follow these steps:
1.	Open the Processing Toolbox:
  o	Go to the Processing menu.
  o	Select Toolbox to open the Processing Toolbox panel.
2.	Locate the Plugin Script:
  o	In the Processing Toolbox, find and expand the Scripts section and click on it.
  o	Click on 'Open existing Script'.
  o	Look for CDA_MAIN_.py python script or other saved script name.
3.	Run the Script:
  o	Double-click on the Coastal Dynamics Analyzer script to open it.
  o	A script editor window will appear with the plugin's Python code.
4.	Execute the Script:
  o	Click on the green Run button (▶️) in the script editor toolbar.
  o	This will execute the script and display the main GUI of the CDA plugin v. 2.0.

# IMPORTANT NOTE: 
Even when a process is successful, a message may appear on the screen stating, “Seems there is no valid script.” In this case click “OK.” Step processing was still successful.

# ABA Metrics
![image](https://github.com/user-attachments/assets/af9761bf-e968-4e65-9d9a-affa9a2283ac)

To obtain linear rates using the ABA approach, the average shoreline displacement is calculated by dividing the area bounded by the transects, shoreline and baseline, by the length of the shoreline between two different transects. This simple geometric ratio is then used to calculate by the plug-in further average rates of shoreline change, including M-NSM [m], M-SCE [m], M-EPR [m/time] and M-LRR [m/time].

# Click here to download the User Manual of CDA v.2.0 [CDA_User_Manual_v2_0_0.pdf](https://github.com/user-attachments/files/19162605/CDA_User_Manual_v2_0_0.pdf)

# Example Results:
![image](https://github.com/user-attachments/assets/39fbe657-c1c6-4ba9-92e8-0e7b39d6deb5)


# Reference to 
https://doi.org/10.1016/j.softx.2024.101894

# Cite as 
Scala et al., 2024 (CDA v1.0); Scala et al., 2025 (Update to CDA v1.0) SoftwareX Elsevier paper



