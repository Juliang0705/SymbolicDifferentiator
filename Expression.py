from abc import ABCMeta, abstractmethod
import numbers
import math
"""
The abstract syntax tree for Expression

type Expression = Constant
                  Variable
                  Plus     Expression Expression
                  Minus    Expression Expression
                  Multiply Expression Expression
                  Divide   Expression Expression
                  E        Expression
                  Ln       Expression
                  Power    Expression Expression
                  Sin      Expression
                  Cos      Expression
                  Tan      Expression
                  Cot      Expression
                  Sec      Expression
                  Csc      Expression

                  
"""
# base class for all expressions
class Expression (object):
    __metaclass__ = ABCMeta
    
    #return: another instance of Expression
    @abstractmethod
    def derivative(self):
        pass
    
    #param: x = a number
    #return: a number
    @abstractmethod
    def compute(self,x):
        pass
    
    #return: a string
    @abstractmethod
    def __str__(self):
        pass
    
    #param: other = an Expression
    @abstractmethod
    def __eq__(self,other):
        pass
    
    def __ne__(self,other):
        return not self.__eq__(other)
    
        
class Constant(Expression):
    
    #param: n = a number
    def __init__(self,n):
        assert isinstance(n, numbers.Number)
        self.value = n
        
    def derivative(self):
        return Constant(0)
    
    def compute(self, x):
        return self.value
    
    def __str__(self):
        return str(self.value)
    
    def __eq__(self, other):
        return isinstance(other,Constant) and self.value == other.value
        
        
class Variable(Expression):
    
    #param: v = a character
    def __init__(self,v):
        assert isinstance(v,str)
        assert len(v) == 1
        self.value = v
        
    def derivative(self):
        return Constant(1)
    
    def compute(self, x):
        return x
    
    def __str__(self):
        return self.value
    
    def __eq__(self, other):
        return isinstance(other,Variable) and self.value == other.value
        
class Plus(Expression):
    
    #param: left = an Expression, right = an Expression
    def __init__(self,left,right):
        assert isinstance(left,Expression)
        assert isinstance(right,Expression)
        self.left = left
        self.right = right
        
    def derivative(self):
        return Plus(self.left.derivative(), self.right.derivative())
    
    def compute(self, x):
        return self.left.compute(x) + self.right.compute(x)
    
    def __str__(self):
        return "(" + self.left.__str__() + "+" + self.right.__str__() + ")"
    
    def __eq__(self, other):
        return isinstance(other,Plus) and self.left == other.left and self.right == other.right   

class Minus(Expression):
    
    #param: left = an Expression, right = an Expression
    def __init__(self,left,right):
        assert isinstance(left,Expression)
        assert isinstance(right,Expression)        
        self.left = left
        self.right = right
        
    def derivative(self):
        return Minus(self.left.derivative(), self.right.derivative())
    
    def compute(self, x):
        return self.left.compute(x) - self.right.compute(x)
    
    def __str__(self):
        return "(" + self.left.__str__() + "-" + self.right.__str__() + ")"
    
    def __eq__(self, other):
        return isinstance(other,Minus) and self.left == other.left and self.right == other.right      
    
class Multiply(Expression):
    
    #param: left = an Expression, right = an Expression
    def __init__(self,left,right):
        assert isinstance(left,Expression)
        assert isinstance(right,Expression)        
        self.left = left
        self.right = right
        
    def derivative(self):
        left = Multiply(self.left.derivative() , self.right)
        right =  Multiply(self.left , self.right.derivative())
        return Plus(left,right)
    
    def compute(self, x):
        return self.left.compute(x) * self.right.compute(x)
    
    def __str__(self):
        return "(" + self.left.__str__() + "*" + self.right.__str__() + ")"
    
    def __eq__(self, other):
        return isinstance(other,Multiply) and self.left == other.left and self.right == other.right      

class Divide(Expression):
    
    #param: left = an Expression, right = an Expression
    def __init__(self,left,right):
        assert isinstance(left,Expression)
        assert isinstance(right,Expression)        
        self.left = left
        self.right = right
        
    def derivative(self):
        left = Multiply(self.left.derivative() , self.right)
        right =  Multiply(self.left , self.right.derivative())
        up = Minus(left,right)
        down = Multiply(self.right, self.right)
        return Divide(up,down)
    
    def compute(self, x):
        return self.left.compute(x) / float(self.right.compute(x))
    
    def __str__(self):
        return "(" + self.left.__str__() + "/" + self.right.__str__() + ")"
    
    def __eq__(self, other):
        return isinstance(other,Divide) and self.left == other.left and self.right == other.right      
    
class E(Expression):
    
    #param: exponent = an Expression
    def __init__(self,exponent):
        assert isinstance(exponent,Expression)
        self.exponent = exponent
    
    def derivative(self):
        return Multiply(self.exponent.derivative(),self)
    
    def compute(self, x):
        return math.pow(math.e,self.exponent.compute(x))
    
    def __str__(self):
        return "(e^" + self.exponent.__str__() + ")"
    
    def __eq__(self, other):
        return isinstance(other,E) and self.exponent == other.exponent
    
class Ln(Expression):
    
    #param: argument = an Expression
    def __init__(self,argument):
        assert isinstance(argument,Expression)
        self.argument = argument
    
    def derivative(self):
        return Multiply(self.argument.derivative(),Power(self.argument, Constant(-1)))
    
    def compute(self, x):
        return math.log(self.argument.compute(x))
    
    def __str__(self):
        return "(ln " + self.argument.__str__() + ")"
    
    def __eq__(self, other):
        return isinstance(other,Ln) and self.argument == other.argument    
    
class Power(Expression):
    
    #param: base = an Expression, Exponent = an Expression
    def __init__(self,base,exponent):
        assert isinstance(base,Expression)
        assert isinstance(exponent,Expression)        
        self.base = base
        self.exponent = exponent
        
    def derivative(self):
        #Power rule
        if isinstance(self.base,Variable) and isinstance(self.exponent,Constant):
            return Multiply(self.exponent, Power(self.base, Constant(self.exponent.value-1)))
        #this method covers everything else
        return E(Multiply(self.exponent, Ln(self.base))).derivative()
    
    def compute(self, x):
        return math.pow(self.base.compute(x), self.exponent.compute(x))
    
    def __str__(self):
        return "(" + self.base.__str__() + "^" + self.exponent.__str__() + ")"
    
    def __eq__(self, other):
        return isinstance(other,Power) and self.base == other.base and self.exponent == other.exponent    

class Sin(Expression):
    
    #param: expression = an Expression
    def __init__(self,expression):
        assert isinstance(expression,Expression)
        self.expression = expression
    
    def derivative(self):
        return Multiply(self.expression.derivative(), Cos(self.expression))
    
    def compute(self, x):
        return math.sin(self.expression.compute(x))
    
    def __str__(self):
        return "(sin " + self.expression.__str__() + ")"
    
    def __eq__(self, other):
        return isinstance(other,Sin) and self.expression == other.expression
    
class Cos(Expression):
    
    #param: expression = an Expression
    def __init__(self,expression):
        assert isinstance(expression,Expression)
        self.expression = expression
    
    def derivative(self):
        return Multiply(self.expression.derivative(), Multiply(Constant(-1),Sin(self.expression)))
    
    def compute(self, x):
        return math.cos(self.expression.compute(x))
    
    def __str__(self):
        return "(cos " + self.expression.__str__() + ")"
    
    def __eq__(self, other):
        return isinstance(other,Cos) and self.expression == other.expression    
    
class Tan(Expression):
    
    #param: expression = an Expression
    def __init__(self,expression):
        assert isinstance(expression,Expression)
        self.expression = expression
    
    def derivative(self):
        return Multiply(self.expression.derivative(), Power(Sec(self.expression),Constant(2)))
    
    def compute(self, x):
        return math.tan(self.expression.compute(x))
    
    def __str__(self):
        return "(tan " + self.expression.__str__() + ")" 
    
    def __eq__(self, other):
        return isinstance(other,Tan) and self.expression == other.expression    

class Cot(Expression):
    
    #param: expression = an Expression
    def __init__(self,expression):
        assert isinstance(expression,Expression)
        self.expression = expression
    
    def derivative(self):
        return Multiply(self.expression.derivative(), Multiply(Constant(-1),Power(Csc(self.expression),Constant(2))))
    
    def compute(self, x):
        return 1 / math.tan(self.expression.compute(x))
    
    def __str__(self):
        return "(cot " + self.expression.__str__() + ")"
    
    def __eq__(self, other):
        return isinstance(other,Cot) and self.expression == other.expression    
    
class Sec(Expression):
    
    #param: expression = an Expression
    def __init__(self,expression):
        assert isinstance(expression,Expression)
        self.expression = expression
    
    def derivative(self):
        return Multiply(self.expression.derivative(), Multiply(self,Tan(self.expression)))
    
    def compute(self, x):
        return 1 / math.cos(self.expression.compute(x))
    
    def __str__(self):
        return "(sec " + self.expression.__str__() + ")"
    
    def __eq__(self, other):
        return isinstance(other,Sec) and self.expression == other.expression    
    
class Csc(Expression):
    
    #param: expression = an Expression
    def __init__(self,expression):
        assert isinstance(expression,Expression)
        self.expression = expression
    
    def derivative(self):
        return Multiply(self.expression.derivative(), Multiply(Constant(-1),Multiply(self,Cot(self.expression))))
    
    def compute(self, x):
        return 1 / math.sin(self.expression.compute(x))
    
    def __str__(self):
        return "(csc " + self.expression.__str__() + ")"
    
    def __eq__(self, other):
        return isinstance(other,Csc) and self.expression == other.expression    
    
    
"""e = Multiply(Variable("x"), Plus(Constant(5.3),Variable("x")))

e = Divide(Plus(Multiply(Constant(3), Variable("z")), Constant(9)), Minus(Constant(2), Variable(
                                                                                               "z")))
                                                                                               """
e = Csc(Variable("x"))
print e
print e.derivative()
print e.derivative().compute(math.pi/2)