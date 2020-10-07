Changelog
=========

- :release:`0.1.2 <2020-10-14>` 
- :feature:`-` First release candidate. Thanks to all those who tested and reported their findings.
- :support:`GEOLIB-177` Clarified that `set_model` should be called as early as possible and added warning if called later.
- :support:`GEOLIB-182` Documented output structure of all models and improved documentation with type hints.
- :support:`GEOLIB-200` Moved Soils to it's own file as not to leak the code in compiled versions.
- :support:`GEOLIB-180` Document console flags, installation procedures etc.
- :support:`GEOLIB-172` Documented how moments, forces displacements can be accessed dependent on the calculation type.
- :bug:`GEOLIB-173` All output stages of DSheetPiling are now accessible.
- :bug:`GEOLIB-187` Setting a color for a soil won't error and will now be converted for the older D-Serie models.
- :bug:`GEOLIB-206` `Xi3`, `xi4`, and `ea_gem` can now be also set on TensionPilesModel in DSheetPiling.
- :bug:`GEOLIB-202` `Soildelta` can now be negative.
- :bug:`GEOLIB-193` User defined partial factors were sometimes non-default.
- :bug:`GEOLIB-191` Loads were repeated if added to multiple stages.


- :release:`0.1.1 <2020-09-27>` 
- :feature:`-` Second beta release for testing. Thanks to all those who tested and reported their findings.

  .. note::
    In this release some quick fixes have been made. This is still a *beta* release.
 
- :support:`-` Both `jinja2` and `requests` have been added as dependencies.
- :support:`-` Added `Application` fields to DStability in order to support the latest release.
- :support:`-` Documented `SoilModel` and `ConsolidationModel` enums for the `set_model` of DSettlement.
- :support:`-` Several typos and missing brackets have been fixed in the tutorials.
- :support:`-` Added error message if console wasn't found, instead of a vague process error.
- :bug:`-` CPT data in DFoundations will not fuse to a single value anymore.
- :bug:`-` Examples and tutorials now use `Path` from `pathlib` instead of strings for filepaths.
- :bug:`-` The `angle` of an `Anchor` in DSheetPiling can now be negative.
- :bug:`-` `BaseModelList.execute()` should now work.

- :release:`0.1.0 <2020-07-20>` 
- :feature:`-` First beta release for testing. Works with the following models:
  
  - DFoundations
  - DSheetPiling
  - DSettlement
  - DStability

  .. note::
    This is a *beta* release, not meant for production.
