import pytest

from .utils import Result, pyright_exist, run_pyright


pytestmark = pytest.mark.skipif(
    not pyright_exist(), reason="These tests require pyright"
)
CODE = """
import strawberry

def get_user_age() -> int:
    return 0


@strawberry.type
class User:
    name: str
    age: int = strawberry.field(resolver=get_user_age)


User(name="Patrick")
User(n="Patrick")

reveal_type(User)
reveal_type(User.__init__)
"""


def test_pyright():
    results = run_pyright(CODE)

    assert results == [
        Result(
            type="error",
            message='No parameter named "n" (reportGeneralTypeIssues)',
            line=15,
            column=6,
        ),
        Result(
            type="error",
            message='Argument missing for parameter "name" (reportGeneralTypeIssues)',
            line=15,
            column=1,
        ),
        Result(
            type="info", message='Type of "User" is "Type[User]"', line=17, column=13
        ),
        Result(
            type="info",
            message='Type of "User.__init__" is "(self: User, name: str) -> None"',
            line=18,
            column=13,
        ),
    ]
