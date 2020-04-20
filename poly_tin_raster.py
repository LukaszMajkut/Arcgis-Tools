'''
Tool which allows you to generate one valuable raster based on a given polygon's height value.
'''
import arcpy
from arcpy import *
from arcpy.sa import *
arcpy.env.overwriteOutput = True

try:
    in_shape = arcpy.GetParameterAsText(0)
    height_value = arcpy.GetParameterAsText (1)
    raster_name = arcpy.GetParameterAsText (2)
    tin_workspace = arcpy.GetParameterAsText (3)

    # extract workspace
    wksSplit = in_shape.split(".")
    wksExt = wksSplit[1].split("\\")[0]
    workspace="{}.{}".format(wksSplit[0],wksExt)
    temp1 = tin_workspace + "\\ttt1"
    raster_path = workspace + "\\" + raster_name
    sr = arcpy.CreateSpatialReference_management("", in_shape)
    para_in = in_shape + " " + height_value +" Hard_Clip <None>"
    
    
    arcpy.CreateTin_3d(temp1,sr, para_in)
    
    
    arcpy.TinRaster_3d(temp1, raster_path, data_type = "FLOAT", method = "LINEAR", sample_distance = "CELLSIZE 1")
    
    
    arcpy.Delete_management(temp1)
except:
    arcpy.AddError('Proces nie został zrealizowany ')
    arcpy.AddMessage(arcpy.GetMessages())
