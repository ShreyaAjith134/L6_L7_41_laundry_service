import pytest

from laundry_service import (
    extra_weight_charge,
    order_acceptable,
    dropoff_status,
)


# Tests for extra_weight_charge()

def test_within_included_weight():
    assert extra_weight_charge("regular", 4, "standard", False) == 0


def test_unknown_garment_type():
    with pytest.raises(ValueError):
        extra_weight_charge("unknown", 5, "standard", False)


def test_negative_weight():
    with pytest.raises(ValueError):
        extra_weight_charge("regular", -1, "standard", False)


def test_member_regular_allowance():
    assert extra_weight_charge("regular", 6, "standard", True) == 0


def test_member_delicate_allowance():
    assert extra_weight_charge("delicate", 5, "standard", True) == 0


def test_member_bedding_no_extra_allowance():
    assert extra_weight_charge("bedding", 9, "standard", True) == 30


def test_standard_extra_weight():
    assert extra_weight_charge("regular", 6, "standard", False) == 30


def test_express_extra_weight():
    assert extra_weight_charge("regular", 6, "express", False) == 50


def test_other_speed_uses_nonstandard_rate():
    assert extra_weight_charge("regular", 6, "overnight", False) == 50


def test_extra_weight_exactly_ten():
    assert extra_weight_charge("regular", 15, "standard", False) == 300


def test_extra_weight_above_ten_standard():
    assert extra_weight_charge("regular", 16, "standard", False) == 495


def test_extra_weight_above_ten_express():
    assert extra_weight_charge("regular", 16, "express", False) == 825


def test_delicate_weight_within_limit():
    assert extra_weight_charge("delicate", 3, "standard", False) == 0


def test_bedding_weight_within_limit():
    assert extra_weight_charge("bedding", 8, "standard", False) == 0


# Tests for order_acceptable()

def test_delicate_order_acceptable():
    assert order_acceptable(10, 5, True) is True


def test_delicate_order_too_many_items():
    assert order_acceptable(10, 6, True) is False


def test_non_delicate_order_overweight():
    assert order_acceptable(26, 10, False) is False


def test_non_delicate_order_at_weight_limit():
    assert order_acceptable(25, 10, False) is True


def test_non_delicate_order_at_item_limit():
    assert order_acceptable(20, 40, False) is True


def test_non_delicate_order_over_item_limit():
    assert order_acceptable(20, 41, False) is False


# Tests for dropoff_status()

def test_bedding_standard_accepted():
    assert dropoff_status(90, True, False) == "accepted"


def test_no_bedding_standard_accepted():
    assert dropoff_status(60, False, False) == "accepted"


def test_bedding_express_accepted():
    assert dropoff_status(120, True, True) == "accepted"


def test_no_bedding_express_accepted():
    assert dropoff_status(90, False, True) == "accepted"


def test_dropoff_late():
    assert dropoff_status(45, False, False) == "late"


def test_bedding_dropoff_late():
    assert dropoff_status(75, True, False) == "late"


def test_express_dropoff_late():
    assert dropoff_status(75, False, True) == "late"


def test_dropoff_rejected():
    assert dropoff_status(39, False, False) == "rejected"


def test_bedding_dropoff_rejected():
    assert dropoff_status(69, True, False) == "rejected"