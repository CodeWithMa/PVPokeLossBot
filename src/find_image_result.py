from attrs import define


@define(frozen=True)
class FindImageResult:
    val: float
    coords: tuple[int, int]
