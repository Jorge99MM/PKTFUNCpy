from pkg_resources import resource_filename
import pandas as pd
import numpy as np

def cargar_tablas():
    ruta = resource_filename('PKTFUNC', 'Datos/TABLAS.xlsx')
    tablas = {
        'PERM2020_2OIND': pd.read_excel(ruta, sheet_name="PERM2020_2OIND"),
        'PERM2020_1OIND': pd.read_excel(ruta, sheet_name="PERM2020_1OIND"),
        'PERM2020_1OCOL': pd.read_excel(ruta, sheet_name="PERM2020_1OCOL"),
        'PERM2020_2OCOL': pd.read_excel(ruta, sheet_name="PERM2020_2OCOL"),
        'PERM2000_CART': pd.read_excel(ruta, sheet_name="PERM2000_CART"),
        'PERM2000_NEWCONTR': pd.read_excel(ruta, sheet_name="PERM2000_NEWCONTR")
    }
    return tablas

# Cargar todas las tablas
tablas = cargar_tablas()





def tabla_gen_anual(generacion, tabla_nombre, año_base=2012, genero="hombre"):
    """
    Crea una tabla generacional anual.
    
    :param generacion: Año de nacimiento de la persona
    :param tabla_nombre: Nombre de la tabla a utilizar (ej: 'PERM2020_2OIND')
    :param año_base: Año base para los cálculos (por defecto 2012)
    :param genero: "hombre" o "mujer" (por defecto "hombre")
    :return: DataFrame con las columnas X, qx, y Lx
    """
    tabla = tablas[tabla_nombre]
    

    
    # Seleccionar columnas basadas en el género
    if genero.lower() == "hombre":
        g, fg = 1, 3
    elif genero.lower() == "mujer":
        g, fg = 2, 4
    else:
        raise ValueError("El género debe ser 'hombre' o 'mujer'")
    
    x = np.arange(len(tabla))
    a = np.zeros(len(tabla))
    lx = np.ones(len(tabla)) * 1000000
    
    for i in range(len(tabla)):
        qxa = tabla.iloc[i, g] / 1000
        factor = tabla.iloc[i, fg]
        diff = (generacion + i) - año_base
        a[i] = qxa * np.exp(-factor * diff)
    
    for o in range(1, len(tabla)):
        lx[o] = lx[o-1] * (1 - a[o-1])
    
    return pd.DataFrame({'X': x, 'qx': a, 'Lx': lx})

# Ejemplos de uso:
resultado_hombre = tabla_gen_anual(2000, 'PERM2020_1OIND', genero="hombre")
resultado_mujer = tabla_gen_anual(2000, 'PERM2020_1OIND', genero="mujer")

print("Resultado para hombre:")
print(resultado_hombre.head())
print("\nResultado para mujer:")
print(resultado_mujer.head())



def tabla_gen_mensual(generacion, tabla_nombre, año_base=2012, genero="hombre"):
    # Primero, obtenemos la tabla anual usando la función anterior
    tabla_anual = tabla_gen_anual(generacion, tabla_nombre, año_base, genero)

    # Creamos el DataFrame mensual
    x = np.repeat(np.arange(126), 12)
    m = np.tile(np.arange(12), 126)
    perm_mensual = pd.DataFrame({'X': x, 'm': m})
    perm_mensual['x_mensual'] = perm_mensual['X'] * 12 + perm_mensual['m']

    # Función para interpolar
    def interpolar(row):
        x = row['X']
        m = row['m']
        lx_actual = tabla_anual.loc[tabla_anual['X'] == x, 'Lx'].values
        lx_siguiente = tabla_anual.loc[tabla_anual['X'] == (x + 1), 'Lx'].values
        
        if len(lx_actual) > 0 and len(lx_siguiente) > 0:
            return lx_actual[0] - (lx_actual[0] - lx_siguiente[0]) * (m / 12)
        else:
            return np.nan

    # Aplicamos la interpolación
    perm_mensual['Lx_mensual'] = perm_mensual.apply(interpolar, axis=1)

    # Reemplazamos los NaN por 0
    perm_mensual['Lx_mensual'] = perm_mensual['Lx_mensual'].fillna(0)

    return perm_mensual

# Ejemplo de uso
resultado_mensual = tabla_gen_mensual(2000, 'PERM2020_2OIND', genero="hombre")
print(resultado_mensual.head(24))  # Muestra los primeros dos años








def tabla_gen_anual_completa(generacion, tabla_nombre, año_base=2012, genero="hombre", interes=0.02):
    # Verificar si el interés es numérico
    if not isinstance(interes, (int, float)):
        raise ValueError("Error: el interés no es numérico")

    # Calculamos la tabla básica
    tabla_completa = tabla_gen_anual(generacion, tabla_nombre, año_base, genero)

    # Calculamos dx
    tabla_completa['dx'] = tabla_completa['Lx'] * tabla_completa['qx']

    # Calculamos v
    v = 1 / (1 + interes)

    # Supervivencia
    tabla_completa['Dx'] = (v ** tabla_completa['X']) * tabla_completa['Lx']

    # Calculamos Nx
    tabla_completa['Nx'] = tabla_completa['Dx'][::-1].cumsum()[::-1]

    # Calculamos Sx
    tabla_completa['Sx'] = tabla_completa['Nx'][::-1].cumsum()[::-1]

    # Mortalidad
    tabla_completa['Cx'] = (v ** (tabla_completa['X'] + 1)) * tabla_completa['dx']
    tabla_completa['Cx2'] = (v ** (tabla_completa['X'] + 0.5)) * tabla_completa['dx']

    # Calculamos Mx y Mx2
    tabla_completa['Mx'] = tabla_completa['Cx'][::-1].cumsum()[::-1]
    tabla_completa['Mx2'] = tabla_completa['Cx2'][::-1].cumsum()[::-1]

    # Calculamos Rx y Rx2
    tabla_completa['Rx'] = tabla_completa['Mx'][::-1].cumsum()[::-1]
    tabla_completa['Rx2'] = tabla_completa['Mx2'][::-1].cumsum()[::-1]

    return tabla_completa

# Ejemplo de uso
resultado_completo = tabla_gen_anual_completa(1998, 'PERM2020_2OIND', genero="hombre", interes=0.02)
print(resultado_completo.head())









def tabla_gen_mensual_completa(generacion, tabla_nombre, año_base=2012, genero="hombre", interes=0.02):
    # Verificar si el interés es numérico
    if not isinstance(interes, (int, float)):
        raise ValueError("Error: el interés no es numérico")

    # Calculamos la tabla básica mensual
    tabla_completa = tabla_gen_mensual(generacion, tabla_nombre, año_base, genero)

    # Calculamos el interés mensual
    interes_mensual = ((1 + interes) ** (1/12)) - 1
    v = 1 / (1 + interes_mensual)

    # Calculamos dx
    tabla_completa['dx'] = tabla_completa['Lx_mensual'].diff(-1).fillna(0)

    # Supervivencia
    tabla_completa['Dx'] = (v ** tabla_completa['x_mensual']) * tabla_completa['Lx_mensual']

    # Calculamos Nx
    tabla_completa['Nx'] = tabla_completa['Dx'][::-1].cumsum()[::-1]

    # Calculamos Sx
    tabla_completa['Sx'] = tabla_completa['Nx'][::-1].cumsum()[::-1]

    # Mortalidad
    tabla_completa['Cx'] = (v ** (tabla_completa['x_mensual'] + 1)) * tabla_completa['dx']
    tabla_completa['Cx2'] = (v ** (tabla_completa['X'] + 0.5)) * tabla_completa['dx']

    # Calculamos Mx y Mx2
    tabla_completa['Mx'] = tabla_completa['Cx'][::-1].cumsum()[::-1]
    tabla_completa['Mx2'] = tabla_completa['Cx2'][::-1].cumsum()[::-1]

    # Calculamos Rx y Rx2
    tabla_completa['Rx'] = tabla_completa['Mx'][::-1].cumsum()[::-1]
    tabla_completa['Rx2'] = tabla_completa['Mx2'][::-1].cumsum()[::-1]

    return tabla_completa

# Ejemplo de uso
resultado_mensual_completo = tabla_gen_mensual_completa(1998, 'PERM2020_2OIND', genero="hombre", interes=0.02)
print(resultado_mensual_completo.head())