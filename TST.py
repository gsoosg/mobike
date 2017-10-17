# -*- coding: utf-8 -*-
# ---------------------------------------------------------------------------
# TST.py
# Created on: 2017-10-13 15:42:24.00000
#   (generated by ArcGIS/ModelBuilder)
# Description: 
# ---------------------------------------------------------------------------

# Import arcpy module
import arcpy

# Set Geoprocessing environments
arcpy.env.outputCoordinateSystem = "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"


# Local variables:
东湖绿道_shp = "E:\\武汉绿道\\东湖绿道.shp"
LVDAO_gdb = "E:\\武汉绿道\\LVDAO.gdb"
输出坐标系 = "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"
输出坐标系__2_ = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
tmpBuffer = "E:\\武汉绿道\\LVDAO.gdb\\tmpBuffer"
tmpSample = "E:\\武汉绿道\\LVDAO.gdb\\tmpSample"
LvDaoSample = "E:\\武汉绿道\\LVDAO.gdb\\LvDaoSample"
LvDaoSample__2_ = "E:\\武汉绿道\\LVDAO.gdb\\LvDaoSample"
绿道_json = "E:\\武汉绿道\\绿道.json"

# Process: 缓冲区
tempEnvironment0 = arcpy.env.outputCoordinateSystem
arcpy.env.outputCoordinateSystem = "PROJCS['WGS_1984_Web_Mercator_Auxiliary_Sphere',GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]],PROJECTION['Mercator_Auxiliary_Sphere'],PARAMETER['False_Easting',0.0],PARAMETER['False_Northing',0.0],PARAMETER['Central_Meridian',0.0],PARAMETER['Standard_Parallel_1',0.0],PARAMETER['Auxiliary_Sphere_Type',0.0],UNIT['Meter',1.0]]"
tempEnvironment1 = arcpy.env.workspace
arcpy.env.workspace = "E:\\武汉绿道\\LVDAO.gdb"
arcpy.Buffer_analysis(东湖绿道_shp, tmpBuffer, "500 Meters", "FULL", "ROUND", "ALL", "", "PLANAR")
arcpy.env.outputCoordinateSystem = tempEnvironment0
arcpy.env.workspace = tempEnvironment1

# Process: 创建渔网
arcpy.CreateFishnet_management(tmpSample, "12728632.5908 3572194.094", "12728632.5908 3572204.094", "200", "200", "", "", "12739592.8285 3579273.5335", "LABELS", tmpBuffer, "POLYLINE")

# Process: 相交
tempEnvironment0 = arcpy.env.outputCoordinateSystem
arcpy.env.outputCoordinateSystem = "GEOGCS['GCS_WGS_1984',DATUM['D_WGS_1984',SPHEROID['WGS_1984',6378137.0,298.257223563]],PRIMEM['Greenwich',0.0],UNIT['Degree',0.0174532925199433]]"
arcpy.Intersect_analysis("E:\\武汉绿道\\LVDAO.gdb\\tmpSample_label #;E:\\武汉绿道\\LVDAO.gdb\\tmpBuffer #", LvDaoSample, "ALL", "", "POINT")
arcpy.env.outputCoordinateSystem = tempEnvironment0

# Process: 添加 XY 坐标
arcpy.AddXY_management(LvDaoSample)

# Process: 要素转 JSON
arcpy.FeaturesToJSON_conversion(LvDaoSample__2_, 绿道_json, "FORMATTED", "NO_Z_VALUES", "NO_M_VALUES")
