from flask import Flask,render_template, request, jsonify
import ply.lex as lex
import ply.yacc as yacc

app = Flask(__name__)

# Definición del lexer (análisis léxico)
tokens = ('NUMBER', 'PLUS', 'MINUS', 'TIMES', 'DIVIDE', 'LPAREN', 'RPAREN')

t_PLUS = r'\+'
t_MINUS = r'-'
t_TIMES = r'\*'
t_DIVIDE = r'/'
t_LPAREN = r'\('
t_RPAREN = r'\)'

t_ignore = ' \t'

def t_NUMBER(t):
    r'\d+'
    t.value = int(t.value)
    return t

def t_error(t):
    print("Caracter no reconocido: '%s'" % t.value[0])
    t.lexer.skip(1)

lexer = lex.lex()

# Definición del parser (análisis sintáctico)
def p_expression_binop(p):
    '''expression : expression PLUS term
                  | expression MINUS term'''
    p[0] = ('op', p[2], p[1], p[3])

def p_expression_term(p):
    'expression : term'
    p[0] = p[1]

def p_term_binop(p):
    '''term : term TIMES factor
            | term DIVIDE factor'''
    p[0] = ('op', p[2], p[1], p[3])

def p_term_factor(p):
    'term : factor'
    p[0] = p[1]

def p_factor_num(p):
    'factor : NUMBER'
    p[0] = ('num', p[1])

def p_factor_expr(p):
    'factor : LPAREN expression RPAREN'
    p[0] = p[2]

def p_error(p):
    print("Error de sintaxis")

parser = yacc.yacc()

@app.route('/')
def calculadora():
    return render_template('index.html')


@app.route('/analizar', methods=['POST'])
def analizar_expresion():
    try:
        data = request.get_json()
        input_expr = data.get('input')

        if not input_expr:
            return jsonify({"error": "No se recibió ninguna expresión"}), 400

        resultado = parser.parse(input_expr)

        return jsonify({"arbol": resultado})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
  

if __name__ == '__main__':
    app.run(debug=True)
