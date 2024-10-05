from setuptools import setup, find_packages

setup(
    name="PKTFUNC",  # Puedes cambiar esto al nombre que prefieras para tu paquete
    version="0.1",
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
    ],
    package_data={
        'PKTFUNC': ['Datos/TABLAS.xlsx'],  # Ajustado a tu estructura
    },
    author="Mallo Jorge, Bernal Alejandro",
    author_email="",
    description="Un paquete para cálculos actuariales",
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Jorge99MM/PKTFUNCpy",  # Reemplaza con la URL de tu repositorio
)