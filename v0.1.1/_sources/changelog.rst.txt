Changelog
=========

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
- :feature:`-` First beta release for testing. 
  Works with the following models:
    - DFoundations
    - DSheetPiling
    - DSettlement
    - DStability

  .. note::
    This is a *beta* release, not meant for production.
