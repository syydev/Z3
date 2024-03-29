import sys
from z3 import *
from pycparser import c_parser, c_ast, parse_file


WEAK_FUNCTION = ['gets', 'scanf', 'strcat', 'strcpy', 'sprintf']
PROBLEM_LIST = []
stack = []
sol = Solver()
a, b, c, d, e, f, g = Ints('a b c d e f g')


def getCondElement(cond):
  element = ''
  try:
    element = cond.name
  except:
    element = cond.value
  return element


def exploreAST(ast):
  if ast == None:
    return

  elif type(ast) == c_ast.Decl:
    # TODO implement dynamic declaration and init
    if ast.init:
      # exec(ast.name + '= Int(\'' + ast.name + '\')')
      # exec(ast.name + '=' + ast.init.value)
      # print(ast.name + '=' + ast.init.value)
      return
    else:
      # exec(ast.name + '= Int(\'' + ast.name + '\')')
      return

  elif type(ast) == c_ast.Assignment:
    # TODO implement dynamic assignment
    # exec(ast.lvalue.name + ast.op + ast.rvalue.value)
    # print(ast.lvalue.name + ast.op + ast.rvalue.value)
    return

  elif type(ast) == c_ast.FuncCall:
    for funcname in WEAK_FUNCTION:
      if funcname == ast.name.name:
        tmp = stack[:]
        PROBLEM_LIST.append([tmp, funcname, ast.name.coord])

  elif type(ast) == c_ast.If:
    left = getCondElement(ast.cond.left)
    right = getCondElement(ast.cond.right)
    stack.append(eval(left + ast.cond.op + right))
    exploreAST(ast.iftrue)
    stack.pop()
    stack.append(Not(eval(left + ast.cond.op + right)))
    exploreAST(ast.iffalse)
    stack.pop()

  elif type(ast) == c_ast.For or type(ast) == c_ast.While or type(ast) == c_ast.DoWhile:
    # TODO implement explore For, While, DoWhile
    return

  elif type(ast) == c_ast.Return:
    return

  elif ast.block_items:
    for block in ast.block_items:
      exploreAST(block)


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
      print('[Critical vulnerability] %s called in %s' % (problemList[1], problemList[2]))
    else:
      print('[Potential vulnerability] %s used in %s' % (problemList[1], problemList[2]))
    sol.reset()
