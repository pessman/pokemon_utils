from math import floor


class stats:

    def __init__(self, base, iv, ev, level, nature):
        self.base = base
        self.ev = ev
        self.iv = iv
        self.level = level
        self.nature = nature

    def get_ev_contribution(self, ev):
        return floor(ev / 4)

    def get_level_contribution(self, base, iv, ev_contribution, level):
        return floor(level * (2 * base + iv + ev_contribution) / 100)

    def get_hp(self):
        free_stats = self.level + 10
        ev_stats = self.get_ev_contribution(self.ev[0])
        level_stats = self.get_level_contribution(self.base[0], self.iv[0], ev_stats, self.level)
        return level_stats + free_stats

    def get_other_stats(self):
        from pokemon.models import Nature

        ev_stats = [self.get_ev_contribution(val) for val in self.ev]
        print (ev_stats)
        level_stats = [self.get_level_contribution(self.base[x], self.iv[x], ev_stats[x], self.level) for x in range(1, len(self.base))]
        print(level_stats)
        nature_modifiers = Nature.objects.get(name=self.nature).modifiers()
        print(nature_modifiers)
        return [floor((level_stats[x-1] + 5) * nature_modifiers[x-1]) for x in range(1, len(self.base))]