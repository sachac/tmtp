#!/usr/bin/env python
# SamplePattern_Pants2.py
# Shaped hem trousers - Back
# Swank-1870-M-T-1

#
# This is a sample pattern design distributed as part of the tmtp
# open fashion design project. It contains a design for one piece
# of the back of a trousers, and will be expanded in the future.
#
# In order to allow designers to control the licensing of their fashion
# designs, this file is not licensed under the GPL but may be used
# in any manner commercial or otherwise, with or without attribution.
#
# Designers are strongly encouraged to release their designs under a
# creative commons license:
#
#  http://creativecommons.org/
#
#
#

from tmtpl.constants import *
from tmtpl.pattern   import *
from tmtpl.document   import *
from tmtpl.support   import *
from tmtpl.client   import Client

# Project specific
#from math import sin, cos, radians

from pysvg.filter import *
from pysvg.gradient import *
from pysvg.linking import *
from pysvg.script import *
from pysvg.shape import *
from pysvg.structure import *
from pysvg.style import *
from pysvg.text import *
from pysvg.builders import *

class PatternDesign():

    def __init__(self):
        self.styledefs = {}
        return

    def pattern(self):
        """
        Method defining a pattern design. This is where the designer places
        all elements of the design definition
        """

        # The following attributes are set before calling this method:
        #
        # self.cd - Client Data, which has been loaded from the client data file
        #
        # self.styledefs - the style difinition dictionary, loaded from the styles file
        #
        # self.cfg - configuration settings from the main app framework
        #
        # TODO find a way to get this administrative cruft out of this pattern method

        cd = self.cd
        self.cfg['clientdata'] = cd

        # pattern name
        pattern_pieces    = 4

        # TODO also extract these from this file to somewhere else
        printer='36" wide carriage plotter'
        if (printer == '36" wide carriage plotter'):
            self.cfg['paper_width']  = ( 36 * in_to_pt )
            self.cfg['border']       = ( 5*cm_to_pt )        # document borders

        border = self.cfg['border']

        # create the document info and fill it in
        # TODO - abstract these into configuration file(s)
        metainfo = {'companyName':'Swank Patterns',      # mandatory
                    'designerName':'Susan Spencer',      # mandatory
                    'patternName':'Steampunk Trousers',  # mandatory
                    'patternNumber':'1870-M-T-1'         # mandatory
                    }
        self.cfg['metainfo'] = metainfo

        # attributes for the entire svg document
        docattrs = {'currentScale' : "0.05 : 1",
                    'fitBoxtoViewport' : "True",
                    'preserveAspectRatio' : "xMidYMid meet",
                    }

        doc = Document(self.cfg, name = 'document', attributes = docattrs)

        # Set up the title block
        tb = TitleBlock('pattern', 'titleblock', self.cfg['border'], self.cfg['border'], stylename = 'titleblock_text_style')
        doc.add(tb)

        #
        # Begin the real work here
        #

        # pattern start, count & placement
        x = border
        y = border

        begin = Point('reference', 'begin', x,   (y + PATTERN_OFFSET), 'point_style')
        doc.add(begin)

        # pattern constants
        rise = cd.outside_leg - cd.inside_leg
        scale = cd.seat/2
        scale_1_4 = scale/4
        scale_1_8 = scale/8

        # The whole pattern in trousers object
        trousers = Pattern('trousers')
        doc.add(trousers)

        # Set up styles dictionary in the pattern object
        trousers.styledefs.update(self.styledefs)

        # Create the back pattern piece
        front = PatternPiece('pattern', 'front', letter = 'A', fabric = 2, interfacing = 0, lining = 0)
        trousers.add(front)

        tf = trousers.front

        start =  Point('reference', 'start', begin.x, begin.y, 'point_style')
        tf.add(start)

        tf.attrs['transform'] = 'translate(' + tf.start.coords + ' )'
        tf.add(Point('reference', 'low', 0, 0, 'point_style'))
        tf.add(Point('reference', 'high', 0, 0, 'point_style'))

        tf.width = border + ( scale_1_8 + (0.5*cm_to_pt)  ) + scale_1_4  + (2*SEAM_ALLOWANCE) + border # (2 to D) + (C to 10) + a seam allowance and a border space for each side
        tf.height = border + (4*cm_to_pt) + cd.outside_leg + HEM_ALLOWANCE + (2*SEAM_ALLOWANCE) + border  #4cm waist height + outside_leg length + 2" hem + a seam allowance and border for waist & hem

        # Points
        tf.add(Point('reference', 'A', start.x + ( scale_1_8 + (0.5*cm_to_pt) ), start.y, 'point_style')) # A is on start top line, over by distance of 2 to D
        tf.add(Point('reference', 'B', tf.A.x, tf.A.y + (4*cm_to_pt), 'point_style')) # B is waistline
        tf.add(Point('reference', 'C', tf.A.x, tf.B.y + (19*cm_to_pt), 'point_style')) # C is seatline
        tf.add(Point('reference', 'D', tf.A.x, tf.A.y + rise, 'point_style')) # D is riseline
        tf.add(Point('reference', 'E', tf.A.x, tf.D.y + ( abs(cd.inside_leg/2) - (0.5*cm_to_pt) ), 'point_style')) # E is kneeline
        tf.add(Point('reference', 'F', tf.A.x, tf.D.y + cd.inside_leg, 'point_style')) # F is hemline
        tf.add(Point('reference', 'I', tf.A.x, tf.B.y + ( abs(tf.C.y - tf.B.y)/2 ) , 'point_style')) # I is midpoint b/w waist and rise

        tf.add(Point('reference', '_2', tf.D.x - ( scale_1_8 + (0.5*cm_to_pt) ),  tf.D.y, 'point_style'))
        distance = (tf.D.x - tf._2.x)/2
        x, y = pointAlongLine(tf.D.x, tf.D.y, tf.D.x - 100, tf.D.y - 100, distance)
        tf.add(Point('reference', '_3', x, y, 'point_style'))
        tf.add(Point('reference', '_4', tf.A.x - (4*cm_to_pt), tf.E.y, 'point_style'))
        tf.add(Point('reference', '_5', tf.A.x - (2.5*cm_to_pt), tf.F.y, 'point_style'))
        tf.add(Point('reference', '_6', tf._4.x, tf.D.y, 'point_style'))
        tf.add(Point('reference', '_7', tf.B.x + (cd.waist/4),  tf.B.y, 'point_style'))
        tf.add(Point('reference', '_8', tf._7.x + (0.5*cm_to_pt), tf.A.y, 'point_style'))
        tf.add(Point('reference', '_9', tf.I.x + (cd.seat/4) - (1*cm_to_pt), tf.I.y, 'point_style'))
        tf.add(Point('reference', '_10', tf.C.x + (cd.seat/4) , tf.C.y, 'point_style'))
        tf.add(Point('reference', '_11', tf._10.x - (0.5*cm_to_pt), tf.D.y, 'point_style'))
        tf.add(Point('reference', '_12', tf._4.x + (cd.knee/2), tf._4.y, 'point_style'))
        tf.add(Point('reference', '_13', tf._5.x + (cd.bottom_width/2), tf._5.y, 'point_style'))
        tf.add(Point('reference', '_14', tf._5.x + ( (tf._13.x - tf._5.x)/2 ), tf._5.y, 'point_style'))
        tf.add(Point('reference', '_15', tf._14.x, tf._14.y - (2*cm_to_pt), 'point_style'))
        tf.add(Point('reference', '_16', tf._2.x + ( (tf._11.x - tf._2.x)/2 ), tf._2.y, 'point_style'))

        tf.add(Point('reference', 'c1', tf._2.x + ( abs(tf._2.x - tf._3.x)*.34 ), tf._2.y - ( abs(tf._2.y - tf._3.y)*.28 ), 'point_style')) #b/w 2 & 3
        tf.add(Point('reference', 'c2', tf._2.x + ( abs(tf._2.x - tf._3.x)*.75 ), tf._2.y - ( abs(tf._2.y - tf._3.y)*.51 ), 'point_style')) #b/w 2 & 3
        tf.add(Point('reference', 'c3', tf._3.x + ( abs(tf._3.x - tf.C.x)*.63 ), tf._3.y - ( abs(tf._3.y - tf.C.y)*.27 ), 'point_style'))  #b/w 3 & C
        tf.add(Point('reference', 'c4', tf.C.x, tf._3.y - ( abs(tf._3.y - tf.C.y)*.65 ), 'point_style')) # b/w 3 & C
        tf.add(Point('reference', 'c5', tf.C.x, tf.C.y - ( abs(tf.C.y - tf.A.y)*.31 ), 'point_style')) # b/w C & A
        tf.add(Point('reference', 'c6', tf.C.x, tf.A.y, 'point_style')) # b/w C & A

        tf.add(Point('reference', 'G', tf._16.x , tf.A.y, 'point_style'))
        distance = (tf._4.y - tf._6.y)/2
        x, y = pointAlongLine(tf._4.x, tf._4.y, tf._5.x, tf._5.y, -distance)
        tf.add(Point('reference', 'J', x,  y, 'point_style'))

        tf.add(Point('reference', 'c7', tf.J.x - ( (tf.J.x - tf._2.x)*.07 ), tf.J.y - ( (tf.J.y - tf._2.y)*.29 ), 'point_style')) #b/w J & _2
        tf.add(Point('reference', 'c8', tf.J.x - ( (tf.J.x - tf._2.x)*.11 ), tf.J.y - ( (tf.J.y - tf._2.y)*.64 ), 'point_style')) #b/w J & _2

        tf.add(Point('reference', 'K',  tf._5.x, tf._5.y + HEM_ALLOWANCE, 'point_style'))
        tf.add(Point('reference', 'L',  tf._13.x, tf._13.y + HEM_ALLOWANCE, 'point_style'))
        tf.add(Point('reference', 'M',  tf._15.x, tf._15.y + HEM_ALLOWANCE, 'point_style'))
        tf.add(Point('reference', 'X', tf._11.x - ( (tf._11.x - tf._12.x)*.57 ), tf._11.y - ( (tf._11.y - tf._12.y)*.5 ), 'point_style')) #inflection point b/w 11 & 12

        tf.add(Point('reference', 'c9', tf._7.x - ( (tf._7.x - tf._9.x)*.4 ), tf._7.y - ( (tf._7.y - tf._9.y)*.33 ), 'point_style')) #b/w 7 & 9
        tf.add(Point('reference', 'c10', tf._7.x - ( (tf._7.x - tf._9.x)*.81 ), tf._7.y - ( (tf._7.y - tf._9.y)*.66 ), 'point_style')) #b/w 7 & 9

        tf.add(Point('reference', 'c11', tf._9.x - ( (tf._9.x - tf._10.x)*.7 ), tf._9.y - ( (tf._9.y - tf._10.y)*.35 ), 'point_style')) #b/w 9 & 10
        tf.add(Point('reference', 'c12', tf._9.x - ( (tf._9.x - tf._10.x)*.96 ), tf._9.y - ( (tf._9.y - tf._10.y)*.67 ), 'point_style')) #b/w 9 & 10

        tf.add(Point('reference', 'c13', tf._10.x - ( (tf._10.x - tf._11.x)*.2 ), tf._10.y - ( (tf._10.y - tf._11.y)*.34 ), 'point_style')) #b/w 10 & 11
        tf.add(Point('reference', 'c14', tf._10.x - ( (tf._10.x - tf._11.x)*.4 ), tf._10.y - ( (tf._10.y - tf._11.y)*.68 ), 'point_style')) #b/w 10 & 11

        tf.add(Point('reference', 'c15', tf.X.x - ( (tf.X.x - tf._12.x)*.53 ), tf.X.y - ( (tf.X.y - tf._12.y)*.35 ), 'point_style')) #b/w X & 12
        tf.add(Point('reference', 'c16', tf.X.x - ( (tf.X.x - tf._12.x)*.74 ), tf.X.y - ( (tf.X.y - tf._12.y)*.67 ), 'point_style')) #b/w X & 12

        tf.add(Point('reference', 'c17', tf.L.x, tf.L.y, 'point_style')) #b/w L & M
        tf.add(Point('reference', 'c18', tf.L.x - ( (tf.L.x - tf.M.x)*.66 ),  tf.M.y, 'point_style')) #b/w L & M

        tf.add(Point('reference', 'c19', tf.M.x - ( (tf.M.x - tf.K.x)*.34 ), tf.M.y, 'point_style')) #b/w M & K
        tf.add(Point('reference', 'c20', tf.K.x,  tf.K.y, 'point_style')) #b/w M & K

        tf.add(Point('reference', 'c21', tf._13.x, tf._13.y, 'point_style')) #b/w 13 & 15
        tf.add(Point('reference', 'c22', tf._13.x - ( (tf._13.x - tf._15.x)*.66 ), tf._15.y, 'point_style')) #b/w 13 & 15

        tf.add(Point('reference', 'c23', tf._15.x - ( (tf._15.x - tf._5.x)*.34 ), tf._15.y, 'point_style')) #b/w 15 & 5
        tf.add(Point('reference', 'c24', tf._5.x, tf._5.y, 'point_style')) #b/w 15 & 5


       # Assemble all paths down here
        # Paths are a bit differemt - we create the SVG and then create the object to hold it
        # See the pysvg library docs for the pysvg methods
        seamline_path_svg = path()
        tf.add(Path('pattern', 'path', 'Trousers Front Seamline Path', seamline_path_svg, 'seamline_path_style'))
        seamline_path_svg.appendMoveToPath(tf.A.x, tf.A.y, relative = False)
        seamline_path_svg.appendLineToPath(tf._8.x, tf._8.y, relative = False)
        seamline_path_svg.appendLineToPath(tf._7.x, tf._7.y, relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c9.x, tf.c9.y, tf.c10.x,  tf.c10.y,  tf._9.x, tf._9.y,  relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c11.x, tf.c11.y, tf.c12.x,  tf.c12.y,  tf._10.x, tf._10.y,  relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c13.x, tf.c13.y, tf.c14.x,  tf.c14.y,  tf._11.x, tf._11.y,  relative = False)
        seamline_path_svg.appendLineToPath(tf.X.x, tf.X.y, relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c15.x, tf.c15.y, tf.c16.x,  tf.c16.y,  tf._12.x, tf._12.y,  relative = False)
        seamline_path_svg.appendLineToPath(tf._13.x, tf._13.y, relative = False)
        seamline_path_svg.appendLineToPath(tf.L.x, tf.L.y, relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c17.x, tf.c17.y, tf.c18.x,  tf.c18.y,  tf.M.x, tf.M.y,  relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c19.x, tf.c19.y, tf.c20.x,  tf.c20.y,  tf.K.x, tf.K.y,  relative = False)
        seamline_path_svg.appendLineToPath(tf._5.x, tf._5.y, relative = False)
        seamline_path_svg.appendLineToPath(tf._4.x, tf._4.y, relative = False)
        seamline_path_svg.appendLineToPath(tf.J.x, tf.J.y, relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c7.x, tf.c7.y, tf.c8.x,  tf.c8.y,  tf._2.x, tf._2.y,  relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c1.x, tf.c1.y, tf.c2.x,  tf.c2.y,  tf._3.x, tf._3.y,  relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c3.x, tf.c3.y, tf.c4.x,  tf.c4.y,  tf.C.x, tf.C.y,  relative = False)
        seamline_path_svg.appendCubicCurveToPath(tf.c5.x, tf.c5.y, tf.c6.x,  tf.c6.y,  tf.A.x, tf.A.y,  relative = False)

        cuttingline_path_svg = path()
        tf.add(Path('pattern', 'path', 'Trousers Front Cuttingline Path', cuttingline_path_svg, 'cuttingline_style'))
        cuttingline_path_svg.appendMoveToPath(tf.A.x, tf.A.y, relative = False)
        cuttingline_path_svg.appendLineToPath(tf._8.x, tf._8.y, relative = False)
        cuttingline_path_svg.appendLineToPath(tf._7.x, tf._7.y, relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c9.x, tf.c9.y, tf.c10.x,  tf.c10.y,  tf._9.x, tf._9.y,  relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c11.x, tf.c11.y, tf.c12.x,  tf.c12.y,  tf._10.x, tf._10.y,  relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c13.x, tf.c13.y, tf.c14.x,  tf.c14.y,  tf._11.x, tf._11.y,  relative = False)
        cuttingline_path_svg.appendLineToPath(tf.X.x, tf.X.y, relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c15.x, tf.c15.y, tf.c16.x,  tf.c16.y,  tf._12.x, tf._12.y,  relative = False)
        cuttingline_path_svg.appendLineToPath(tf._13.x, tf._13.y, relative = False)
        cuttingline_path_svg.appendLineToPath(tf.L.x, tf.L.y, relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c17.x, tf.c17.y, tf.c18.x,  tf.c18.y,  tf.M.x, tf.M.y,  relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c19.x, tf.c19.y, tf.c20.x,  tf.c20.y,  tf.K.x, tf.K.y,  relative = False)
        cuttingline_path_svg.appendLineToPath(tf._5.x, tf._5.y, relative = False)
        cuttingline_path_svg.appendLineToPath(tf._4.x, tf._4.y, relative = False)
        cuttingline_path_svg.appendLineToPath(tf.J.x, tf.J.y, relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c7.x, tf.c7.y, tf.c8.x,  tf.c8.y,  tf._2.x, tf._2.y,  relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c1.x, tf.c1.y, tf.c2.x,  tf.c2.y,  tf._3.x, tf._3.y,  relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c3.x, tf.c3.y, tf.c4.x,  tf.c4.y,  tf.C.x, tf.C.y,  relative = False)
        cuttingline_path_svg.appendCubicCurveToPath(tf.c5.x, tf.c5.y, tf.c6.x,  tf.c6.y,  tf.A.x, tf.A.y,  relative = False)

        hemline_path_svg = path()
        tf.add(Path('pattern', 'path', 'Trousers Front Hemline Path', hemline_path_svg, 'dart_style'))
        hemline_path_svg.appendMoveToPath(tf._13.x, tf._13.y, relative = False)
        hemline_path_svg.appendCubicCurveToPath(tf.c21.x, tf.c21.y, tf.c22.x,  tf.c22.y,  tf._15.x, tf._15.y,  relative = False)
        hemline_path_svg.appendCubicCurveToPath(tf.c23.x, tf.c23.y, tf.c24.x,  tf.c24.y,  tf._5.x, tf._5.y,  relative = False)

        waistline_path_svg = path()
        tf.add(Path('pattern', 'path', 'Trousers Front Waistline Path', waistline_path_svg, 'dart_style'))
        waistline_path_svg.appendMoveToPath(tf.B.x, tf.B.y, relative = False)
        waistline_path_svg.appendLineToPath(tf._7.x, tf._7.y, relative = False)

        # set the label location. Somday this should be automatic
        tf.label_x = tf._16.x + 30
        tf.label_y = tf._16.y

        # end of first pattern piece

        # call draw once for the entire pattern
        doc.draw()
        return

# vi:set ts=4 sw=4 expandtab:
