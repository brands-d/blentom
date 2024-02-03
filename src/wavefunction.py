from pathlib import Path


class Wavefunction:

    @classmethod
    def read(cls, filename, name=None, level=None):
        if name is None:
            name = Path(filename).stem

        data, origin, axes, unit_cell = Wavefunction._parse_cube(filename)
        wavefunction = Wavefunction(
            data, origin, axes, level=level, unit_cell=unit_cell
        )
        return wavefunction

    @classmethod
    def read(cls, filename, name=None, level=None):
        if name is None:
            name = Path(filename).stem
        density = VaspChargeDensity(filename).chg[-1]
        unit_cell = VaspChargeDensity(filename).atoms[-1].cell
        return ChargeDensity(density, unit_cell, name, level=level)
