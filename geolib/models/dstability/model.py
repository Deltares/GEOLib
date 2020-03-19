from geolib.models import Model


class DStability(Model):
    def write(self, filepath, filename):
        """BB. Write class to an stix input file using the given filepath and filename."""

    def add_soil_from_parameters(self, name, code, ydry, ysat, c, phi, dilatancy):
        """BB. Add a soil layer to the object."""

    def add_geometry(self, soilname, points):
        """BB. Add a geometry to the object."""

    def add_phreatic_line(self, label, points):
        """BB. Add a phreatic line to the object."""

    def add_head_line(self, label, points):
        """BB. Add a hydraulic headline to the object."""

    def add_reference_line(self, topheadline_id, bottomheadline_id, label, points):
        """BB. Add a reference line to the object."""

    def add_uniform_load(
        self,
        label,
        x_start,
        x_end,
        magnitude,
        angle_of_distribution=0,
        consolidationfactor_cohesive_layers=100,
    ):
        """BB. Add a uniform load to the object."""

    def set_calculationtype(self, calculation_type, parameters):
        """BB. Sets the calculation type based on the given input and parameters (calls the nnf / sga subfunctions)."""
        pass

    def _set_calculationtype_bbf(
        self, sleft, sbottom, sspacing, snumxy, tbottom, tspacing, tnum, minslipplane
    ):
        """BB. Sets the calculation type to bishop brute force using the given parameters."""

    def _set_calculationtype_sga(self, splaneA, splaneB, minthrust=0, minangle=0):
        """BB. Sets the calculation type to spencer genetic algorithm using the given parameters."""
