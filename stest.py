class Test:
    flex = 12

    def r(self, par, eq):
        hell = eval(f'self.{par}')
        hell = eq

flex = Test()
exec('flex.flex = 14')
print(flex.flex)