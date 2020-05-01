import pytest
from random import randint
from typing import get_type_hints, _GenericAlias

from geolib.models.dsettlement.dsettlement_parserprovider import DSettlementStructure
from geolib.models.dseries_parser import (
    DSeriesSinglePropertyGroup,
    DSeriesListTreeStructureCollection,
    DSeriesTreeStructure)
from geolib.models.dsettlement.internal import (
    Accuracy,
    Curves, Curve,
    PiezoLines, PiezoLine,
    Boundaries, Boundary,
    Layers, Layer,
)


def generate_structure_text(struct_id: int, properties: list) -> str:
    text = f"\t{struct_id} - Object Id\n"
    for property_value in properties:
        if isinstance(property_value, list):
            formatted_value = "\t".join(str(value) for value in property_value)
            text += "" + \
                f"\t\t{len(property_value)} - number of values on first property for object\n" + \
                f"\t\t\t{formatted_value}\n"
        else:
            text += f"\t\t{property_value} - value for this property.\n"
    return text


def generate_collection_text(structure_dict: dict) -> str:
    text = f"{len(structure_dict)} - Number of objects -\n"

    for struct_id, struct_value in structure_dict.items():
        text += generate_structure_text(struct_id, struct_value)

    return text


def get_structure_content(class_type: type) -> list:
    structure_content = []
    for field_name, field_type in ((k, v) for k, v in get_type_hints(class_type).items() if not k.startswith('__')):
        if field_name == "id":
            continue
        field_value = str(randint(0, 100))
        if isinstance(field_type, _GenericAlias) and field_type._name == "List" or issubclass(field_type, list):
            field_value = [str(randint(0, 100)), str(randint(0, 100))]
        structure_content.append(field_value)

    return structure_content


def get_structure_collection_content(class_type: type, collection_size: int) -> dict:
    collection_dict = {}
    for struct_id in range(collection_size):
        collection_dict[str(randint(1, 100))] = get_structure_content(class_type)
    return collection_dict


class TestCurve:

    @pytest.mark.integrationtest
    def test_given_curvetext_when_parse_then_creates_structure(self):
        # 1. Define test data.
        parsed_curve: DSettlementStructure = None
        curve_content = get_structure_content(Curve)
        curve_id = randint(0, 100)
        text = generate_structure_text(curve_id, curve_content)
        # remove general header (only needed when testing for collections)

        # 2. Run test.
        parsed_curve = Curve.parse_text(text)

        # 4. Verify final expectations.
        assert parsed_curve, "No structure was parsed."
        assert isinstance(parsed_curve, DSeriesTreeStructure), "" + \
            f"Parsed structure type ({type(parsed_curve)}) " + \
            f"is not of expected type {DSeriesTreeStructure}"
        assert isinstance(parsed_curve, Curve), "" + \
            f"Parsed curve {type(parsed_curve)} not of type {Curve}"
        parsed_curve_points = [str(point) for point in parsed_curve.points]
        assert parsed_curve.id == curve_id
        assert parsed_curve_points == curve_content[0], "" + \
            f"Curve {parsed_curve.id}, parsed points {parsed_curve.points} " + \
            f"not as expected {curve_content[parsed_curve.id]}."


class TestAccuracy:

    @pytest.mark.integrationtest
    def test_given_accuracytext_when_parse_then_creates_structure(self):
        # 1. Set up test data.
        value = 42.24
        text = f"\t\t{value}"
        parsed_accuracy = None

        # 2. Run test.
        parsed_accuracy = Accuracy.parse_text(text)

        # 3. Verify final expectation.
        assert isinstance(parsed_accuracy, DSeriesSinglePropertyGroup)
        assert parsed_accuracy.accuracy == value, "" + \
            f"Parsed value {parsed_accuracy.accuracy} " + \
            f"does not match expected {value}"


class TestInternalDSeriesListStructureCollections:

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "collection_type, structure_type",
        [
            pytest.param(Curves, Curve, id="Curves"),
            pytest.param(PiezoLines, PiezoLine, id="Piezo Lines"),
            pytest.param(Boundaries, Boundary, id="Boundaries"),
            pytest.param(Layers, Layer, id="Layers"),
        ])
    def test_given_treecollectiontext_when_parse_then_creates_structure(
            self,
            collection_type: DSeriesListTreeStructureCollection,
            structure_type: DSeriesTreeStructure):
        # 1. Define test data.
        parsed_collection: DSettlementStructure = None
        structure_content = get_structure_collection_content(structure_type, 4)
        text = generate_collection_text(structure_content)

        # 2. Verify initial expectations
        assert text is not None

        # 3. Run test.
        parsed_collection = collection_type.parse_text(text)

        # 4. Verify final expectations.
        assert parsed_collection, "No piezolines parsed."
        assert isinstance(parsed_collection, DSeriesListTreeStructureCollection)
        field_name = collection_type.__name__.lower()
        parsed_structures = dict(parsed_collection)[field_name]
        assert len(parsed_structures) == len(structure_content), "" + \
            "Not all the structures were parsed correctly."
        for parsed_structure in parsed_structures:
            assert isinstance(parsed_structure, structure_type), "" + \
                f"Parsed type {type(parsed_structure)} " + \
                f"does not match expected {structure_type}."
            properties = list(dict(parsed_structure).values())
            structure_id = str(properties.pop(0))
            for prop_idx, property_value in enumerate(properties):
                parsed_values = []
                if isinstance(property_value, list):
                    parsed_values = [str(value) for value in property_value]
                else:
                    parsed_values = str(property_value)
                assert parsed_values == structure_content[structure_id][prop_idx], "" + \
                    f"Structure {structure_id}, " + \
                    f"parsed values {parsed_values} " + \
                    f"do not match expected {structure_content[structure_id]}."
