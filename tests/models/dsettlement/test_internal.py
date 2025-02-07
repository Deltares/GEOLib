from random import randint
from typing import get_origin

import pytest

from geolib.geometry.one import Point
from geolib.models.dseries_parser import (
    DSeriesTreeStructure,
    DSeriesTreeStructureCollection,
)
from geolib.models.dsettlement.internal import (
    Boundaries,
    Boundary,
    Curve,
    Curves,
    DSettlementStructure,
    GeometryData,
    Layer,
    Layers,
    PiezoLine,
    PiezoLines,
    ProbabilisticData,
)
from geolib.models.dsettlement.probabilistic_calculation_types import (
    ProbabilisticCalculationType,
)
from geolib.models.utils import get_filtered_type_hints


def generate_structure_text(struct_id: int, properties: list) -> str:
    text = f"\t{struct_id} - Object Id\n"
    for property_value in properties:
        if isinstance(property_value, list):
            formatted_value = "\t".join(str(value) for value in property_value)
            text += (
                ""
                + f"\t\t{len(property_value)} - number of values on first property for object\n"
                + f"\t\t\t{formatted_value}\n"
            )
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
    for field_name, field_type in get_filtered_type_hints(class_type):
        if field_name == "id":
            continue
        field_value = str(randint(0, 99))

        # Extract base type for generic aliases
        base_type = get_origin(field_type)  # e.g., get list from list[int]

        if base_type is list or (
            isinstance(field_type, type) and issubclass(field_type, list)
        ):
            field_value = [str(randint(0, 99)), str(randint(0, 99))]
        structure_content.append(field_value)

    return structure_content


def get_structure_collection_content(class_type: type, collection_size: int) -> dict:
    collection_dict = {}
    for struct_id in range(collection_size):
        collection_dict[str(randint(1, 99))] = get_structure_content(class_type)
    return collection_dict


class TestCurve:
    @pytest.mark.integrationtest
    def test_given_curvetext_when_parse_then_creates_structure(self):
        # 1. Define test data.
        parsed_curve: DSettlementStructure = None
        curve_content = get_structure_content(Curve)
        curve_id = randint(1, 100)
        text = generate_structure_text(curve_id, curve_content)
        # remove general header (only needed when testing for collections)

        # 2. Run test.
        parsed_curve = Curve.parse_text(text)

        # 4. Verify final expectations.
        assert parsed_curve, "No structure was parsed."
        assert isinstance(parsed_curve, DSeriesTreeStructure), (
            ""
            + f"Parsed structure type ({type(parsed_curve)}) "
            + f"is not of expected type {DSeriesTreeStructure}"
        )
        assert isinstance(parsed_curve, Curve), (
            "" + f"Parsed curve {type(parsed_curve)} not of type {Curve}"
        )
        parsed_curve_points = [str(point) for point in parsed_curve.points]
        assert parsed_curve.id == curve_id
        assert parsed_curve_points == curve_content[0], (
            ""
            + f"Curve {parsed_curve.id}, parsed points {parsed_curve.points} "
            + f"not as expected {curve_content[parsed_curve.id]}."
        )


class TestInternalDSeriesListStructureCollections:
    @pytest.mark.unittest
    def test_sort_based_on_new_indexes(self):
        # initialise values
        mylist = ["a", "b", "c", "d", "e"]
        myorder = [3, 2, 0, 1, 4]

        # initialise model
        geometry = GeometryData()

        # run test
        result = geometry.sort_based_on_new_indexes(
            new_indexes=myorder, unsorted_list=mylist
        )

        # check if test succeeds
        assert ["d", "c", "a", "b", "e"] == result

    @pytest.mark.integrationtest
    def test_set_probabilistic_data_raises_error(self):
        # Set inputs
        point_of_vertical = Point(x=1, y=1, z=1)
        residual_settlement = 0.01
        maximum_number_of_samples = 15
        maximum_iterations = 100
        reliability_type = ProbabilisticCalculationType.SettlementsDeterministic
        is_reliability_calculation = True
        expected_error = "is_reliability_calculation is set to True but reliability type <ProbabilisticCalculationType.SettlementsDeterministic: -1> is not probabilistic."
        # initialise model
        prob_data = ProbabilisticData()
        # Check expectations
        with pytest.raises(ValueError, match=expected_error):
            prob_data.set_probabilistic_data(
                point_of_vertical=point_of_vertical,
                residual_settlement=residual_settlement,
                maximum_number_of_samples=maximum_number_of_samples,
                maximum_iterations=maximum_iterations,
                reliability_type=reliability_type,
                is_reliability_calculation=is_reliability_calculation,
            )

    @pytest.mark.integrationtest
    def test_set_probabilistic_data(self):
        # Set inputs
        point_of_vertical = Point(x=1, y=2, z=3)
        residual_settlement = 0.01
        maximum_number_of_samples = 15
        maximum_iterations = 10
        reliability_type = ProbabilisticCalculationType.BandWidthOfSettlementsFOSM
        is_reliability_calculation = True
        # initialise model
        prob_data = ProbabilisticData()
        # Check expectations
        test_data = prob_data.set_probabilistic_data(
            point_of_vertical=point_of_vertical,
            residual_settlement=residual_settlement,
            maximum_number_of_samples=maximum_number_of_samples,
            maximum_iterations=maximum_iterations,
            reliability_type=reliability_type,
            is_reliability_calculation=is_reliability_calculation,
        )
        assert test_data.reliability_x_co__ordinate == 1
        assert test_data.residual_settlement == 0.01
        assert test_data.maximum_drawings == 15
        assert test_data.maximum_iterations == 10
        assert test_data.reliability_type.value == 0
        assert test_data.is_reliability_calculation.value == 1

    @pytest.mark.integrationtest
    @pytest.mark.parametrize(
        "collection_type, structure_type",
        [
            pytest.param(Curves, Curve, id="Curves"),
            pytest.param(PiezoLines, PiezoLine, id="Piezo Lines"),
            pytest.param(Boundaries, Boundary, id="Boundaries"),
            pytest.param(Layers, Layer, id="Layers"),
        ],
    )
    def test_given_treecollectiontext_when_parse_then_creates_structure(
        self,
        collection_type: DSeriesTreeStructureCollection,
        structure_type: DSeriesTreeStructure,
    ):
        # TODO Refactor test to test more relevant use cases (such as names)
        # than self generated ones that are always string.
        # 1. Define test data
        parsed_collection: DSettlementStructure = None
        structure_content = get_structure_collection_content(structure_type, 4)
        text = generate_collection_text(structure_content)

        # 2. Verify initial expectations
        assert text is not None

        # 3. Run test.
        parsed_collection = collection_type.parse_text(text)

        # 4. Verify final expectations.
        assert parsed_collection, "No piezolines parsed."
        assert isinstance(parsed_collection, DSeriesTreeStructureCollection)
        field_name = collection_type.__name__.lower()
        parsed_structures = dict(parsed_collection)[field_name]
        assert len(parsed_structures) == len(structure_content), (
            "" + "Not all the structures were parsed correctly."
        )
        for parsed_structure in parsed_structures:
            assert isinstance(parsed_structure, structure_type), (
                ""
                + f"Parsed type {type(parsed_structure)} "
                + f"does not match expected {structure_type}."
            )
            properties = list(dict(parsed_structure).values())
            structure_id = str(properties.pop(0))
            for prop_idx, property_value in enumerate(properties):
                parsed_values = []
                if isinstance(property_value, list):
                    parsed_values = [str(value) for value in property_value]
                else:
                    parsed_values = str(property_value)
                for a, b in zip(parsed_values, structure_content[structure_id][prop_idx]):
                    assert b.startswith(a), (
                        ""
                        + f"Structure {structure_id}, "
                        + f"parsed values {parsed_values} "
                        + f"do not match expected {structure_content[structure_id]}."
                    )
