"""
Ejemplos exitosos para análisis semántico de funciones.
Incluye declaraciones de funciones, llamadas de funciones, parámetros, return y ámbitos de funciones.
"""

EJEMPLOS_EXITOSOS_SEMANTIC_FUNCIONES = [
    {
        "codigo": """
func int suma(int a, int b) {
    return a + b;
}
        """,
        "descripcion": "Función simple con parámetros y return - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func int factorial(int n) {
    if (n <= 1) {
        return 1;
    } else {
        return n * factorial(n - 1);
    }
}
        """,
        "descripcion": "Función recursiva con condicional - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func void saludar() {
    print("Hola mundo");
}
        """,
        "descripcion": "Función sin parámetros que no retorna valor - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func int maximo(int a, int b) {
    if (a > b) {
        return a;
    } else {
        return b;
    }
}
        """,
        "descripcion": "Función con múltiples returns en condicional - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func float calcular_area(float radio) {
    float pi = 3.14;
    return pi * radio * radio;
}
        """,
        "descripcion": "Función con variable local y cálculo - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func int potencia(int base, int exponente) {
    int resultado = 1;
    int i = 0;
    while (i < exponente) {
        resultado = resultado * base;
        i = i + 1;
    }
    return resultado;
}
        """,
        "descripcion": "Función con bucle y variables locales - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func bool es_par(int numero) {
    int mitad = numero / 2;
    int doble = mitad * 2;
    if (doble == numero) {
        return true;
    } else {
        return false;
    }
}
        """,
        "descripcion": "Función que retorna booleano con cálculo - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func int fibonacci(int n) {
    if (n <= 1) {
        return n;
    }
    int a = 0;
    int b = 1;
    int i = 2;
    while (i <= n) {
        int temp = a + b;
        a = b;
        b = temp;
        i = i + 1;
    }
    return b;
}
        """,
        "descripcion": "Función Fibonacci iterativa con variables locales - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func void intercambiar(int a, int b) {
    int temp = a;
    a = b;
    b = temp;
}
        """,
        "descripcion": "Función void con modificación de parámetros - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func int suma_rango(int inicio, int fin) {
    int suma = 0;
    int i = inicio;
    while (i <= fin) {
        suma = suma + i;
        i = i + 1;
    }
    return suma;
}
        """,
        "descripcion": "Función con múltiples parámetros y bucle - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func float promedio(int a, int b, int c) {
    int suma = a + b + c;
    float resultado = suma / 3.0;
    return resultado;
}
        """,
        "descripcion": "Función con conversión de tipos en operación - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func bool validar_rango(int valor, int minimo, int maximo) {
    if (valor >= minimo) {
        if (valor <= maximo) {
            return true;
        }
    }
    return false;
}
        """,
        "descripcion": "Función con condicionales anidados y múltiples returns - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func int buscar_maximo(int array_size) {
    int maximo = 0;
    int i = 1;
    while (i <= array_size) {
        int valor = i * 2;
        if (valor > maximo) {
            maximo = valor;
        }
        i = i + 1;
    }
    return maximo;
}
        """,
        "descripcion": "Función que simula búsqueda en array - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func void mostrar_tabla(int numero) {
    int i = 1;
    while (i <= 10) {
        int resultado = numero * i;
        print(resultado);
        i = i + 1;
    }
}
        """,
        "descripcion": "Función void con bucle y llamada a función predefinida - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func int contar_digitos(int numero) {
    int contador = 0;
    if (numero == 0) {
        return 1;
    }
    while (numero > 0) {
        numero = numero / 10;
        contador = contador + 1;
    }
    return contador;
}
        """,
        "descripcion": "Función con caso especial y bucle de procesamiento - análisis semántico exitoso",
        "salida_esperada_semantica": True
    },
    {
        "codigo": """
func bool es_primo(int numero) {
    if (numero <= 1) {
        return false;
    }
    if (numero == 2) {
        return true;
    }
    int i = 2;
    while (i * i <= numero) {
        int division = numero / i;
        int producto = division * i;
        if (producto == numero) {
            return false;
        }
        i = i + 1;
    }
    return true;
}
        """,
        "descripcion": "Función compleja con múltiples condicionales y bucle - análisis semántico exitoso",
        "salida_esperada_semantica": True
    }
]
