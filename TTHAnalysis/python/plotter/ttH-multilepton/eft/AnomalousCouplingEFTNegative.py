from HiggsAnalysis.CombinedLimit.PhysicsModel import *
from HiggsAnalysis.CombinedLimit.SMHiggsBuilder import SMHiggsBuilder
import ROOT, os

#
# See derivation and explanation, validation, tests in AN-20-204
#


class AnaliticAnomalousCouplingEFTNegative(PhysicsModel):

    "Float independently cross sections and branching ratios"
    def __init__(self):
        PhysicsModel.__init__(self)
        self.mHRange = []
        self.poiNames = []
        self.alternative = False

        self.sgnl_known = ['ttH','ttZ','ttW']



        self.Operators = [
            'ctp', 'ctG', 'cptb', 'cpt',
        ]

        self.numOperators = len(self.Operators)

        print " Operators = ", self.Operators

        # regular expressions for process names:
        self.sm_re    = re.compile('(?P<proc>.*)_SM')
        self.lin_re   = re.compile('(?P<proc>.*)_lin_(?P<c1>.*)')
        self.quad_re  = re.compile('(?P<proc>.*)_quad_(?P<c1>.*)')
        self.mixed_re = re.compile('(?P<proc>.*)_quad_(?P<c1>.*)_(?P<c2>.*)') # should go before quad


    def setPhysicsOptions(self,physOptions):
        for po in physOptions:

            if po.startswith("eftOperators="):
                self.Operators = po.replace("eftOperators=","").split(",")
                print " Operators = ", self.Operators
                self.numOperators = len(self.Operators)

            if po.startswith("eftAlternative"):
                self.alternative = True
                raise RuntimeError("Alternative not yet implemented")


#
# Define parameters of interest
#

    def doParametersOfInterest(self):
        """Create POI and other parameters, and define the POI set."""

        self.modelBuilder.doVar("r[1,-10,10]")
        self.poiNames = "r"


        for operator in range(0, self.numOperators):
          self.modelBuilder.doVar(str(self.Operators[operator]) + "[0,-200,200]")
          self.poiNames += "," + str(self.Operators[operator])



        if not self.alternative :

          if self.numOperators != 1:
            self.modelBuilder.factory_(
                 "expr::func_sm(\"@0*(1-(" +
                                          "@" + "+@".join([str(i+1) for i in range(len(self.Operators))])  +
                                          "-@" + "-@".join([str(i+1)+"*@"+str(j+1) for i in range(len(self.Operators)) for j in range(len(self.Operators)) if i<j ]) +
                                          "))\",r," + "" + ", ".join([str(self.Operators[i]) for i in range(len(self.Operators))]) + ")"
                 )
          else :
            self.modelBuilder.factory_(
                 "expr::func_sm(\"@0*(1-(" +
                                          "@1" +
                                          "))\",r," + "" + str(self.Operators[0]) + ")"
                 )
        else :


          if self.numOperators != 1:
            self.modelBuilder.factory_(
                 "expr::func_sm(\"@0*(1-(" +
                                          "@" + "+@".join([str(i+1) for i in range(len(self.Operators))])  +
                                          "))\",r," + "" + ", ".join([str(self.Operators[i]) for i in range(len(self.Operators))]) + ")"
                 )
          else :
            self.modelBuilder.factory_(
                 "expr::func_sm(\"@0*(1-(" +
                                          "@1" +
                                          "))\",r," + "" + str(self.Operators[0]) + ")"
                 )





        #
        # this is the coefficient of "SM + Lin_i + Quad_i"
        #

        if not self.alternative :
          if self.numOperators != 1:
            for operator in range(0, self.numOperators):
              #print " Test = "
              #print "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +                                           \
                                 #"(\"@0*(" +                                                                                      \
                                 #"@1 * (1-(" + "@" + "+@".join( [str(j+2) for j in range(len(self.Operators) -1) ] ) + ") )" +      \
                                 #")\",r," + str(self.Operators[operator]) +                                                     \
                                 #", " + ", ".join( [str(self.Operators[j]) for j in range(len(self.Operators)) if operator!=j ] ) +            \
                                 #")"
              #
              #
              # expr::func_sm_linear_quadratic_cG("@0*(@1 * (1-2*(@2+@3) ))",r,cG, cGtil, cH)
              #
              #
              self.modelBuilder.factory_(
                      "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +
                                 "(\"@0*(" +
                                 "@1 * (1-(" + "@" + "+@".join( [str(j+2) for j in range(len(self.Operators) -1) ] ) + ") )" +
                                 ")\",r," + str(self.Operators[operator]) +
                                 ", " + ", ".join( [str(self.Operators[j]) for j in range(len(self.Operators)) if operator!=j ] ) +
                                 ")"
                      )
          else :
            #print "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +                   \
                      #"(\"@0*(" +                                                                      \
                      #"@1" +                                                                           \
                      #")\",r," + str(self.Operators[0]) +                                           \
                      #")"
  
            self.modelBuilder.factory_(
                    "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +
                               "(\"@0*(" +
                               "@1" +
                               ")\",r," + str(self.Operators[0]) +
                               ")"
                    )

        else :
          for operator in range(0, self.numOperators):
            #print "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +                   \
                      #"(\"@0*(" +                                                                      \
                      #"@1" +                                                                           \
                      #")\",r," + str(self.Operators[operator]) +                                           \
                      #")"

            self.modelBuilder.factory_(
                    "expr::func_sm_linear_quadratic_" + str(self.Operators[operator]) +
                                "(\"@0*(" +
                                "@1" +
                                ")\",r," + str(self.Operators[operator]) +
                                ")"
                    )
          
          
        #
        # quadratic term in each Wilson coefficient
        #
        #
        # e.g. expr::func_sm_linear_quadratic_cH("@0*(@1 * (1-2*(@2+@3) ))",r,cH, cG, cGtil)
        #

        for operator in range(0, self.numOperators):

          #
          # this is the coefficient of "Quad_i"
          #
          
          if not self.alternative :

            #print "expr::func_quadratic_"+ str(self.Operators[operator]) + "(\"@0*(@1*@1-@1)\",r," + str(self.Operators[operator]) + ")"

            self.modelBuilder.factory_("expr::func_quadratic_"+ str(self.Operators[operator]) + "(\"@0*(@1*@1-@1)\",r," + str(self.Operators[operator]) + ")")


          else :

            if self.numOperators != 1:

              #print "expr::func_quadratic_"+ str(self.Operators[operator]) +    \
                                        #"(\"@0*(@1*@1-@1-@1*(" + "@" + "+@".join([str(j+1) for j in range(len(self.Operators)) if j != 0 ]) +   \
                                        #"))\",r," + "" +  str(self.Operators[operator]) + ", " + ", ".join([str(self.Operators[i]) for i in range(len(self.Operators)) if i != operator ]) + ")"

              self.modelBuilder.factory_("expr::func_quadratic_"+ str(self.Operators[operator]) +      \
                                        "(\"@0*(@1*@1-@1-@1*(" + "@" + "+@".join([str(j+1) for j in range(len(self.Operators)) if j != 0 ]) +   \
                                        "))\",r," + "" +  str(self.Operators[operator]) + ", " + ", ".join([str(self.Operators[i]) for i in range(len(self.Operators)) if i != operator ]) + ")"
                                        )
                                                                                                                                                                                

            else:

              #print "expr::func_quadratic_"+ str(self.Operators[0]) + \
                                        #"(\"@0*(@1*@1-@1" +   \
                                        #")\",r," + str(self.Operators[0]) + ")"

              self.modelBuilder.factory_("expr::func_quadratic_"+ str(self.Operators[operator]) +  \
                                        "(\"@0*(@1*@1-@1" +   \
                                        ")\",r," + str(self.Operators[0]) + ")"
                                        )



        #
        # (SM + linear) + quadratic + interference between pairs of Wilson coefficients
        #
        
        if not self.alternative :
          self.quadFactors=[]
          if self.numOperators != 1:
            for operator in range(0, self.numOperators):
              for operator_sub in range(operator+1, self.numOperators):

                #
                # this is the coefficient of "SM + Lin_i + Lin_j + Quad_i + Quad_j + 2 * M_ij"
                #
                #print "expr::func_sm_linear_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]) +          \
                #"(\"@0*@1*@2\",r," + str(self.Operators[operator]) + "," + str(self.Operators[operator_sub]) +                      \
                #")"
                self.quadFactors.append("func_sm_linear_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]))
                self.modelBuilder.factory_(
                        "expr::func_sm_linear_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]) +
                        "(\"@0*@1*@2\",r," + str(self.Operators[operator]) + "," + str(self.Operators[operator_sub]) +
                        ")")

        else:
          self.quadFactors=[]
          if self.numOperators != 1:
            for operator in range(0, self.numOperators):
              for operator_sub in range(operator+1, self.numOperators):

                #
                # this is the coefficient of "Quad_i + Quad_j + 2 * M_ij"
                #
                #print "expr::func_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]) +          \
                #"(\"@0*@1*@2\",r," + str(self.Operators[operator]) + "," + str(self.Operators[operator_sub]) +                      \
                #")"
                self.quadFactors.append("func_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]))
                self.modelBuilder.factory_(
                        "expr::func_quadratic_mixed_" + str(self.Operators[operator_sub]) + "_" + str(self.Operators[operator]) +
                        "(\"@0*@1*@2\",r," + str(self.Operators[operator]) + "," + str(self.Operators[operator_sub]) +
                        ")")



        print " parameters of interest = ", self.poiNames
        print " self.numOperators = ", self.numOperators
        
        self.modelBuilder.doSet("POI",self.poiNames)





#
# Define how the yields change
#


    def getYieldScale(self,bin,process):

        if any( process.startswith(x) for x in self.sgnl_known):
            if self.sm_re.search(process): 
                return "func_sm"
            elif self.lin_re.search(process): 
                match=self.lin_re.search(process)
                return "func_sm_linear_quadratic_"+ match.group('c1')
            elif self.mixed_re.search(process):
                match=self.mixed_re.search(process)
                c1=match.group('c1')
                c2=match.group('c2')
                if "func_sm_linear_quadratic_mixed_" + c1 + "_" + c2 in self.quadFactors:
                    return "func_sm_linear_quadratic_mixed_" + c1 + "_" + c2
                else:
                    return "func_sm_linear_quadratic_mixed_" + c2 + "_" + c1
                
            elif  self.quad_re.search(process):
                match=self.quad_re.search(process)
                c1=match.group('c1')
                return "func_quadratic_"+c1
            else:
                raise RuntimeError("Undefined process %s"%process)

        else:
            print 'Process %s not a signal'%process
            return 1
        


#
#  Standard inputs:
# 
#     S
#     S + Li + Qi
#     Qi
#     S + Li + Lj + Qi + Qj + 2*Mij
#    
#
#
#  Alternative (triggered by eftAlternative):
#
#     S
#     S + Li + Qi
#     Qi
#     Qi + Qj + 2*Mij
#    
#  


analiticAnomalousCouplingEFTNegative = AnaliticAnomalousCouplingEFTNegative()
