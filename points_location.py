#script that allows you to update points location based on x and y field in attribute table

from arcpy import env

#define workspace location:
env.workspace = r'N:\Work\Majkut\python_test\testowa.gdb'

with arcpy.da.UpdateCursor("gminy_spotkania1",["SHAPE@XY","X","Y"]) as cur:
     for row in cur:
         x,y = row[0]
         xn = row[1]
         yn = row[2]
         row[0] = (xn,yn)
         cur.updateRow(row)
del cur

print('update completed')
