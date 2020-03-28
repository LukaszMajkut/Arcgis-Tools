"""
This tool allows you to create concentric, non-covering buffers surrounding objects with an area larger than 5km2 (in the indicated layer)
"""
import arcpy
from arcpy import *
from arcpy.sa import *
arcpy.env.overwriteOutput = True

try:
    warstwa_bazowa = arcpy.GetParameterAsText(0)
    rozmiar_buf = arcpy.GetParameter(1)

    # extract workspace
    wksSplit = warstwa_bazowa.split(".")
    wksExt = wksSplit[1].split("\\")[0]
    workspace="{}.{}".format(wksSplit[0],wksExt)

    output_name = workspace + "\\_5KM" 

    arcpy.Select_analysis(warstwa_bazowa,output_name,"Shape_Area>5000000")
    warstwa_in = output_name
    war = warstwa_in
    lista1 = []
    lista2 = []
    warstwa_out = ""
    warstwa_out_E = ""
    for i in range(3):
        warstwa_out = warstwa_in + "_" + str(i)
        arcpy.Buffer_analysis(war,warstwa_out,rozmiar_buf,"","","ALL")
        lista1.append(warstwa_out)
        war = warstwa_out
    for j in range(len(lista1)):
        warstwa_out_E = warstwa_in + "_Erase_" + str(j)
        if j == 0: 
            arcpy.Erase_analysis(lista1[j],warstwa_in,warstwa_out_E)
        else:
            arcpy.Erase_analysis(lista1[j],lista1[j-1],warstwa_out_E)
        arcpy.AddField_management(warstwa_out_E, "BUFOR", "SHORT")
        expr = str(j*rozmiar_buf)
        arcpy.CalculateField_management(warstwa_out_E, "BUFOR", expr, "PYTHON3")
        lista2.append(warstwa_out_E)

    arcpy.Merge_management(lista2,'wynik_koncowy_v2') 
    
    # deleting temp files
    for i in lista1:
        arcpy.Delete_management(i)
    for j in lista2:
        arcpy.Delete_management(j)

except:
    arcpy.AddError('Proces nie został zrealizowany ')
    arcpy.AddMessage(arcpy.GetMessages())
