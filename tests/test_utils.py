import pytest

from geolib.models import BaseDataClass
from geolib.models.utils import get_filtered_type_hints, get_required_class_field


class TestGetFields:
    class DummyClass(BaseDataClass):
        regular_field: int
        optional_field: int = 42

    class DummyClassUnderscored(BaseDataClass):
        regular_field: int
        __underscored_field: int

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "class_type",
        [
            pytest.param(DummyClass, id="Without underscores"),
            pytest.param(DummyClassUnderscored, id="With underscore"),
        ],
    )
    def test_given_class_when_get_required_class_field_then_only_valid_fields_returned(
        self, class_type: type
    ):
        filtered_types = get_required_class_field(class_type)
        assert isinstance(filtered_types, list)
        assert len(filtered_types) == 1
        field_name, field_type = filtered_types[0]
        assert field_name == "regular_field"
        assert field_type.annotation == int

    @pytest.mark.unittest
    @pytest.mark.parametrize(
        "class_type",
        [
            pytest.param(DummyClass, id="Without underscores"),
            pytest.param(DummyClassUnderscored, id="With underscore"),
        ],
    )
    def test_given_class_when_get_filtered_type_hints_then_only_valid_fields_returned(
        self, class_type: type
    ):
        filtered_types = get_filtered_type_hints(class_type)
        assert isinstance(filtered_types, list)
        assert len(filtered_types) == 2
        # 1. First field.
        field_name, field_type = filtered_types[0]
        assert field_name == "regular_field"
        assert field_type == int
