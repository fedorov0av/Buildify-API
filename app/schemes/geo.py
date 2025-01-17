from pydantic import BaseModel


class GeoSquare(BaseModel):
    a: tuple[float, float]
    b: tuple[float, float]
    c: tuple[float, float]
    d: tuple[float, float]

    @staticmethod
    def check_valid_geo_square(geo_square: 'GeoSquare'):
        if geo_square.d[0] <= geo_square.a[0] >= geo_square.b[0]:
            return False
        if geo_square.d[1] <= geo_square.a[1] >= geo_square.c[1]:
            return False
        return True