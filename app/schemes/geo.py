from pydantic import BaseModel


class GeoSquare(BaseModel):
    a: tuple[float, float] # (долгота, широта)
    c: tuple[float, float]

    @staticmethod
    def check_valid_geo_square(geo_square: 'GeoSquare'):
        if geo_square.a[0] >= geo_square.c[0]:
            return False
        if geo_square.a[1] >= geo_square.c[1]:
            return False
        return True