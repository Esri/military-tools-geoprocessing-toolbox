# -*- coding: utf-8 -*-
r"""A Geoprocessing Toolbox for ArcGIS for Desktop that contains
collections of tools to import geometry from tables, determine ranges,
and provide basic visibility analysis capabilities."""
__all__ = ['AddLinearLineOfSightFields', 'AddRadialLineOfSightObserverFields',
           'ConvertCoordinates', 'CreateGRGFromArea', 'CreateGRGFromPoint',
           'CreateReferenceSystemGRGFromArea', 'FindLocalPeaks',
           'HighestPoints', 'LinearLineOfSight', 'LowestPoints',
           'RadialLineOfSight', 'RadialLineOfSightAndRange',
           'RangeRingFromMinimumAndMaximum', 'RangeRingsFromInterval',
           'RangeRingsFromMinAndMaxTable', 'TableTo2PointLine',
           'TableToEllipse', 'TableToLineOfBearing', 'TableToPoint',
           'TableToPolygon', 'TableToPolyline']
__alias__ = 'mt'
from arcpy.geoprocessing._base import gptooldoc, gp, gp_fixargs
from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject

# Conversion toolset
@gptooldoc('ConvertCoordinates_mt', None)
def ConvertCoordinates(Input_Table=None, Input_Coordinate_Format=None, X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_=None, Y_Field__latitude_=None, Output_Table=None, Spatial_Reference=None):
    """ConvertCoordinates_mt(Input_Table, Input_Coordinate_Format, X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_, {Y_Field__latitude_}, Output_Table, {Spatial_Reference})

        Converts source coordinates in a table to multiple coordinate
        formats. This tool uses an input table with coordinates and outputs a
        new table with fields for the following coordinate formats: Decimal
        Degrees, Decimal Degrees Minutes, Degrees Minutes Seconds, Universal
        Transverse Mercator, Military Grid Reference System, U.S. National
        Grid, Global Area Reference System, and World Geographic Reference
        System.

     INPUTS:
      Input_Table (Table View):
          There is no python reference for this parameter.
      Input_Coordinate_Format (String):
          There is no python reference for this parameter.
      X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_ (Field):
          There is no python reference for this parameter.
      Y_Field__latitude_ {Field}:
          There is no python reference for this parameter.
      Spatial_Reference {Spatial Reference}:
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Table (Table):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.ConvertCoordinates_mt(*gp_fixargs((Input_Table, Input_Coordinate_Format, X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_, Y_Field__latitude_, Output_Table, Spatial_Reference), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('TableTo2PointLine_mt', None)
def TableTo2PointLine(Input_Table=None, Start_Point_Format=None, Start_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_=None, Start_Y_Field__latitude_=None, End_Point_Format=None, End_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_=None, End_Y_Field__latitude_=None, Output_Lines=None, Line_Type=None, Spatial_Reference=None):
    """TableTo2PointLine_mt(Input_Table, Start_Point_Format, Start_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_, {Start_Y_Field__latitude_}, End_Point_Format, End_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_, {End_Y_Field__latitude_}, Output_Lines, {Line_Type}, {Spatial_Reference})

        Creates a line feature from start and end point coordinates. This
        tool uses an input table with coordinate pairs and outputs line
        features.

     INPUTS:
      Input_Table (Table View):
          There is no python reference for this parameter.
      Start_Point_Format (String):
          There is no python reference for this parameter.
      Start_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_ (Field):
          There is no python reference for this parameter.
      Start_Y_Field__latitude_ {Field}:
          There is no python reference for this parameter.
      End_Point_Format (String):
          There is no python reference for this parameter.
      End_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_ (Field):
          There is no python reference for this parameter.
      End_Y_Field__latitude_ {Field}:
          There is no python reference for this parameter.
      Line_Type {String}:
          There is no python reference for this parameter.
      Spatial_Reference {Spatial Reference}:
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Lines (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.TableTo2PointLine_mt(*gp_fixargs((Input_Table, Start_Point_Format, Start_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_, Start_Y_Field__latitude_, End_Point_Format, End_X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_, End_Y_Field__latitude_, Output_Lines, Line_Type, Spatial_Reference), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('TableToEllipse_mt', None)
def TableToEllipse(Input_Table=None, Input_Coordinate_Format=None, X_Field__longitude__UTM__MGRS__USNG__GARS__GeoRef_=None, Y_Field__latitude_=None, Major_Field=None, Minor_Field=None, Distance_Units=None, Output_Ellipse=None, Azimuth_Field=None, Azimuth_Units=None, Spatial_Reference=None):
    """TableToEllipse_mt(Input_Table, Input_Coordinate_Format, X_Field__longitude__UTM__MGRS__USNG__GARS__GeoRef_, {Y_Field__latitude_}, Major_Field, Minor_Field, Distance_Units, Output_Ellipse, {Azimuth_Field}, {Azimuth_Units}, {Spatial_Reference})

        Creates ellipse features from tabular coordinates and input data
        values. This tool uses an input table with coordinate values for
        ellipse centers and values for major and minor axis lengths.

     INPUTS:
      Input_Table (Table View):
          There is no python reference for this parameter.
      Input_Coordinate_Format (String):
          There is no python reference for this parameter.
      X_Field__longitude__UTM__MGRS__USNG__GARS__GeoRef_ (Field):
          There is no python reference for this parameter.
      Y_Field__latitude_ {Field}:
          There is no python reference for this parameter.
      Major_Field (Field):
          There is no python reference for this parameter.
      Minor_Field (Field):
          There is no python reference for this parameter.
      Distance_Units (String):
          There is no python reference for this parameter.
      Azimuth_Field {Field}:
          There is no python reference for this parameter.
      Azimuth_Units {String}:
          There is no python reference for this parameter.
      Spatial_Reference {Spatial Reference}:
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Ellipse (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.TableToEllipse_mt(*gp_fixargs((Input_Table, Input_Coordinate_Format, X_Field__longitude__UTM__MGRS__USNG__GARS__GeoRef_, Y_Field__latitude_, Major_Field, Minor_Field, Distance_Units, Output_Ellipse, Azimuth_Field, Azimuth_Units, Spatial_Reference), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('TableToLineOfBearing_mt', None)
def TableToLineOfBearing(Input_Table=None, Input_Coordinate_Format=None, X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_=None, Y_Field__latitude_=None, Bearing_Units=None, Bearing_Field=None, Distance_Units=None, Distance_Field=None, Output_Lines=None, Line_Type=None, Spatial_Reference=None):
    """TableToLineOfBearing_mt(Input_Table, Input_Coordinate_Format, X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_, {Y_Field__latitude_}, Bearing_Units, Bearing_Field, Distance_Units, Distance_Field, Output_Lines, {Line_Type}, {Spatial_Reference})

        Creates lines of bearing from tabular coordinates.

     INPUTS:
      Input_Table (Table View):
          There is no python reference for this parameter.
      Input_Coordinate_Format (String):
          There is no python reference for this parameter.
      X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_ (Field):
          There is no python reference for this parameter.
      Y_Field__latitude_ {Field}:
          There is no python reference for this parameter.
      Bearing_Units (String):
          There is no python reference for this parameter.
      Bearing_Field (Field):
          There is no python reference for this parameter.
      Distance_Units (String):
          There is no python reference for this parameter.
      Distance_Field (Field):
          There is no python reference for this parameter.
      Line_Type {String}:
          There is no python reference for this parameter.
      Spatial_Reference {Spatial Reference}:
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Lines (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.TableToLineOfBearing_mt(*gp_fixargs((Input_Table, Input_Coordinate_Format, X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_, Y_Field__latitude_, Bearing_Units, Bearing_Field, Distance_Units, Distance_Field, Output_Lines, Line_Type, Spatial_Reference), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('TableToPoint_mt', None)
def TableToPoint(Input_Table=None, Input_Coordinate_Format=None, X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_=None, Y_Field__latitude_=None, Output_Points=None, Spatial_Reference=None):
    """TableToPoint_mt(Input_Table, Input_Coordinate_Format, X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_, {Y_Field__latitude_}, Output_Points, {Spatial_Reference})

        Creates point features from tabular coordinates.

     INPUTS:
      Input_Table (Table View):
          There is no python reference for this parameter.
      Input_Coordinate_Format (String):
          There is no python reference for this parameter.
      X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_ (Field):
          There is no python reference for this parameter.
      Y_Field__latitude_ {Field}:
          There is no python reference for this parameter.
      Spatial_Reference {Spatial Reference}:
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Points (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.TableToPoint_mt(*gp_fixargs((Input_Table, Input_Coordinate_Format, X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_, Y_Field__latitude_, Output_Points, Spatial_Reference), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('TableToPolygon_mt', None)
def TableToPolygon(Input_Table=None, Input_Coordinate_Format=None, X_Field_Longitude_UTM_MGRS_USNG_GARS_GeoRef_=None, Y_Field__latitude_=None, Output_Polygon_Features=None, Line_Field=None, Sort_Field=None, Spatial_Reference=None):
    """TableToPolygon_mt(Input_Table, Input_Coordinate_Format, X_Field_Longitude_UTM_MGRS_USNG_GARS_GeoRef_, {Y_Field__latitude_}, Output_Polygon_Features, {Line_Field}, {Sort_Field}, {Spatial_Reference})

        Creates polygon features from tabular coordinates.

     INPUTS:
      Input_Table (Table View):
          There is no python reference for this parameter.
      Input_Coordinate_Format (String):
          There is no python reference for this parameter.
      X_Field_Longitude_UTM_MGRS_USNG_GARS_GeoRef_ (Field):
          There is no python reference for this parameter.
      Y_Field__latitude_ {Field}:
          There is no python reference for this parameter.
      Line_Field {Field}:
          There is no python reference for this parameter.
      Sort_Field {Field}:
          There is no python reference for this parameter.
      Spatial_Reference {Spatial Reference}:
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Polygon_Features (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.TableToPolygon_mt(*gp_fixargs((Input_Table, Input_Coordinate_Format, X_Field_Longitude_UTM_MGRS_USNG_GARS_GeoRef_, Y_Field__latitude_, Output_Polygon_Features, Line_Field, Sort_Field, Spatial_Reference), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('TableToPolyline_mt', None)
def TableToPolyline(Input_Table=None, Input_Coordinate_Format=None, X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_=None, Y_Field__latitude_=None, Output_Polyline_Features=None, Line_Field=None, Sort_Field=None, Spatial_Reference=None):
    """TableToPolyline_mt(Input_Table, Input_Coordinate_Format, X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_, {Y_Field__latitude_}, Output_Polyline_Features, {Line_Field}, {Sort_Field}, {Spatial_Reference})

        Creates polyline features from tabular coordinates.

     INPUTS:
      Input_Table (Table View):
          There is no python reference for this parameter.
      Input_Coordinate_Format (String):
          There is no python reference for this parameter.
      X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_ (Field):
          There is no python reference for this parameter.
      Y_Field__latitude_ {Field}:
          There is no python reference for this parameter.
      Line_Field {Field}:
          There is no python reference for this parameter.
      Sort_Field {Field}:
          There is no python reference for this parameter.
      Spatial_Reference {Spatial Reference}:
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Polyline_Features (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.TableToPolyline_mt(*gp_fixargs((Input_Table, Input_Coordinate_Format, X_Field__longitude__UTM__MGRS__USNG__GARS__GEOREF_, Y_Field__latitude_, Output_Polyline_Features, Line_Field, Sort_Field, Spatial_Reference), True)))
        return retval
    except Exception as e:
        raise e


# Distance and Direction toolset
@gptooldoc('RangeRingFromMinimumAndMaximum_mt', None)
def RangeRingFromMinimumAndMaximum(Input_Center_Features=None, Minimum_Range=None, Maximum_Range=None, Distance_Units=None, Number_of_Radials=None, Output_Ring_Features=None, Output_Radial_Features=None, Spatial_Reference=None):
    """RangeRingFromMinimumAndMaximum_mt(Input_Center_Features, Minimum_Range, Maximum_Range, Distance_Units, Number_of_Radials, Output_Ring_Features, Output_Radial_Features, {Spatial_Reference})

        Create a concentric circle from a center with two rings depicting a
        minimum range and a maximum range.

     INPUTS:
      Input_Center_Features (Feature Set):
          There is no python reference for this parameter.
      Minimum_Range (Double):
          There is no python reference for this parameter.
      Maximum_Range (Double):
          There is no python reference for this parameter.
      Distance_Units (String):
          There is no python reference for this parameter.
      Number_of_Radials (Long):
          There is no python reference for this parameter.
      Spatial_Reference {Spatial Reference}:
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Ring_Features (Feature Class):
          There is no python reference for this parameter.
      Output_Radial_Features (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.RangeRingFromMinimumAndMaximum_mt(*gp_fixargs((Input_Center_Features, Minimum_Range, Maximum_Range, Distance_Units, Number_of_Radials, Output_Ring_Features, Output_Radial_Features, Spatial_Reference), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('RangeRingsFromInterval_mt', None)
def RangeRingsFromInterval(Input_Center_Features=None, Number_of_Rings=None, Interval_Between_Rings=None, Distance_Units=None, Number_of_Radials=None, Output_Ring_Features=None, Output_Radial_Features=None, Spatial_Reference=None):
    """RangeRingsFromInterval_mt(Input_Center_Features, Number_of_Rings, Interval_Between_Rings, Distance_Units, Number_of_Radials, Output_Ring_Features, Output_Radial_Features, {Spatial_Reference})

        Create a concentric circle from a center, with a number of rings,
        and the distance between rings.

     INPUTS:
      Input_Center_Features (Feature Set):
          There is no python reference for this parameter.
      Number_of_Rings (Long):
          There is no python reference for this parameter.
      Interval_Between_Rings (Double):
          There is no python reference for this parameter.
      Distance_Units (String):
          There is no python reference for this parameter.
      Number_of_Radials (Long):
          There is no python reference for this parameter.
      Spatial_Reference {Spatial Reference}:
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Ring_Features (Feature Class):
          There is no python reference for this parameter.
      Output_Radial_Features (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.RangeRingsFromInterval_mt(*gp_fixargs((Input_Center_Features, Number_of_Rings, Interval_Between_Rings, Distance_Units, Number_of_Radials, Output_Ring_Features, Output_Radial_Features, Spatial_Reference), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('RangeRingsFromMinAndMaxTable_mt', None)
def RangeRingsFromMinAndMaxTable(Input_Center_Features=None, Input_Table=None, Selected_Type=None, Number_Of_Radials=None, Output_Ring_Features=None, Output_Radial_Features=None, Spatial_Reference=None, Input_Table_Type_Name_Field=None, Input_Table_Minimum_Range_Field=None, Input_Table_Maximum_Range_Field=None):
    """RangeRingsFromMinAndMaxTable_mt(Input_Center_Features, Input_Table, Selected_Type, Number_Of_Radials, Output_Ring_Features, Output_Radial_Features, {Spatial_Reference}, {Input_Table_Type_Name_Field}, {Input_Table_Minimum_Range_Field}, {Input_Table_Maximum_Range_Field})

        Create a concentric circle from a center with two rings depicting a
        minimum range and a maximum range from a table.

     INPUTS:
      Input_Center_Features (Feature Set):
          There is no python reference for this parameter.
      Input_Table (Table):
          There is no python reference for this parameter.
      Selected_Type (String):
          There is no python reference for this parameter.
      Number_Of_Radials (Long):
          There is no python reference for this parameter.
      Spatial_Reference {Spatial Reference}:
          There is no python reference for this parameter.
      Input_Table_Type_Name_Field {Field}:
          There is no python reference for this parameter.
      Input_Table_Minimum_Range_Field {Field}:
          There is no python reference for this parameter.
      Input_Table_Maximum_Range_Field {Field}:
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Ring_Features (Feature Class):
          There is no python reference for this parameter.
      Output_Radial_Features (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.RangeRingsFromMinAndMaxTable_mt(*gp_fixargs((Input_Center_Features, Input_Table, Selected_Type, Number_Of_Radials, Output_Ring_Features, Output_Radial_Features, Spatial_Reference, Input_Table_Type_Name_Field, Input_Table_Minimum_Range_Field, Input_Table_Maximum_Range_Field), True)))
        return retval
    except Exception as e:
        raise e


# Gridded Reference Graphic toolset
@gptooldoc('CreateGRGFromArea_mt', None)
def CreateGRGFromArea(input_grg_area=None, cell_width=None, cell_height=None, cell_units=None, label_start_position=None, label_type=None, label_seperator=None, output_grg_features=None):
    """CreateGRGFromArea_mt(input_grg_area, cell_width, cell_height, cell_units, label_start_position, label_type, label_seperator, output_grg_features)

        Creates a Gridded Reference Graphic (GRG) over a specified area
        with a custom size. By default, the cells are labeled with a
        sequential alpha numeric scheme, starting in the lower left. The cells
        can also be labeled by a sequential alpha-alpha scheme or just numbers
        and the starting point can be specified as either the top left, bottom
        left, top right, or bottom right.

     INPUTS:
      input_grg_area (Feature Set):
          Select an existing layer in the map, or use the tool to sketch an
          area on the map. The rotation of this input area determines the
          rotation of the output features.
      cell_width (Double):
          The width of each grid cell in the output features.
      cell_height (Double):
          The height of each grid cell in the output features.
      cell_units (String):
          The units of the Cell Width and Cell Height.   Meters    Feet
          Kilometers   Miles   Nautical Miles   Yards
      label_start_position (String):
          The grid cell where the labeling will start from. The default is
          Upper-Left   Upper-Left   Lower-Left   Upper-Right   Lower-Right
      label_type (String):
          The labeling type for each grid cell. The default is Alpha-Numeric.
          Alpha-Numeric: letter/number combination as A1, A2, A3, A4....X1, X2,
          X3...   Alpha-Alpha: letter/letter combination: AA, AB, AC, AD, ...
          XA, XB, XC...   Numeric: sequentially numbered 1, 2, 3, 4, .... 99,
          100, 101...
      label_seperator (String):
          Seperator to be used between x and y values when using Alpha-Alpha
          labeling. Example: A-A, A-AA, AA-A.   -   ,   .   /

     OUTPUTS:
      output_grg_features (Feature Class):
          Specify the output grg features to be created."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.CreateGRGFromArea_mt(*gp_fixargs((input_grg_area, cell_width, cell_height, cell_units, label_start_position, label_type, label_seperator, output_grg_features), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('CreateGRGFromPoint_mt', None)
def CreateGRGFromPoint(input_start_location=None, horizontal_cells=None, vertical_cells=None, cell_width=None, cell_height=None, cell_units=None, label_start_position=None, label_type=None, label_seperator=None, grid_angle=None, output_grg_features=None):
    """CreateGRGFromPoint_mt(input_start_location, horizontal_cells, vertical_cells, cell_width, cell_height, cell_units, label_start_position, label_type, label_seperator, grid_angle, output_grg_features)

        Creates a Gridded Reference Graphic (GRG) over a specified area
        with a custom size. The grid is centered on the input start location.
        The cells are labeled with sequential letters or numbers.

     INPUTS:
      input_start_location (Feature Set):
          Select a layer for the center point for the gridded reference
          graphic, or use the input_start_location to sketch a starting point on
          the map.
      horizontal_cells (Double):
          The horizontal number of grid cells.
      vertical_cells (Double):
          The vertical number of grid cells.
      cell_width (Double):
          The width of each grid cell.
      cell_height (Double):
          The height of each grid cell.
      cell_units (String):
          The units of the Cell Width and Cell Height.   Meters    Feet
          Kilometers   Miles   Nautical Miles   Yards
      label_start_position (String):
          The grid cell where the labeling will start from. The default is
          Upper-Left   Upper-Left   Lower-Left   Upper-Right   Lower-Right
      label_type (String):
          The labeling type for each grid cell. The default is Alpha-Numeric.
          Alpha-Numeric: letter/number combination as A1, A2, A3, A4....X1, X2,
          X3...   Alpha-Alpha: letter/letter combination: AA, AB, AC, AD, ...
          XA, XB, XC...   Numeric: sequentially numbered 1, 2, 3, 4, .... 99,
          100, 101...
      label_seperator (String):
          Seperator to be used between x and y values when using Alpha-Alpha
          labeling. Example: A-A, A-AA, AA-A.   -   ,   .   /
      grid_angle (Long):
          The angle to rotate the grid by. Valid values between -89 and 89.

     OUTPUTS:
      output_grg_features (Feature Class):
          Specify the output grg features to be created."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.CreateGRGFromPoint_mt(*gp_fixargs((input_start_location, horizontal_cells, vertical_cells, cell_width, cell_height, cell_units, label_start_position, label_type, label_seperator, grid_angle, output_grg_features), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('CreateReferenceSystemGRGFromArea_mt', None)
def CreateReferenceSystemGRGFromArea(input_area_features=None, input_grid_reference_system=None, grid_square_size=None, output_grid_features=None, large_grid_handling=None):
    """CreateReferenceSystemGRGFromArea_mt(input_area_features, input_grid_reference_system, grid_square_size, output_grid_features, {large_grid_handling})

        Creates grid features for Military Grid Reference System (MGRS) or
        United States National Grid (USNG) reference grids.

     INPUTS:
      input_area_features (Feature Set):
          Select an area feature class or draw an area on the map to create a
          reference grid.
      input_grid_reference_system (String):
          Select the grid type to create:   MGRS: Military Grid Reference
          System (default)   USNG: United States National Grid
      grid_square_size (String):
          Select the size of the grid to create:   GRID_ZONE_DESIGNATOR -
          grids will be of the Grid Zone Designator (GZD) and Latitude Band
          combination, ex. 4Q   100000M_GRID - grids will be 100,000 m grid
          square, ex. 4QFJ   10000M_GRID - grids will be 10,000m grid square,
          ex. 4QFJ16   1000M_GRID - grids will be 1,000m grid square, ex.
          4QFJ1267   100M_GRID - grids will be 100m grid square, ex. 4QFJ123678
          10M_GRID - grids will be 10m grid square, ex.         4QFJ12346789
      large_grid_handling {String}:
          Select how to handle large areas that may contain many features.
          NO_LARGE_GRIDS - Tool will stop processing if more than 2000 features
          will be created.   ALLOW_LARGE_GRIDS - Features will be created
          regardless of the number of features.

     OUTPUTS:
      output_grid_features (Feature Class):
          Type (or browse to) the path and name of the features to create."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.CreateReferenceSystemGRGFromArea_mt(*gp_fixargs((input_area_features, input_grid_reference_system, grid_square_size, output_grid_features, large_grid_handling), True)))
        return retval
    except Exception as e:
        raise e


# Visibility toolset
@gptooldoc('AddLinearLineOfSightFields_mt', None)
def AddLinearLineOfSightFields(Input_Observer_Features=None, Observer_Height_Above_Surface=None, Input_Target_Features=None, Target_Height_Above_Surface=None):
    """AddLinearLineOfSightFields_mt(Input_Observer_Features, Observer_Height_Above_Surface, Input_Target_Features, Target_Height_Above_Surface)

        Adds height field to observer and target point features classes
        before they are used to run Linear Line of Sight (LLOS).

     INPUTS:
      Input_Observer_Features (Feature Layer):
          There is no python reference for this parameter.
      Observer_Height_Above_Surface (Double):
          There is no python reference for this parameter.
      Input_Target_Features (Feature Layer):
          There is no python reference for this parameter.
      Target_Height_Above_Surface (Double):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.AddLinearLineOfSightFields_mt(*gp_fixargs((Input_Observer_Features, Observer_Height_Above_Surface, Input_Target_Features, Target_Height_Above_Surface), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('AddRadialLineOfSightObserverFields_mt', None)
def AddRadialLineOfSightObserverFields(input_observer_features=None, Observer_Offset=None, Surface_Offset=None, Minimum_Distance_Radius=None, Maximum_Distance_Radius=None, Left_Bearing_Azimuth=None, Right_Bearing_Azimuth=None, Top_Vertical_Angle=None, Bottom_Vertical_Angle=None):
    """AddRadialLineOfSightObserverFields_mt(input_observer_features, Observer_Offset, Surface_Offset, Minimum_Distance_Radius, Maximum_Distance_Radius, Left_Bearing_Azimuth, Right_Bearing_Azimuth, Top_Vertical_Angle, Bottom_Vertical_Angle)

        Adds the required visibility modifier fields to a point feature
        class for use in Radial Line Of Sight (RLOS).

     INPUTS:
      input_observer_features (Feature Layer):
          There is no python reference for this parameter.
      Observer_Offset (Double):
          There is no python reference for this parameter.
      Surface_Offset (Double):
          There is no python reference for this parameter.
      Minimum_Distance_Radius (Double):
          There is no python reference for this parameter.
      Maximum_Distance_Radius (Double):
          There is no python reference for this parameter.
      Left_Bearing_Azimuth (Double):
          There is no python reference for this parameter.
      Right_Bearing_Azimuth (Double):
          There is no python reference for this parameter.
      Top_Vertical_Angle (Double):
          There is no python reference for this parameter.
      Bottom_Vertical_Angle (Double):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.AddRadialLineOfSightObserverFields_mt(*gp_fixargs((input_observer_features, Observer_Offset, Surface_Offset, Minimum_Distance_Radius, Maximum_Distance_Radius, Left_Bearing_Azimuth, Right_Bearing_Azimuth, Top_Vertical_Angle, Bottom_Vertical_Angle), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('FindLocalPeaks_mt', None)
def FindLocalPeaks(Input_Area=None, Number_Of_Peaks=None, Input_Surface=None, Output_Peak_Features=None):
    """FindLocalPeaks_mt(Input_Area, Number_Of_Peaks, Input_Surface, Output_Peak_Features)

        Finds the highest local maximums within the defined area. Peaks are
        found by inverting the surface and then finding the sinks in the
        surface. These points are then used to extract elevation values from
        the original surface, sorted based on elevation.

     INPUTS:
      Input_Area (Feature Set):
          There is no python reference for this parameter.
      Number_Of_Peaks (Long):
          There is no python reference for this parameter.
      Input_Surface (Raster Layer):
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Peak_Features (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.FindLocalPeaks_mt(*gp_fixargs((Input_Area, Number_Of_Peaks, Input_Surface, Output_Peak_Features), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('HighestPoints_mt', None)
def HighestPoints(Input_Area=None, Input_Surface=None, Output_Highest_Point_Features=None):
    """HighestPoints_mt(Input_Area, Input_Surface, Output_Highest_Point_Features)

        Finds the highest point (or points if several have the same
        elevation) of the input surface within a defined area.  <SPAN />

     INPUTS:
      Input_Area (Feature Set):
          There is no python reference for this parameter.
      Input_Surface (Raster Layer):
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Highest_Point_Features (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.HighestPoints_mt(*gp_fixargs((Input_Area, Input_Surface, Output_Highest_Point_Features), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('LinearLineOfSight_mt', None)
def LinearLineOfSight(Observers=None, Observer_Height_Above_Surface=None, Targets=None, Target_Height_Above_Surface=None, Input_Elevation_Surface=None, Output_Line_Of_Sight_Features=None, Output_Sight_Line_Features=None, Output_Observer_Features=None, Output_Target_Features=None, Input_Obstruction_Features=None):
    """LinearLineOfSight_mt(Observers, Observer_Height_Above_Surface, Targets, Target_Height_Above_Surface, Input_Elevation_Surface, Output_Line_Of_Sight_Features, Output_Sight_Line_Features, Output_Observer_Features, Output_Target_Features, {Input_Obstruction_Features})

        Creates line(s) of sight between observers and targets.

     INPUTS:
      Observers (Feature Set):
          There is no python reference for this parameter.
      Observer_Height_Above_Surface (Double):
          There is no python reference for this parameter.
      Targets (Feature Set):
          There is no python reference for this parameter.
      Target_Height_Above_Surface (Double):
          There is no python reference for this parameter.
      Input_Elevation_Surface (Raster Layer):
          There is no python reference for this parameter.
      Input_Obstruction_Features {Feature Layer}:
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Line_Of_Sight_Features (Feature Class):
          There is no python reference for this parameter.
      Output_Sight_Line_Features (Feature Class):
          There is no python reference for this parameter.
      Output_Observer_Features (Feature Class):
          There is no python reference for this parameter.
      Output_Target_Features (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.LinearLineOfSight_mt(*gp_fixargs((Observers, Observer_Height_Above_Surface, Targets, Target_Height_Above_Surface, Input_Elevation_Surface, Output_Line_Of_Sight_Features, Output_Sight_Line_Features, Output_Observer_Features, Output_Target_Features, Input_Obstruction_Features), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('LowestPoints_mt', None)
def LowestPoints(Input_Area=None, Input_Surface=None, Output_Lowest_Point_Features=None):
    """LowestPoints_mt(Input_Area, Input_Surface, Output_Lowest_Point_Features)

        Finds the lowest point (or points if several have the same
        elevation) of the input surface within a defined area.

     INPUTS:
      Input_Area (Feature Set):
          There is no python reference for this parameter.
      Input_Surface (Raster Layer):
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Lowest_Point_Features (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.LowestPoints_mt(*gp_fixargs((Input_Area, Input_Surface, Output_Lowest_Point_Features), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('RadialLineOfSight_mt', None)
def RadialLineOfSight(Input_Observer_Features=None, Observer_Height_Above_Surface=None, Radius_Of_Observer=None, Input_Surface=None, Output_Visibility=None, Force_Visibility_To_Infinity__Edge_Of_Surface_=None, Spatial_Reference=None):
    """RadialLineOfSight_mt(Input_Observer_Features, Observer_Height_Above_Surface, Radius_Of_Observer, Input_Surface, Output_Visibility, {Force_Visibility_To_Infinity__Edge_Of_Surface_}, {Spatial_Reference})

        Shows the areas visible (green) and not visible (red) to an
        observer at a specified distance and viewing angle.

     INPUTS:
      Input_Observer_Features (Feature Set):
          There is no python reference for this parameter.
      Observer_Height_Above_Surface (Double):
          There is no python reference for this parameter.
      Radius_Of_Observer (Double):
          There is no python reference for this parameter.
      Input_Surface (Raster Layer):
          There is no python reference for this parameter.
      Force_Visibility_To_Infinity__Edge_Of_Surface_ {Boolean}:
          There is no python reference for this parameter.
      Spatial_Reference {Spatial Reference}:
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Visibility (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.RadialLineOfSight_mt(*gp_fixargs((Input_Observer_Features, Observer_Height_Above_Surface, Radius_Of_Observer, Input_Surface, Output_Visibility, Force_Visibility_To_Infinity__Edge_Of_Surface_, Spatial_Reference), True)))
        return retval
    except Exception as e:
        raise e

@gptooldoc('RadialLineOfSightAndRange_mt', None)
def RadialLineOfSightAndRange(Input_Observer=None, Input_Surface=None, Maximum_Distance__RADIUS2_=None, Left_Azimuth__AZIMUTH1_=None, Right_Azimuth__AZIMUTH2_=None, Observer_Offset__OFFSETA_=None, Near_Distance__RADIUS1_=None, Output_Viewshed=None, Output_Wedge=None, Output_FullWedge=None):
    """RadialLineOfSightAndRange_mt(Input_Observer, Input_Surface, Maximum_Distance__RADIUS2_, Left_Azimuth__AZIMUTH1_, Right_Azimuth__AZIMUTH2_, Observer_Offset__OFFSETA_, Near_Distance__RADIUS1_, Output_Viewshed, Output_Wedge, Output_FullWedge)

        Shows visible areas to one or more observers. Shows the areas
        visible (green) and not visible (red) to an observer at a specified
        distance and viewing angle.

     INPUTS:
      Input_Observer (Feature Set):
          There is no python reference for this parameter.
      Input_Surface (Raster Layer):
          There is no python reference for this parameter.
      Maximum_Distance__RADIUS2_ (String):
          There is no python reference for this parameter.
      Left_Azimuth__AZIMUTH1_ (String):
          There is no python reference for this parameter.
      Right_Azimuth__AZIMUTH2_ (String):
          There is no python reference for this parameter.
      Observer_Offset__OFFSETA_ (String):
          There is no python reference for this parameter.
      Near_Distance__RADIUS1_ (String):
          There is no python reference for this parameter.

     OUTPUTS:
      Output_Viewshed (Feature Class):
          There is no python reference for this parameter.
      Output_Wedge (Feature Class):
          There is no python reference for this parameter.
      Output_FullWedge (Feature Class):
          There is no python reference for this parameter."""
    from arcpy.geoprocessing._base import gp, gp_fixargs
    from arcpy.arcobjects.arcobjectconversion import convertArcObjectToPythonObject
    try:
        retval = convertArcObjectToPythonObject(gp.RadialLineOfSightAndRange_mt(*gp_fixargs((Input_Observer, Input_Surface, Maximum_Distance__RADIUS2_, Left_Azimuth__AZIMUTH1_, Right_Azimuth__AZIMUTH2_, Observer_Offset__OFFSETA_, Near_Distance__RADIUS1_, Output_Viewshed, Output_Wedge, Output_FullWedge), True)))
        return retval
    except Exception as e:
        raise e


# End of generated toolbox code
del gptooldoc, gp, gp_fixargs, convertArcObjectToPythonObject