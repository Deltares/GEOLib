from typing import Optional

from geolib.models import BaseDataClass
from geolib.models.dsheetpiling.internal import SheetPileElement
from geolib.models.dsheetpiling.settings import SheetPilingElementMaterialType


class PileProperties(BaseDataClass):
    """
    Pile selected from the model window in D-Sheet Piling

    Arguments:
     material_type : Select the material of the sheet piling element : User defined, Steel, Concrete, Wood, Synthetic.
     elastic_stiffness_ei  : Stiffness of the section per running meter.
     section_bottom_level  : the vertical co-ordinate of the bottom of the sheet piling, in relation to the reference level.
     mr_char_el : Characterictic elastic moment without safety factors.
     material_factor_gamma_m  : The partial safety factor \u03B3 m should be defined, only if the User defined material type
     is selected. Otherwise, the program will automatically apply the following factors
     (acc. to the corresponding Eurocode) to calculate the design allowable moment
     * Steel : \u03B3m = 1 , acc. to Eurocode 3 – Part 5, art. 5.1.1(4)
     * Concrete : \u03B3m = 1.1, acc. to Eurocode 2 – Part 1.1, art. 3.1.6
     * Wood : \u03B3m = 1 , acc. to Eurocode 5 – Part 1-2, art. 2.3(1)
     * Synthetic : \u03B3m = 1.2
     modification_factor_k_mod  :  The modification factor kmod should be defined, only if the User defined
     and synthetic material type is selected.
     Otherwise, the program will automatically apply the following factors
     * Steel : kmod = 1
     * Concrete : kmod = 1
     * Wood : kmod= 1
     reduction_factor_on_maximum_moment  : The reduction factor applied to the maximum allowable moment
    """

    material_type: Optional[
        SheetPilingElementMaterialType
    ] = SheetPilingElementMaterialType.Steel
    elastic_stiffness_ei: Optional[float] = None
    diameter: Optional[float] = None
    section_bottom_level: Optional[float] = None
    reduction_factor_on_ei: Optional[float] = None
    mr_char_el: Optional[float] = None
    mr_char_pl: Optional[float] = None
    modification_factor_k_mod: Optional[float] = None
    material_factor_gamma_m: Optional[float] = None
    reduction_factor_on_maximum_moment: Optional[float] = None
    note_on_reduction_factor: Optional[str] = None


class WoodenSheetPileProperties(BaseDataClass):
    """
    Wooden pile selected from the model window in D-Sheet Piling


    Arguments:
     elasticity_modulus_e_m_0_mean : The mean modulus of elasticity per running meter.
     charac_flexural_strength_f_m_0_char : The characteristic flexural strength.
     system_factor_k_sys : The system factor that considers the cooperation of structural elements.
     deform_factor_k_def : Specifies deformation factor for the hardwoods or the reduction of the stiffness caused by the saturation of softwoods.
     creep_factor_psi_2_eff : The value of considers the percentage of the load that is constantly present.
     material_factor_gamma_m : The material factor.
     modif_factor_on_f_m_0_char_short_term_k_mod_f_short : The short term modification factor of the strength to count for duration life of the wooden pile.
     modif_factor_on_f_m_0_char_long_term_k_mod_f_long : The long term modification factor of the strength to count for duration life of the wooden pile.
     modification_factor_on_e_m_0_d_k_mod_e : This value describes the modification factor of the elasticity.

    """

    elasticity_modulus_e_m_0_mean: Optional[float] = None
    charac_flexural_strength_f_m_0_char: Optional[float] = None
    system_factor_k_sys: Optional[float] = None
    deform_factor_k_def: Optional[float] = None
    creep_factor_psi_2_eff: Optional[float] = None
    material_factor_gamma_m: Optional[float] = None
    modif_factor_on_f_m_0_char_short_term_k_mod_f_short: Optional[float] = None
    modif_factor_on_f_m_0_char_long_term_k_mod_f_long: Optional[float] = None
    modification_factor_on_e_m_0_d_k_mod_e: Optional[float] = None


class SheetPileProperties(BaseDataClass):
    """
    Pile selected from the model window in D-Sheet Piling


    Arguments:
     material_type : Select the material of the sheet piling element : User defined, Steel, Concrete, Wood, Synthetic.
     acting_width : The acting width can be used when the effective width changes along the sheet piling. D-SHEET PILING uses the acting width as a multiplication factor for the sheet piling stiffness and all loads, supports and reactions, except the normal force.
     elastic_stiffness_ei : Stiffness of the section per running meter.
     section_bottom_level : the vertical co-ordinate of the bottom of the sheet piling, in relation to the reference level.
     mr_char_el: Characterictic elastic moment without safety factors.
     material_factor_gamma_m : The partial safety factor \u03B3m should be defined, only if the User defined material type is selected. Otherwise, the program will automatically apply the following factors (acc. to the corresponding Eurocode) to calculate the design allowable moment:

        * Steel: \u03B3m = 1 , acc. to Eurocode 3 – Part 5, art. 5.1.1(4)
        * Concrete: \u03B3m = 1.1, acc. to Eurocode 2 – Part 1.1, art. 3.1.6
        * Wood: \u03B3m = 1 , acc. to Eurocode 5 – Part 1-2, art. 2.3(1)
        * Synthetic: \u03B3m = 1.2

     modification_factor_k_mod :  The modification factor kmod should be defined, only if the User defined and synthetic material type is selected. Otherwise, the program will automatically apply the following factors:

        * Steel: kmod = 1
        * Concrete: kmod = 1
        * Wood: kmod= 1

     reduction_factor_on_maximum_moment : The reduction factor applied to the maximum allowable moment
     reduction_factor_on_ei : Reduction factor applied on the stiffness EI of the pile.
     coating_area : The area of coating of the sheet piling (> 1). This is defined as the
     length of the perimeter of the sheet piling section per running meter of wall [m2/m2 wall].

     height : The thickness of the sheet piling profile [mm].
     elastic_section_modulus_w_el: The section modulus (also called resisting moment in the Netherlands) of the sheet piling,
     [cm3/m], used for a Feasibility control
     section_area : The cross-sectional area of the sheet piling, [cm3/m].

    """

    material_type: Optional[
        SheetPilingElementMaterialType
    ] = SheetPilingElementMaterialType.Steel
    elastic_stiffness_ei: Optional[float] = None
    acting_width: Optional[float] = None
    section_bottom_level: Optional[
        float
    ] = None  # TODO important paramter, shouldn't be default
    height: Optional[int] = 400  # value is defined in mm
    coating_area: Optional[float] = None
    width_of_sheet_piles: Optional[float] = None
    section_area: Optional[int] = None
    elastic_section_modulus_w_el: Optional[int] = None
    reduction_factor_on_ei: Optional[float] = None
    note_on_reduction_factor: Optional[str] = None
    mr_char_el: Optional[float] = None
    mr_char_pl: Optional[float] = None
    modification_factor_k_mod: Optional[float] = None
    material_factor_gamma_m: Optional[float] = None
    reduction_factor_on_maximum_moment: Optional[float] = None


class SheetPileModelPlasticCalculationProperties(BaseDataClass):
    """
    Refering to Moment-Curvature Diagram(M-N-Kappa) in  the D-SheetPiling UI


    Arguments:
     plastic_moment_positive : The plastic moment of the positive part of the moment-curvature diagram (in compression).
     plastic_moment_negative : The plastic moment of the positive part of the moment-curvature diagram (in traction).

    .. image:: /figures/dsheetpiling/sheetpileplastic.png
        :height: 400px
        :width: 600 px
        :scale: 70 %
        :align: center
    """

    symmetrical: Optional[bool] = False
    plastic_moment_positive: Optional[float] = None
    plastic_moment_negative: Optional[float] = None


class FullPlasticCalculationProperties(BaseDataClass):
    """
    Refering to Moment-Curvature Diagram(M-N-Kappa) in  the D-SheetPiling UI


    Arguments:
     symmetrical : This option is True in case of a symmetric moment-curvature diagram.
     eI_branch_2_positive : The flexural stiffness of the 2nd branch of the moment-curvature diagram (in compression).
     eI_branch_2_negative : The flexural stiffness of the 2nd branch of the moment-curvature diagram (in traction).
     moment_point_1_positive : The limit moment of the of the 1st branch of the moment-curvature diagram (in compression).
     moment_point_1_negative : The limit moment of the of the 1st branch of the moment-curvature diagram (in traction).
     plastic_moment_positive : The plastic moment of the positive part of the moment-curvature diagram (in compression).
     plastic_moment_negative : The plastic moment of the positive part of the moment-curvature diagram (in traction).
     eI_branch_3_positive : The flexural stiffness of the 3rd branch of the moment-curvaturediagram (in compression).
     moment_point_2_positive : The limit moment of the of the 2nd branch of the moment-curvature diagram (in compression).
     eI_branch_3_negative : The flexural stiffness of the 3rd branch of the moment-curvaturediagram (in traction).
     moment_point_2_negative : The limit moment of the of the 2nd branch of the moment-curvature diagram (in traction).

    .. image:: /figures/dsheetpiling/fullplastic.png
        :height: 400px
        :width: 600 px
        :scale: 70 %
        :align: center
    """

    symmetrical: Optional[bool] = False
    eI_branch_2_positive: Optional[float] = None
    eI_branch_2_negative: Optional[float] = None
    moment_point_1_positive: Optional[float] = None
    moment_point_1_negative: Optional[float] = None
    plastic_moment_positive: Optional[float] = None
    plastic_moment_negative: Optional[float] = None
    eI_branch_3_positive: Optional[float] = None
    moment_point_2_positive: Optional[float] = None
    eI_branch_3_negative: Optional[float] = None
    moment_point_2_negative: Optional[float] = None


class DiaphragmWallProperties(BaseDataClass):
    """
    Pile selected from the model window in D-Sheet Piling

    Arguments:
        material_type : Select the material of the sheet piling element : User defined, Steel, Concrete, Wood, Synthetic.
        acting_width : The acting width can be used when the effective width changes along the sheet piling.
            D-SHEET PILING uses the acting width as a multiplication factor for the sheet piling stiffness and all loads,
            supports and reactions, except the normal force.
        elastic_stiffness_ei : Stiffness of the section per running meter.
        section_bottom_level : the vertical co-ordinate of the bottom of the sheet piling, in relation to the reference level.
        mr_char_el:: Characterictic elastic moment without safety factors.
        material_factor_gamma_m : The partial safety factor \u03B3m should be defined, only if the User defined material type
            is selected. Otherwise, the program will automatically apply the following factors
            (acc. to the corresponding Eurocode) to calculate the design allowable moment:

            * Steel: \u03B3m = 1 , acc. to Eurocode 3 – Part 5, art. 5.1.1(4) ;
            * Concrete: \u03B3m = 1.1, acc. to Eurocode 2 – Part 1.1, art. 3.1.6;
            * Wood: \u03B3m = 1 , acc. to Eurocode 5 – Part 1-2, art. 2.3(1);
            * Synthetic: \u03B3m = 1.2

        modification_factor_k_mod :  The modification factor kmod should be defined, only if the User defined
            and synthetic material type is selected.
            Otherwise, the program will automatically apply the following factors:

            * Steel: kmod = 1 ;
            * Concrete: kmod = 1 ;
            * Wood: kmod= 1 ;

        reduction_factor_on_ei : Reduction factor applied on the stiffness EI of the pile.

    """

    material_type: Optional[
        SheetPilingElementMaterialType
    ] = SheetPilingElementMaterialType.Steel
    section_bottom_level: Optional[float] = None
    elastic_stiffness_ei: Optional[float] = None
    acting_width: Optional[float] = None
    reduction_factor_on_ei: Optional[float] = None
    note_on_reduction_factor: Optional[str] = None
    mr_char_el: Optional[float] = None
    mr_char_pl: Optional[float] = None
    modification_factor_k_mod: Optional[float] = None
    material_factor_gamma_m: Optional[float] = None
    reduction_factor_on_maximum_moment: Optional[float] = None


class DiaphragmWall(BaseDataClass):
    """
    Diaphragm Wall selected from the model window in D-Sheet Piling


    Arguments:
     name : Name of the element inputted
     diaphragm_wall_properties : properties specifically used for the Diaphragm Wall element.
     plastic_properties : plastic calculation properties. For the Diaphragm Wall option, these are always present.
    """

    name: str = ""
    diaphragm_wall_properties: Optional[
        DiaphragmWallProperties
    ] = DiaphragmWallProperties()
    plastic_properties: Optional[
        FullPlasticCalculationProperties
    ] = FullPlasticCalculationProperties()

    def to_internal(self) -> SheetPileElement:
        return SheetPileElement(
            name=self.name,
            sheetpilingelementmaterialtype=self.diaphragm_wall_properties.material_type,
            sheetpilingelementei=self.diaphragm_wall_properties.elastic_stiffness_ei,
            sheetpilingelementwidth=self.diaphragm_wall_properties.acting_width,
            sheetpilingelementlevel=self.diaphragm_wall_properties.section_bottom_level,
            sheetpilingelementreductionfactorei=self.diaphragm_wall_properties.reduction_factor_on_ei,
            sheetpilingelementnote=self.diaphragm_wall_properties.note_on_reduction_factor,
            sheetpilingelementmaxcharacteristicmoment=self.diaphragm_wall_properties.mr_char_el,
            sheetpilingelementmaxplasticcharacteristicmoment=self.diaphragm_wall_properties.mr_char_pl,
            sheetpilingelementkmod=self.diaphragm_wall_properties.modification_factor_k_mod,
            sheetpilingelementmaterialfactor=self.diaphragm_wall_properties.material_factor_gamma_m,
            ssheetpilingelementreductionfactormaxmoment=self.diaphragm_wall_properties.reduction_factor_on_maximum_moment,
            diaphragmwallissymmetric=self.plastic_properties.symmetrical,
            diaphragmwallposeielastoplastic1=self.plastic_properties.eI_branch_2_positive,
            diaphragmwallnegeielastoplastic1=self.plastic_properties.eI_branch_2_negative,
            diaphragmwallposmomelastic=self.plastic_properties.moment_point_1_positive,
            diaphragmwallnegmomelastic=self.plastic_properties.moment_point_1_negative,
            diaphragmwallposmomplastic=self.plastic_properties.plastic_moment_positive,
            diaphragmwallnegmomplastic=self.plastic_properties.plastic_moment_negative,
            diaphragmwallposeielastoplastic2=self.plastic_properties.eI_branch_3_positive,
            diaphragmwallposmomelastoplastic=self.plastic_properties.moment_point_2_positive,
            diaphragmwallnegeielastoplastic2=self.plastic_properties.eI_branch_3_negative,
            diaphragmwallnegmomelastoplastic=self.plastic_properties.moment_point_2_negative,
        )


class Sheet(BaseDataClass):
    """
    Sheet Piling selected from the model window in D-Sheet Piling

    Arguments:
     name : Name of the element inputted
     sheet_pile_properties : properties specifically used for the Sheet pile element.
     plastic_properties : plastic calculation properties. If Elastic calculation checkbox is not selected.
    """

    name: str = ""
    sheet_pile_properties: Optional[SheetPileProperties] = SheetPileProperties()
    plastic_properties: Optional[
        SheetPileModelPlasticCalculationProperties
    ] = SheetPileModelPlasticCalculationProperties()
    wooden_sheet_pile_properties: Optional[
        WoodenSheetPileProperties
    ] = WoodenSheetPileProperties()

    def to_internal(self) -> SheetPileElement:
        return SheetPileElement(
            name=self.name,
            sheetpilingelementmaterialtype=self.sheet_pile_properties.material_type,
            sheetpilingelementei=self.sheet_pile_properties.elastic_stiffness_ei,
            sheetpilingelementwidth=self.sheet_pile_properties.acting_width,
            sheetpilingelementlevel=self.sheet_pile_properties.section_bottom_level,
            sheetpilingelementheight=self.sheet_pile_properties.height,
            sheetpilingelementcoatingarea=self.sheet_pile_properties.coating_area,
            sheetpilingpilewidth=self.sheet_pile_properties.width_of_sheet_piles,
            sheetpilingelementsectionarea=self.sheet_pile_properties.section_area,
            sheetpilingelementresistingmoment=self.sheet_pile_properties.elastic_section_modulus_w_el,
            sheetpilingelementreductionfactorei=self.sheet_pile_properties.reduction_factor_on_ei,
            sheetpilingelementnote=self.sheet_pile_properties.note_on_reduction_factor,
            sheetpilingelementmaxcharacteristicmoment=self.sheet_pile_properties.mr_char_el,
            sheetpilingelementmaxplasticcharacteristicmoment=self.sheet_pile_properties.mr_char_pl,
            sheetpilingelementkmod=self.sheet_pile_properties.modification_factor_k_mod,
            sheetpilingelementmaterialfactor=self.sheet_pile_properties.material_factor_gamma_m,
            ssheetpilingelementreductionfactormaxmoment=self.sheet_pile_properties.reduction_factor_on_maximum_moment,
            diaphragmwallissymmetric=self.plastic_properties.symmetrical,
            diaphragmwallposmomplastic=self.plastic_properties.plastic_moment_positive,
            diaphragmwallnegmomplastic=self.plastic_properties.plastic_moment_negative,
            woodensheetpilingelemente=self.wooden_sheet_pile_properties.elasticity_modulus_e_m_0_mean,
            woodensheetpilingelementcharacflexuralstrength=self.wooden_sheet_pile_properties.charac_flexural_strength_f_m_0_char,
            woodensheetpilingelementksys=self.wooden_sheet_pile_properties.system_factor_k_sys,
            woodensheetpilingelementkdef=self.wooden_sheet_pile_properties.deform_factor_k_def,
            woodensheetpilingelementpsi2eff=self.wooden_sheet_pile_properties.creep_factor_psi_2_eff,
            woodensheetpilingelementmaterialfactor=self.wooden_sheet_pile_properties.material_factor_gamma_m,
            woodensheetpilingelementkmodfshort=self.wooden_sheet_pile_properties.modif_factor_on_f_m_0_char_short_term_k_mod_f_short,
            woodensheetpilingelementkmodflong=self.wooden_sheet_pile_properties.modif_factor_on_f_m_0_char_long_term_k_mod_f_long,
            woodensheetpilingelementkmode=self.wooden_sheet_pile_properties.modification_factor_on_e_m_0_d_k_mod_e,
        )


class Pile(BaseDataClass):
    """
    Pile selected from the model window in D-Sheet Piling

    Arguments:
     name: Name of the element inputted
     pile_properties: properties specifically used for the Pile element.
     plastic_properties: plastic calculation properties. If Elastic calculation checkbox is not selected.
    """

    name: str = ""
    pile_properties: Optional[PileProperties] = PileProperties()
    plastic_properties: Optional[
        FullPlasticCalculationProperties
    ] = FullPlasticCalculationProperties()

    def to_internal(self) -> SheetPileElement:
        return SheetPileElement(
            name=self.name,
            sheetpilingelementmaterialtype=self.pile_properties.material_type,
            sheetpilingelementei=self.pile_properties.elastic_stiffness_ei,
            sheetpilingelementwidth=self.pile_properties.diameter,
            sheetpilingelementlevel=self.pile_properties.section_bottom_level,
            sheetpilingelementreductionfactorei=self.pile_properties.reduction_factor_on_ei,
            sheetpilingelementnote=self.pile_properties.note_on_reduction_factor,
            sheetpilingelementmaxcharacteristicmoment=self.pile_properties.mr_char_el,
            sheetpilingelementmaxplasticcharacteristicmoment=self.pile_properties.mr_char_pl,
            sheetpilingelementkmod=self.pile_properties.modification_factor_k_mod,
            sheetpilingelementmaterialfactor=self.pile_properties.material_factor_gamma_m,
            ssheetpilingelementreductionfactormaxmoment=self.pile_properties.reduction_factor_on_maximum_moment,
            diaphragmwallissymmetric=self.plastic_properties.symmetrical,
            diaphragmwallposeielastoplastic1=self.plastic_properties.eI_branch_2_positive,
            diaphragmwallnegeielastoplastic1=self.plastic_properties.eI_branch_2_negative,
            diaphragmwallposmomelastic=self.plastic_properties.moment_point_1_positive,
            diaphragmwallnegmomelastic=self.plastic_properties.moment_point_1_negative,
            diaphragmwallposmomplastic=self.plastic_properties.plastic_moment_positive,
            diaphragmwallnegmomplastic=self.plastic_properties.plastic_moment_negative,
            diaphragmwallposeielastoplastic2=self.plastic_properties.eI_branch_3_positive,
            diaphragmwallposmomelastoplastic=self.plastic_properties.moment_point_2_positive,
            diaphragmwallnegeielastoplastic2=self.plastic_properties.eI_branch_3_negative,
            diaphragmwallnegmomelastoplastic=self.plastic_properties.moment_point_2_negative,
        )
