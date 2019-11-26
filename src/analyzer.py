import sys
from z3 import *
from pycparser import c_parser, c_ast, parse_file


WEAK_FUNCTION = ['gets', 'scanf', 'strcat', 'strcpy', 'sprintf']
PROBLEM_LIST = []
stack = []
sol = Solver()
a, b, c, d, e, f, g = Ints('a b c d e f g')


def exploreAST(ast):
  if ast == None:
    return

  elif type(ast) == c_ast.FuncCall:
    for funcname in WEAK_FUNCTION:
      if funcname == ast.name.name:
        tmp = stack[:]
        PROBLEM_LIST.append([tmp, funcname, ast.name.coord])

  elif type(ast) == c_ast.If:
    stack.append(eval(ast.cond.left.name + ast.cond.op + ast.cond.right.value))
    exploreAST(ast.iftrue)
    stack.pop()
    stack.append(Not(eval(ast.cond.left.name + ast.cond.op + ast.cond.right.value)))
    exploreAST(ast.iffalse)
    stack.pop()

  elif type(ast) == c_ast.Decl:
    print(ast)

  elif ast.block_items:
    for block in ast.block_items:
      if type(block) == c_ast.FuncCall:
        for funcname in WEAK_FUNCTION:
          if funcname == block.name.name:
            tmp = stack[:]
            PROBLEM_LIST.append([tmp, funcname, ast.name.coord])
      elif type(block) == c_ast.If:
        stack.append(eval(block.cond.left.name + block.cond.op + block.cond.right.value))
        exploreAST(block.iftrue)
        stack.pop()
        stack.append(Not(eval(block.cond.left.name + block.cond.op + block.cond.right.value)))
        exploreAST(block.iffalse)
        stack.pop()
      elif type(block) == c_ast.Decl:
        if block.init:
          print(block.type.type.names[0], block.name, block.init.value)
        else:
          print(block.type.type.names[0], block.name)


def run():
  if len(sys.argv) > 1:
    filename = sys.argv[1]
  else:
    filename = 'sample.c'

  ast = parse_file('examples/' + filename)
  exploreAST(ast.ext[0].body)

  for problemList in PROBLEM_LIST:
    for problem in problemList[0]:
      sol.add(problem)
    if str(sol.check()) == 'sat':
      print(str(sol.check()), problemList[0], problemList[1], problemList[2], sol.model())
    else:
      print(str(sol.check()), problemList[0], problemList[1], problemList[2])
    sol.reset()
  