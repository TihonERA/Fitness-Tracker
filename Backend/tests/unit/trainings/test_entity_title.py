import pytest

from Backend.trainings.domain.exceptions.workout_exceptions import TitleError
from Backend.trainings.domain.value_objects.title import EntityTitle

from faker import Faker


def test_success(faker: Faker) -> None:
    title = faker.name()
    title_object = EntityTitle(title)

    assert title_object.value == title


def test_empty_title() -> None:
    with pytest.raises(TitleError):
        EntityTitle("")


def test_long_title() -> None:
    with pytest.raises(TitleError):
        EntityTitle("long" * 30)
