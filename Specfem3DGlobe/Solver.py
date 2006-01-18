#!/usr/bin/env python


from pyre.components.Component import Component
from pyre.units.time import minute
import Specfem3DGlobeCode


class Solver(Component):
    
    class Inventory(Component.Inventory):

        from pyre.inventory import bool, dimensional, float, inputFile, int
    
        cmtSolution                   = inputFile("cmt-solution", default="DATA/CMTSOLUTION")
        
        MOVIE_SURFACE                 = bool("movie-surface")
        MOVIE_VOLUME                  = bool("movie-volume")
        RECEIVERS_CAN_BE_BURIED       = bool("receivers-can-be-buried")
        PRINT_SOURCE_TIME_FUNCTION    = bool("print-source-time-function")
        
        HDUR_MOVIE                    = float("hdur-movie")
        record_length                 = dimensional("record-length", default=0.0*minute)
        
        NTSTEP_BETWEEN_FRAMES         = int("ntstep-between-frames")
        NTSTEP_BETWEEN_OUTPUT_INFO    = int("ntstep-between-output-info")
        NTSTEP_BETWEEN_OUTPUT_SEISMOS = int("ntstep-between-output-seismos")
        NUMBER_OF_RUNS                = int("number-of-runs")
        NUMBER_OF_THIS_RUN            = int("number-of-this-run")

        stations                      = inputFile("stations", default="DATA/STATIONS")

    def __init__(self, name):
        Component.__init__(self, name, "solver")
        self.CMTSOLUTION = None
        self.STATIONS = None

    def _init(self):
        Component._init(self)

        # convert to minutes
        self.RECORD_LENGTH_IN_MINUTES = self.inventory.record_length / minute

        # Access our InputFile inventory items to make sure they're
        # readable.  (They will be reopened by the Fortran code.)
        f = self.inventory.cmtSolution;  self.CMTSOLUTION = f.name;  f.close()
        f = self.inventory.stations;     self.STATIONS    = f.name;  f.close()


# end of file