#workaround for using existing tools with Lorentz vector
class Singlet(object):
    def __init__(self,leg):
        self.leg = leg
        
    def p4(self):
        return self.leg
 
    def __getattr__(self, name):
            return getattr(self.leg,name)
