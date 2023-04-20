Changelog
=========
- :release:`0.6.0 <2023-04-20>`
- :feature:`-` Add support for D-Sheet Piling & D-Foundations 23.1 (#115)

- :release:`0.5.1 <2023-04-04>`
- :feature:`-` Add optional parameter for stage_id to DStabilityModel.get_result (#114)

- :release:`0.5.0 <2023-04-03>`
- :feature:`-` Breaking change: D-Stability output property now returns the results for all stages.
- :feature:`-` Add methods to D-Stability model: add_state_correlation, add_soil_correlation.
- :bug:`-` Cannot add features to default stage 0 (#95) 
- :bug:`-` D-Stability cant set the stochastic properties of a pop parameter (#104)
- :bug:`-` Increased maximum length of pile name to 100 characters (#105)
- :bug:`-` Remove Earthquake from D-SheetPiling (#107)
- :bug:`-` The wall types Wooden Sheet Piling and Diaphragm Wall are not correctly defined (#111)
 
- :release:`0.4.0 <2023-01-24>`
- :feature:`-` Add extra method for D-Stability and D-Geo Flow to look up a Soil by name and edit it. By yida-tao. 👍
- :feature:`-` Add official support for Python 3.11.

- :release:`0.3.0 <2023-01-06>`
- :feature:`-` Add support for serializing to a BytesIO buffer. (Issue #68) By Mbweehuizen. 👍

- :release:`0.2.4 <2022-12-08>`
- :bug:`-` Return generated soil id when using add_soil method in D-Stability and D-Geo Flow. (Issue #64)

- :release:`0.2.3 <2022-12-05>`
- :bug:`-` Set default value for Cu (0.0) in D-Foundations.

- :release:`0.2.2 <2022-11-28>`
- :feature:`-` Set dates in project info for D-Geo Flow and D-Stability. By yurnih. 👍
- :feature:`-` Update python package dependencies.
- :support:`-` Various documentation improvements.

- :release:`0.2.1 <2022-10-31>`
- :bug:`-` Fix: Updated D-Geo Flow model to latest version before release.
 
- :release:`0.2.0 <2022-10-24>`
- :feature:`-` Feature: Add support for upcoming release of D-Geo Flow 2022.01. By MatthiasHauthVIKTOR & carloslubbers. 👍
 
- :release:`0.1.12 <2022-10-21>`
- :bug:`-` Fix: Fixed documentation typo link.

- :release:`0.1.11 <2022-10-10>`
- :bug:`-` Fix: Changed default value pre stress in anchors D-SheetPiling from 0.1 to 0.0 (#28). By martinapippi. 👍

- :release:`0.1.9 <2022-10-04>`
- :bug:`-` D-Stability parsing error with NaN values in Soil

- :release:`0.1.8 <2022-08-08>`
- :bug:`-` Allow load_type: DSHEETPILING_DETERMINED for UnformLoad and SurchargeLoad in DSheetPiling. By Mbweehuizen. 👍
- :feature:`-` Added support for D-Stability 2022.01.(x) files.
- :feature:`-` Added support for Python 3.10. By yurnih. 👍


- :release:`0.1.7 <2022-06-21>`
- :bug:`-` Fix for D-Stability files that cannot be parsed due to incorrect directory separators.
- :feature:`-` Added support for Python 3.9. By yurnih. 👍

- :release:`0.1.6 <2021-10-5>`
- :bug:`-` Set correct number of lines in [RUN IDENTIFICATION] in DSettlement and DSheetPiling. By Maarten Betman of Boskalis. 👍
- :bug:`-` Constrain the length of the `name` field in DSheetPiling structures. Reported by Martina Pippi of CEMS. 👍
- :bug:`-` Fixed an edge case in the sorting of boundaries in DSettlement. By Thijs Damsma of van Oord. 👍
- :feature:`-` Enable (unsupported) soilvisualizations field for DStability. By Thijs Damsma of van Oord. 👍
- :support:`-` Extra installation instructions and typo fix. By Thijs Damsma of van Oord. 👍

- :release:`0.1.5 <2021-04-10>`
- :bug:`-` Large values in DSheetPiling input, such as Anchor, could fuse together, producing invalid files.
- :bug:`-` Removed monkeypatching of Pydantic Config, resulting in odd bugs with other packages such as GEOLib+
- :bug:`-` Now parses names with spaces of layers, materials.

- :release:`0.1.4 <2021-03-10>`
- :feature:`-` Add support for D-Stability **20.3**. 🎉 Note that this drops support for older DStability releases, the console release should follow soon.
- :bug:`-` Fix consolidation validation for layer loads in DStability model. By Joost Dobken of van Oord. 👍
- :bug:`-` Aligned and relaxed constraints of Anchor and Strut fields with the internal models used in DSheetPiling.
- :bug:`-` Fix unused consolidations in DStability.
- :bug:`-` Always parse Model settings in DSheetPiling.
- :support:`-` Clarified documentation about [moments_forces_displacements] in the DSheetPiling output.
- :support:`-` Add env option to ignore extra_fields instead of raising a ValidationError.
- :bug:`-` Allow negative angle of Anchor.

- :release:`0.1.3 <2020-11-9>`
- :feature:`-` Hotfix release.
- :support:`-` Limits Pydantic version, as the new 1.7 release broke GEOLib (`Version` object has no attribute `__field__defaults__`)
- :bug:`-` Fixed ValidationError on console folder when doing a remote execution. Bug was created in the fix for GEOLIB-204 in `0.1.2`.

- :release:`0.1.2 <2020-10-16>`
- :feature:`-` First release. Thanks to all those who tested and reported their findings.
- :support:`-` Dialed down the logging levels and documented how to change the logging levels.
- :support:`GEOLIB-177` Clarified that `set_model` should be called as early as possible and added warning if called later.
- :support:`GEOLIB-182` Documented output structure of all models and improved documentation with type hints.
- :support:`GEOLIB-200` Moved Soils to it's own file as not to leak the code in compiled versions.
- :support:`GEOLIB-180` Document console flags, installation procedures, licenses for consoles.
- :support:`GEOLIB-172` Documented how moments, forces displacements can be accessed dependent on the calculation type.
- :support:`GEOLIB-186` Documented soil_type_nl for DFoundations.
- :support:`GEOLIB-196` Fixed erroneous documentation about Soil for DStability.
- :support:`GEOLIB-198` Clarified Soil construction in documentation and made usage of extra fields an error (**breaking**).
- :support:`GEOLIB-205` Improved error handling on the webservice so it's easier to debug.
- :support:`GEOLIB-208` Improved handling of urls without trailing / for remote execution.
- :support:`GEOLIB-190` Set the load_type of VerificationLoadSettingsHorizontalLineLoad to DSheetPiling Determined.
- :support:`GEOLIB-184` Renamed the pile factors in a Pile for clarity in DFoundations (**breaking**).
- :support:`GEOLIB-194` Renamed some PartialFactorSets Enums for clarity in DSheetPiling (**breaking**).
- :support:`GEOLIB-211` Clarified vertical_permeability in Soil should be in [m/day].
- :support:`-` Added errors attribute to BaseModelList for failed models.
- :support:`-` Added tutorial about multiple calculations using BaseModelList.
- :support:`-` Unified settings into metadata for both local and remote models. Added timeout for execution to metadata.
- :bug:`GEOLIB-173` All output stages of DSheetPiling are now accessible.
- :bug:`GEOLIB-187` Setting a color for a soil won't error and will now be converted for the older D-Serie models.
- :bug:`GEOLIB-206` `Xi3`, `xi4`, and `ea_gem` can now be also set on TensionPilesModel in DSheetPiling.
- :bug:`GEOLIB-202` `Soildelta` can now be negative.
- :bug:`GEOLIB-193` User defined partial factors were sometimes non-default.
- :bug:`GEOLIB-191` Loads were repeated if added to multiple stages.
- :bug:`GEOLIB-166` Clarified how to generate geometry in order to have a correct surface line.
- :bug:`GEOLIB-187` Added actual conversion of Soil colors for the older D-Serie models.
- :bug:`GEOLIB-207` Usage of NaNs in the older D-Serie models will now yield an error.
- :bug:`GEOLIB-209` ShearStrengthModelTypePhreaticLevel is now only defined once.
- :bug:`GEOLIB-210` We now always try to parse output after execution, even if the return code is non-zero.
- :bug:`GEOLIB-197` compression_input_type is now defined and documented.
- :bug:`GEOLIB-202` Soildelta can now be negative as well.
- :bug:`GEOLIB-206` Xi3, Xi4 and other options can now be set on TensionPilesModel as well.
- :bug:`GEOLIB-203` DStability files containing NaNs failed to serialize after execution in the webservice.
- :bug:`GEOLIB-204` On remote execution, console folder was derived from the given model, not the geolib.env file.
- :bug:`GEOLIB-192` LateralEarthPressureMethodStage in SheetPileMethod appeared as mixed when it should be C_PHI_DELTA.

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
