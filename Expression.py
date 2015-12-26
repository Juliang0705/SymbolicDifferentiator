from abc import ABCMeta, abstractmethod
import numbers
"""
The abstract syntax tree for Expression

type Expression = Constant
                  Variable
                  Plus     Expression Expression
                  Minus    Expression Expression
                  Multiply Expression Expression
                  Divide   Expression Expression
                  Power    Expression Expression
                  Log      Expression Expression
                  Sin      Expression
                  Cos      Expression
                  Tan      Expression
                  Cot      Expression
                  Sec      Expression
                  Csc      Expression
                  E        Expression
                  Ln       Expression
                  
"""
# base class for all expressions
class Expression (object):
    __metaclass__ = ABCMeta
    
    #return: another instance of Expression
    @abstractmethod
    def differetiate(self):
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
        
class Constant(Expression):
    
    #param: n = a number
    def __init__(self,n):
        assert isinstance(n, numbers.Number)
        self.value = n
        
    def differetiate(self):
        return Constant(0)
    
    def compute(self, x):
        return self.value
    
    def __str__(self):
        return str(self.value)
        
class Variable(Expression):
    
    #param: v = a character
    def __init__(self,v):
        self.value = v
        
    def differetiate(self):
        return Constant(1)
    
    def compute(self, x):
        return x
    
    def __str__(self):
        return self.value
        
class Plus(Expression):
    
    #param: left = an Expression, right = an Expression
    def __init__(self,left,right):
        assert isinstance(left,Expression)
        assert isinstance(right,Expression)
        self.left = left
        self.right = right
        
    def differetiate(self):
        return Plus(self.left.differetiate(), self.right.differetiate())
    
    def compute(self, x):
        return self.left.compute(x) + self.right.compute(x)
    
    def __str__(self):
        return "(" + self.left.__str__() + "+" + self.right.__str__() + ")"

class Minus(Expression):
    
    #param: left = an Expression, right = an Expression
    def __init__(self,left,right):
        assert isinstance(left,Expression)
        assert isinstance(right,Expression)        
        self.left = left
        self.right = right
        
    def differetiate(self):
        return Minus(self.left.differetiate(), self.right.differetiate())
    
    def compute(self, x):
        return self.left.compute(x) - self.right.compute(x)
    
    def __str__(self):
        return "(" + self.left.__str__() + "-" + self.right.__str__() + ")"
    
class Multiply(Expression):
    
    #param: left = an Expression, right = an Expression
    def __init__(self,left,right):
        assert isinstance(left,Expression)
        assert isinstance(right,Expression)        
        self.left = left
        self.right = right
        
    def differetiate(self):
        left = Multiply(self.left.differetiate() , self.right)
        right =  Multiply(self.left , self.right.differetiate())
        return Plus(left,right)
    
    def compute(self, x):
        return self.left.compute(x) * self.right.compute(x)
    
    def __str__(self):
        return "(" + self.left.__str__() + "*" + self.right.__str__() + ")"

class Divide(Expression):
    
    #param: left = an Expression, right = an Expression
    def __init__(self,left,right):
        assert isinstance(left,Expression)
        assert isinstance(right,Expression)        
        self.left = left
        self.right = right
        
    def differetiate(self):
        left = Multiply(self.left.differetiate() , self.right)
        right =  Multiply(self.left , self.right.differetiate())
        up = Minus(left,right)
        down = Multiply(right, right)
        return Devide(up,down)
    
    def compute(self, x):
        return self.left.compute(x) / float(self.right.compute(x))
    
    def __str__(self):
        return "(" + self.left.__str__() + "/" + self.right.__str__() + ")"
    
    
e = Multiply(Variable("x"), Plus(Constant(5.3),Variable("x")))
print e
print e.differetiate()
print e.differetiate().compute(7)