import attr

@attr.s(frozen=True)
class FindImageResult:
    val = attr.ib()
    coords = attr.ib()
    width = attr.ib()
    height = attr.ib()
